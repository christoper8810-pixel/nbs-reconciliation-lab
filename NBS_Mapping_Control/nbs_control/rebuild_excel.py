"""Excel export of a rebuild run in the BO table layout, plus a validator that re-reads the saved file.

Each table sheet uses the BO's actual validated headers. Generated money is shown in QAR thousands
(rounded to 0 dp like the BO; pre-round values remain in the run database). Unavailable cells are
the text 'n.a.' and never zero. The validator checks headers, values and error cells independently
of the writer's in-memory data.
"""
from __future__ import annotations
import json
from decimal import Decimal, ROUND_HALF_EVEN

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

from .maturity import TEMPLATE_T10, TEMPLATE_T10_HEADERS
from .rebuild_compare import display, template_columns

NA = 'n.a.'
STATUS_FILL = {'DRAFT_CANDIDATE_PREVIEW': 'FFF2CC', 'PARTIAL': 'FCE4D6', 'UNAVAILABLE': 'EDEDED', 'PROVISIONAL': 'DDEBF7',
               'CALCULATED_SUPPORTED': 'E2EFDA', 'UNRESOLVED_DUPLICATE_BASIS': 'F8CBAD', 'MANUAL_OVERRIDE': 'D9D2E9'}


def shown(value, kind):
    d = display(value, kind)
    if d is None:
        return NA
    if kind == 'count':
        return int(d)
    return float(d.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def write_workbook(path, manifest, results, catalogue, bo_rows, live_rows, controls, store, bo_ref):
    wb = Workbook()
    ws = wb.active
    ws.title = 'README'
    lines = [('NBS rebuild run', manifest['run_id']), ('Report date', manifest['period']['report_date']),
             ('Monetary unit', manifest['monetary_unit']), ('BO reference', bo_ref), ('Live reference', manifest['reference_versions']['live']),
             ('Mapping version', manifest['mapping_version']),
             ('Category basis', json.dumps(manifest.get('category_reporting_basis'), default=str)),
             ('Status meaning', 'DRAFT_CANDIDATE_PREVIEW = unreviewed candidate mapping, never certified; PARTIAL = available portion only; '
                                'UNAVAILABLE = no supported input (n.a., not zero); MANUAL_OVERRIDE = owner adjustment'),
             ('Completeness', 'NOT a complete or reconciled NBS. See Coverage, Compare_BO, Controls and Data_Requests.')]
    for r in lines:
        ws.append(r)
    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 120
    headers = {t: json.loads(h) for t, h in store.execute('SELECT table_code, headers FROM bo_headers WHERE ref_version=?', (bo_ref,))}
    by_table = {}
    for tid, r in results.items():
        by_table.setdefault(r['target']['table'], []).append(r)
    for table in sorted(catalogue['tables']):
        sh = wb.create_sheet('T' + table)
        hdr = headers.get(table, {})
        cols = sorted(hdr, key=lambda x: (len(x), x))
        names = [hdr[c] for c in cols]
        sh.append(names + ['Generation status'])
        for cell in sh[1]:
            cell.font = Font(bold=True)
        measures = catalogue['tables'][table].get('measures', {})
        order = {i: n for n, (i,) in enumerate(store.execute('SELECT item_code FROM bo_items WHERE ref_version=? AND table_code=? ORDER BY row_no', (bo_ref, table)))}
        for r in sorted(by_table.get(table, []), key=lambda x: order.get(x['target']['item_code'], 1e9)):
            t = r['target']
            row = []
            statuses = set()
            for name in names:
                if name == 'Table Code':
                    row.append(table)
                elif name == 'Qcb Item Code':
                    row.append(t['item_code'])
                elif name in ('Qcb Item Description', 'Qcb Item Desc'):
                    row.append(t['description'])
                elif name in ('Report Date', 'Rep Date'):
                    row.append(manifest['period']['report_date'])
                elif name in measures:
                    cell = r['cells'][name]
                    statuses.add(cell['status'])
                    row.append(shown(cell['value'], measures[name]['kind']))
                else:
                    row.append(NA)
            row.append(', '.join(sorted(statuses)))
            sh.append(row)
            fill = next((STATUS_FILL[s] for s in ('UNRESOLVED_DUPLICATE_BASIS', 'DRAFT_CANDIDATE_PREVIEW', 'PARTIAL', 'PROVISIONAL', 'MANUAL_OVERRIDE', 'CALCULATED_SUPPORTED') if s in statuses), None)
            if fill:
                sh.cell(sh.max_row, len(row)).fill = PatternFill('solid', fgColor=fill)
    # Corrected legacy Table 10 in the existing template's own header layout (row 769 meanings).
    sh = wb.create_sheet('Legacy_T10_layout')
    sh.append(['Description'] + [TEMPLATE_T10_HEADERS[c] for c in 'BCDEFGHIJKLM'] + ['Template row'])
    for tid, r in sorted(results.items()):
        if r['layout'] == 'maturity_loan':
            cols = template_columns('maturity_loan', r['semantic'])
            sh.append([r['target']['description']] + [float(cols[c].quantize(Decimal(1))) if c in cols else NA for c in 'BCDEFGHIJKLM'] + [r['target'].get('legacy_rule_id')])
    _table(wb, 'Compare_BO', bo_rows)
    _table(wb, 'Compare_Live', live_rows)
    _table(wb, 'Controls', [{'control': k, 'value': json.dumps(v, default=str)[:32000]} for k, v in controls.items()])
    from .rebuild_run import DATA_REQUESTS
    _table(wb, 'Data_Requests', [{'topic': a, 'request': b, 'current_treatment': x} for a, b, x in DATA_REQUESTS])
    wb.save(path)


def _table(wb, name, rows):
    sh = wb.create_sheet(name)
    rows = list(rows)
    if not rows:
        sh.append(['No rows'])
        return
    fields = list(rows[0])
    sh.append(fields)
    for r in rows:
        sh.append([(float(v) if isinstance(v, Decimal) else v) for v in (r.get(f) for f in fields)])


def verify_workbook(path, results, catalogue, store, bo_ref):
    wb = load_workbook(path, read_only=True, data_only=True)
    problems = []
    checked = 0
    headers = {t: json.loads(h) for t, h in store.execute('SELECT table_code, headers FROM bo_headers WHERE ref_version=?', (bo_ref,))}
    by_key = {(r['target']['table'], r['target']['item_code']): r for r in results.values()}
    for table, hdr in headers.items():
        sh = wb['T' + table]
        rows = list(sh.iter_rows(values_only=True))
        expected = [hdr[c] for c in sorted(hdr, key=lambda x: (len(x), x))]
        if list(rows[0][:len(expected)]) != expected:
            problems.append(f'T{table}: headers differ from BO')
            continue
        measures = catalogue['tables'][table].get('measures', {})
        for row in rows[1:]:
            rec = dict(zip(expected, row))
            r = by_key.get((table, rec.get('Qcb Item Code'))) if 'Qcb Item Code' in rec else None
            for v in row:
                if isinstance(v, str) and v.startswith('#'):
                    problems.append(f'T{table}: error cell {v}')
            if r is None:
                continue
            for name, m in measures.items():
                want = shown(r['cells'][name]['value'], m['kind'])
                if rec.get(name) != want:
                    problems.append(f'T{table} {rec.get("Qcb Item Code")} {name}: {rec.get(name)!r} != {want!r}')
                checked += 1
    t10 = list(wb['Legacy_T10_layout'].iter_rows(values_only=True))
    if t10 and list(t10[0][1:13]) != [TEMPLATE_T10_HEADERS[c] for c in 'BCDEFGHIJKLM']:
        problems.append('Legacy_T10_layout header mismatch')
    wb.close()
    return {'checked_cells': checked, 'problems': problems[:50], 'problem_count': len(problems), 'status': 'PASS' if not problems else 'FAIL'}
