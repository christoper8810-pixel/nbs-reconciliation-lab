"""Report-level calculation policies on top of the component engine.

Every result is review output. Amounts are only produced when all inputs for
the selected population are complete; otherwise the amount is None with the
reasons. Different currencies, dates, companies and sources are never added.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import Any, Callable

import mapping_engine

from .selectors import parse_expression


def validate_maturity_buckets(buckets: Any) -> list[str]:
    """Buckets must be integer-day, contiguous from 0, non-overlapping, ending open-ended."""
    problems: list[str] = []
    if not isinstance(buckets, list) or not buckets:
        return ["at least one bucket is required"]
    expected = 0
    codes = set()
    for index, bucket in enumerate(buckets):
        code = bucket.get("code") if isinstance(bucket, dict) else None
        if not code or code in codes:
            problems.append(f"bucket {index} needs a unique code")
        codes.add(code)
        lo, hi = bucket.get("min_days"), bucket.get("max_days")
        if not isinstance(lo, int) or isinstance(lo, bool):
            problems.append(f"{code}: min_days must be an integer")
            continue
        if lo != expected:
            problems.append(f"{code}: starts at {lo}, expected {expected} (gap or overlap)")
        last = index == len(buckets) - 1
        if hi is None:
            if not last:
                problems.append(f"{code}: only the last bucket may be open-ended")
            break
        if not isinstance(hi, int) or isinstance(hi, bool) or hi < lo:
            problems.append(f"{code}: max_days must be an integer >= min_days")
            continue
        if last:
            problems.append(f"{code}: last bucket must be open-ended so the model is complete")
        expected = hi + 1
    return problems


def maturity_state(maturity_date: str | None, reporting_date: str, buckets: list[dict[str, Any]],
                   overdue_state: str = "MATURED_OR_OVERDUE", missing_state: str = "MISSING_MATURITY_DATE") -> str:
    """Remaining maturity = maturity_date - reporting_date (never system date minus maturity)."""
    if maturity_date is None or not str(maturity_date).strip():
        return missing_state
    remaining = (date.fromisoformat(str(maturity_date).strip()) - date.fromisoformat(reporting_date)).days
    if remaining < 0:
        return overdue_state
    for bucket in buckets:
        if remaining >= bucket["min_days"] and (bucket["max_days"] is None or remaining <= bucket["max_days"]):
            return bucket["code"]
    raise ValueError("Maturity buckets are incomplete")  # unreachable when validated


def credit_quality_totals(detail: dict[str, Decimal | None], totals: dict[str, list[str]]) -> dict[str, Decimal | None]:
    """Compute total columns once from same-row detail columns; None propagates (no partial totals)."""
    values: dict[str, Decimal | None] = dict(detail)
    pending = dict(totals)
    while pending:
        progressed = False
        for column, parts in list(pending.items()):
            if all(part in values for part in parts):
                inputs = [values[part] for part in parts]
                values[column] = None if any(v is None for v in inputs) else mapping_engine.exact_sum(inputs)
                del pending[column]
                progressed = True
        if not progressed:
            raise ValueError(f"Unresolvable total columns: {sorted(pending)}")
    return {column: values[column] for column in totals}


def metric_status(name: str, policy: dict[str, Any], rules: dict[str, Any], seen: tuple[str, ...] = ()) -> dict[str, Any]:
    metrics = policy["metrics"]
    if name not in metrics:
        return {"available": False, "reasons": [f"UNKNOWN_METRIC:{name}"]}
    if name in seen:
        return {"available": False, "reasons": [f"CIRCULAR_METRIC:{name}"]}
    metric = metrics[name]
    if metric["kind"] == "UNDEFINED":
        return {"available": False, "reasons": [f"METRIC_UNDEFINED:{name}"]}
    if metric["kind"] == "BALANCE_GROUP":
        return {"available": metric["group"] in rules["groups"], "reasons": []}
    reasons: list[str] = []
    for _, ref in parse_expression(metric["expression"]):
        reasons += metric_status(ref, policy, rules, seen + (name,))["reasons"]
    return {"available": not reasons, "reasons": list(dict.fromkeys(reasons))}


def contract_metric(contract: dict[str, Any], name: str, policy: dict[str, Any]) -> tuple[Decimal | None, list[str]]:
    """Metric for one engine contract result. Unavailable components yield None, never zero."""
    metric = policy["metrics"].get(name)
    if metric is None:
        return None, [f"UNKNOWN_METRIC:{name}"]
    if metric["kind"] == "UNDEFINED":
        return None, [f"METRIC_UNDEFINED:{name}"]
    totals = contract.get("group_totals_for_supplied_records")
    if metric["kind"] == "BALANCE_GROUP":
        if totals is None:
            return None, ["CONTRACT_INCOMPLETE"]
        return Decimal(totals[metric["group"]]), []
    parts: list[Decimal] = []
    reasons: list[str] = []
    for coefficient, ref in parse_expression(metric["expression"]):
        value, why = contract_metric(contract, ref, policy)
        reasons += why
        if value is not None:
            parts.append(coefficient * value)
    if reasons:
        return None, list(dict.fromkeys(reasons))
    return mapping_engine.exact_sum(parts), []


def compute_report_rows(effective: list[dict[str, Any]], engine_result: dict[str, Any],
                        attributes: dict[str, dict[str, Any]], policy: dict[str, Any],
                        compile_fn: Callable[[dict[str, Any]], Callable[[dict[str, Any]], bool | None]],
                        run_basis: str = "CLOSING_STOCK") -> dict[str, Any]:
    """Compute report-row amounts per (company, source, currency, date) for effective mappings.

    attributes maps contract_id -> selector attributes (T24.CATEGORY, ...).
    A row amount is None when any selected contract is incomplete, any selector
    attribute is missing, a metric is unavailable, or exclusivity is violated.
    """
    contracts = engine_result.get("contracts", [])
    rows: list[dict[str, Any]] = []
    matches_by_group: dict[tuple[str, tuple[str, ...]], list[str]] = defaultdict(list)
    for mapping in effective:
        spec = mapping["effective_spec"]
        metric_name = spec["metric_expression"]
        reasons: list[str] = []
        metric = policy["metrics"].get(metric_name)
        if metric is None:
            reasons.append(f"UNKNOWN_METRIC:{metric_name}")
        elif metric["amount_basis"] != spec["amount_basis"] or spec["amount_basis"] != run_basis:
            reasons.append(f"AMOUNT_BASIS_MISMATCH:{spec['amount_basis']}!={run_basis}")
        predicate = compile_fn(spec["selectors"])
        partitions: dict[tuple[str, ...], dict[str, Any]] = {}
        for contract in contracts:
            attrs = attributes.get(contract["contract_id"])
            key = (contract["company"], contract["source_system"], contract["currency"], contract["as_of"])
            part = partitions.setdefault(key, {"values": [], "reasons": list(reasons), "contracts": []})
            if attrs is None:
                part["reasons"].append(f"ATTRIBUTES_MISSING:{contract['contract_id']}")
                continue
            selected = predicate(attrs)
            if selected is None:
                part["reasons"].append(f"SELECTOR_ATTRIBUTE_MISSING:{contract['contract_id']}")
                continue
            if not selected:
                continue
            part["contracts"].append(contract["contract_id"])
            if spec.get("exclusive_group"):
                matches_by_group[(spec["exclusive_group"], key)].append(contract["contract_id"])
            if not reasons:
                value, why = contract_metric(contract, metric_name, policy)
                if why:
                    part["reasons"] += [f"{r}:{contract['contract_id']}" for r in why]
                else:
                    part["values"].append(value)
        for key, part in sorted(partitions.items()):
            rows.append({
                "business_id": mapping["business_id"],
                "exclusive_group": spec.get("exclusive_group"),
                "company": key[0], "source_system": key[1], "currency": key[2], "as_of": key[3],
                "metric": metric_name,
                "contract_count": len(part["contracts"]),
                "contracts": part["contracts"],
                "amount": None if part["reasons"] else format(mapping_engine.exact_sum(part["values"]), "f"),
                "reasons": list(dict.fromkeys(part["reasons"])),
            })
    violations = []
    for (group, key), contract_ids in matches_by_group.items():
        repeated = sorted({c for c in contract_ids if contract_ids.count(c) > 1})
        if repeated:
            violations.append({"exclusive_group": group, "partition": list(key), "contracts": repeated})
            for row in rows:
                if row["exclusive_group"] == group and (row["company"], row["source_system"], row["currency"], row["as_of"]) == key:
                    row["amount"] = None
                    row["reasons"].append("EXCLUSIVITY_VIOLATION:" + ",".join(repeated))
    return {
        "report_kind": "OWNER_REVIEW_ONLY",
        "production_ready": False,
        "rows": rows,
        "exclusivity_violations": violations,
        "engine_complete": engine_result.get("complete_for_supplied_records_and_required_types"),
        "limitations": [
            "Row amounts cover only the supplied contracts; population completeness is not verified.",
            "No FX conversion: each currency is a separate partition.",
            "Not reconciled to legacy/control extracts.",
        ],
    }
