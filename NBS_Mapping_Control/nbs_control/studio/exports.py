"""Mapping Studio reports A-G, generated from the stored analysis only.

A BO_RECONCILIATION.xlsx         B PROPOSED_MAPPING_PATCH.xlsx     C CORRECTED_MAPPING_PREVIEW.xlsx
D FINANCE_DECISION_WORKLIST.xlsx E MAPPING_VALIDATION_REPORT.xlsx  F PATCH_AUDIT_LOG.xlsx
G EXECUTIVE_SUMMARY.html
"""
from __future__ import annotations

import html
import json
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from . import patchbook

FILES = ('BO_RECONCILIATION.xlsx', 'PROPOSED_MAPPING_PATCH.xlsx', 'CORRECTED_MAPPING_PREVIEW.xlsx', 'FINANCE_DECISION_WORKLIST.xlsx',
         'MAPPING_VALIDATION_REPORT.xlsx', 'PATCH_AUDIT_LOG.xlsx', 'EXECUTIVE_SUMMARY.html')
BOLD, FILL = Font(bold=True), PatternFill('solid', fgColor='DDE6F0')


def num(v):
    if v is None or v == '':
        return None
    try:
        return float(Decimal(str(v)))
    except Exception:  # noqa: BLE001
        return v


def cell(v):
    if isinstance(v, (list, tuple, dict)):
        return json.dumps(v, default=str)[:32000]
    if isinstance(v, Decimal):
        return float(v)
    return v


def sheet(wb, title, cols, rows, money=()):
    ws = wb.create_sheet(title[:31])
    ws.append(cols)
    for c in ws[1]:
        c.font, c.fill = BOLD, FILL
    for i, r in enumerate(rows):
        if i >= 1_048_000:
            ws.append(['... truncated; see result.json'])
            break
        ws.append([num(r.get(c)) if c in money else cell(r.get(c)) for c in cols])
    for i, c in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = min(60, max(10, len(c) + 2))
        if c in money:
            for row in ws.iter_rows(min_row=2, min_col=i, max_col=i):
                row[0].number_format = '#,##0.00;[Red]-#,##0.00'
    ws.freeze_panes = 'A2'
    if rows:
        ws.auto_filter.ref = ws.dimensions
    return ws


def _wb():
    wb = Workbook()
    wb.remove(wb.active)
    return wb


def _keystr(k):
    return ' / '.join(str(x) for x in k if x not in ('', None))


def write_analysis(store, rid, folder, res):
    folder = Path(folder)
    props = store.proposals(rid)
    bo_reconciliation(res, props, folder / FILES[0])
    patch_proposals(res, props, folder / FILES[1])
    finance_worklist(res, props, folder / FILES[3])
    validation_report(res, folder / FILES[4])
    audit_log(store, rid, None, folder / FILES[5])
    executive_summary(res, props, None, folder / FILES[6], res.get('parent_summary'))


