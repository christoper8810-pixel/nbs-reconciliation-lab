"""Build the review catalog from imported evidence.

Produces, for every populated source row, a mapping item with:
- a stable business mapping ID (independent of row number and file version),
- an evidence fingerprint (changes when the row's cells, notes or headers change),
- source evidence (cells, formulas, aliases, comments, column headers),
- a proposal for owner review (never effective on its own).

Also builds the cell-level findings queue and the section-alignment items.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from typing import Any

from .selectors import draft_category_selector

TITLE = re.compile(r"^\s*(table\s*\(\s*\d+\s*\)|(assets|liabilities|contra items|income|expenses?)\s+as\s+at\b)", re.I)
TABLE_ID = re.compile(r"table\s*\(\s*(\d+)\s*\)\s*-\s*\(\s*([^)]*?)\s*\)", re.I)
BASE_TITLE = re.compile(r"^\s*(assets|liabilities|contra items|income|expenses?)\s+as\s+at\b", re.I)
BALANCE_TOKEN = re.compile(r"(?<![A-Z0-9_.])([A-Z]{3,}(?:ACCOUNT|PFT)(?:SP)?)(?![A-Z0-9_.])")
SOURCE_TABLE = re.compile(r"(?<![A-Z0-9_])((?:[A-Z]{2,}\.)+[A-Z]{2,}|ECB)(?![A-Z0-9_])")
LEGACY_METRIC = {
    "OUTSTANDING": re.compile(r"outstanding_qar", re.I),
    "AMORTIZED_EARNED": re.compile(r"amortized_earned_qar", re.I),
    "LOAN_FEES": re.compile(r"loan_fees_qar", re.I),
}
PL_BASE = {"INCOME", "EXPENSE", "EXPENSES"}
CONTEXT_RANGE = re.compile(r"^[A-Z]{1,3}\d+:[A-Z]{1,3}\d+$")
SINGLE_CELL = re.compile(r"^([A-Z]{1,3})(\d+)$")


def _hash(value: Any, length: int = 64) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value).replace("\xa0", " ")).strip()


def path_key(text: str) -> str:
    return clean_text(text).lstrip(".").strip().casefold()


def level_of(text: str) -> int:
    stripped = str(text).replace("\xa0", " ").strip()
    return len(stripped) - len(stripped.lstrip("."))


def parse_title(title: str) -> dict[str, Any]:
    match = TABLE_ID.search(clean_text(title))
    if match:
        code = re.sub(r"\s+", "", match.group(2).replace("\xa0", "")) or None
        return {"table_number": int(match.group(1)), "report_code": code, "base_report": None}
    base = BASE_TITLE.match(clean_text(title))
    if base:
        name = base.group(1).title()
        return {"table_number": None, "report_code": None, "base_report": "Expenses" if name == "Expense" else name}
    return {"table_number": None, "report_code": None, "base_report": None}


def description_cell(raw: dict[str, Any], columns: tuple[str, ...] = ("A", "B")) -> tuple[str | None, str | None]:
    for column in columns:
        entry = raw.get(column)
        if entry and entry.get("type") == "s" and clean_text(entry.get("v", "")):
            return column, entry["v"]
    return None, None


def detect_tokens(text: str) -> list[str]:
    return list(dict.fromkeys(BALANCE_TOKEN.findall(str(text).upper())))


def _merge_spans(merged_ranges: list[str]) -> dict[tuple[int, str], list[str]]:
    """Map (row, anchor column) to the columns a horizontal merge covers."""
    from openpyxl.utils import get_column_letter, range_boundaries

    spans = {}
    for text in merged_ranges:
        min_col, min_row, max_col, _ = range_boundaries(text)
        spans[(min_row, get_column_letter(min_col))] = [get_column_letter(c) for c in range(min_col, max_col + 1)]
    return spans


def _column_index(column: str) -> int:
    from openpyxl.utils import column_index_from_string
    return column_index_from_string(column)


def build_structure(bundle: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Assign blocks, hierarchy, headers and business keys to one source's rows."""
    system = bundle["source_system"]
    merges = {sheet["name"]: sheet.get("merged_ranges", []) for sheet in bundle.get("sheets", [])}
    by_sheet: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in bundle["rows"]:
        by_sheet[row["sheet"]].append(row)
    items: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    for sheet, rows in by_sheet.items():
        rows.sort(key=lambda r: r["source_row"])
        spans = _merge_spans(merges.get(sheet, []))
        block: dict[str, Any] = {"ordinal": 0, "title": None, "title_coord": None, "key": None}
        stack: list[tuple[int, str, str]] = []
        headers: dict[str, list[str]] = {}
        header_rows_left = 0
        occurrences: dict[str, int] = defaultdict(int)
        ordinal = 0

        def open_block(title: str | None, coord: str | None) -> dict[str, Any]:
            nonlocal ordinal
            parsed = parse_title(title) if title else {"table_number": None, "report_code": None, "base_report": None}
            if title is None:
                key = f"{system}|{clean_text(sheet).upper()}|PRE-TITLE"
            elif system == "ETHIX" and parsed["table_number"] is not None:
                key = f"ETHIX|T{parsed['table_number']}|R{parsed['report_code'] or '-'}"
            elif system == "ETHIX" and parsed["base_report"]:
                key = f"ETHIX|BASE|{parsed['base_report'].upper()}"
            else:
                key = f"{system}|{clean_text(sheet).upper()}|B{ordinal}"
            info = {"source_system": system, "sheet": sheet, "ordinal": ordinal, "title": title,
                    "title_coord": coord, "key": key, **parsed, "rows": []}
            blocks.append(info)
            return info

        block = open_block(None, None)
        for row in rows:
            raw = row["raw_cells"]
            desc_col, desc = description_cell(raw)
            if desc is not None and TITLE.match(clean_text(desc)) and not clean_text(desc).lower().startswith("dukhan"):
                ordinal += 1
                block = open_block(clean_text(desc), raw[desc_col]["coord"])
                block["description_column"] = desc_col
                stack, headers, header_rows_left = [], {}, 0
                kind = "TITLE"
            else:
                if block["title"] is not None:
                    # Inside a titled block the description lives only in the title's column.
                    desc_col, desc = description_cell(raw, (block["description_column"],))
                kind = None
            if kind == "TITLE":
                pass
            elif desc is not None and clean_text(desc).lower() == "description":
                kind = "HEADER"
                header_rows_left = 1
                headers = {}
                _add_header_row(headers, raw, desc_col, row["source_row"], spans, forward_fill=True)
            elif header_rows_left and desc is None and raw and all(
                    e.get("type") == "s" and len(clean_text(e.get("v", ""))) <= 25 for e in raw.values()):
                kind = "HEADER"
                header_rows_left = 0
                _add_header_row(headers, raw, None, row["source_row"], spans, forward_fill=False)
            else:
                header_rows_left = 0
                rule_columns = [c for c in raw if c != desc_col]
                kind = "RULE" if rule_columns else "LABEL"
                if block["title"] is None:
                    kind = "NOTE"
            if kind in ("RULE", "LABEL", "NOTE") and desc is not None:
                level = level_of(desc)
                while stack and stack[-1][0] >= level:
                    stack.pop()
                stack.append((level, path_key(desc), clean_text(desc)))
                own_path = [entry[1] for entry in stack]
                display_path = " > ".join(entry[2] for entry in stack)
            else:
                own_path = [entry[1] for entry in stack] + [f"#{kind.lower()}"]
                display_path = " > ".join(entry[2] for entry in stack)
            base_key = f"{block['key']}|{' > '.join(own_path)}|{kind}"
            occurrences[base_key] += 1
            business_key = f"{base_key}|{occurrences[base_key]}"
            cells = []
            for column in sorted(raw, key=_column_index):
                entry = raw[column]
                cell = {"column": column, "coord": entry["coord"], "value": entry.get("v"), "type": entry.get("type"),
                        "header": " / ".join(headers.get(column, [])) or None}
                for optional in ("note", "merge", "alias", "refs"):
                    if optional in entry:
                        cell[optional] = entry[optional]
                cells.append(cell)
            fingerprint_basis = {
                "kind": kind, "description": clean_text(desc) if desc else None,
                "cells": [{k: c.get(k) for k in ("column", "value", "type", "header", "note")} |
                          {"alias": (c.get("alias") or {}).get("value")} for c in cells],
            }
            item = {
                "business_id": "BM-" + _hash(business_key, 12),
                "business_key": business_key,
                "source_system": system,
                "source_id": row["source_id"],
                "source_file": row["source_file"],
                "source_hash": row["source_hash"],
                "sheet": sheet,
                "source_row": row["source_row"],
                "block_key": block["key"],
                "block_ordinal": block["ordinal"],
                "block_title": block["title"],
                "block_title_coord": block["title_coord"],
                "table_number": block["table_number"],
                "report_code": block["report_code"],
                "base_report": block["base_report"],
                "kind": kind,
                "description": clean_text(desc) if desc else None,
                "description_column": desc_col,
                "hierarchy_path": display_path,
                "path_key": " > ".join(own_path),
                "cells": cells,
                "fingerprint": _hash(fingerprint_basis),
            }
            block["rows"].append(row["source_row"])
            items.append(item)
    ids = defaultdict(list)
    for item in items:
        ids[item["business_id"]].append(item)
    for duplicates in ids.values():
        if len(duplicates) > 1:  # hash collision guard; keys themselves are unique
            raise RuntimeError("Business ID collision: " + duplicates[0]["business_key"])
    for info in blocks:
        info["first_row"] = info["rows"][0] if info["rows"] else None
        info["last_row"] = info["rows"][-1] if info["rows"] else None
        info["row_count"] = len(info.pop("rows"))
    return items, blocks


