"""Stakeholder export of the NBS mapping: Excel specification + machine-readable JSON/CSV.

Everything is taken from the versioned engine configuration (target mappings, legacy population rules,
measure catalogue, hierarchy predicates, balance and product policies, QCB rules) and, when given, from a
run's results. The export is a specification for review; it does not certify any figure.
"""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from . import rebuild_run as rr, target_mappings as tm
from .rebuild_engine import correct_components, inherit_hierarchy

OPS = {'eq': 'is', 'in': 'is one of', 'prefix': 'starts with', 'range': 'is between', 'blank': 'is blank', 'not_blank': 'is not blank'}
FIELD_NAMES = {'category': 'T24 category', 'sector': 'T24 sector', 'industry': 'SIC / industry code', 'personal': 'customer type',
               'residency': 'residency', 'product': 'account/product type', 'currency': 'currency', 'country': 'country',
               'gl': 'GL account', 'rim': 'customer (RIM)', 'risk': 'risk grade', 'account': 'account', 'maturity': 'maturity date',
               'pl_category': 'PL.CATEGORY', 'product_category': 'PRODUCT.CATEGORY'}
SOURCE_NAMES = {'ECB': 'T24 ECB balances (all categories)', 'ECB_LOAN': 'T24 ECB balances joined to the loan file',
                'ECB_DEPOSIT': 'T24 ECB balances joined to the deposit file', 'TB': 'Ethix trial balance (GL)'}
MEASURE_NAMES = {'components': 'sum of the listed ECB balance types', 'outstanding': 'owner OUTSTANDING balance group (sign reversed)',
                 'earned': 'owner AMORTIZED_EARNED group (sign reversed)', 'unearned': 'owner UNEARNED_PROFIT group (sign reversed)',
                 'carrying': 'outstanding + earned + Ethix loan fees (hybrid)', 'ethix_carrying': 'product-policy carrying amount (RCM/CLM policies) + Ethix loan fees (hybrid)',
                 'deposit': 'ECB CREDIT + CURACCOUNT', 'amount': 'source amount'}
LAYOUTS = {'geo': 'Inside/Outside Qatar x LC/FC', 'tb': 'LC/FC totals only (no residency in GL)', 'maturity_loan': 'remaining maturity bands (loans)',
           'maturity_deposit': 'current & call / saving / time-deposit maturity bands', 'size': 'amount bands (counts and amounts)',
           'risk': 'credit classification (direct)', 'sector_columns': 'economic sector x LC/FC', None: 'Inside/Outside Qatar x LC/FC'}
HEAD = PatternFill('solid', fgColor='1F3A5F')
AMBER = PatternFill('solid', fgColor='FFF2CC')


def readable(node):
    if not node:
        return 'all records of the source'
    if 'all' in node:
        return ' AND '.join('(' + readable(x) + ')' if ('any' in x or 'all' in x) else readable(x) for x in node['all'])
    if 'any' in node:
        return ' OR '.join(readable(x) for x in node['any'])
    if 'not' in node:
        return 'NOT (' + readable(node['not']) + ')'
    vals = node.get('values', [])
    return f"{FIELD_NAMES.get(node['field'], node['field'])} {OPS.get(node['op'], node['op'])} {', '.join(str(v) for v in vals)}".strip()


def describe_measure(spec):
    m = spec.get('measure')
    text = MEASURE_NAMES.get(m, m or 'not defined')
    if m == 'components':
        text += ': ' + ', '.join(spec.get('components') or [])
    if spec.get('negative_filter'):
        text += '; deducted when ' + readable(spec['negative_filter'])
    if spec.get('factor') not in (None, 1, 1.0):
        text += f'; presentation sign x{spec["factor"]}'
    return text


def _sheet(wb, title, rows, widths=None, wrap=False, amber=()):
    ws = wb.create_sheet(title)
    rows = list(rows)
    if not rows:
        ws.append(['No rows'])
        return ws
    fields = list(rows[0])
    ws.append(fields)
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for r in rows:
        ws.append([float(v) if isinstance(v, Decimal) else (json.dumps(v) if isinstance(v, (dict, list)) else v) for v in (r.get(f) for f in fields)])
    ws.freeze_panes = 'C2' if len(fields) > 4 else 'A2'
    ws.auto_filter.ref = ws.dimensions
    for i, f in enumerate(fields, start=1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(f, min(60, max(10, len(f) + 2)))
        if f in amber:
            for row in ws.iter_rows(min_row=2, min_col=i, max_col=i):
                row[0].fill = AMBER
    if wrap:
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical='top')
    return ws