def bo_reconciliation(res, props, path):
    wb = _wb()
    s = res['summary']
    ws = wb.create_sheet('Summary')
    rows = [('Run', res.get('run_id')), ('Workbook', res['workbook']['name']), ('Workbook SHA-256', res['workbook']['sha256']),
            ('BO report', (res.get('bo') or {}).get('name')), ('Comparison grain', 'line' + ''.join(' + ' + d for d in res['key_dims'])),
            ('Tolerance', res['tolerance']), ('Source records', s['source_records']), ('BO keys', s['bo_keys']),
            ('Matched before corrections', s['bo_matched_before']), ('Open before corrections', s['bo_open_before']),
            ('Absolute detail difference before', num(s['bo_abs_difference_before'])),
            ('Matched if all proposals were approved', s['bo_matched_after_proposals']),
            ('Absolute detail difference after proposals', num(s['bo_abs_difference_after_proposals'])),
            ('Note', 'Expected = the workbook conditions executed on the supplied source records. Nothing is forced to agree.')]
    for r in rows:
        ws.append(list(r))
    ws.column_dimensions['A'].width, ws.column_dimensions['B'].width = 44, 90
    after = {_keystr(r['key']): r for r in res['recon_after']}
    causes = {}
    for p in props:
        for k in (p.get('lines') or {}):
            causes.setdefault(k, []).append(f"{p['id']} {p['kind']} ({p['confidence']}) {', '.join(e['cell'] for e in p['edits'])}")
    for r in res['residuals']:
        causes.setdefault(r['key'], []).append(f"{r['category']} - {r['responsibility']} ({r['confidence']}): {r['evidence_needed']}")
    lines = {l['line']: l for l in res['lines']}
    rec = []
    for r in res['recon_before']:
        k = _keystr(r['key'])
        rules = res['line_rules'].get(r['line'], [])
        rec.append({'Key': k, 'Line': r['line'], 'Type': r['line_type'], 'Description': (lines.get(r['line']) or {}).get('description', ''),
                    'Expected': r['expected'], 'BO actual': r['actual'], 'Difference': r['difference'], 'Status': r['status'],
                    'Difference after proposals': (after.get(k) or {}).get('difference'), 'Root cause / proposal': ' | '.join(causes.get(k, [])),
                    'Workbook conditions': ' OR '.join(f"[{x['rule']}] {x['description']}" for x in rules),
                    'Condition cells': ', '.join(c['cell'] for x in rules for c in x['cells'].values())})
    sheet(wb, 'Reconciliation', list(rec[0]) if rec else ['Key'], rec, money={'Expected', 'BO actual', 'Difference', 'Difference after proposals'})
    sigs = {s_['id']: s_ for s_ in res['signatures']}
    contrib = []
    for k, ids in res['contributions'].items():
        for i in ids:
            sg = sigs[i]
            contrib.append({'Key': k, 'Amount': sg['amount'], 'Records': sg['records'], 'Dimensions': sg['dims'], 'Status': sg['status'],
                            'Rules matched': ', '.join(sg['rules']), 'GL Mapping rows': sg['gl_rows'], 'Sample accounts': ', '.join(sg['accounts']),
                            'Source rows': ', '.join(sg['refs'])})
    sheet(wb, 'Expected_Detail', list(contrib[0]) if contrib else ['Key'], contrib, money={'Amount'})
    un = [{'Status': sg['status'], 'Path': sg['path'], 'Amount': sg['amount'], 'Records': sg['records'], 'Dimensions': sg['dims'],
           'Sample accounts': ', '.join(sg['accounts']), 'Source rows': ', '.join(sg['refs'])} for sg in res['signatures'] if sg['status'] != 'ALLOCATED']
    sheet(wb, 'Unallocated_or_Overlap', ['Status', 'Path', 'Amount', 'Records', 'Dimensions', 'Sample accounts', 'Source rows'], un, money={'Amount'})
    sheet(wb, 'Residual_Causes', ['key', 'line', 'expected', 'actual', 'difference', 'category', 'responsibility', 'confidence', 'evidence_needed'],
          res['residuals'], money={'expected', 'actual', 'difference'})
    sheet(wb, 'BO_Internal_Totals', ['line', 'key', 'bo_total', 'bo_members_sum', 'difference', 'members', 'basis', 'responsibility'],
          res['bo_internal_totals'], money={'bo_total', 'bo_members_sum', 'difference'})
    sheet(wb, 'Root_Causes', ['id', 'root_cause', 'type', 'cells', 'proposal', 'records', 'financial_impact', 'lines', 'responsibility', 'confidence'],
          res['root_causes'], money={'financial_impact'})
    wb.save(path)


def _edit_rows(props):
    out = []
    for p in props:
        for e in p['edits']:
            out.append({'Proposal': p['id'], 'Worksheet': e['sheet'], 'Cell': e['cell'].split('!')[-1], 'Full address': e['cell'],
                        'Existing value': e['existing'], 'Proposed value': e['proposed'], 'Kind': p['kind'], 'Reason': p['reason'],
                        'Rule reference': p.get('rule_ref', ''), 'Evidence': p['evidence'], 'Affected records': p.get('affected_records', 0),
                        'Financial impact': p.get('financial_impact'), 'Confidence': p['confidence'], 'Approval status': p.get('status', 'PROPOSED'),
                        'Finance approval required': 'YES' if p['confidence'] != 'HIGH' else 'NO (deterministic)', 'Origin': p.get('origin'),
                        'Alternatives': ', '.join(p.get('alternatives') or []), 'BO lines before -> after': p.get('lines') or p.get('bo_evidence'),
                        'Decided by': p.get('decided_by'), 'Decided at': p.get('decided_at'), 'Note': p.get('note', '')})
    return out


def patch_proposals(res, props, path):
    wb = _wb()
    rows = _edit_rows(props)
    sheet(wb, 'Proposed_Patch', list(rows[0]) if rows else ['Proposal'], rows, money={'Financial impact'})
    wb.save(path)


