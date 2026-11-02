"""Read-only import of the original workbooks into a cell-level evidence inventory.

Captures every populated row with cell addresses, formulas (as inert text),
comments/notes, merged ranges and direct-reference formula aliases. The source
file is hashed and never modified. Workbook content is evidence only: formulas
are not calculated and text is not interpreted as instructions.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.utils import get_column_letter, range_boundaries

SOURCE_SYSTEMS = ("T24", "ETHIX")
_SHEET = r"(?:'((?:[^']|'')+)'|([A-Za-z_][A-Za-z0-9_.]*))!"
_CELL = r"\$?([A-Z]{1,3})\$?([0-9]+)"
SINGLE_REF = re.compile(r"^=\s*\+?\s*(?:" + _SHEET + r")?" + _CELL + r"\s*$")
ANY_REF = re.compile(r"(?<![A-Za-z0-9_.'!])(?:" + _SHEET + r")?" + _CELL + r"(?![A-Za-z0-9_(])")
MAX_ALIAS_DEPTH = 8


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_id(source_system: str, file_hash: str, sheet: str, row: int) -> str:
    """Evidence identity for one row of one source version (reproduces the supplied inventory)."""
    token = hashlib.sha256(f"{file_hash}|{sheet}|{row}".encode("utf-8")).hexdigest()[:14]
    return f"{source_system}-{token}"


def _cell_value(value: Any) -> tuple[Any, str]:
    if isinstance(value, str):
        return value, "f" if value.startswith("=") else "s"
    if isinstance(value, bool):
        return value, "b"
    if isinstance(value, (int, float)):
        return value, "n"
    if isinstance(value, (datetime, date, time)):
        return value.isoformat(), "d"
    text = getattr(value, "text", None)  # ArrayFormula / DataTableFormula
    if isinstance(text, str):
        return text if text.startswith("=") else "=" + text, "f"
    return str(value), "s"


def _populated(value: Any) -> bool:
    return value is not None and not (isinstance(value, str) and value == "")


def formula_references(formula: str, own_sheet: str) -> list[str]:
    """Cell references named in a formula, as 'Sheet!A1'. Text only; nothing is evaluated."""
    refs = []
    for match in ANY_REF.finditer(formula):
        quoted, bare, column, row = match.groups()
        sheet = quoted.replace("''", "'") if quoted else bare or own_sheet
        refs.append(f"{sheet}!{column}{row}")
    return list(dict.fromkeys(refs))


def import_workbook(path: str | Path, source_system: str) -> dict[str, Any]:
    if source_system not in SOURCE_SYSTEMS:
        raise ValueError(f"Unknown source system {source_system}")
    path = Path(path)
    file_hash = file_sha256(path)
    workbook = openpyxl.load_workbook(path, data_only=False, read_only=False)
    sheets: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    cells_by_ref: dict[str, Any] = {}
    try:
        for worksheet in workbook.worksheets:
            merged = []
            merge_anchor: dict[str, str] = {}
            for merged_range in worksheet.merged_cells.ranges:
                text = str(merged_range)
                merged.append(text)
                min_col, min_row, _, _ = range_boundaries(text)
                merge_anchor[f"{get_column_letter(min_col)}{min_row}"] = text
            sheet_rows = 0
            for row_cells in worksheet.iter_rows():
                raw: dict[str, Any] = {}
                for cell in row_cells:
                    if not _populated(cell.value) and cell.comment is None:
                        continue
                    if not _populated(cell.value):
                        # A comment on an empty cell is still evidence; keep it, typed as note-only.
                        entry = {"v": None, "coord": cell.coordinate, "type": "note"}
                    else:
                        value, kind = _cell_value(cell.value)
                        entry = {"v": value, "coord": cell.coordinate, "type": kind}
                    if cell.comment is not None:
                        entry["note"] = cell.comment.text
                    if cell.coordinate in merge_anchor:
                        entry["merge"] = merge_anchor[cell.coordinate]
                    raw[cell.column_letter] = entry
                    cells_by_ref[f"{worksheet.title}!{cell.coordinate}"] = entry
                if not raw:
                    continue
                row_number = row_cells[0].row
                sheet_rows += 1
                rows.append({
                    "source_id": source_id(source_system, file_hash, worksheet.title, row_number),
                    "source_system": source_system,
                    "source_file": path.name,
                    "source_hash": file_hash,
                    "sheet": worksheet.title,
                    "source_row": row_number,
                    "raw_cells": raw,
                })
            sheets.append({"name": worksheet.title, "dimensions": worksheet.dimensions,
                           "merged_ranges": sorted(merged), "populated_rows": sheet_rows})
    finally:
        workbook.close()
    resolve_aliases(rows, cells_by_ref)
    return {"source_system": source_system, "file_name": path.name, "file_path": str(path),
            "sha256": file_hash, "sheet_count": len(sheets), "sheets": sheets, "rows": rows}


def resolve_aliases(rows: list[dict[str, Any]], cells_by_ref: dict[str, Any]) -> None:
    """Record dependencies for formulas and resolve pure single-cell references (aliases)."""
    for row in rows:
        for entry in row["raw_cells"].values():
            if entry.get("type") != "f" or not isinstance(entry.get("v"), str):
                continue
            formula = entry["v"]
            entry["refs"] = formula_references(formula, row["sheet"])
            chain = []
            current_sheet, current = row["sheet"], formula
            while len(chain) < MAX_ALIAS_DEPTH:
                match = SINGLE_REF.match(current)
                if not match:
                    break
                quoted, bare, column, number = match.groups()
                current_sheet = quoted.replace("''", "'") if quoted else bare or current_sheet
                target = f"{current_sheet}!{column}{number}"
                if target in chain:
                    chain.append(target)
                    entry["alias"] = {"chain": chain, "status": "CIRCULAR"}
                    break
                chain.append(target)
                target_entry = cells_by_ref.get(target)
                if target_entry is None:
                    entry["alias"] = {"chain": chain, "status": "TARGET_EMPTY"}
                    break
                if target_entry.get("type") != "f":
                    entry["alias"] = {"chain": chain, "status": "RESOLVED", "value": target_entry.get("v")}
                    break
                current = target_entry["v"]
            else:
                entry["alias"] = {"chain": chain, "status": "TOO_DEEP"}


def import_sources(paths: dict[str, str | Path]) -> dict[str, Any]:
    """Import both originals. Missing files are an error; nothing is guessed."""
    results = {}
    for system, path in paths.items():
        if not Path(path).is_file():
            raise FileNotFoundError(f"{system} source not found: {path}")
        results[system] = import_workbook(path, system)
    return results


def load_supplied_inventory(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def inventory_from_supplied(path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    """Build an import from the read-only supplied inventory when originals are unavailable."""
    supplied = load_supplied_inventory(path)
    manifest = {item["source_system"]: item for item in json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))}
    by_system: dict[str, dict[str, Any]] = {}
    for record in supplied:
        system = record["source_system"]
        bundle = by_system.setdefault(system, {
            "source_system": system, "file_name": record["source_file"], "file_path": None,
            "sha256": record["source_hash"], "sheet_count": manifest.get(system, {}).get("sheet_count"),
            "sheets": [], "rows": [], "imported_from": "supplied source_inventory.json (read-only)",
        })
        bundle["rows"].append({key: record[key] for key in (
            "source_id", "source_system", "source_file", "source_hash", "sheet", "source_row", "raw_cells")})
    for bundle in by_system.values():
        cells = {f"{r['sheet']}!{c['coord']}": c for r in bundle["rows"] for c in r["raw_cells"].values()}
        for row in bundle["rows"]:
            for entry in row["raw_cells"].values():
                entry.pop("alias", None)
        resolve_aliases(bundle["rows"], cells)
    return by_system


def _comparable(value: Any) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return "" if value is None else str(value)


def compare_with_supplied(imported: dict[str, Any], supplied: list[dict[str, Any]]) -> dict[str, Any]:
    """Coverage parity between a fresh import and the supplied inventory (same file hash)."""
    fresh = {r["source_id"]: r for bundle in imported.values() for r in bundle["rows"]}
    given = {r["source_id"]: r for r in supplied}
    hashes = {bundle["source_system"]: bundle["sha256"] for bundle in imported.values()}
    supplied_hashes = {r["source_system"]: r["source_hash"] for r in supplied}
    value_differences = []
    note_count_fresh = note_count_given = 0
    for sid in sorted(set(fresh) & set(given)):
        a, b = fresh[sid]["raw_cells"], given[sid]["raw_cells"]
        note_count_fresh += sum("note" in c for c in a.values())
        note_count_given += sum("note" in c for c in b.values())
        for column in sorted(set(a) | set(b)):
            left, right = a.get(column, {}), b.get(column, {})
            if _comparable(left.get("v")) != _comparable(right.get("v")):
                value_differences.append({"source_id": sid, "column": column,
                                          "fresh": left.get("v"), "supplied": right.get("v")})
    return {
        "hash_match": {system: hashes.get(system) == supplied_hashes.get(system) for system in supplied_hashes},
        "fresh_rows": len(fresh),
        "supplied_rows": len(given),
        "only_in_fresh": sorted(set(fresh) - set(given)),
        "only_in_supplied": sorted(set(given) - set(fresh)),
        "value_differences": value_differences,
        "notes_fresh": note_count_fresh,
        "notes_supplied": note_count_given,
    }
