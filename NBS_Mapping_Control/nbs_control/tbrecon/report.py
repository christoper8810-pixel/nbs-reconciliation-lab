"""Run outputs: indexed run.sqlite (drill-down), CSV, audit JSON, self-contained HTML and Excel."""
from __future__ import annotations

import csv
import html
import json
import sqlite3
from decimal import Decimal
from pathlib import Path

TABLES = {
    'gl_rows': ['target_gl', 'currency', 'class', 'legacy_gls', 'expected', 'expected_by_stream', 'actual_closing',
                'post_cob_movements', 'actual_opening', 'difference', 'abs_difference', 'unresolved_candidate_amount',
                'mapping_status', 'recon_status', 'exception_reason'],
    'components': ['engine', 'source_row', 'account', 'ref', 'legacy_gl', 'currency', 'balance_type', 'amount', 'status',
                   'contra', 'rule_id', 'line', 'target_gl', 'target_account', 'candidates', 'candidate_rules', 'reason',
                   'misalignment', 'duplicate_source', 'gl_mapping_conflict', 'flags'],
    'exceptions': ['exception_id', 'category', 'level', 'engine', 'amount', 'reason', 'account', 'consol_key', 'balance_type',
                   'currency', 'legacy_gl', 'target_gl', 'rule_id', 'rules', 'candidates', 'dimension', 'subtype',
                   'confidence', 'informational', 'paired_with'],
    'issues': ['issue_id', 'category', 'title', 'level', 'group', 'records', 'accounts', 'net_amount', 'absolute_amount',
               'related_rules', 'proposed_action', 'confidence', 'open_question', 'informational', 'evidence'],
    'worklist': ['proposal_id', 'kind', 'file', 'rule_id', 'source_row', 'original_value', 'proposed_value', 'reason',
                 'evidence', 'amount_affected', 'confidence', 'auto_applicable', 'status'],
    'controls': ['id', 'control', 'status', 'detail', 'values'],
    'contributions': ['consol_key', 'balance_type', 'target_gl', 'amount', 'components'],
    'gl_report': ['line', 'type', 'description', 'target_gl', 'amount', 'components', 'status', 'total_of'],
    'rollforward': ['target_gl', 'currency', 'opening_migrated_expected', 'validated_post_cob_movements', 'by_type',
                    'computed_closing', 'actual_closing', 'rollforward_difference'],
    'benchmark': ['target_gl', 'currency', 'expected', 'benchmark', 'difference', 'status'],
    'legacy_lines': ['legacy_gl', 'currency', 'class', 'tb_amount', 'stream', 'population', 'gap', 'targets', 'status'],
    'unallocated': ['engine', 'legacy_gl', 'currency', 'amount', 'status', 'candidates', 'account', 'balance_type'],
    'rule_diagnostics': ['engine', 'type', 'rule', 'line', 'row', 'rules', 'targets', 'detail', 'dimensions', 'errors', 'name'],
    'misalignment': ['type', 'rule_column', 'source_column', 'expected_dimension', 'observed_dimension', 'own_domain_hit_rate',
                     'observed_domain_hit_rate', 'affected_rules', 'affected_rows', 'affected_accounts', 'net_amount',
                     'absolute_amount', 'evidence', 'segments_verified', 'examples'],
    'account_recon': ['target_account', 'expected', 'actual', 'difference', 'status', 'sources'],
    'unsupported_bt': ['rule_id', 'line', 'balance_type', 'targets', 'row', 'reason'],
}
NUMERIC = {'amount', 'expected', 'actual_closing', 'actual_opening', 'difference', 'abs_difference', 'net_amount', 'absolute_amount',
           'tb_amount', 'population', 'gap', 'benchmark', 'actual', 'amount_affected', 'post_cob_movements',
           'unresolved_candidate_amount', 'opening_migrated_expected', 'validated_post_cob_movements', 'computed_closing',
           'rollforward_difference'}