def finance_worklist(res, props, path):
    items = []
    for p in props:
        if p['confidence'] != 'HIGH' and p.get('status') != 'APPROVED':
            items.append({'Type': 'PROPOSED CORRECTION', 'Reference': p['id'], 'Issue': p['reason'], 'Cells': ', '.join(e['cell'] for e in p['edits']),
                          'Proposed change': '; '.join(f"{e['existing']!r} -> {e['proposed']!r}" for e in p['edits']), 'Amount': p.get('financial_impact'),
                          'Records': p.get('affected_records'), 'Confidence': p['confidence'], 'Evidence / question': p['evidence']})
    for r in res['residuals']:
        if r['responsibility'] in ('UNDETERMINED', 'SOURCE_DATA', 'MAPPING_OR_BO', 'MAPPING') or r['confidence'] in ('UNRESOLVED', 'LOW'):
            items.append({'Type': 'UNRESOLVED DIFFERENCE', 'Reference': r['key'], 'Issue': r['category'], 'Cells': '', 'Proposed change': '',
                          'Amount': r['difference'], 'Records': None, 'Confidence': r['confidence'], 'Evidence / question': r['evidence_needed']})
    with_prop = {e['cell'] for p in props for e in p['edits']}
    for v in res['validation']:
        if v['severity'] == 'ERROR' and v['classification'] in ('MAPPING_DEFECT', 'REFERENCE_DATA') and v['cell'] not in with_prop \
                and not v['check'].startswith('SOURCE_'):
            items.append({'Type': 'MAPPING FINDING', 'Reference': v['id'], 'Issue': v['check'], 'Cells': v['cell'], 'Proposed change': '',
                          'Amount': v.get('amount'), 'Records': v.get('records'), 'Confidence': 'LOW', 'Evidence / question': v['message']})
    items.sort(key=lambda x: -abs(num(x['Amount']) or 0))
    for i, x in enumerate(items, 1):
        x['Priority'] = i
        x.update({'Decision (approve / reject / evidence)': '', 'Name': '', 'Date': '', 'Comment': ''})
    wb = _wb()
    cols = ['Priority', 'Type', 'Reference', 'Issue', 'Cells', 'Proposed change', 'Amount', 'Records', 'Confidence', 'Evidence / question',
            'Decision (approve / reject / evidence)', 'Name', 'Date', 'Comment']
    sheet(wb, 'Finance_Decisions', cols, items, money={'Amount'})
    wb.save(path)


def validation_report(res, path):
    wb = _wb()
    s = res['summary']
    cov = [{'Measure': k, 'Value': v} for k, v in [
        ('Sheets', ', '.join(res['workbook']['sheets'])), ('Recognised sheet roles', res['workbook']['roles']),
        ('Report lines', s['lines']), ('Detail lines', s['detail_lines']), ('Criteria rows (rules)', s['rules']),
        ('Rules not executable', s['rules_not_executable']), ('Conditions compiled', s['conditions']),
        ('Named ranges', len(res['named_ranges'])), ('GL Mapping rows', s['gl_mapping_rows']), ('Reference data', res['reference']),
        ('Validation findings', s['validation']), ('Source signatures', s['signatures']), ('Source records', s['source_records']),
        ('Allocation status (signatures)', s['allocation_status']), ('Share of source amount allocated to exactly one line', s['allocated_share'])]]
    sheet(wb, 'Coverage', ['Measure', 'Value'], cov)
    sheet(wb, 'Findings', ['id', 'severity', 'classification', 'check', 'cell', 'message', 'line', 'rule', 'records', 'amount'], res['validation'],
          money={'amount'})
    rules = []
    for r in res['rules']:
        if not r['conditions']:
            rules.append({'Rule': r['rule'], 'Line': r['line'], 'Row': r['row'], 'Executable': r['usable'], 'Errors': '; '.join(r['errors'])})
        for d, c in r['conditions'].items():
            rules.append({'Rule': r['rule'], 'Line': r['line'], 'Row': r['row'], 'Dimension': d, 'Workbook text': c['text'], 'Compiled as': c['compiled'],
                          'Cell': c['cell'], 'Formula / cross-sheet reference': c['formula'], 'Executable': r['usable'], 'Errors': '; '.join(r['errors'])})
    sheet(wb, 'Compiled_Rules', ['Rule', 'Line', 'Row', 'Dimension', 'Workbook text', 'Compiled as', 'Cell', 'Formula / cross-sheet reference',
                                 'Executable', 'Errors'], rules)
    sheet(wb, 'Lines', ['line', 'type', 'type_given', 'description', 'cell', 'rules', 'total_members', 'total_basis', 'target_gl'], res['lines'])
    sheet(wb, 'Named_Ranges', ['Name', 'Values', 'Defined at', 'Source', 'Field'],
          [{'Name': k, 'Values': v['text'], 'Defined at': v['ref'], 'Source': v['source'], 'Field': v.get('field')} for k, v in res['named_ranges'].items()])
    cm = [{'Sheet role': k, 'Header row': v['header_row'], 'Columns': v['columns'], 'Evidence': '\n'.join(v['evidence'])}
          for k, v in res['workbook']['column_maps'].items()]
    sheet(wb, 'Column_Map', ['Sheet role', 'Header row', 'Columns', 'Evidence'], cm)
    wb.save(path)