def build_rows(root, run_id=None):
    p = rr.Paths(root)
    doc = tm.load(p.config)
    rules = json.loads(p.rules.read_text(encoding='utf-8'))['rules']
    catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
    settings = rr.run_settings(p)
    hier = settings.get('hierarchy_predicates')
    corrections = settings.get('component_corrections')
    cmp_by_target = defaultdict(list)
    run_dir = (p.runs / run_id) if run_id else None
    if run_dir and (run_dir / 'comparison_bo.csv').exists():
        for r in csv.DictReader(open(run_dir / 'comparison_bo.csv', encoding='utf-8-sig')):
            cmp_by_target[r['target_id']].append(r)
    depth = {}
    for tid, t in doc['targets'].items():
        d, par = 0, t.get('parent_code')
        while par:
            d += 1
            par = doc['targets'].get(f'{t["table"]}|{par}', {}).get('parent_code')
        depth[tid] = d
    out = []
    for tid, t in sorted(doc['targets'].items(), key=lambda x: (x[1]['table'], x[1]['item_code'])):
        spec = rules.get(t.get('legacy_rule_id') or '') if t['method'] == 'LEGACY_RULE' else None
        specs = [rules.get(x) for x in t.get('legacy_rule_ids') or []] if t['method'] == 'QCB_POPULATION' else ([spec] if spec else [])
        specs = [s for s in specs if s]
        effective, inherited = [], []
        for s in specs:
            s, fixes = correct_components(s, corrections)
            e, notes = inherit_hierarchy(s, hier)
            effective.append(e)
            inherited += fixes + notes
        comps = cmp_by_target.get(tid, [])
        comparable = [c for c in comps if c['difference'] not in ('', None) and c['kind'] == 'money' and c['primary'] == 'True']
        flags = []
        if t.get('candidate_basis') == 'SELECTOR_NOT_DISTINCT':
            flags.append('Selector cannot distinguish sibling items')
        if t.get('suggested_legacy_rule_id') and t['status'] == 'UNRESOLVED' and 'label differs' in (t.get('evidence') or ''):
            flags.append('QCB label differs from legacy label')
        if any(s.get('source') and s['source'] == 'ECB_LOAN' and s.get('measure') in ('carrying', 'ethix_carrying') for s in specs):
            flags.append('Hybrid: uses Ethix loan fees')
        if specs and not all(s.get('enabled') and s.get('source') for s in specs):
            flags.append('Population rule has no data source yet')
        out.append({
            'target_id': tid, 'table': t['table'], 'qcb_item_code': t['item_code'], 'level': depth[tid],
            'description': ('    ' * depth[tid]) + (t.get('description') or ''), 'parent_code': t.get('parent_code'),
            'mapping_status': t['status'], 'method': t['method'],
            'data_source': '; '.join(sorted({SOURCE_NAMES.get(s.get('source'), s.get('source') or 'none') for s in specs})) if specs else
                           ('Derived from other NBS items (QCB rule)' if t['method'] == 'QCB_COMPOSITION' else ''),
            'account_population': ' UNION '.join('[' + readable(e.get('filter')) + ']' for e in effective) if effective else '',
            'inherited_dimensions': '; '.join(dict.fromkeys(inherited)),
            'balance_definition': '; '.join(dict.fromkeys(describe_measure(s) for s in effective)),
            'breakdown': LAYOUTS.get(t.get('layout') if t['method'] == 'QCB_POPULATION' else (specs[0].get('layout') if specs else None), '') if specs else '',
            'size_band_grain': (hier or {}).get('size_band_grain', {}).get(t['table'], '') if t['table'] in ('012', '025') else '',
            'qcb_rules_used': '; '.join(sorted({f'{v["qcb_code"]} ({v["rule_id"]})' for v in (t.get('qcb_composition') or {}).values()}
                                              | ({f'{t.get("qcb_code")} ({t.get("qcb_rule_id")})'} if t.get('qcb_rule_id') else set()))),
            'legacy_rule_id': ', '.join(x for x in ([t.get('legacy_rule_id')] + (t.get('legacy_rule_ids') or [])) if x),
            'legacy_row': ', '.join(str(s.get('row')) for s in specs if s.get('row')),
            'legacy_path': ' | '.join(s.get('path', '') for s in specs)[:300],
            'suggested_rule_for_review': t.get('suggested_legacy_rule_id') or '',
            'candidate_basis': t.get('candidate_basis'), 'evidence': t.get('evidence'), 'review_flags': '; '.join(flags),
            'population_filter_json': json.dumps([e.get('filter') for e in effective]) if effective else '',
            'generated_cells': sum(1 for c in comps if c['generated'] not in ('', None)),
            'bo_cells_within_tolerance': sum(1 for c in comparable if c['category'] in ('WITHIN_TOLERANCE', 'ROUNDING')),
            'bo_cells_compared': len(comparable),
            'largest_abs_difference_qar_k': max((abs(Decimal(c['difference'])) for c in comparable), default=''),
            'last_changed_by': t.get('author'), 'last_changed_at': t.get('changed_at') or doc.get('created_at'),
            'stakeholder_comment': '', 'stakeholder_decision': '',
        })
    return doc, out, catalogue, rules, hier