def cell(v):
    if v is None:
        return ''
    if isinstance(v, Decimal):
        return format(v, 'f')
    if isinstance(v, bool):
        return 'Y' if v else ''
    if isinstance(v, (list, tuple, set, dict)):
        return json.dumps(v if not isinstance(v, set) else sorted(v), default=str, separators=(',', ':')) if v else ''
    return str(v)


def collect(res):
    E = res['engines']
    rec = res['recon']
    diags = [{'engine': k, **d} for k in ('A', 'C') for d in (E[k].get('rule_diagnostics') or [])]
    return {
        'gl_rows': rec['gl_rows'],
        'components': [c for e in E.values() for c in e.get('components') or []],
        'exceptions': res['exceptions'], 'issues': res['issues'], 'worklist': res['worklist'], 'controls': res['controls'],
        'contributions': E['A'].get('contributions') or [], 'gl_report': rec['gl_report'], 'rollforward': rec['rollforward'],
        'benchmark': rec['benchmark'] or [], 'legacy_lines': rec['legacy_lines'], 'unallocated': rec['unallocated'],
        'rule_diagnostics': diags, 'misalignment': E['A'].get('misalignment') or [],
        'account_recon': E['B'].get('account_reconciliation') or [], 'unsupported_bt': E['A'].get('unsupported_balance_types') or [],
    }


def write_all(res, folder):
    folder = Path(folder)
    data = collect(res)
    db = folder / 'run.sqlite'
    if db.exists():
        db.unlink()
    c = sqlite3.connect(db)
    try:
        for name, cols in TABLES.items():
            c.execute(f'CREATE TABLE {name} (' + ', '.join(f'"{x}" {"REAL" if x in NUMERIC else "TEXT"}' for x in cols) +
                      (', amount_exact TEXT' if 'amount' in cols or 'difference' in cols else '') + ')')
            exact_col = 'amount' if 'amount' in cols else 'difference' if 'difference' in cols else None
            rows = []
            for r in data[name]:
                vals = [(float(r[x]) if isinstance(r.get(x), Decimal) else r.get(x)) if x in NUMERIC else cell(r.get(x)) for x in cols]
                if exact_col:
                    vals.append(cell(r.get(exact_col)))
                rows.append(vals)
            ph = ', '.join('?' for _ in range(len(cols) + (1 if exact_col else 0)))
            c.executemany(f'INSERT INTO {name} VALUES ({ph})', rows)
        c.execute('CREATE INDEX comp_gl ON components(target_gl, currency)')
        c.execute('CREATE INDEX comp_acct ON components(account)')
        c.execute('CREATE INDEX comp_status ON components(status)')
        c.execute('CREATE INDEX exc_cat ON exceptions(category)')
        c.execute('CREATE INDEX gl_key ON gl_rows(target_gl, currency)')
        c.execute('CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)')
        for k in ('meta', 'statistics'):
            c.execute('INSERT INTO meta VALUES (?, ?)', (k, json.dumps(res[k], default=cell)))
        c.execute('INSERT INTO meta VALUES (?, ?)', ('engines', json.dumps(
            {k: {kk: e.get(kk) for kk in ('engine', 'name', 'status', 'reason', 'stats', 'status_amounts', 'schema', 'aliases',
                                          'layout', 'explicit_dimension_columns', 'many_to_one_targets')}
             for k, e in res['engines'].items()}, default=cell)))
        c.execute('INSERT INTO meta VALUES (?, ?)', ('totals', json.dumps(res['recon']['totals'], default=cell)))
        c.commit()
    finally:
        c.close()
    for name in ('gl_rows', 'exceptions', 'issues', 'worklist', 'controls', 'contributions', 'components', 'gl_report',
                 'rollforward', 'legacy_lines', 'unallocated', 'benchmark', 'misalignment', 'rule_diagnostics', 'account_recon'):
        fname = {'gl_rows': 'tb_reconciliation', 'issues': 'root_causes', 'worklist': 'proposed_mapping_corrections'}.get(name, name)
        with (folder / f'{fname}.csv').open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerow(TABLES[name])
            for r in data[name]:
                w.writerow([cell(r.get(x)) for x in TABLES[name]])
    from .run import top_exceptions
    audit = {'meta': res['meta'], 'statistics': res['statistics'], 'controls': res['controls'], 'systemic_issues': res['issues'],
             'proposed_mapping_corrections': res['worklist'], 'top_20_exceptions': top_exceptions(res),
             'tb_reconciliation': data['gl_rows'], 'legacy_lines': data['legacy_lines'], 'gl_report': data['gl_report'],
             'rollforward': data['rollforward'], 'benchmark': data['benchmark'], 'misalignment': data['misalignment'],
             'unsupported_balance_types': data['unsupported_bt'], 'rule_diagnostics': data['rule_diagnostics'],
             'engines': {k: {kk: e.get(kk) for kk in ('engine', 'name', 'status', 'reason', 'stats', 'status_amounts', 'layout')}
                         for k, e in res['engines'].items()},
             'totals': res['recon']['totals'], 'exceptions': res['exceptions'],
             'note': 'Generated from the supplied inputs only. Nothing is plugged, suppressed or forced to zero. '
                     'SOURCE_PENDING / INCOMPLETE lines are not reconciled.'}
    (folder / 'audit.json').write_text(json.dumps(audit, indent=1, default=cell), encoding='utf-8')
    (folder / 'report.html').write_text(html_report(res, data), encoding='utf-8')
    write_xlsx(res, data, folder / 'reconciliation.xlsx')
    return folder