def audit_log(store, rid, correction, path):
    wb = _wb()
    sheet(wb, 'Audit_Log', ['id', 'ts', 'run_id', 'proposal_id', 'actor', 'action', 'cell', 'before', 'after', 'evidence'], store.audit(rid))
    if correction:
        v = correction['verification']
        rows = [{'Item': 'Corrected copy', 'Value': correction['path']}, {'Item': 'Edits applied', 'Value': len(correction['applied'])},
                {'Item': 'Edits refused (conflict)', 'Value': len(correction['conflicts'])},
                {'Item': 'Cells compared with the original', 'Value': v['cells_compared']},
                {'Item': 'Unexpected differences', 'Value': len(v['unexpected_differences'])},
                {'Item': 'Original preserved apart from approved cells', 'Value': 'YES' if v['preserved'] else 'NO - see details'},
                {'Item': 'Package parts not carried over by the Excel library', 'Value': ', '.join(correction['lossy_parts']) or 'none'}]
        sheet(wb, 'Corrected_Copy_Check', ['Item', 'Value'], rows)
        sheet(wb, 'Conflicts', ['cell', 'existing', 'found', 'proposed', 'reason'], correction['conflicts'])
    wb.save(path)


def executive_summary(res, props, correction, path, parent=None):
    s = res['summary']
    esc = html.escape

    def money(v):
        return '' if v in (None, '') else f'{float(Decimal(str(v))):,.2f}'
    conf = {}
    for p in props:
        conf.setdefault(p['confidence'], [0, 0])
        conf[p['confidence']][0] += 1
        conf[p['confidence']][1] += p.get('status') == 'APPROVED'
    top_props = sorted(props, key=lambda p: -abs(num(p.get('financial_impact')) or 0))[:15]
    top_res = sorted(res['residuals'], key=lambda r: -abs(num(r['difference']) or 0))[:15]
    sysrc = res['root_causes'][:15]
    rows = lambda items, cols: ''.join('<tr>' + ''.join(f'<td>{c(i)}</td>' for c in cols) + '</tr>' for i in items)  # noqa: E731
    par = ''
    if parent:
        par = (f"<h2>Before and after</h2><table><tr><th></th><th>Before</th><th>After</th></tr>"
               f"<tr><td>BO keys matched</td><td>{parent.get('bo_matched_before')}</td><td>{s['bo_matched_before']}</td></tr>"
               f"<tr><td>Absolute detail difference</td><td>{money(parent.get('bo_abs_difference_before'))}</td><td>{money(s['bo_abs_difference_before'])}</td></tr>"
               f"<tr><td>Open keys</td><td>{parent.get('bo_open_before')}</td><td>{s['bo_open_before']}</td></tr></table>")
    corr = ''
    if correction:
        v = correction['verification']
        corr = (f"<p>Corrected copy written with {len(correction['applied'])} approved cell edit(s); {len(correction['conflicts'])} refused. "
                f"{v['cells_compared']} cells compared with the original: {'no other change' if v['preserved'] else 'UNEXPECTED DIFFERENCES - see PATCH_AUDIT_LOG.xlsx'}."
                + (f" Parts not carried over: {esc(', '.join(correction['lossy_parts']))}." if correction['lossy_parts'] else '') + '</p>')
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Mapping Studio executive summary</title>
<style>body{{font:14px system-ui,Segoe UI,sans-serif;margin:24px;color:#1d2330;max-width:1200px}}table{{border-collapse:collapse;width:100%;margin:8px 0 20px}}
th,td{{border-bottom:1px solid #d9dde4;padding:5px 7px;text-align:left;vertical-align:top}}th{{background:#eef1f5}}.k{{display:inline-block;margin:0 18px 12px 0}}
.k b{{display:block;font-size:22px}}.note{{background:#fff4d6;padding:8px 10px;border-radius:6px}}</style></head><body>
<h1>NBS Mapping Studio - executive summary</h1>
<p class="note">Run {esc(str(res.get('run_id')))} ({esc(res.get('kind') or 'ANALYSIS')}), {esc(res['created'])}. Workbook {esc(res['workbook']['name'])}
(SHA-256 {res['workbook']['sha256'][:16]}...). BO report {esc(str((res.get('bo') or {}).get('name')))}. Grain: line{esc(''.join(' + ' + d for d in res['key_dims']))};
tolerance {res['tolerance']}. All figures come from the supplied files; nothing is forced to agree.</p>
<div><span class="k"><b>{s['rules']}</b>criteria rows compiled ({s['rules_not_executable']} not executable)</span>
<span class="k"><b>{s['conditions']}</b>conditions with cell references</span>
<span class="k"><b>{s['validation'].get('ERROR', 0)}</b>validation errors</span>
<span class="k"><b>{s['bo_matched_before']} / {s['bo_keys']}</b>BO keys matched</span>
<span class="k"><b>{money(s['bo_abs_difference_before'])}</b>absolute BO difference (detail lines)</span>
<span class="k"><b>{s['bo_matched_after_proposals'] if s['bo_matched_after_proposals'] is not None else '-'}</b>keys matched if all proposals approved</span>
<span class="k"><b>{s['unresolved']}</b>unresolved (evidence needed)</span></div>
{par}{corr}
<h2>Proposed corrections</h2><p>{', '.join(f'{k}: {v[0]} ({v[1]} approved)' for k, v in sorted(conf.items())) or 'none'}</p>
<table><tr><th>ID</th><th>Cell(s)</th><th>Change</th><th>Reason</th><th>Records</th><th>Impact</th><th>Confidence</th><th>Status</th></tr>
{rows(top_props, [lambda p: p['id'], lambda p: esc(', '.join(e['cell'] for e in p['edits'])),
                  lambda p: esc('; '.join(f"{e['existing']!r} -> {e['proposed']!r}" for e in p['edits'])), lambda p: esc(p['reason']),
                  lambda p: p.get('affected_records', ''), lambda p: money(p.get('financial_impact')), lambda p: p['confidence'], lambda p: p.get('status', 'PROPOSED')])}</table>
<h2>Systemic root causes</h2><table><tr><th>ID</th><th>Root cause</th><th>Responsibility</th><th>Records</th><th>Impact</th><th>Confidence</th></tr>
{rows(sysrc, [lambda r: r['id'], lambda r: esc(r['root_cause']), lambda r: r['responsibility'], lambda r: r['records'], lambda r: money(r['financial_impact']), lambda r: r['confidence']])}</table>
<h2>Material differences not explained by a mapping correction</h2><table><tr><th>Key</th><th>Difference</th><th>Category</th><th>Responsibility</th><th>Evidence needed</th></tr>
{rows(top_res, [lambda r: esc(r['key']), lambda r: money(r['difference']), lambda r: r['category'], lambda r: r['responsibility'], lambda r: esc(r['evidence_needed'])])}</table>
<p>Details: BO_RECONCILIATION.xlsx, PROPOSED_MAPPING_PATCH.xlsx, FINANCE_DECISION_WORKLIST.xlsx, MAPPING_VALIDATION_REPORT.xlsx, PATCH_AUDIT_LOG.xlsx.</p>
</body></html>"""
    Path(path).write_text(doc, encoding='utf-8')


def write_corrected(store, rid, folder, res, actor):
    """C (corrected copy of approved edits) and F, with B, D and G refreshed for the approval state."""
    folder = Path(folder)
    props = store.proposals(rid)
    approved = [p for p in props if p.get('status') == 'APPROVED']
    edits = [e for p in sorted(approved, key=lambda p: p['id']) for e in p['edits']]
    corr = patchbook.write_corrected(res['workbook_path'], edits, folder / FILES[2])
    store.log(rid, actor, 'CORRECTED_COPY_WRITTEN', f"{len(corr['applied'])} edits applied, {len(corr['conflicts'])} refused; "
              f"preserved={corr['verification']['preserved']}")
    for c in corr['conflicts']:
        store.log(rid, actor, 'EDIT_REFUSED_CONFLICT', c['reason'], c['cell'], c['existing'], c['found'])
    patch_proposals(res, props, folder / FILES[1])
    finance_worklist(res, props, folder / FILES[3])
    audit_log(store, rid, corr, folder / FILES[5])
    executive_summary(res, props, corr, folder / FILES[6], res.get('parent_summary'))
    return corr
