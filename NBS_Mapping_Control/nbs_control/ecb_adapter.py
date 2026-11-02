"""File-based EB.CONTRACT.BALANCES (ECB) adapter producing engine records.

Input is a JSON export (no bank connection). Each ECB record carries aligned
multivalue arrays: balance types with their opening balance and signed credit
and debit movements (RECONSTRUCT mode) or a closing amount (CLOSING_SNAPSHOT
mode). Arrays are never exploded independently: a length mismatch rejects the
record. Movements are never added to a closing snapshot. Signs are used exactly
as supplied; no absolute values, no invented debit/credit signs, no FX.

CLM: a category-3713 parent is CLM only through an explicit flag, a configured
positive indicator, or a verified link to a category-6050 CLS account in the
same company/source/currency/date. Only the configured CLS components of a
verified, unambiguous link are attached to the parent. Everything rejected or
unclassified is retained in exceptions.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import Any

import mapping_engine

from .selectors import compile_selector

HEADER_FIELDS = ("record_id", "company", "source_system", "contract_id", "currency", "snapshot_as_of",
                 "date_basis", "category")


def _text(value: Any) -> str | None:
    if value is None or isinstance(value, bool):
        return None
    token = str(value).strip()
    return token or None


def _flag(value: Any) -> bool | None:
    try:
        return mapping_engine.parse_clm(value)
    except ValueError:
        return None


def adapt(payload: dict[str, Any], rules: dict[str, Any], rules_doc: dict[str, Any], policy: dict[str, Any],
          selectors_cfg: dict[str, Any]) -> dict[str, Any]:
    adapter = policy["ecb_adapter"]
    fields = adapter["fields"]
    mode = adapter["mode"]
    reporting_date = _text(payload.get("reporting_date"))
    if reporting_date is None or date.fromisoformat(reporting_date).isoformat() != reporting_date:
        raise ValueError("reporting_date (YYYY-MM-DD) is required")
    if mode == "CLOSING_SNAPSHOT" and not fields.get("closing"):
        raise ValueError("CLOSING_SNAPSHOT mode requires ecb_adapter.fields.closing")
    excluded_types = {mapping_engine.normalize_code(c) for c in adapter.get("owner_excluded_balance_types", [])}
    clm_cfg = rules_doc["clm"]
    candidate, source_category = rules["candidate_category"], rules["source_category"]
    exceptions: list[dict[str, Any]] = []
    warnings: list[str] = []
    population = selectors_cfg.get("populations", {}).get("LENDING_BASE")
    if population is None:
        raise ValueError("No LENDING_BASE population configured")
    in_population = compile_selector(population["selector"], selectors_cfg["fields"], require_approved=False)
    if population.get("status") != "APPROVED":
        warnings.append("LENDING_BASE population is not owner-approved; output is review-only")
    if not adapter.get("approved"):
        warnings.append("ECB adapter field names/mode are not owner-approved; output is review-only")

    def reject(record: dict[str, Any], reason: str, **extra: Any) -> None:
        exceptions.append({"kind": "ECB_RECORD_REJECTED", "reason": reason,
                           "record_id": record.get("record_id"), "contract_id": record.get("contract_id"), **extra})

    # 1. Validate ECB records and expand aligned multivalues into balance rows.
    snapshots: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for index, record in enumerate(payload.get("ecb_records", []), start=1):
        if not isinstance(record, dict):
            exceptions.append({"kind": "ECB_RECORD_REJECTED", "reason": "RECORD_NOT_OBJECT", "input_row": index})
            continue
        missing = [f for f in HEADER_FIELDS if _text(record.get(f)) is None]
        if missing:
            reject(record, "MISSING_HEADER_FIELDS", missing=missing)
            continue
        if record["snapshot_as_of"] != reporting_date:
            reject(record, "SNAPSHOT_DATE_NOT_REPORTING_DATE", snapshot_as_of=record["snapshot_as_of"])
            continue
        if record["date_basis"] != adapter["date_basis"]:
            reject(record, "DATE_BASIS_MISMATCH", date_basis=record["date_basis"], expected=adapter["date_basis"])
            continue
        types = record.get(fields["balance_type"])
        if mode == "RECONSTRUCT_FROM_OPENING_AND_MOVEMENTS":
            if fields.get("closing") and record.get(fields["closing"]) is not None:
                reject(record, "CLOSING_AND_MOVEMENTS_BOTH_SUPPLIED_DOUBLE_COUNT_RISK")
                continue
            arrays = [record.get(fields[k]) for k in ("opening", "credit_movement", "debit_movement")]
        else:
            arrays = [record.get(fields["closing"])]
            if any(record.get(fields[k]) is not None for k in ("credit_movement", "debit_movement") if fields.get(k)):
                warnings.append(f"{record['record_id']}: movements ignored in CLOSING_SNAPSHOT mode (never added to closing)")
        if not isinstance(types, list) or not types or not all(isinstance(a, list) for a in arrays):
            reject(record, "MULTIVALUE_FIELDS_MISSING")
            continue
        if any(len(a) != len(types) for a in arrays):
            reject(record, "MULTIVALUE_LENGTH_MISMATCH", lengths=[len(types)] + [len(a) for a in arrays])
            continue
        try:
            codes = [mapping_engine.normalize_code(t) for t in types]
            amounts = [[mapping_engine.parse_money(v) for v in a] for a in arrays]
        except ValueError as exc:
            reject(record, "INVALID_MULTIVALUE_ENTRY", detail=str(exc))
            continue
        if len(set(codes)) != len(codes):
            reject(record, "DUPLICATE_BALANCE_TYPE_IN_RECORD")
            continue
        balances = []
        for position, code in enumerate(codes):
            parts = [a[position] for a in amounts]
            balances.append({"balance_type": code, "position": position,
                             "amount": mapping_engine.exact_sum(parts),
                             "components": [format(p, "f") for p in parts]})
        key = (record["company"].strip(), record["source_system"].strip().upper(), record["contract_id"].strip(),
               record["currency"].strip().upper(), reporting_date)
        snapshots[key].append({"record": record, "balances": balances})

    contracts: dict[tuple[str, ...], dict[str, Any]] = {}
    for key, entries in snapshots.items():
        if len(entries) > 1:
            for entry in entries:
                reject(entry["record"], "DUPLICATE_SNAPSHOT_FOR_CONTRACT_GRAIN",
                       note="Repeated balance snapshot (e.g. once per journal entry) is not counted again")
            continue
        contracts[key] = entries[0]

    # 2. Validate CLM links.
    by_contract = {(k[0], k[1], k[2]): k for k in contracts}
    accepted_links: dict[tuple[str, ...], dict[str, Any]] = {}
    rejected_links: list[dict[str, Any]] = []
    candidates_links = []
    seen_link_ids = set()
    for link in payload.get("links", []):
        reasons = []
        link_id = _text(link.get("link_id"))
        if link_id is None or link_id in seen_link_ids:
            reasons.append("LINK_ID_MISSING_OR_REUSED")
        seen_link_ids.add(link_id)
        if link.get("verified") is not True:
            reasons.append("LINK_NOT_VERIFIED")
        if _text(link.get("parent_category")) != candidate or _text(link.get("child_category")) != source_category:
            reasons.append("LINK_CATEGORY_MISMATCH")
        if (_text(link.get("child_product")) or "").upper() != rules["source_product"]:
            reasons.append("LINK_CHILD_PRODUCT_NOT_CLS")
        if _text(link.get("evidence")) is None:
            reasons.append("LINK_EVIDENCE_MISSING")
        company, source = _text(link.get("company")), (_text(link.get("source_system")) or "").upper()
        parent_key = by_contract.get((company, source, _text(link.get("parent_contract_id"))))
        child_key = by_contract.get((company, source, _text(link.get("child_contract_id"))))
        if parent_key is None or child_key is None:
            reasons.append("LINK_PARENT_OR_CHILD_SNAPSHOT_MISSING")
        else:
            if parent_key[3] != child_key[3] or _text(link.get("currency")) != parent_key[3]:
                reasons.append("LINK_CURRENCY_CONTEXT_MISMATCH")
            if _text(link.get("as_of")) != reporting_date:
                reasons.append("LINK_DATE_MISMATCH")
            if _text(contracts[parent_key]["record"].get("category")) != candidate:
                reasons.append("PARENT_SNAPSHOT_NOT_CATEGORY_3713")
            if _text(contracts[child_key]["record"].get("category")) != source_category:
                reasons.append("CHILD_SNAPSHOT_NOT_CATEGORY_6050")
        if reasons:
            rejected_links.append({**link, "reasons": reasons})
        else:
            candidates_links.append({**link, "parent_key": parent_key, "child_key": child_key})
    by_child: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    by_parent: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for link in candidates_links:
        by_child[link["child_key"]].append(link)
        by_parent[link["parent_key"]].append(link)
    for link in candidates_links:
        reasons = []
        if len({l["parent_key"] for l in by_child[link["child_key"]]}) > 1:
            reasons.append("CHILD_LINKED_TO_CONFLICTING_PARENTS")
        elif len(by_child[link["child_key"]]) > 1:
            reasons.append("DUPLICATE_RELATIONSHIP_REUSE")
        if len({l["child_key"] for l in by_parent[link["parent_key"]]}) > 1:
            reasons.append("PARENT_HAS_MULTIPLE_CLS_CHILDREN_NO_ALLOCATION_POLICY")
        clean = {k: v for k, v in link.items() if k not in ("parent_key", "child_key")}
        if reasons:
            rejected_links.append({**clean, "reasons": reasons})
        else:
            accepted_links[link["child_key"]] = {**clean, "parent_key": link["parent_key"], "child_key": link["child_key"]}
    linked_parents = {link["parent_key"]: link for link in accepted_links.values()}
    rejected_parent_keys = {by_contract.get((_text(l.get("company")), (_text(l.get("source_system")) or "").upper(),
                                             _text(l.get("parent_contract_id")))) for l in rejected_links}

    # 3. Determine CLM status and route balances.
    records: list[dict[str, Any]] = []
    clm_contracts: list[str] = []
    detector = clm_cfg.get("detector_field")
    true_values = {str(v) for v in clm_cfg.get("true_values", [])}
    false_values = {str(v) for v in clm_cfg.get("false_values", [])}
    virtual = rules_doc.get("virtual_balances") or {}
    for key, entry in sorted(contracts.items()):
        record = entry["record"]
        company, source, contract_id, currency, as_of = key
        category = _text(record["category"])
        attrs = {"T24.CATEGORY": category}
        if category == source_category:
            link = accepted_links.get(key)
            if link is None:
                for balance in entry["balances"]:
                    exceptions.append({"kind": "UNLINKED_CLS_ACCOUNT", "reason": "No verified link to a 3713 CLM parent",
                                       "contract_id": contract_id, "balance_type": balance["balance_type"],
                                       "amount": format(balance["amount"], "f"), "currency": currency})
                continue
            continue  # linked children are emitted with their parent below
        selected = in_population(attrs)
        if selected is not True:
            for balance in entry["balances"]:
                exceptions.append({"kind": "OUT_OF_SELECTED_POPULATION", "contract_id": contract_id, "category": category,
                                   "balance_type": balance["balance_type"], "amount": format(balance["amount"], "f"),
                                   "currency": currency})
            continue
        explicit = _flag(record.get("is_clm")) if "is_clm" in record else None
        detected = None
        if detector and record.get(detector) is not None:
            value = str(record[detector]).strip()
            detected = True if value in true_values else False if value in false_values else None
        link = linked_parents.get(key)
        if category != candidate:
            is_clm: bool | None = False if explicit is not True else None
        else:
            signals = {s for s in (explicit, detected) if s is not None}
            if link is not None:
                signals.add(True)
            if len(signals) > 1:
                is_clm = None
                exceptions.append({"kind": "CLM_STATUS_CONFLICT", "contract_id": contract_id,
                                   "detail": "Explicit flag, indicator and verified link disagree"})
            elif signals == {True} and link is None:
                is_clm = None
                exceptions.append({"kind": "CLM_WITHOUT_VERIFIED_LINK", "contract_id": contract_id,
                                   "detail": "Positive CLM status but no verified CLS link; components cannot be attached"})
            else:
                is_clm = next(iter(signals)) if signals else None
            if key in rejected_parent_keys and link is None:
                is_clm = None
                exceptions.append({"kind": "CLM_LINK_REJECTED", "contract_id": contract_id,
                                   "detail": "A link for this parent was rejected; CLM status unresolved"})
        if is_clm is True:
            clm_contracts.append(contract_id)
        codes_present = {b["balance_type"] for b in entry["balances"]}
        for code, parts in virtual.items():
            overlap = codes_present & {mapping_engine.normalize_code(p) for p in parts}
            if mapping_engine.normalize_code(code) in codes_present and overlap:
                exceptions.append({"kind": "VIRTUAL_AGGREGATE_AND_COMPONENT_BOTH_PRESENT", "contract_id": contract_id,
                                   "virtual": code, "components": sorted(overlap)})
        for balance in entry["balances"]:
            code = balance["balance_type"]
            base = {"company": company, "source_system": source, "contract_id": contract_id, "currency": currency,
                    "as_of": as_of, "category": category, "is_clm": is_clm if is_clm is not None else "unknown",
                    "balance_type": code, "record_id": f"{record['record_id']}#{balance['position']}:{code}",
                    "signed_closing_balance": format(balance["amount"], "f"),
                    "ecb_record_id": record["record_id"], "multivalue_position": balance["position"],
                    "amount_components": balance["components"], "amount_mode": mode}
            if code in rules["membership"]:
                records.append(base)
            elif code in excluded_types:
                exceptions.append({"kind": "OWNER_EXCLUDED_BALANCE_TYPE", "contract_id": contract_id,
                                   "balance_type": code, "amount": base["signed_closing_balance"]})
            else:
                exceptions.append({"kind": "UNCLASSIFIED_BALANCE_TYPE", "contract_id": contract_id, "balance_type": code,
                                   "amount": base["signed_closing_balance"], "currency": currency, "blocks_contract": True})
        if adapter.get("sparse_zero_convention"):
            for code in sorted(set(rules["membership"]) - codes_present):
                records.append({"company": company, "source_system": source, "contract_id": contract_id,
                                "currency": currency, "as_of": as_of, "category": category,
                                "is_clm": is_clm if is_clm is not None else "unknown", "balance_type": code,
                                "record_id": f"SPARSE-ZERO:{contract_id}:{code}", "signed_closing_balance": "0",
                                "zero_filled_by_convention": adapter["sparse_zero_convention"]})
        if link is not None:
            child = contracts[link["child_key"]]
            for balance in child["balances"]:
                code = balance["balance_type"]
                if code not in rules["extra_membership"]:
                    exceptions.append({"kind": "CLS_BALANCE_NOT_IN_CLM_SCOPE", "contract_id": child["record"]["contract_id"],
                                       "parent_contract_id": contract_id, "balance_type": code,
                                       "amount": format(balance["amount"], "f")})
                    continue
                embedded = [v for v, parts in virtual.items()
                            if code in {mapping_engine.normalize_code(p) for p in parts}
                            and mapping_engine.normalize_code(v) in codes_present]
                if embedded:
                    exceptions.append({"kind": "CLM_COMPONENT_ALREADY_EMBEDDED_IN_VIRTUAL_BALANCE",
                                       "parent_contract_id": contract_id, "balance_type": code, "virtual": embedded,
                                       "blocks_contract": True})
                records.append({
                    "company": company, "source_system": source, "contract_id": child["record"]["contract_id"],
                    "parent_contract_id": contract_id, "parent_category": candidate, "category": source_category,
                    "component_origin": rules["source_product"], "verified_link": True,
                    "currency": currency, "as_of": as_of, "is_clm": is_clm if is_clm is not None else "unknown",
                    "balance_type": code, "record_id": f"{child['record']['record_id']}#{balance['position']}:{code}",
                    "signed_closing_balance": format(balance["amount"], "f"),
                    "ecb_record_id": child["record"]["record_id"], "multivalue_position": balance["position"],
                    "amount_components": balance["components"], "amount_mode": mode,
                    "relationship": {"link_id": link["link_id"], "evidence": link["evidence"]},
                })
    blocking = defaultdict(list)
    for item in exceptions:
        if item.get("blocks_contract"):
            blocking[item.get("parent_contract_id") or item["contract_id"]].append(item["kind"] + ":" + item.get("balance_type", ""))
    if not virtual and clm_contracts:
        for contract_id in clm_contracts:
            blocking[contract_id].append("CLM_EMBEDDING_IN_VIRTUAL_BALANCES_UNVERIFIED")
    return {"reporting_date": reporting_date, "mode": mode, "records": records, "exceptions": exceptions,
            "accepted_links": [{k: v for k, v in l.items() if k not in ("parent_key", "child_key")}
                               for l in accepted_links.values()],
            "rejected_links": rejected_links, "blocking_by_contract": dict(blocking), "warnings": warnings,
            "clm_contracts": clm_contracts}


def run_review(payload: dict[str, Any], rules: dict[str, Any], rules_doc: dict[str, Any], policy: dict[str, Any],
               selectors_cfg: dict[str, Any]) -> dict[str, Any]:
    """Adapter + component engine + post-checks. Review output only."""
    adapted = adapt(payload, rules, rules_doc, policy, selectors_cfg)
    result = mapping_engine.aggregate(rules, adapted["records"])
    for contract in result["contracts"]:
        blockers = adapted["blocking_by_contract"].get(contract["contract_id"])
        if blockers:
            contract["flags"] = list(dict.fromkeys(contract["flags"] + blockers))
            contract["complete_for_supplied_records_and_required_types"] = False
            contract["group_totals_for_supplied_records"] = None
    if any(adapted["blocking_by_contract"].get(c["contract_id"]) for c in result["contracts"]):
        result["complete_for_supplied_records_and_required_types"] = False
        result["partition_totals_for_supplied_records"] = None
    blocking_exception_kinds = {"ECB_RECORD_REJECTED", "CLM_STATUS_CONFLICT", "CLM_WITHOUT_VERIFIED_LINK", "CLM_LINK_REJECTED"}
    if any(e["kind"] in blocking_exception_kinds for e in adapted["exceptions"]) or adapted["rejected_links"]:
        result["complete_for_supplied_records_and_required_types"] = False
        result["partition_totals_for_supplied_records"] = None
    result["adapter"] = {k: v for k, v in adapted.items() if k != "records"}
    result["limitations"].append("Exceptions (rejected, unclassified, unlinked, out-of-population) are listed under adapter.exceptions and are excluded from totals.")
    return result