def write_xlsx(res, data, path):
    import openpyxl
    wb = openpyxl.Workbook(write_only=True)
    ws = wb.create_sheet('Summary')
    ws.append(['NBS Mapping Control - whole-TB migration reconciliation'])
    for k in ('run_id', 'created', 'label', 'engine_version', 'result_hash', 'config_hash', 'rules_hash', 'legacy_semantics'):
        ws.append([k, cell(res['meta'].get(k))])
    ws.append(['tolerance', cell(res['meta']['tolerance'])])
    ws.append(['missing inputs', ', '.join(res['meta']['missing_inputs']) or 'none'])
    ws.append([])
    for k, v in res['statistics'].items():
        ws.append([k, float(v) if isinstance(v, Decimal) else cell(v)])
    sheets = [('Controls', 'controls'), ('TB_Reconciliation', 'gl_rows'), ('Legacy_TB_Lines', 'legacy_lines'), ('GL_Report', 'gl_report'),
              ('RollForward', 'rollforward'), ('Root_Causes', 'issues'), ('Correction_Worklist', 'worklist'),
              ('Exceptions', 'exceptions'), ('Unallocated', 'unallocated'), ('Allocation_Grain', 'contributions'),
              ('Misalignment', 'misalignment'), ('Rule_Diagnostics', 'rule_diagnostics'), ('Unsupported_BT', 'unsupported_bt'),
              ('Internal_Accounts', 'account_recon'), ('Benchmark', 'benchmark')]
    for title, name in sheets:
        ws = wb.create_sheet(title)
        ws.append(TABLES[name])
        for i, r in enumerate(data[name]):
            if i >= 1_000_000:
                ws.append(['... truncated: see CSV export'])
                break
            ws.append([float(r[x]) if isinstance(r.get(x), Decimal) else cell(r.get(x)) for x in TABLES[name]])
    wb.save(path)


def _fmt(v):
    if v is None or v == '':
        return ''
    if isinstance(v, Decimal):
        return f'{v:,.2f}'
    return html.escape(cell(v))


def _table(rows, cols, limit=200):
    h = '<table><tr>' + ''.join(f'<th>{html.escape(c)}</th>' for c in cols) + '</tr>'
    for r in rows[:limit]:
        h += '<tr>' + ''.join(f'<td class="{"num" if isinstance(r.get(c), Decimal) else ""} {html.escape(str(r.get(c))) if c in ("status", "recon_status") else ""}">{_fmt(r.get(c))}</td>' for c in cols) + '</tr>'
    if len(rows) > limit:
        h += f'<tr><td colspan="{len(cols)}">... {len(rows) - limit} more rows in the CSV / Excel export</td></tr>'
    return h + '</table>'