def export(root, run_id=None, out_dir=None):
    p = rr.Paths(root)
    if run_id is None:
        latest = rr.latest_run(root)
        run_id = latest['run_id'] if latest else None
    doc, rows, catalogue, rules, hier = build_rows(root, run_id)
    manifest = json.loads((p.runs / run_id / 'manifest.json').read_text(encoding='utf-8')) if run_id else None
    out_dir = Path(out_dir or p.root / 'exports' / 'mapping_specification')
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = f'v{doc["version"]}_{date.today().isoformat()}'
    xl = out_dir / f'NBS_Mapping_Specification_{stamp}.xlsx'
    mapping_sha = hashlib.sha256((p.config / tm.MAPPING_FILE).read_bytes()).hexdigest()
    wb = Workbook()
    ws = wb.active
    ws.title = 'README'
    status = Counter(r['mapping_status'] for r in rows)
    method = Counter(r['method'] for r in rows)
    lines = [
        ('NBS mapping specification', f'Mapping version {doc["version"]} (sha256 {mapping_sha[:16]}...), exported {date.today().isoformat()}'),
        ('Target identity', 'BO table code + full QCB item code. Measures are the BO column headers of each table (see Measures).'),
        ('Scope', f'{len(rows)} targets: ' + ', '.join(f'{k} {v}' for k, v in status.most_common())),
        ('Methods', ', '.join(f'{k} {v}' for k, v in method.most_common())),
        ('LEGACY_RULE', 'An account population + balance definition over T24 ECB balances (joined to the loan/deposit files where needed) or the Ethix trial balance.'),
        ('QCB_COMPOSITION', 'Defined by a QCB validation identity from other mapped items (e.g. a Table 100 line = its detail-table items). Passes that rule by construction.'),
        ('QCB_POPULATION', 'Same accounts as the items a QCB identity equates it with, split by this table\'s breakdown (maturity, size band, sector ...).'),
        ('Inherited dimensions', 'A row inherits the dimensions of its parent rows (Inside/Outside Qatar -> residency, Current & Call / Saving & Time -> account type, sector levels). See Hierarchy_rules.'),
        ('DRAFT_CANDIDATE', 'Unreviewed: proposed from the QCB code structure, the legacy report rows or QCB rules. Not approved by the owner. Never a certified figure.'),
        ('UNRESOLVED', 'No usable definition yet; reason in evidence/review_flags. Listed in Review_queue.'),
        ('Amber columns', 'stakeholder_comment / stakeholder_decision are for reviewers; return the workbook to the mapping owner.'),
        ('Figures', f'From engine run {run_id} (report date {manifest["period"]["report_date"]}) - generated vs BO reference, QAR thousands.' if manifest else 'No run figures included.'),
        ('Not a GL mapping', 'See Why_not_GL: the bank\'s own account files show that any GL-to-line mapping must misplace a large share of balances.'),
        ('BO consistency', 'The BO reference itself fails some QCB validation rules (see QCB_validations); a 100% match to BO would reproduce those inconsistencies.'),
    ]
    for a, b in lines:
        ws.append([a, b])
    ws.column_dimensions['A'].width = 24
    ws.column_dimensions['B'].width = 140
    for row in ws.iter_rows():
        row[0].font = Font(bold=True)
        row[1].alignment = Alignment(wrap_text=True)
    # Summary by table
    summ = []
    by_table = defaultdict(list)
    for r in rows:
        by_table[r['table']].append(r)
    titles = {t: v.get('title', '') for t, v in catalogue['tables'].items()}
    for t, rs in sorted(by_table.items()):
        summ.append({'table': t, 'title': titles.get(t, ''), 'targets': len(rs),
                     'draft_legacy_rule': sum(r['method'] == 'LEGACY_RULE' and r['mapping_status'] == 'DRAFT_CANDIDATE' for r in rs),
                     'qcb_composition': sum(r['method'] == 'QCB_COMPOSITION' for r in rs), 'qcb_population': sum(r['method'] == 'QCB_POPULATION' for r in rs),
                     'approved_or_provisional': sum(r['mapping_status'] in ('APPROVED', 'PROVISIONAL') for r in rs),
                     'unresolved': sum(r['mapping_status'] == 'UNRESOLVED' for r in rs),
                     'no_data_source_yet': sum('no data source' in r['review_flags'] for r in rs),
                     'generated_cells': sum(r['generated_cells'] for r in rs),
                     'bo_cells_compared': sum(r['bo_cells_compared'] for r in rs), 'bo_cells_within_tolerance': sum(r['bo_cells_within_tolerance'] for r in rs)})
    _sheet(wb, 'Summary_by_table', summ, {'title': 60})
    _sheet(wb, 'Mapping', rows, {'description': 45, 'account_population': 80, 'balance_definition': 45, 'evidence': 60, 'legacy_path': 50,
                                 'inherited_dimensions': 40, 'population_filter_json': 40, 'qcb_rules_used': 30, 'data_source': 30,
                                 'stakeholder_comment': 30, 'stakeholder_decision': 20}, amber=('stakeholder_comment', 'stakeholder_decision'))
    meas = [{'table': t, 'header': h, 'semantic': m.get('semantic'), 'kind': m['kind'], 'unit': m['unit'], 'primary': m.get('primary', True),
             'additive': m.get('additive', True), 'note': m.get('note') or m.get('sign_note') or ''}
            for t, v in sorted(catalogue['tables'].items()) for h, m in v.get('measures', {}).items()]
    _sheet(wb, 'Measures', meas, {'header': 26, 'semantic': 28, 'note': 60})
    bal = json.loads((p.config / 'balance_rules.json').read_text(encoding='utf-8'))
    pol = json.loads((p.config / 'report_product_policies.json').read_text(encoding='utf-8'))
    defs = [{'definition': f'Owner group {g}', 'components': ', '.join(ts), 'source': 'config/balance_rules.json'} for g, ts in bal['groups'].items()]
    defs += [{'definition': f'Product policy {k}', 'components': json.dumps(v), 'source': 'config/report_product_policies.json'} for k, v in pol.get('products', {}).items()]
    defs += [{'definition': k, 'components': v, 'source': 'engine measure'} for k, v in MEASURE_NAMES.items()]
    _sheet(wb, 'Balance_definitions', defs, {'components': 100, 'definition': 30}, wrap=True)
    hr = [{'label': k, 'applies_to': src, 'predicate': readable(v) if src != 'SECTOR' else f'sector filter "{v}"',
           'always_applied': bool(e.get('FORCE')), 'provisional': e.get('PROVISIONAL', '')}
          for k, e in (hier or {}).get('labels', {}).items() for src, v in e.items()
          if src == 'SECTOR' or (isinstance(v, dict) and src in ('ECB','ECB_LOAN','ECB_DEPOSIT','TB'))]
    hr += [{'label': 'namespace correction', 'applies_to': 'industry field', 'predicate': json.dumps((hier or {}).get('namespace_corrections', {})),
            'always_applied': True, 'provisional': ''}]
    hr += [{'label': k, 'applies_to': 'NOT INHERITED', 'predicate': v} for k, v in (hier or {}).get('not_inherited_without_evidence', {}).items()]
    _sheet(wb, 'Hierarchy_rules', hr, {'predicate': 90, 'label': 30})
    if run_id and (p.runs / run_id / 'qcb_validation_results.csv').exists():
        q = list(csv.DictReader(open(p.runs / run_id / 'qcb_validation_results.csv', encoding='utf-8-sig')))
        _sheet(wb, 'QCB_validations', q, {'left': 60, 'right': 60, 'description': 50})
    ev_path = p.data / 'gl_evidence.json'
    if ev_path.exists():
        ev = json.loads(ev_path.read_text(encoding='utf-8'))
        gl_rows = []
        for src in ('LOAN', 'DEPOSIT'):
            a = ev['accounts'][src]
            for k, v in a['by_breakdown'].items():
                gl_rows.append({'portfolio': src, 'accounts': a['accounts'], 'gls': a['gls'], 'customers': a['customers'], 'breakdown': k,
                                'gls_spanning_several_cells': v['gls_spanning_several_cells'], 'balance_in_those_gls_qar': Decimal(v['balance_in_mixed_gls_qar']),
                                'minimum_misplaced_by_any_gl_mapping_qar': Decimal(v['minimum_misplaced_by_any_gl_mapping_qar']),
                                'minimum_misplaced_pct': v['minimum_misplaced_pct']})
        ws2 = _sheet(wb, 'Why_not_GL', gl_rows, {'breakdown': 50})
        ws2.append([])
        ws2.append(['Reading', 'For every GL, a GL mapping can put its whole balance in only one cell. Even choosing the best cell for every GL leaves the '
                               '"minimum misplaced" balance in the wrong cell. Figures are lower bounds computed from the 30 Sep 2026 loan and deposit files.'])
        ws2.append(['Trial balance', ev['accounts']['TRIAL_BALANCE_ATTRIBUTES']['note']])
        for r in ev['cells']['by_requirement']:
            ws2.append([f'BO cells needing {r["requirement"]}', f'{r["cells"]} cells ({r["share_of_cells_pct"]}%), {r["nonzero_cells"]} nonzero - {r["meaning"]}'])
        ws2.append(['QCB rules', ev['qcb_rules']['note']])
    _sheet(wb, 'Review_queue', [r for r in rows if r['mapping_status'] == 'UNRESOLVED' or r['review_flags']],
           {'description': 45, 'evidence': 80, 'review_flags': 40}, amber=('stakeholder_comment', 'stakeholder_decision'))
    _sheet(wb, 'Data_requests', [{'topic': a, 'request': b, 'current_treatment': c} for a, b, c in rr.DATA_REQUESTS + EXTRA_REQUESTS],
           {'request': 100, 'current_treatment': 60}, wrap=True)
    hist = tm.history(p.config)
    by_ver = Counter((h['version'], h['actor'], h['reason']) for h in hist)
    _sheet(wb, 'Change_history', [{'version': v, 'actor': a, 'reason': r, 'targets_changed': n} for (v, a, r), n in sorted(by_ver.items())], {'reason': 90})
    wb.save(xl)
    # Machine-readable copies
    (out_dir / f'NBS_Mapping_Specification_{stamp}.json').write_text(json.dumps({
        'mapping_version': doc['version'], 'mapping_sha256': mapping_sha, 'exported': date.today().isoformat(), 'run_id': run_id,
        'targets': doc['targets'], 'population_rules': {k: rules[k] for k in {x for t in doc['targets'].values() for x in
                                                                               ([t.get('legacy_rule_id')] + (t.get('legacy_rule_ids') or []) + [t.get('suggested_legacy_rule_id')]) if x and x in rules}},
        'hierarchy_predicates': hier, 'measure_catalogue': catalogue}, indent=1, default=str), encoding='utf-8')
    with open(out_dir / f'NBS_Mapping_Specification_{stamp}.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("'" + v if isinstance(v, str) and v[:1] in ('=', '+', '-', '@') else v) for k, v in r.items()})
    return {'xlsx': str(xl), 'targets': len(rows), 'mapping_version': doc['version'], 'run_id': run_id, 'verification': verify(xl, rows)}


EXTRA_REQUESTS = [
    ('SIC dictionary', 'The Ethix Sic_Code dictionary (code -> QCB economic sub-sector, e.g. Governments / Regional Governments / Social Insurance Funds), '
                       'customer nationality (Qatari / non-Qatari) and segment definitions (Small Business, Consumers).', 'Drafts that cannot separate sibling items are withheld'),
    ('Loan product crosswalk', 'Mapping of loan account types (RCM, MUR, IJR, IST, CLM, SYN, TWM, ...) to QCB product lines (Overdraft, Loans and advances, Islamic finance types).',
     'Product-level rows rely on unreviewed draft selectors'),
    ('Form changes', 'Confirmation of QCB form changes where BO labels differ from the legacy layout (e.g. "Consumers" vs "Personal Against Salary"; new "Small Business", "Others *", GCC country sections in Table 044).',
     'Kept UNRESOLVED with the suggested legacy row'),
]


def verify(xl, rows):
    from openpyxl import load_workbook
    wb = load_workbook(xl, read_only=True)
    ws = wb['Mapping']
    data = list(ws.iter_rows(values_only=True))
    hdr = list(data[0])
    ids = [r[hdr.index('target_id')] for r in data[1:]]
    problems = []
    if ids != [r['target_id'] for r in rows]:
        problems.append('Mapping sheet target order/identity differs from the engine export')
    errs = sum(1 for sh in wb.worksheets for row in sh.iter_rows(values_only=True) for v in row if isinstance(v, str) and v.startswith('#') and v[1:4].isupper())
    wb.close()
    return {'targets_in_sheet': len(ids), 'problems': problems, 'error_like_cells': errs, 'status': 'PASS' if not problems else 'FAIL'}
