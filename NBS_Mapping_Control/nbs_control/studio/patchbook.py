"""Corrected copy of the mapping workbook: approved cell edits only, original file never touched.

Every edited cell must still hold the value the proposal was based on (otherwise the edit is refused as a
conflict). After saving, every other cell's value / formula, number format and comment is compared with the
original to prove nothing else changed. Package parts that openpyxl cannot carry over (charts, images,
pivot caches, external links, VBA without keep_vba) are detected and reported.
"""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from openpyxl import load_workbook

from .workbook import text

LOSSY_PARTS = ('xl/charts/', 'xl/drawings/', 'xl/media/', 'xl/pivotCache', 'xl/pivotTables/', 'xl/externalLinks/', 'xl/slicers/')


def _coerce(new, old):
    if isinstance(old, (int, float)) and str(new).strip().lstrip('-').isdigit():
        return int(new)
    return new


def write_corrected(original, edits, out_path):
    original, out_path = Path(original), Path(out_path)
    keep_vba = original.suffix.lower() == '.xlsm'
    with zipfile.ZipFile(original) as z:
        lossy = sorted({p for n in z.namelist() for p in LOSSY_PARTS if n.startswith(p) and not n.lower().endswith('.vml')})
    wb = load_workbook(original, keep_vba=keep_vba)
    applied, conflicts = [], []
    for e in edits:
        ws = wb[e['sheet']]
        cell = ws.cell(row=e['row'], column=e['col'])
        cur = text(cell.value)
        if cur != text(e['existing']):
            conflicts.append({**e, 'found': cur, 'reason': 'cell no longer holds the value the proposal was based on'})
            continue
        cell.value = _coerce(e['proposed'], cell.value) if e['proposed'] != '' else None
        applied.append(e)
    tmp = out_path.with_suffix(out_path.suffix + '.tmp')
    wb.save(tmp)
    wb.close() if hasattr(wb, 'close') else None
    shutil.move(str(tmp), str(out_path))
    check = verify(original, out_path, applied)
    return {'applied': applied, 'conflicts': conflicts, 'lossy_parts': lossy, 'verification': check, 'path': str(out_path)}


def verify(original, corrected, applied):
    changed = {(e['sheet'], e['row'], e['col']) for e in applied}
    a = load_workbook(original)
    b = load_workbook(corrected)
    diffs, cells = [], 0
    try:
        if a.sheetnames != b.sheetnames:
            diffs.append({'issue': 'sheet list differs', 'original': a.sheetnames, 'corrected': b.sheetnames})
        for name in a.sheetnames:
            wa, wbk = a[name], b[name]
            for row in wa.iter_rows():
                for ca in row:
                    if ca.value is None and ca.comment is None:
                        continue
                    cells += 1
                    cb = wbk.cell(row=ca.row, column=ca.column)
                    key = (name, ca.row, ca.column)
                    if key in changed:
                        continue
                    if ca.value != cb.value:
                        diffs.append({'cell': f"'{name}'!{ca.coordinate}", 'issue': 'value/formula changed', 'original': ca.value, 'corrected': cb.value})
                    if ca.number_format != cb.number_format:
                        diffs.append({'cell': f"'{name}'!{ca.coordinate}", 'issue': 'number format changed'})
                    if (ca.comment.text if ca.comment else None) != (cb.comment.text if cb.comment else None):
                        diffs.append({'cell': f"'{name}'!{ca.coordinate}", 'issue': 'comment changed'})
            if set(map(str, wa.merged_cells.ranges)) != set(map(str, wbk.merged_cells.ranges)):
                diffs.append({'cell': name, 'issue': 'merged cells changed'})
        names_a = sorted(str(n) for n in a.defined_names)
        names_b = sorted(str(n) for n in b.defined_names)
        if names_a != names_b:
            diffs.append({'issue': 'defined names changed'})
    finally:
        a.close()
        b.close()
    return {'cells_compared': cells, 'unexpected_differences': diffs[:200], 'preserved': not diffs, 'edited_cells': len(changed)}