def html_report(res, data):
    from .run import top_exceptions
    m, s = res['meta'], res['statistics']
    css = ('body{font:13px system-ui,Segoe UI,sans-serif;margin:20px;color:#1d2330}table{border-collapse:collapse;width:100%;margin:8px 0 18px}'
           'th,td{border-bottom:1px solid #d9dde4;padding:4px 6px;text-align:left;vertical-align:top}th{background:#eef1f5}'
           '.num{text-align:right;font-variant-numeric:tabular-nums}.PASS,.RECONCILED{color:#1d7a46}.FAIL,.DIFFERENCE{color:#b42318}'
           '.WARN,.INCOMPLETE,.SOURCE_PENDING{color:#9a6200}.note{background:#fff4d6;padding:8px;border-radius:6px}')
    engines = ''.join(f'<li><b>{k}</b> {html.escape(e["name"])}: {e["status"]}{" - " + html.escape(e.get("reason", "")) if e.get("reason") else ""}</li>'
                      for k, e in res['engines'].items())
    stats = ''.join(f'<tr><td>{html.escape(k)}</td><td class="num">{_fmt(v)}</td></tr>' for k, v in s.items())
    open_gl = sorted((r for r in data['gl_rows'] if r['recon_status'] != 'RECONCILED'), key=lambda r: -r['abs_difference'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>TB reconciliation {html.escape(m['run_id'])}</title><style>{css}</style></head><body>
<h1>Whole-TB migration reconciliation - run {html.escape(m['run_id'])}</h1>
<p class="note">Generated from the supplied inputs only. No plug, suppression or forced zero. SOURCE_PENDING and INCOMPLETE lines are not reconciled.
Tolerance: absolute {m['tolerance']['absolute']}, relative {m['tolerance']['relative']}. Result hash {m['result_hash']}.
Missing inputs: {html.escape(', '.join(m['missing_inputs']) or 'none')}. {'LEGACY TOKEN SEMANTICS (baseline measurement only).' if m['legacy_semantics'] else ''}</p>
<h2>Streams</h2><ul>{engines}</ul>
<h2>Statistics</h2><table>{stats}</table>
<h2>Controls</h2>{_table(res['controls'], ['id', 'control', 'status', 'detail'])}
<h2>Open GL lines (largest first)</h2>{_table(open_gl, ['target_gl', 'currency', 'class', 'legacy_gls', 'expected', 'actual_opening', 'difference', 'mapping_status', 'recon_status', 'exception_reason'])}
<h2>Systemic root causes</h2>{_table(res['issues'], ['issue_id', 'title', 'level', 'group', 'records', 'accounts', 'net_amount', 'absolute_amount', 'confidence', 'proposed_action', 'open_question'])}
<h2>Top 20 exceptions</h2>{_table(top_exceptions(res), ['exception_id', 'category', 'level', 'engine', 'amount', 'reason'])}
<h2>Proposed mapping corrections (original mapping unchanged)</h2>{_table(res['worklist'], ['proposal_id', 'kind', 'rule_id', 'original_value', 'proposed_value', 'reason', 'confidence', 'amount_affected'])}
<h2>GL Report (H / D / T)</h2>{_table(data['gl_report'], ['line', 'type', 'description', 'target_gl', 'amount', 'status'])}
<h2>Roll-forward</h2>{_table(data['rollforward'], ['target_gl', 'currency', 'opening_migrated_expected', 'validated_post_cob_movements', 'computed_closing', 'actual_closing', 'rollforward_difference'])}
<h2>Full TB reconciliation</h2>{_table(data['gl_rows'], ['target_gl', 'currency', 'class', 'legacy_gls', 'expected', 'actual_opening', 'difference', 'mapping_status', 'recon_status'], 2000)}
</body></html>"""
