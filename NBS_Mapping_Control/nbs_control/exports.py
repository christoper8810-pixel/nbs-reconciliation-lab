"""Exports and owner-workbook round trip.

Three separate outputs as required: source-versus-proposed differences,
unresolved exceptions, and the approved (effective) mapping configuration.
The owner review workbook can be edited and re-imported; imported rows are
validated like UI decisions and stale rows (changed evidence) are refused.
Workbook text is always written as inert text, never as formulas.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from .config import parse_json
from .store import ACTIONS, DecisionError

DISCLAIMER = ("Owner review output. Approval is application state, not bank reconciliation. "
              "No amount here certifies an NBS report.")
DECISION_COLUMNS = ["Business mapping ID", "Evidence fingerprint", "Source", "Sheet", "Row", "Kind", "Hierarchy path",
                    "Legacy rule text", "Proposal", "Proposed metric", "Proposed selector (JSON)", "Current decision",
                    "Decision validity", "Effective state", "Blocking reasons",
                    "Action", "Owner", "Approved on", "Reason", "Approval evidence", "Metric expression",
                    "Selectors (JSON)", "Amount basis", "Exclusive group", "Effective from", "Effective to",
                    "NBS target business IDs"]
EDITABLE_FROM = DECISION_COLUMNS.index("Action")
AMBER = PatternFill("solid", fgColor="FFF2CC")
HEAD = PatternFill("solid", fgColor="DDEBF7")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def inert(value: Any) -> Any:
    """Make text safe for spreadsheets and CSV (no formula execution)."""
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + value
    return value


def rule_text(item: dict[str, Any]) -> str:
    parts = []
    for cell in item["cells"]:
        if cell["column"] == item.get("description_column"):
            continue
        text = f"{cell['coord']}: {cell['value']}"
        alias = cell.get("alias") or {}
        if alias.get("status") == "RESOLVED":
            text += f"  [alias of {alias['chain'][-1]}: {alias.get('value')}]"
        if cell.get("note"):
            text += f"  [comment: {cell['note']}]"
        parts.append(text)
    return "\n".join(parts)


def _write_csv(path: Path, header: list[str], rows: list[list[Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow([inert(v) if not isinstance(v, (dict, list)) else json.dumps(v, ensure_ascii=False) for v in row])
    return path


def export_source_vs_proposed(service, path: Path) -> Path:
    header = ["business_id", "source_system", "sheet", "row", "source_id", "hierarchy_path", "legacy_rule_text",
              "legacy_tokens", "proposed_metric", "proposal_basis", "owner_group_codes_missing_from_legacy",
              "legacy_codes_outside_proposed_group", "unknown_identifiers", "draft_selector", "selector_status",
              "amount_basis", "formula_corrections", "dependencies", "notes", "finding_refs", "nbs_row_candidates"]
    rows = []
    for item in service.catalog["mappings"]:
        if item["kind"] != "RULE":
            continue
        p = item["proposal"]
        diff = p.get("token_diff") or {}
        rows.append([item["business_id"], item["source_system"], item["sheet"], item["source_row"], item["source_id"],
                     item["hierarchy_path"], rule_text(item), ", ".join(diff.get("legacy_tokens", [])),
                     p.get("metric_expression"), p.get("basis"), ", ".join(diff.get("missing_from_legacy", [])),
                     ", ".join(diff.get("legacy_outside_best_group", [])), ", ".join(diff.get("unknown", [])),
                     p.get("selectors"), p.get("selector_status"), p.get("amount_basis"),
                     "\n".join(f"{c['coord']}: {c['legacy']} -> {c['proposed']} ({c['kind']})" for c in p["formula_corrections"]),
                     "; ".join(p.get("dependencies", [])), "; ".join(p.get("notes", [])),
                     ", ".join(item.get("finding_refs", [])),
                     ", ".join(f"{c['sheet']}!{c['row']} ({c['business_id']})" for c in item.get("nbs_row_candidates", []))])
    return _write_csv(path, header, rows)


def export_unresolved(service, path: Path) -> Path:
    view = service.unresolved_view()
    header = ["category", "id", "source_system", "location", "description", "state", "reasons_or_detail"]
    rows: list[list[Any]] = []
    for entry in view["global"]:
        rows.append(["GLOBAL:" + entry["area"], entry["item"], "", "", "", "OPEN", entry["detail"]])
    for entry in view["sections"]:
        s = entry["section"]
        rows.append(["SECTION", s["section_id"], "ETHIX/T24", s["ethix_range"], f"{s['identity']} {s['title']}",
                     entry["validity"] if entry["decision"] else "NO_DECISION", "; ".join(s["problems"]) or "Join awaiting owner approval"])
    for entry in view["findings"]:
        f = entry["entry"]
        rows.append(["FINDING:" + f["kind"], f["item_id"], f["source_system"], f"{f['sheet']}!{f['cell']}",
                     f["finding_title"], entry["validity"] if entry["decision"] else "NO_DECISION",
                     f["required_owner_decision"]])
    for entry in view["mappings"]:
        item = entry["item"]
        rows.append(["MAPPING", item["business_id"], item["source_system"], f"{item['sheet']}!{item['source_row']}",
                     item["hierarchy_path"], entry["state"], "; ".join(entry["reasons"])])
    return _write_csv(path, header, rows)


def export_approved_config(service, path: Path, as_of: str | None = None) -> Path:
    effective = service.effective_compiled(as_of)
    document = {
        "document": "approved_mapping_configuration",
        "generated_at": _stamp(),
        "statement": DISCLAIMER + " Only mappings with explicit, current owner approval and validated selectors, "
                                  "metrics, signs and dependencies are included.",
        "catalog_version": service.catalog["catalog_version"],
        "sources": service.catalog["sources"],
        "config_hashes": service.config.hashes(),
        "balance_rule_version": service.config["balance_rules"].get("rule_version"),
        "mapping_count": len(effective),
        "mappings": [{
            "business_id": e["business_id"],
            "source_system": e["item"]["source_system"],
            "sheet": e["item"]["sheet"],
            "hierarchy_path": e["item"]["hierarchy_path"],
            "evidence_fingerprint": e["item"]["fingerprint"],
            "spec": e["effective_spec"],
            "decision": {k: v for k, v in service.store.current("MAPPING", e["business_id"]).items()
                         if k in ("version", "action", "actor", "approved_on", "reason", "approval_evidence", "recorded_at")},
        } for e in effective],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _sheet(workbook, title: str, header: list[str], rows: list[list[Any]], widths: dict[int, int] | None = None,
           editable_from: int | None = None):
    ws = workbook.create_sheet(title)
    ws.append(header)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = AMBER if editable_from is not None and cell.column - 1 >= editable_from else HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for row_number, row in enumerate(rows, start=2):
        values = []
        for value in row:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            values.append(value)
        ws.append(values)
        for column, value in enumerate(values, start=1):
            if isinstance(value, str) and value[:1] in ("=", "+", "-", "@"):
                ws.cell(row_number, column).data_type = "s"  # keep inert text, never a formula
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    for index, width in (widths or {}).items():
        ws.column_dimensions[openpyxl.utils.get_column_letter(index)].width = width
    return ws


def export_owner_workbook(service, path: Path) -> Path:
    workbook = openpyxl.Workbook()
    readme = workbook.active
    readme.title = "README"
    summary = service.summary()
    lines = [
        ["NBS mapping control - owner review workbook"],
        [DISCLAIMER],
        [f"Generated {_stamp()} from catalog version {summary['catalog_version']}"],
        *[[f"Source {s}: {v['file_name']} sha256 {v['sha256']}"] for s, v in summary["sources"].items()],
        [""],
        ["Edit only the amber columns on 'Owner decisions'. Re-import with: python -m nbs_control import-decisions <file>"],
        ["Each row is keyed by the stable Business mapping ID; edits survive sorting and refresh."],
        ["A row whose Evidence fingerprint no longer matches the current source is refused as STALE."],
        ["APPROVE_PROPOSAL / APPROVE_OVERRIDE need Owner, Approved on (YYYY-MM-DD), Reason and Approval evidence."],
        ["Selectors are structured JSON on configured T24 fields only, e.g. {\"field\": \"T24.CATEGORY\", \"op\": \"in\", \"values\": [\"3701\"]}."],
        ["Metric expression names configured metrics only, e.g. OUTSTANDING or OUTSTANDING + AMORTIZED_EARNED."],
        ["Recording a decision does not make it effective: see 'Effective state' and 'Blocking reasons'."],
    ]
    for line in lines:
        readme.append(line)
    readme.column_dimensions["A"].width = 140

    evaluations = service.evaluations()
    decision_rows = []
    for e in evaluations:
        item, decision = e["item"], e["decision"]
        p = item["proposal"]
        spec = (decision or {}).get("payload", {}).get("spec", {}) if decision else {}
        decision_rows.append([
            item["business_id"], item["fingerprint"], item["source_system"], item["sheet"], item["source_row"],
            item["kind"], item["hierarchy_path"], rule_text(item), p.get("basis"), p.get("metric_expression"),
            p.get("selectors"), f"v{decision['version']} {decision['action']}" if decision else None,
            e["validity"], e["state"], "; ".join(e["reasons"]),
            None, None, None, None, None, spec.get("metric_expression"), spec.get("selectors"), spec.get("amount_basis"),
            spec.get("exclusive_group"), spec.get("effective_from"), spec.get("effective_to"),
            ", ".join(spec.get("nbs_target_business_ids", [])) or None,
        ])
    ws = _sheet(workbook, "Owner decisions", DECISION_COLUMNS, decision_rows,
                {1: 18, 7: 50, 8: 60, 9: 40, 15: 50, 22: 40}, editable_from=EDITABLE_FROM)
    validation = DataValidation(type="list", formula1='"' + ",".join(ACTIONS["MAPPING"]) + '"', allow_blank=True)
    ws.add_data_validation(validation)
    action_col = openpyxl.utils.get_column_letter(EDITABLE_FROM + 1)
    validation.add(f"{action_col}2:{action_col}{ws.max_row}")
    basis = DataValidation(type="list", formula1='"' + ",".join(service.config["calculation_policy"]["amount_bases"]) + '"',
                           allow_blank=True)
    ws.add_data_validation(basis)
    basis_col = openpyxl.utils.get_column_letter(DECISION_COLUMNS.index("Amount basis") + 1)
    basis.add(f"{basis_col}2:{basis_col}{ws.max_row}")

    proposed = [[i["business_id"], i["source_system"], i["sheet"], i["source_row"], i["hierarchy_path"],
                 i["proposal"]["metric_expression"], i["proposal"]["basis"], i["proposal"]["selector_status"],
                 i["proposal"]["selectors"], "; ".join(i["proposal"]["dependencies"]), ", ".join(i["finding_refs"])]
                for i in service.proposed_view()]
    _sheet(workbook, "Proposed", ["Business ID", "Source", "Sheet", "Row", "Hierarchy path", "Proposed metric",
                                  "Basis", "Selector status", "Draft selector", "Dependencies", "Findings"], proposed,
           {5: 50, 7: 60, 9: 40, 10: 50})
    effective = [[e["business_id"], e["item"]["source_system"], e["item"]["sheet"], e["item"]["hierarchy_path"],
                  e["decision"]["payload"]["spec"]] for e in evaluations if e["state"] == "EFFECTIVE"]
    _sheet(workbook, "Effective", ["Business ID", "Source", "Sheet", "Hierarchy path", "Effective spec"], effective,
           {4: 50, 5: 80})
    unresolved = service.unresolved_view()
    _sheet(workbook, "Unresolved", ["Business ID", "Source", "Sheet", "Row", "Hierarchy path", "State", "Reasons"],
           [[e["item"]["business_id"], e["item"]["source_system"], e["item"]["sheet"], e["item"]["source_row"],
             e["item"]["hierarchy_path"], e["state"], "; ".join(e["reasons"])] for e in unresolved["mappings"]],
           {5: 50, 7: 80})
    _sheet(workbook, "Findings queue", ["Item ID", "Finding", "Kind", "Source", "Sheet", "Cell", "Blocking",
                                        "Current value", "Implication", "Required decision", "Owner update", "Decision"],
           [[f["item_id"], f["finding_title"], f["kind"], f["source_system"], f["sheet"], f["cell"], f["blocking"],
             f["current_value"], f["implication"], f["required_owner_decision"], f["owner_update"],
             (service.store.current("FINDING", f["item_id"]) or {}).get("action")] for f in service.catalog["findings_queue"]],
           {1: 40, 2: 50, 8: 50, 9: 60, 10: 60})
    _sheet(workbook, "Sections", ["Section ID", "Identity", "Title", "Ethix range", "NBS candidates", "Problems", "Decision"],
           [[s["section_id"], s["identity"], s["title"], s["ethix_range"],
             "; ".join(f"{c['nbs_sheet']}!{c['nbs_title_cell']} -> {c['block_key']}" for c in s["candidates"]) or "NONE",
             "; ".join(s["problems"]), (service.store.current("SECTION", s["section_id"]) or {}).get("action")]
            for s in service.catalog["sections"]], {3: 60, 5: 60})
    _sheet(workbook, "Global open items", ["Area", "Item", "Detail"],
           [[g["area"], g["item"], g["detail"]] for g in unresolved["global"]], {2: 40, 3: 100})
    rules = service.rules
    balance_rows = [[group, code, "BASE", "Approved lending population only", "Owner rule"]
                    for group, codes in rules["groups"].items() for code in codes]
    balance_rows += [[group, code, "CLM LINKED CLS", f"Parent {rules['candidate_category']} / child {rules['source_category']}",
                      "Approved" if rules["extra_approval"][code]["owner_approved"] else "PROPOSED - owner approval required"]
                     for code, group in rules["extra_membership"].items()]
    _sheet(workbook, "Balance rules", ["Group", "Balance type", "Role", "Scope", "Status"], balance_rows, {4: 40, 5: 40})
    _sheet(workbook, "Bank inputs", ["#", "Required input", "Exact field / definition"],
           [[i + 1, a, b] for i, (a, b) in enumerate(BANK_INPUTS)], {2: 45, 3: 110})
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return path


def import_owner_workbook(service, path: Path, default_actor: str | None = None) -> dict[str, Any]:
    """Apply amber-column decisions from an exported workbook. Each row is validated independently."""
    workbook = openpyxl.load_workbook(path, data_only=False, read_only=True)
    try:
        ws = workbook["Owner decisions"]
        rows = ws.iter_rows(values_only=True)
        header = list(next(rows))
        if header != DECISION_COLUMNS:
            raise ValueError("Unexpected 'Owner decisions' header; export a fresh workbook")
        applied, errors = [], []
        catalog_ids = {m["business_id"]: m for m in service.catalog["mappings"]}
        for number, row in enumerate(rows, start=2):
            record = dict(zip(header, row))
            action = (record.get("Action") or "").strip() if isinstance(record.get("Action"), str) else None
            if not action:
                continue
            business_id = record["Business mapping ID"]
            try:
                item = catalog_ids.get(business_id)
                if item is None:
                    raise DecisionError("Business mapping ID not in current catalog (orphaned)")
                if record["Evidence fingerprint"] != item["fingerprint"]:
                    raise DecisionError("STALE: source evidence changed since export; review the refreshed row")
                spec = {}
                if record.get("Metric expression"):
                    spec["metric_expression"] = str(record["Metric expression"]).strip()
                if record.get("Selectors (JSON)"):
                    spec["selectors"] = parse_json(str(record["Selectors (JSON)"]))
                if record.get("Amount basis"):
                    spec["amount_basis"] = str(record["Amount basis"]).strip()
                for column, key in (("Exclusive group", "exclusive_group"), ("Effective from", "effective_from"),
                                    ("Effective to", "effective_to")):
                    value = record.get(column)
                    if value not in (None, ""):
                        spec[key] = value.date().isoformat() if hasattr(value, "date") else str(value).strip()
                if record.get("NBS target business IDs"):
                    spec["nbs_target_business_ids"] = [t.strip() for t in str(record["NBS target business IDs"]).split(",") if t.strip()]
                approved_on = record.get("Approved on")
                if hasattr(approved_on, "date"):
                    approved_on = approved_on.date().isoformat()
                service.decide_mapping(
                    business_id, action, actor=str(record.get("Owner") or default_actor or "").strip(),
                    reason=str(record.get("Reason") or ""), approved_on=str(approved_on).strip() if approved_on else None,
                    approval_evidence=str(record.get("Approval evidence") or "") or None,
                    spec=spec or None, origin="WORKBOOK_IMPORT")
                applied.append(business_id)
            except (DecisionError, ValueError) as exc:
                errors.append({"row": number, "business_id": business_id, "error": str(exc)})
        return {"applied": applied, "errors": errors}
    finally:
        workbook.close()


def import_legacy_review_workbook(service, path: Path) -> dict[str, Any]:
    """Read owner fields from the starter review workbook as review notes only (never executable)."""
    workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
    by_source = {m["source_id"]: m for m in service.catalog["mappings"]}
    recorded, skipped = [], []
    try:
        for name in ("T24 register", "Ethix register"):
            if name not in workbook.sheetnames:
                continue
            rows = workbook[name].iter_rows(min_row=6, values_only=True)
            header = list(next(rows))
            for row in rows:
                record = dict(zip(header, row))
                decision = str(record.get("Owner decision") or "").strip()
                if decision in ("", "PENDING"):
                    continue
                item = by_source.get(record.get("Evidence ID"))
                if item is None:
                    skipped.append({"evidence_id": record.get("Evidence ID"), "reason": "Evidence ID not in current source version"})
                    continue
                service.decide_mapping(item["business_id"], "RECORD_REVIEW_NOTE",
                                       actor=str(record.get("Approved by") or "Legacy review workbook"),
                                       reason=f"Workbook decision '{decision}': {record.get('Decision reason') or ''}".strip(),
                                       spec={"owner_metric_text": record.get("Owner metric")}, origin="LEGACY_WORKBOOK")
                recorded.append(item["business_id"])
    finally:
        workbook.close()
    return {"recorded_as_review_notes": recorded, "skipped": skipped,
            "note": "Free-text workbook decisions are review notes, not executable mappings."}


def export_all(service, directory: Path) -> dict[str, str]:
    directory.mkdir(parents=True, exist_ok=True)
    return {
        "source_vs_proposed": str(export_source_vs_proposed(service, directory / "source_vs_proposed.csv")),
        "unresolved_exceptions": str(export_unresolved(service, directory / "unresolved_exceptions.csv")),
        "approved_mapping_config": str(export_approved_config(service, directory / "approved_mapping_config.json")),
        "owner_review_workbook": str(export_owner_workbook(service, directory / "NBS_Owner_Review.xlsx")),
    }


BANK_INPUTS = [
    ("Local balance dictionary", "AC.BALANCE.TYPE records for all 19 base types plus CREDIT and ACCDEPOSITPFT (and PDO*, *SP, DUEPRINCIPALPFT, NABPRINCIPALPFT seen in the workbook): @ID, description, virtual/real flag and virtual component list -> config/balance_rules.json valid_balance_types / virtual_balances"),
    ("ECB extract schema", "EB.CONTRACT.BALANCES field names for the multivalue balance type (workbook text says CURR.ASSET.TYPE / CUR.ASSET.TYPE), OPEN.BALANCE, CREDIT.MVMT, DEBIT.MVMT or a closing field; sign convention; snapshot date and book/value date basis -> calculation_policy.ecb_adapter"),
    ("CLM indicator", "Bank field (table + field name) and values that positively identify a CLM arrangement within category 3713 -> balance_rules.clm.detector_field / true_values / false_values"),
    ("CLM relationship", "Authoritative 3713 Murabaha arrangement -> 6050 CLS account link: source table/field, company, currency, effective date; one-to-one or allocation policy"),
    ("CREDIT group", "Owner decision on CREDIT's report group (proposed OUTSTANDING), sign and valuation basis -> balance_rules.clm.extra_balances owner_approved"),
    ("Loan fees", "T24 source and balance identifiers for Ethix Loan_Fees_QAR, sign, valuation basis and overlap with OUTSTANDING/AMORTIZED_EARNED -> calculation_policy.metrics.LOAN_FEES"),
    ("Suspense SP", "Definitions of ACCDEFERREDPFTSP ... NABPRINCIPALPFTSP and the Table 11 row 25 metric -> calculation_policy.metrics.SUSPENSE_SP"),
    ("Unlisted identifiers", "Local definitions and owner disposition for PDOACCOUNT, PDODEFERREDPFT, PDOPRINCIPALPFT, DUEPRINCIPALPFT, NABPRINCIPALPFT -> owner_excluded_balance_types or a new owner-approved metric"),
    ("Selector fields", "Exact T24 tables/fields for CATEGORY, PRODUCT, PRODUCT.LINE, SECTOR, INDUSTRY, TARGET, RESIDENCE, L.INT.RISK.RT and local fields -> report_selectors.fields (status APPROVED)"),
    ("Ethix crosswalk", "SIC, RIM, SYN/IST/IJR, Personal/NonPersonal, GL and residency value maps to T24 fields; resolve RIM2398 K37/L37 asymmetry, SYN private-sector overlap and GL1300050001 allocation -> report_selectors.crosswalk / contradictions"),
    ("Lending population", "Approved category/product selector for the loan population to which the 19 rules apply -> report_selectors.populations.LENDING_BASE"),
    ("Maturity", "Maturity date field (AA.ACCOUNT.DETAILS MATURITY.DATE?), reporting date, treatment of matured/overdue, same-day and 'Without Maturity' column, contractual vs behavioural maturity -> calculation_policy.maturity"),
    ("Risk feed", "Risk grade field and values (L.INT.RISK.RT 1-10?), feed date, join key and Direct/Indirect classification -> calculation_policy.credit_quality"),
    ("Currency/FX", "Local-currency equivalent fields or FX rate source and rate date for QAR reporting -> calculation_policy.currency"),
    ("P&L adapter", "CONSOLIDATE.PRFT.LOSS fields, period/YTD conventions for Income/Expense rows -> amount basis PERIOD_MOVEMENT_YTD"),
    ("Section joins", "Owner choice of NBS block for Table 6 (B3 vs revised B34), ASSET - 100 (A1/A57), Tables 26, 28, 37, 42; decision on missing Table 38 / report 303"),
    ("Reconciliation", "Representative reconciled contracts (current, due, delinquent, grace, prepaid, nonaccrual, CLM) and approved legacy/control totals for the same population, date and valuation basis"),
]