def _add_header_row(headers: dict[str, list[str]], raw: dict[str, Any], skip: str | None, row_number: int,
                    spans: dict[tuple[int, str], list[str]], forward_fill: bool) -> None:
    populated = sorted((c for c in raw if c != skip and raw[c].get("type") == "s"), key=_column_index)
    for column in populated:
        text = clean_text(raw[column]["v"])
        covered = spans.get((row_number, column), [column])
        for target in covered:
            headers.setdefault(target, []).append(text)
    if forward_fill and not spans:
        # Fallback without merge metadata: a group heading covers the empty columns to its right.
        indices = [_column_index(c) for c in populated]
        for index, column in enumerate(populated):
            stop = indices[index + 1] if index + 1 < len(indices) else indices[index] + 3
            from openpyxl.utils import get_column_letter
            for position in range(indices[index] + 1, stop):
                headers.setdefault(get_column_letter(position), []).append(clean_text(raw[column]["v"]))


def propose(item: dict[str, Any], rules: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Draft a proposal for owner review. Proposals are never effective by themselves."""
    membership = rules["membership"]
    extras = rules["extra_membership"]
    groups = rules["groups"]
    rule_cells = [c for c in item["cells"] if c["column"] != item["description_column"]]
    texts = [str(c["value"]) for c in rule_cells if c["value"] is not None]
    for cell in rule_cells:
        alias = cell.get("alias") or {}
        if alias.get("status") == "RESOLVED" and alias.get("value") is not None:
            texts.append(str(alias["value"]))
    joined = "\n".join(texts)
    tokens = detect_tokens(joined)
    proposal: dict[str, Any] = {
        "status": "NO_PROPOSAL",
        "basis": None,
        "metric_expression": None,
        "selectors": None,
        "selector_status": "NOT_APPLICABLE",
        "amount_basis": None,
        "source_tables": list(dict.fromkeys(SOURCE_TABLE.findall(joined.upper()))),
        "dependencies": [],
        "token_diff": None,
        "cell_token_diffs": [],
        "formula_corrections": [],
        "notes": [],
        "exclusive_group": None,
    }
    if item["kind"] not in ("RULE",):
        proposal["basis"] = "Heading/label/context row: no mapping proposed"
        return proposal
    base = (item.get("base_report") or "").upper()
    if clean_text(item["sheet"]).upper() in PL_BASE or base in PL_BASE:
        proposal.update(status="PROPOSED", amount_basis="PERIOD_MOVEMENT_YTD", metric_expression="PL_PERIOD_MOVEMENT",
                        basis="Income/expense row: period/YTD movement logic, separate from loan closing stock")
        proposal["dependencies"].append("PL_PERIOD_MOVEMENT definition and PERIOD_MOVEMENT_YTD adapter")
        proposal["selector_status"] = "REQUIRES_OWNER_STRUCTURED_SELECTOR"
        return proposal

    legacy = [name for name, pattern in LEGACY_METRIC.items() if pattern.search(joined)]
    if item["source_system"] == "ETHIX":
        proposal["selector_status"] = "REQUIRES_APPROVED_ETHIX_TO_T24_CROSSWALK"
        if set(legacy) == {"OUTSTANDING", "AMORTIZED_EARNED", "LOAN_FEES"}:
            proposal.update(status="PROPOSED", metric_expression="ETHIX_LOAN_CARRYING_AMOUNT", amount_basis="CLOSING_STOCK",
                            basis="Ethix cell states Outstanding_QAR + Amortized_Earned_QAR + Loan_Fees_QAR; components kept separate")
            proposal["dependencies"].append("LOAN_FEES definition (T24 source, identifiers, sign, overlap)")
        elif legacy:
            proposal["notes"].append(f"Partial legacy metric names {legacy}; owner must define the row metric")
        else:
            proposal["basis"] = "Legacy Ethix selector: requires owner-approved field/product crosswalk"
        cells_without_metric = [c["coord"] for c in rule_cells if legacy and isinstance(c["value"], str)
                                and not any(p.search(c["value"]) for p in LEGACY_METRIC.values())]
        if cells_without_metric:
            proposal["notes"].append(f"Cells without the metric expression: {', '.join(cells_without_metric)}")
        return proposal

    # T24 rows
    drafts = []
    for cell in rule_cells:
        if isinstance(cell["value"], str):
            draft = draft_category_selector(cell["value"])
            if draft is not None and draft not in drafts:
                drafts.append(draft)
    if len(drafts) == 1:
        proposal["selectors"] = drafts[0]
        proposal["selector_status"] = "DRAFT_FROM_LEGACY_TEXT"
        if _selector_may_include(drafts[0], rules["candidate_category"]):
            proposal["notes"].append(
                f"Category {rules['candidate_category']} satisfies this legacy selector; Murabaha/CLM routing is an owner decision (NBS-02)")
            proposal["dependencies"].append("CLM: CREDIT group approval, CLM indicator and verified CLS links")
    elif len(drafts) > 1:
        proposal["selector_status"] = "CONFLICTING_LEGACY_SELECTORS_IN_ROW"
    else:
        proposal["selector_status"] = "REQUIRES_OWNER_STRUCTURED_SELECTOR"

    for cell in rule_cells:
        cell_tokens = detect_tokens(cell["value"]) if isinstance(cell["value"], str) else []
        if cell_tokens:
            proposal["cell_token_diffs"].append({"coord": cell["coord"], "header": cell.get("header"),
                                                 **_token_diff(cell_tokens, membership, extras, groups)})
    _formula_corrections(item, proposal, policy)
    if not tokens:
        if proposal["formula_corrections"]:
            proposal.update(status="PROPOSED", basis="Structural formula correction only")
        else:
            proposal["basis"] = "No exact balance identifiers in the row; report-specific rule required"
        return proposal
    diff = _token_diff(tokens, membership, extras, groups)
    proposal["token_diff"] = diff
    proposal["amount_basis"] = "CLOSING_STOCK"
    description = (item.get("description") or "").lower()
    if tokens and all(t.endswith("SP") for t in tokens):
        proposal.update(status="PROPOSED", metric_expression="SUSPENSE_SP",
                        basis="All identifiers are SP-suffixed: separate suspense metric; SP is never stripped to a base code")
        proposal["dependencies"].append("SUSPENSE_SP local definition")
        return proposal
    if re.search(r"deferred\s+(interest|income)", description):
        proposal.update(status="PROPOSED", metric_expression="UNEARNED_PROFIT",
                        basis="Deferred interest/income row: owner option UNEARNED_PROFIT (DEFERREDPFT + ACCDEFERREDPFT); legacy list mixes groups (NBS-03)")
        proposal["notes"].append("Owner must choose the intended metric for this row; legacy list is not the owner dictionary")
        return proposal
    best = diff["best_group"]
    if best:
        proposal.update(status="PROPOSED", metric_expression=best,
                        basis=f"Legacy identifiers overlap most with owner group {best}; owner must confirm the row metric")
    else:
        proposal["basis"] = "Legacy identifiers do not identify a single owner group"
    if diff["unknown"]:
        proposal["dependencies"].append("Local definitions for: " + ", ".join(diff["unknown"]))
    if "credit classification" in (item.get("block_title") or "").lower():
        proposal["dependencies"].append("credit_quality policy: risk grade field, grades and one metric for all columns (NBS-08)")
    return proposal


def _token_diff(tokens: list[str], membership: dict[str, str], extras: dict[str, str],
                groups: dict[str, list[str]]) -> dict[str, Any]:
    by_group = defaultdict(list)
    unknown = []
    for token in tokens:
        if token in membership:
            by_group[membership[token]].append(token)
        elif token in extras:
            by_group["CLM_LINKED_" + extras[token]].append(token)
        else:
            unknown.append(token)
    counts = {group: len(codes) for group, codes in by_group.items() if group in groups}
    best = None
    if counts:
        top = max(counts.values())
        winners = [g for g, n in counts.items() if n == top]
        best = winners[0] if len(winners) == 1 else None
    owner_codes = groups.get(best, []) if best else []
    return {
        "legacy_tokens": tokens,
        "by_group": dict(by_group),
        "unknown": unknown,
        "best_group": best,
        "missing_from_legacy": [c for c in owner_codes if c not in tokens],
        "legacy_outside_best_group": [t for t in tokens if t not in owner_codes],
    }


def _selector_may_include(selector: dict[str, Any], category: str) -> bool:
    if "all" in selector:
        return all(_selector_may_include(child, category) for child in selector["all"])
    if selector.get("field") != "T24.CATEGORY":
        return True
    if selector["op"] == "range":
        return category.isdigit() and selector["min"] <= int(category) <= selector["max"]
    if selector["op"] == "in":
        return category in selector["values"]
    if selector["op"] == "not_in":
        return category not in selector["values"]
    return True


def _formula_corrections(item: dict[str, Any], proposal: dict[str, Any], policy: dict[str, Any]) -> None:
    sheet = clean_text(item["sheet"]).upper()
    row = item["source_row"]
    if sheet == "TABLE 11":
        totals = policy.get("credit_quality", {}).get("totals", {})
        for cell in item["cells"]:
            if cell["type"] == "f" and cell["column"] in totals:
                proposed = "=" + "+".join(f"{c}{row}" for c in totals[cell["column"]])
                legacy_refs = sorted(r.split("!")[1] for r in cell.get("refs", []))
                proposed_refs = sorted(f"{c}{row}" for c in totals[cell["column"]])
                if legacy_refs != proposed_refs:
                    proposal["formula_corrections"].append({
                        "coord": cell["coord"], "legacy": cell["value"], "proposed": proposed,
                        "finding_refs": ["NBS-06", "NBS-07"], "kind": "PROVEN_FORMULA_DEFECT",
                        "note": "Rebuilt from same-row detail columns once; risk-grade selection kept separate from component selection"})
    if sheet == "TABLE 10":
        buckets = {b["column"]: b for b in policy.get("maturity", {}).get("buckets", [])}
        for cell in item["cells"]:
            if isinstance(cell["value"], str) and "MATURITY.DATE" in cell["value"].upper():
                bucket = buckets.get(cell["column"])
                if bucket:
                    upper = "no upper bound" if bucket["max_days"] is None else f"<= {bucket['max_days']}"
                    text = f"(maturity_date - reporting_date) in days >= {bucket['min_days']} and {upper}"
                else:
                    text = "Owner disposition required: column is not a remaining-maturity interval in the proposed policy"
                proposal["formula_corrections"].append({
                    "coord": cell["coord"], "legacy": cell["value"], "proposed": text,
                    "finding_refs": ["NBS-04", "NBS-05"], "kind": "PROVEN_LOGIC_DEFECT",
                    "note": "Reporting-date basis; mutually exclusive complete intervals; missing maturity and matured/overdue are separate states"})


def build_findings_queue(findings: list[dict[str, Any]], classification: dict[str, Any],
                         items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_cell: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in items:
        for cell in item["cells"]:
            by_cell[(item["source_system"], clean_text(item["sheet"]).upper(), cell["coord"])] = {"item": item, "cell": cell}
    queue = []
    kinds = classification.get("findings", {})
    for finding in findings:
        targets = [(finding["source_system"], finding["source_sheet"], ref) for ref in finding.get("source_cells", [])]
        extra = finding.get("nbs_evidence")
        if extra:
            targets += [("T24", extra["sheet"], ref) for ref in extra.get("cells", [])]
        for system, sheet, ref in targets:
            context = bool(CONTEXT_RANGE.match(ref))
            hit = None if context else by_cell.get((system, clean_text(sheet).upper(), ref))
            current_value = hit["cell"]["value"] if hit else None
            queue.append({
                "item_id": f"FQ-{finding['id']}-{system}-{clean_text(sheet)}!{ref}",
                "finding_id": finding["id"],
                "finding_title": finding["title"],
                "kind": kinds.get(finding["id"], "UNCLASSIFIED"),
                "source_system": system,
                "sheet": sheet,
                "cell": ref,
                "scope": "CONTEXT_RANGE" if context else "CELL",
                "blocking": not context,
                "business_id": hit["item"]["business_id"] if hit else None,
                "current_value": current_value,
                "cell_found": bool(hit) or context,
                "implication": finding.get("implication"),
                "required_owner_decision": finding.get("required_owner_decision"),
                "owner_update": finding.get("owner_update"),
                "fingerprint": _hash({"finding": finding.get("evidence"), "value": current_value}),
            })
    return queue


def build_section_items(sections: list[dict[str, Any]], blocks: list[dict[str, Any]],
                        items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nbs_blocks = {(clean_text(b["sheet"]).upper(), b["title_coord"]): b for b in blocks if b["source_system"] == "T24"}
    ethix_blocks = {b["first_row"]: b for b in blocks if b["source_system"] == "ETHIX" and b["title"]}
    result = []
    for section in sections:
        candidates = []
        for candidate in section.get("nbs_section_candidates", []):
            block = nbs_blocks.get((clean_text(candidate["nbs_sheet"]).upper(), candidate["nbs_title_cell"]))
            candidates.append({**candidate, "block_key": block["key"] if block else None,
                               "block_found": block is not None,
                               "block_rows": f"{block['first_row']}-{block['last_row']}" if block else None})
        ethix_block = ethix_blocks.get(section["start_row"])
        identity = (f"T{section['table_number']}|R{section['report_id'] or '-'}" if section["table_number"] is not None
                    else f"BASE|{section['base_report']}")
        problems = []
        if not candidates:
            problems.append("MISSING_NBS_MAPPING")
        if len(candidates) > 1:
            problems.append("BLOCK_IDENTITY_REQUIRED")
        if any(not c["block_found"] for c in candidates):
            problems.append("CANDIDATE_BLOCK_NOT_FOUND_IN_CURRENT_IMPORT")
        if ethix_block is None:
            problems.append("ETHIX_SECTION_NOT_FOUND_IN_CURRENT_IMPORT")
        result.append({
            "section_id": "SEC-" + _hash(identity + "|" + clean_text(section["title"]).casefold(), 12),
            "identity": identity,
            "title": clean_text(section["title"]),
            "table_number": section["table_number"],
            "report_code": section["report_id"],
            "ethix_range": section["range"],
            "ethix_block_key": ethix_block["key"] if ethix_block else None,
            "candidates": candidates,
            "problems": problems,
            "fingerprint": _hash({"title": clean_text(section["title"]),
                                  "candidates": [(c["nbs_sheet"], c["nbs_title_cell"], c["nbs_title"]) for c in candidates]}),
        })
    return result


def row_join_candidates(items: list[dict[str, Any]], section_items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Ethix row -> NBS rows with the same full normalized hierarchy path in a candidate block.

    Leaf descriptions alone never create a candidate. Results await owner approval.
    """
    nbs_by_block_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        if item["source_system"] == "T24" and item["kind"] in ("RULE", "LABEL"):
            nbs_by_block_path[(item["block_key"], item["path_key"])].append(item)
    blocks_for_section = {s["ethix_block_key"]: [c["block_key"] for c in s["candidates"] if c["block_key"]]
                          for s in section_items if s["ethix_block_key"]}
    result: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if item["source_system"] != "ETHIX" or item["kind"] not in ("RULE", "LABEL"):
            continue
        matches = []
        for block_key in blocks_for_section.get(item["block_key"], []):
            for target in nbs_by_block_path.get((block_key, item["path_key"]), []):
                matches.append({"business_id": target["business_id"], "block_key": block_key,
                                "sheet": target["sheet"], "row": target["source_row"], "match": "FULL_PATH"})
        result[item["business_id"]] = matches
    return result


def build_catalog(imports: dict[str, Any], findings: list[dict[str, Any]], sections: list[dict[str, Any]],
                  rules: dict[str, Any], policy: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    for system in ("T24", "ETHIX"):
        if system in imports:
            system_items, system_blocks = build_structure(imports[system])
            items += system_items
            blocks += system_blocks
    for item in items:
        item["proposal"] = propose(item, rules, policy)
    queue = build_findings_queue(findings, classification, items)
    by_id = {item["business_id"]: item for item in items}
    for item in items:
        item["finding_refs"] = []
    for entry in queue:
        item = by_id.get(entry["business_id"])
        if item is not None and entry["finding_id"] not in item["finding_refs"]:
            item["finding_refs"].append(entry["finding_id"])
    section_items = build_section_items(sections, blocks, items)
    joins = row_join_candidates(items, section_items)
    for item in items:
        if item["business_id"] in joins:
            item["nbs_row_candidates"] = joins[item["business_id"]]
    sources = {system: {"file_name": bundle["file_name"], "sha256": bundle["sha256"],
                        "file_path": bundle.get("file_path"), "rows": len(bundle["rows"]),
                        "sheet_count": bundle.get("sheet_count"),
                        "imported_from": bundle.get("imported_from", "original workbook")}
               for system, bundle in imports.items()}
    return {"sources": sources, "mappings": items, "blocks": blocks, "findings_queue": queue,
            "sections": section_items}
