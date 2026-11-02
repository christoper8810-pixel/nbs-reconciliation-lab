"""Review-only, exact balance-type mapping for owner-supplied loan rules.

No bank connection, workbook evaluation, category inference, sign conversion,
legacy valuation inference, or report-production approval is performed here.
Amounts are signed closing balances supplied by the owner. Missing types are
never zero-filled. See the accompanying Claude brief before configuring CLM.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any


GROUPS = ("OUTSTANDING", "AMORTIZED_EARNED", "UNEARNED_PROFIT")
REQUIRED_FIELDS = (
    "company", "currency", "as_of", "source_system", "contract_id",
    "balance_type", "is_clm", "record_id", "signed_closing_balance",
)
PARTITION_FIELDS = ("company", "currency", "as_of", "source_system", "contract_id")
AMOUNT_PATTERN = re.compile(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)\Z")


class RuleError(ValueError):
    """An owner-supplied configuration is invalid."""


def normalize_code(value: Any) -> str:
    """Only surrounding whitespace and case are normalized; never aliases."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected a nonempty text code")
    return value.strip().upper()


def parse_clm(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        token = value.strip().lower()
        if token == "true":
            return True
        if token == "false":
            return False
        if token in ("unknown", ""):
            return None
    raise ValueError("is_clm must be true, false, or unknown; no inferred flag")


def validate_rules(raw: Any) -> dict[str, Any]:
    """Normalize and validate explicit membership and optional local catalogue.

    Empty CLM extras are an allowed unresolved configuration. Any CLM=true
    classification then fails closed. A nonempty exception must contain exactly
    two distinct, non-base balance types, each assigned to one of the groups.
    """
    if not isinstance(raw, dict) or not isinstance(raw.get("groups"), dict):
        raise RuleError("rules.groups must be an object")
    try:
        groups: dict[str, list[str]] = {}
        membership: dict[str, str] = {}
        for raw_group, codes in raw["groups"].items():
            group = normalize_code(raw_group)
            if group not in GROUPS or group in groups:
                raise RuleError("Only the three explicit target groups are supported")
            if not isinstance(codes, list) or not codes:
                raise RuleError(f"{group} must contain a nonempty balance-type list")
            groups[group] = []
            for value in codes:
                code = normalize_code(value)
                if code in membership:
                    raise RuleError(f"Duplicate balance type: {code}")
                membership[code] = group
                groups[group].append(code)
        if set(groups) != set(GROUPS):
            raise RuleError("All three target groups must be configured")
        catalogue = raw.get("valid_balance_types")
        valid_codes: set[str] | None = None
        if catalogue is not None:
            if not isinstance(catalogue, list) or not catalogue:
                raise RuleError("valid_balance_types must be a nonempty list when supplied")
            normalized = [normalize_code(code) for code in catalogue]
            if len(set(normalized)) != len(normalized):
                raise RuleError("Duplicate valid_balance_types entry")
            valid_codes = set(normalized)
            if set(membership) - valid_codes:
                raise RuleError("Base rules contain codes absent from the supplied local catalogue")
        clm = raw.get("clm", {})
        if not isinstance(clm, dict):
            raise RuleError("clm must be an object")
        if clm.get("detector_field") is not None and not isinstance(clm["detector_field"], str):
            raise RuleError("clm.detector_field must be text or null")
        if not isinstance(clm.get("true_values", []), list):
            raise RuleError("clm.true_values must be a list")
        extras = clm.get("extra_balances", [])
        if not isinstance(extras, list) or len(extras) not in (0, 2):
            raise RuleError("CLM must have exactly two extra balances, or an empty unresolved list")
        extra_membership: dict[str, str] = {}
        extra_basis: dict[str, str] = {}
        extra_approval: dict[str, dict[str, Any]] = {}
        for extra in extras:
            if not isinstance(extra, dict):
                raise RuleError("Each CLM extra must have balance_type and group")
            code = normalize_code(extra.get("balance_type"))
            group = normalize_code(extra.get("group"))
            if group not in GROUPS:
                raise RuleError(f"Invalid CLM target group: {group}")
            if code in membership or code in extra_membership:
                raise RuleError(f"CLM extra duplicates a base or exception type: {code}")
            if valid_codes is not None and code not in valid_codes:
                raise RuleError(f"CLM extra is absent from the supplied local catalogue: {code}")
            extra_membership[code] = group
            extra_basis[code] = normalize_code(extra.get("basis", "UNSPECIFIED"))
            approved = extra.get("owner_approved", False)
            if not isinstance(approved, bool):
                raise RuleError("CLM owner_approved must be an explicit boolean")
            approver = extra.get("approved_by")
            approved_on = extra.get("approved_on")
            if approved:
                if not isinstance(approver, str) or not approver.strip():
                    raise RuleError("Approved CLM grouping requires approved_by")
                if not isinstance(approved_on, str) or date.fromisoformat(approved_on).isoformat() != approved_on:
                    raise RuleError("Approved CLM grouping requires approved_on as YYYY-MM-DD")
            extra_approval[code] = {"owner_approved": approved, "approved_by": approver,
                                    "approved_on": approved_on}

        candidate_category = str(clm.get("candidate_category", "3713")).strip()
        source_category = str(clm.get("source_category", "6050")).strip()
        source_product = normalize_code(clm.get("source_product", "CLS"))
        if not candidate_category or not source_category:
            raise RuleError("CLM candidate and linked source categories must be explicit")

        crosswalk_raw = raw.get("ethix_crosswalk")
        crosswalk: dict[str, str] | None = None
        if crosswalk_raw is not None:
            if not isinstance(crosswalk_raw, dict):
                raise RuleError("ethix_crosswalk must be an owner-approved object")
            for key in ("approved_by", "approved_on"):
                if not isinstance(crosswalk_raw.get(key), str) or not crosswalk_raw[key].strip():
                    raise RuleError(f"Ethix crosswalk requires {key}")
            approval_date = date.fromisoformat(crosswalk_raw["approved_on"].strip())
            if approval_date.isoformat() != crosswalk_raw["approved_on"].strip():
                raise RuleError("Ethix approved_on must use YYYY-MM-DD")
            mapping = crosswalk_raw.get("mappings")
            if not isinstance(mapping, dict) or not mapping:
                raise RuleError("Ethix crosswalk requires explicit mappings")
            crosswalk = {}
            for source, target in mapping.items():
                source_code, target_code = normalize_code(source), normalize_code(target)
                if source_code in crosswalk:
                    raise RuleError("Duplicate normalized Ethix crosswalk source")
                if target_code not in membership and target_code not in extra_membership:
                    raise RuleError(f"Unknown Ethix crosswalk target: {target_code}")
                crosswalk[source_code] = target_code
        return {
            "groups": groups,
            "membership": membership,
            "extra_membership": extra_membership,
            "extra_basis": extra_basis,
            "extra_approval": extra_approval,
            "candidate_category": candidate_category,
            "source_category": source_category,
            "source_product": source_product,
            "valid_balance_types": valid_codes,
            "ethix_crosswalk": crosswalk,
            "ethix_approval": None if crosswalk_raw is None else {
                "approved_by": crosswalk_raw["approved_by"].strip(),
                "approved_on": crosswalk_raw["approved_on"].strip(),
            },
        }
    except RuleError:
        raise
    except (ValueError, TypeError) as exc:
        raise RuleError(str(exc)) from exc


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Ambiguous JSON: duplicate field {key}")
        result[key] = value
    return result


def load_rules(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8-sig") as handle:
        return validate_rules(json.load(handle, object_pairs_hook=_unique_json_object))


def classify(
    rules: dict[str, Any], balance_type: str, is_clm: bool | str | None,
    category: str | int | None = None, source_system: str = "T24",
    parent_category: str | int | None = None, component_origin: str | None = None,
    verified_link: bool | str | None = None,
) -> dict[str, Any]:
    """Classify one explicitly supplied type; report every unresolved condition.

    category=3713 is only the candidate scope. It never sets is_clm=True.
    Ethix needs an explicit owner-approved crosswalk, even for an identical
    spelling; that crosswalk alone cannot establish valuation equivalence.
    """
    flags: list[str] = []
    try:
        code, source = normalize_code(balance_type), normalize_code(source_system)
        clm = parse_clm(is_clm)
    except ValueError as exc:
        return {"balance_type": str(balance_type), "group": None,
                "status": "INCOMPLETE", "ready_for_mapping": False,
                "production_ready": False, "flags": ["INVALID_INPUT"], "detail": str(exc)}
    raw_code = code
    if source == "ETHIX":
        crosswalk = rules["ethix_crosswalk"]
        if crosswalk is None:
            flags.append("ETHIX_CROSSWALK_NOT_APPROVED")
            code = None
        elif code not in crosswalk:
            flags.append("ETHIX_TYPE_NOT_IN_APPROVED_CROSSWALK")
            code = None
        else:
            code = crosswalk[code]
    elif source not in ("T24", "TRANSACT"):
        flags.append("UNSUPPORTED_SOURCE_SYSTEM")
        code = None
    category_token = None if category is None or str(category).strip() == "" else str(category).strip()
    parent_category_token = None if parent_category is None else str(parent_category).strip()
    origin_token = component_origin.strip().upper() if isinstance(component_origin, str) else None
    is_extra = code is not None and code in rules["extra_membership"]
    link_verified = None
    try:
        link_verified = parse_clm(verified_link)
    except ValueError:
        flags.append("INVALID_VERIFIED_LINK_FLAG")
    if clm is None:
        flags.append("CLM_STATUS_UNKNOWN")
        if category_token == rules["candidate_category"]:
            flags.append("CATEGORY_3713_REQUIRES_EXPLICIT_CLM_REVIEW")
    if clm is True:
        if category_token is None:
            flags.append("CLM_SCOPE_UNVERIFIED")
        elif not is_extra and category_token != rules["candidate_category"]:
            flags.append("CLM_SCOPE_MISMATCH")
        if len(rules["extra_membership"]) != 2:
            flags.append("CLM_TWO_EXTRA_TYPES_NOT_CONFIGURED")
    group = rules["membership"].get(code)
    candidate_group = group
    if group is None and code is not None:
        if is_extra:
            candidate_group = rules["extra_membership"][code]
            if clm is True:
                scoped = True
                if category_token != rules["source_category"]:
                    flags.append("CLM_EXTRA_SOURCE_CATEGORY_MISMATCH")
                    scoped = False
                if parent_category_token != rules["candidate_category"]:
                    flags.append("CLM_EXTRA_PARENT_CATEGORY_UNVERIFIED")
                    scoped = False
                if origin_token != rules["source_product"]:
                    flags.append("CLM_EXTRA_SOURCE_PRODUCT_UNVERIFIED")
                    scoped = False
                if link_verified is not True:
                    flags.append("CLM_EXTRA_LINK_NOT_VERIFIED")
                    scoped = False
                if scoped:
                    group = candidate_group
                if not rules["extra_approval"][code]["owner_approved"]:
                    flags.append("CLM_GROUP_ASSIGNMENT_REQUIRES_OWNER_APPROVAL")
            else:
                flags.append("CLM_ONLY_BALANCE_NOT_APPLICABLE")
        else:
            flags.append("UNKNOWN_BALANCE_TYPE")
    return {
        "source_system": source,
        "source_balance_type": raw_code,
        "balance_type": code,
        "category": category_token,
        "parent_category": parent_category_token,
        "component_origin": origin_token,
        "verified_link_supplied": link_verified,
        "is_clm": clm,
        "group": group,
        "candidate_group": candidate_group,
        "grouping_basis": rules["extra_basis"].get(code) if is_extra else "OWNER_BASE_RULE",
        "grouping_approval": rules["extra_approval"].get(code) if is_extra else None,
        "status": "CLASSIFIED" if not flags else "INCOMPLETE",
        "ready_for_mapping": not flags,
        "production_ready": False,
        "local_catalogue_supplied": rules["valid_balance_types"] is not None,
        "flags": flags,
    }


def parse_money(value: Any) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("Use decimal text or integers, never binary floating-point money")
    if not isinstance(value, (str, int, Decimal)):
        raise ValueError("A signed closing balance is required")
    token = str(value).strip()
    if not AMOUNT_PATTERN.fullmatch(token):
        raise ValueError("Amount must be an unambiguous signed decimal without commas or formulas")
    amount = Decimal(token)
    if not amount.is_finite():
        raise ValueError("Amount must be finite")
    return amount


def exact_sum(values: list[Decimal]) -> Decimal:
    """Sum without losing precision at Decimal's default 28-digit boundary."""
    if not values:
        return Decimal("0")
    fraction_digits = max(max(0, -v.as_tuple().exponent) for v in values)
    integer_digits = max(max(1, v.adjusted() + 1) for v in values)
    with localcontext() as context:
        context.prec = integer_digits + fraction_digits + len(str(len(values))) + 2
        return sum(values, Decimal("0"))


def _identifier(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Identifier must be nonempty text")
    return value.strip()


def _json_safe(value: Any) -> Any:
    """Preserve optional source metadata without introducing float conversion."""
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def aggregate(rules: dict[str, Any], records: list[Any]) -> dict[str, Any]:
    """Review one signed closing-balance record per contract/type/source grain.

    All configured base types must be explicitly present, including any zeros.
    CLM contracts also require both configured extras. Input completeness is
    scoped to supplied contracts; this cannot verify the population or source
    extraction. Incomplete contracts have no totals, including no partial totals.
    """
    if not isinstance(records, list):
        raise ValueError("Input must be a record list")
    review_rows: list[dict[str, Any]] = []
    buckets: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    orphan_count = 0
    for index, record in enumerate(records, start=1):
        row: dict[str, Any] = {"input_row": index, "flags": [], "group": None,
                               "accepted": False, "signed_closing_balance": None}
        if not isinstance(record, dict):
            row["flags"].append("RECORD_NOT_OBJECT")
            review_rows.append(row)
            orphan_count += 1
            continue
        row["source_record"] = _json_safe(record)
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            row["flags"].append("MISSING_REQUIRED_FIELDS")
            row["missing_fields"] = missing
        normalized: dict[str, Any] = {}
        for field in PARTITION_FIELDS:
            try:
                value = record.get(field)
                if field in ("source_system", "currency"):
                    normalized[field] = normalize_code(value)
                else:
                    normalized[field] = _identifier(value)
                if field == "as_of":
                    checked_date = date.fromisoformat(normalized[field])
                    if checked_date.isoformat() != normalized[field]:
                        raise ValueError("as_of must use YYYY-MM-DD")
            except (ValueError, TypeError):
                row["flags"].append(f"INVALID_{field.upper()}")
        row.update(normalized)
        try:
            row["record_id"] = _identifier(record.get("record_id"))
        except ValueError:
            row["flags"].append("INVALID_RECORD_ID")
        try:
            amount = parse_money(record.get("signed_closing_balance"))
            row["_amount"] = amount
            row["signed_closing_balance"] = format(amount, "f")
        except ValueError:
            row["flags"].append("INVALID_SIGNED_CLOSING_BALANCE")
        classified = classify(
            rules, record.get("balance_type"), record.get("is_clm"),
            record.get("category"), normalized.get("source_system", "UNKNOWN"),
            record.get("parent_category"), record.get("component_origin"), record.get("verified_link"),
        )
        for field in ("source_balance_type", "balance_type", "category", "is_clm", "group", "candidate_group",
                      "parent_category", "component_origin", "verified_link_supplied", "grouping_basis",
                      "grouping_approval"):
            row[field] = classified.get(field)
        row["flags"].extend(classified["flags"])
        report_contract_id = normalized.get("contract_id")
        if row.get("balance_type") in rules["extra_membership"]:
            try:
                row["parent_contract_id"] = _identifier(record.get("parent_contract_id"))
                report_contract_id = row["parent_contract_id"]
                if report_contract_id == normalized.get("contract_id"):
                    row["flags"].append("CLM_COMPONENT_EQUALS_PARENT_CONTRACT")
            except ValueError:
                row["flags"].append("CLM_EXTRA_PARENT_CONTRACT_ID_MISSING")
        elif record.get("parent_contract_id") not in (None, ""):
            row["flags"].append("UNEXPECTED_PARENT_LINK_ON_BASE_BALANCE")
        row["report_contract_id"] = report_contract_id
        if all(field in normalized for field in PARTITION_FIELDS):
            bucket_key = tuple(normalized[field] for field in PARTITION_FIELDS[:-1]) + (report_contract_id,)
            row["_key"] = bucket_key
            buckets[bucket_key].append(row)
        else:
            orphan_count += 1
        review_rows.append(row)

    identities: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    grains: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    components: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in review_rows:
        if all(field in row for field in ("source_system", "company", "record_id")):
            identities[(row["source_system"], row["company"], row["record_id"])].append(row)
        if "_key" in row and row.get("balance_type") is not None:
            grains[(*row["_key"], row["balance_type"])].append(row)
        if row.get("balance_type") in rules["extra_membership"] and all(
            field in row for field in ("company", "source_system", "as_of", "contract_id", "parent_contract_id")
        ):
            # A component has one parent at an as-of date. Relinking across dates
            # is allowed; conflicting parents across currencies on one date fail.
            components[(row["company"], row["source_system"], row["as_of"], row["contract_id"])].append(row)
    for duplicates, flag in ((identities, "DUPLICATE_RECORD_ID"), (grains, "DUPLICATE_CONTRACT_BALANCE_GRAIN")):
        for matching in duplicates.values():
            if len(matching) > 1:
                for row in matching:
                    row["flags"].append(flag)
    for component_rows in components.values():
        if len({row["parent_contract_id"] for row in component_rows}) > 1:
            for row in component_rows:
                row["flags"].append("CLM_LINKED_COMPONENT_REUSED_ACROSS_PARENTS")

    contracts: list[dict[str, Any]] = []
    for key, rows in sorted(buckets.items()):
        flags: list[str] = []
        clm_values = {row.get("is_clm") for row in rows}
        if len(clm_values) != 1:
            flags.append("MIXED_CONTRACT_CLM_FLAGS")
        clm = next(iter(clm_values)) if len(clm_values) == 1 else None
        base_rows = [row for row in rows if row.get("balance_type") in rules["membership"]]
        extra_rows = [row for row in rows if row.get("balance_type") in rules["extra_membership"]]
        categories = {row["category"] for row in base_rows if row.get("category") is not None}
        if len(categories) > 1:
            flags.append("MIXED_CONTRACT_CATEGORIES")
        required = set(rules["membership"])
        if clm is True:
            required.update(rules["extra_membership"])
            if len(rules["extra_membership"]) != 2:
                flags.append("CLM_TWO_EXTRA_TYPES_NOT_CONFIGURED")
        if extra_rows:
            component_ids = {row["contract_id"] for row in extra_rows if "contract_id" in row}
            if len(component_ids) != 1:
                flags.append("CLM_EXTRA_BALANCES_FROM_DIFFERENT_COMPONENT_CONTRACTS")
                for row in extra_rows:
                    row["flags"].append("CLM_EXTRA_BALANCES_FROM_DIFFERENT_COMPONENT_CONTRACTS")
            parent_confirmed = bool(base_rows) and all(
                row.get("category") == rules["candidate_category"] and row.get("is_clm") is True
                and row.get("contract_id") == key[-1] for row in base_rows
            )
            if not parent_confirmed:
                flags.append("CLM_EXTRA_PARENT_NOT_PRESENT_OR_CONFIRMED")
                for row in extra_rows:
                    row["flags"].append("CLM_EXTRA_PARENT_NOT_PRESENT_OR_CONFIRMED")
        present = {row["balance_type"] for row in rows if row.get("balance_type") is not None}
        missing_types = sorted(required - present)
        if missing_types:
            flags.append("MISSING_REQUIRED_BALANCE_TYPES")
        if any(row["flags"] for row in rows):
            flags.append("RECORD_VALIDATION_FAILED")
        complete = not flags
        totals = None
        if complete:
            totals = {
                group: format(exact_sum([row["_amount"] for row in rows if row["group"] == group]), "f")
                for group in GROUPS
            }
        for row in rows:
            row["accepted"] = not row["flags"]
        contracts.append({
            **dict(zip(PARTITION_FIELDS, key)),
            "is_clm": clm,
            "category": next(iter(categories)) if len(categories) == 1 else None,
            "record_count": len(rows),
            "linked_component_contract_ids": sorted({row["contract_id"] for row in extra_rows
                                                     if "contract_id" in row}),
            "complete_for_supplied_records_and_required_types": complete,
            "missing_required_balance_types": missing_types,
            "flags": flags,
            "group_totals_for_supplied_records": totals,
            "production_ready": False,
        })
    all_complete = bool(contracts) and not orphan_count and all(
        contract["complete_for_supplied_records_and_required_types"] for contract in contracts
    )
    partition_totals = None
    if all_complete:
        partitions: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
        for contract in contracts:
            partitions[tuple(contract[field] for field in PARTITION_FIELDS[:-1])].append(contract)
        partition_totals = [{
            **dict(zip(PARTITION_FIELDS[:-1], key)),
            "contract_count": len(contracts_in_partition),
            "group_totals_for_supplied_records": {
                group: format(exact_sum([Decimal(c["group_totals_for_supplied_records"][group])
                                         for c in contracts_in_partition]), "f")
                for group in GROUPS
            },
        } for key, contracts_in_partition in sorted(partitions.items())]
    for row in review_rows:
        row.pop("_amount", None)
        row.pop("_key", None)
        row["flags"] = list(dict.fromkeys(row["flags"]))
    return {
        "report_kind": "OWNER_REVIEW_ONLY",
        "production_ready": False,
        "population_and_source_extraction_verified": False,
        "local_catalogue_supplied": rules["valid_balance_types"] is not None,
        "ethix_crosswalk_approval": rules["ethix_approval"],
        "ethix_valuation_equivalence_verified": False,
        "complete_for_supplied_records_and_required_types": all_complete,
        "input_record_count": len(records),
        "rejected_record_count": sum(not row["accepted"] for row in review_rows),
        "unassigned_record_count": orphan_count,
        "partition_totals_for_supplied_records": partition_totals,
        "contracts": contracts,
        "records": review_rows,
        "limitations": [
            "Totals use supplied signed closing balances; no sign or valuation transformation is inferred.",
            "Every required type must be supplied explicitly; absent types are not zero.",
            "Category 3713 identifies CLM review scope, not CLM status.",
            "CLM extras require a supplied verified link from the specific CLS6050 component to its Murabaha3713 parent.",
            "Exactly one linked CLS component must supply both extras for a parent at each as-of date.",
            "No loan population, bank dictionary, feed extraction, or legacy valuation equivalence is certified.",
        ],
    }


def load_records(path: str | Path) -> list[Any]:
    source = Path(path)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        if source.suffix.lower() == ".csv":
            reader = csv.DictReader(handle)
            if reader.fieldnames is None or len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ValueError("CSV requires distinct named headers")
            records = list(reader)
            if any(None in row or any(value is None for value in row.values()) for row in records):
                raise ValueError("CSV has ambiguous row width; quote amounts and fields correctly")
            return records
        payload = json.load(handle, parse_float=Decimal, object_pairs_hook=_unique_json_object)
    records = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ValueError("JSON must contain a record array or an object with records")
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    one = commands.add_parser("classify", help="Review exact membership of one balance type")
    one.add_argument("--rules", required=True)
    one.add_argument("--balance-type", required=True)
    one.add_argument("--is-clm", required=True, choices=("true", "false", "unknown"))
    one.add_argument("--category")
    one.add_argument("--source-system", default="T24")
    one.add_argument("--parent-category")
    one.add_argument("--component-origin")
    one.add_argument("--verified-link", choices=("true", "false", "unknown"))
    many = commands.add_parser("aggregate", help="Review supplied signed closing balances")
    many.add_argument("--rules", required=True)
    many.add_argument("--input", required=True)
    many.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        rules = load_rules(args.rules)
        if args.command == "classify":
            result = classify(rules, args.balance_type, args.is_clm, args.category, args.source_system,
                              args.parent_category, args.component_origin, args.verified_link)
            print(json.dumps(result, indent=2))
            return 0 if result["ready_for_mapping"] else 2
        result = aggregate(rules, load_records(args.input))
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(target), "production_ready": False,
                          "complete_for_supplied_records_and_required_types":
                          result["complete_for_supplied_records_and_required_types"]}, indent=2))
        return 0 if result["complete_for_supplied_records_and_required_types"] else 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "production_ready": False, "detail": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
