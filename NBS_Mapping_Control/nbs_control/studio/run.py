"""Mapping Studio orchestration:
workbook -> rule compiler -> validation -> expected BO allocation -> BO reconciliation -> investigation -> proposals."""
from __future__ import annotations

import datetime as dt
import json
import secrets
import shutil
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from . import STUDIO_VERSION, bo as B, validate
from .compiler import compile_workbook
from .engine import Allocation, expected, totals
from .investigate import Investigation
from .workbook import Workbook

ZERO = Decimal(0)
DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / 'config' / 'studio.json'


def load_config(path=None):
    p = Path(path) if path else DEFAULT_CONFIG
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def _layout():
    try:
        from ..tbrecon.keys import layouts
        from ..tbrecon.run import load_config as tbcfg
        return layouts(tbcfg())['AC']
    except Exception:  # noqa: BLE001 - CONSOL_KEY decoding is optional
        return None


def jsonable(o):
    if isinstance(o, Decimal):
        return format(o, 'f')
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def analyse(workbook_path, bo_path=None, source_paths=(), cfg=None):
    cfg = cfg or load_config()
    tol = Decimal(str(cfg.get('tolerance', '0.01')))
    wb = Workbook(workbook_path)
    model = compile_workbook(wb, cfg)
    rules_snapshot = [{'rule': r.id, 'line': r.line, 'row': r.row, 'usable': r.usable, 'errors': r.errors,
                       'conditions': {d: {'text': r.raw.get(d, ''), 'compiled': c.describe(), 'cell': r.cells.get(d, ''),
                                          'formula': r.formulas.get(d)} for d, c in r.conds.items()},
                       'description': r.describe()} for r in model.rules]
    sigs, src = [], None
    if source_paths:
        from . import sources
        sigs, src = sources.load(source_paths, cfg, _layout())
    alloc = Allocation(model, sigs, cfg) if sigs else None
    val = validate.run(model, alloc, sigs)
    bo_rows, bo_meta, key_dims = None, None, ['currency'] if sigs and any(s.dims.get('currency') for s in sigs) else []
    if bo_path:
        bo_rows, bo_meta = B.load(bo_path)
        src_dims = {d for s in sigs for d in s.dims} if sigs else set()
        key_dims = B.grain(bo_meta, src_dims)
    E0, contrib = expected(alloc, key_dims) if alloc else ({}, {})
    alloc_status = {}
    if alloc:
        for s in sigs:
            alloc_status[s.id] = alloc.status(s)
    signatures = [{'id': s.id, 'dims': s.dims, 'amount': s.amount, 'records': s.count, 'accounts': s.accounts[:10], 'refs': s.refs[:10],
                   'path': s.path, 'status': alloc_status.get(s.id), 'lines': list(alloc.lines_of[s.id]) if alloc else [],
                   'rules': sorted(alloc.sig_rules.get(s.id, ())) if alloc else [], 'gl_rows': s.glrows} for s in sigs]
    proposals, residuals, recon_before, recon_after, presentation, bo_internal = list(val.proposals), [], [], [], {}, []
    A = {}
    if bo_rows is not None:
        A, rows_of, dups = B.actual(bo_rows, key_dims, Decimal(str(cfg.get('bo_amount_scale', 1))), Decimal(str(cfg.get('bo_sign', 1))))
        presentation = B.detect_scale_sign({k: v for k, v in E0.items()}, A, tol)
        recon_before = B.compare(model, totals(model, E0, key_dims), A, tol)
        bo_internal = _bo_totals(model, A, tol)
        if alloc:
            inv = Investigation(model, alloc, E0, A, key_dims, tol, cfg)
            found = inv.run(val.proposals if cfg.get('evaluate_validation_proposals', True) else (), cfg.get('max_iterations', 60))
            proposals = [p for p in val.proposals] + found
            residuals = inv.residuals(bo_meta, src or {}, dups, presentation)
            recon_after = B.compare(model, totals(model, dict(inv.E), key_dims), A, tol)
        else:
            residuals = [{'key': r['line'], 'line': r['line'], 'expected': None, 'actual': r['actual'], 'difference': None,
                          'category': 'NO_SOURCE_RECORDS', 'responsibility': 'UNDETERMINED', 'confidence': 'UNRESOLVED',
                          'evidence_needed': 'Supporting source records are needed to reconstruct the expected allocation'}
                         for r in recon_before if r['status'] != 'LINE_NOT_IN_MAPPING'] + \
                        [{'key': r['line'], 'line': r['line'], 'expected': None, 'actual': r['actual'], 'difference': None,
                          'category': 'LINE_NOT_IN_MAPPING', 'responsibility': 'MAPPING_OR_BO', 'confidence': 'MEDIUM',
                          'evidence_needed': f'BO line {r["line"]} is not defined in the workbook'} for r in recon_before
                         if r['status'] == 'LINE_NOT_IN_MAPPING']
    for i, p in enumerate(proposals, 1):
        p['id'] = f'P{i:04d}'
        p.setdefault('responsibility', 'MAPPING')
        p['finance_required'] = p['confidence'] != 'HIGH'
        p.setdefault('rule_ref', p.get('rule', '') or p.get('legacy_gl', ''))
        for e in p['edits']:
            e.setdefault('sheet', validate.parse_addr(e['cell'])[0])
            e.setdefault('row', validate.parse_addr(e['cell'])[1])
            e.setdefault('col', validate.parse_addr(e['cell'])[2])
    line_rules = {lid: [{'rule': rid, 'description': next(x['description'] for x in rules_snapshot if x['rule'] == rid),
                         'cells': next(x['conditions'] for x in rules_snapshot if x['rule'] == rid)} for rid in ln['rules']]
                  for lid, ln in model.lines.items()}
    result = {
        'version': STUDIO_VERSION, 'created': dt.datetime.now().isoformat(timespec='seconds'), 'config': cfg, 'tolerance': str(tol),
        'workbook': {'name': wb.path.name, 'sha256': wb.sha256, 'sheets': wb.sheetnames, 'roles': wb.roles,
                     'column_maps': {k: {'header_row': v['header_row'], 'columns': {f: c for f, c in v['columns'].items()},
                                         'evidence': v['evidence']} for k, v in model.column_maps.items()},
                     'defined_names': len(wb.defined_names)},
        'lines': [{k: v for k, v in ln.items()} for ln in model.lines.values()], 'line_rules': line_rules,
        'rules': rules_snapshot, 'named_ranges': model.named, 'gl_mapping_rows': len(model.glmap),
        'reference': {'categories': len(model.categories), 'sectors': len(model.sectors), 'coa': len(model.coa),
                      'refsets': {k: {'codes': len(v[0]), 'where': v[1]} for k, v in model.refsets.items()}},
        'source': src, 'bo': bo_meta, 'key_dims': key_dims, 'signatures': signatures,
        'contributions': {' | '.join(map(str, k)): ids for k, ids in contrib.items()},
        'validation': val.items, 'proposals': proposals, 'residuals': residuals, 'presentation': presentation,
        'bo_internal_totals': bo_internal, 'recon_before': recon_before, 'recon_after': recon_after,
    }
    result['root_causes'] = root_causes(result)
    result['summary'] = summary(result)
    return result


def _bo_totals(model, A, tol):
    """BO internal consistency: each BO total line against the sum of its BO member lines."""
    out = []
    rest = {k[1:] for k in A}
    for lid, ln in model.lines.items():
        if ln['type'] != 'T' or not ln.get('total_members'):
            continue
        for rk in rest:
            k = (lid,) + rk
            if k not in A:
                continue
            s = sum((A.get((m,) + rk, ZERO) for m in ln['total_members']), ZERO)
            if abs(A[k] - s) > tol:
                out.append({'line': lid, 'key': ' / '.join(x for x in k if x), 'bo_total': A[k], 'bo_members_sum': s,
                            'difference': A[k] - s, 'members': ln['total_members'], 'basis': ln.get('total_basis'),
                            'responsibility': 'BO_REPORT', 'category': 'BO_TOTAL_NOT_SUM_OF_DETAILS'})
    return out


def root_causes(res):
    out = []
    for p in res['proposals']:
        out.append({'root_cause': p['reason'], 'type': p['kind'], 'cells': ', '.join(e['cell'] for e in p['edits']), 'proposal': p['id'],
                    'records': p.get('affected_records', 0), 'financial_impact': p.get('financial_impact'), 'lines': list((p.get('lines') or {}).keys()),
                    'responsibility': p.get('responsibility', 'MAPPING'), 'confidence': p['confidence']})
    grp = defaultdict(lambda: {'count': 0, 'amount': ZERO, 'keys': []})
    for r in res['residuals']:
        g = grp[(r['category'], r['responsibility'], r['confidence'])]
        g['count'] += 1
        g['amount'] += abs(r['difference'] or ZERO)
        g['keys'].append(r['key'])
    for (cat, resp, conf), g in grp.items():
        out.append({'root_cause': f'{cat} on {g["count"]} report key(s)', 'type': cat, 'cells': '', 'proposal': '', 'records': g['count'],
                    'financial_impact': g['amount'], 'lines': g['keys'][:20], 'responsibility': resp, 'confidence': conf})
    vg = defaultdict(lambda: {'count': 0, 'cells': []})
    for v in res['validation']:
        if v['severity'] == 'ERROR':
            g = vg[(v['check'], v['classification'])]
            g['count'] += 1
            g['cells'].append(v['cell'])
    for (check, cls), g in vg.items():
        out.append({'root_cause': f'{check}: {g["count"]} finding(s)', 'type': check, 'cells': ', '.join(c for c in g['cells'][:10] if c),
                    'proposal': '', 'records': g['count'], 'financial_impact': None, 'lines': [],
                    'responsibility': 'MAPPING' if cls == 'MAPPING_DEFECT' else cls, 'confidence': 'HIGH'})
    out.sort(key=lambda x: -abs(Decimal(str(x['financial_impact'] or 0))))
    for i, x in enumerate(out, 1):
        x['id'] = f'RC{i:03d}'
    return out


def summary(res):
    by_status = defaultdict(int)
    for s in res['signatures']:
        by_status[s['status']] += 1
    alloc_amt = defaultdict(lambda: ZERO)
    for s in res['signatures']:
        alloc_amt[s['status']] += abs(s['amount'])
    total_abs = sum(alloc_amt.values(), ZERO)
    rb = res['recon_before']
    ra = res['recon_after']
    conf = defaultdict(int)
    for p in res['proposals']:
        conf[p['confidence']] += 1
    sev = defaultdict(int)
    for v in res['validation']:
        sev[v['severity']] += 1
    return {
        'lines': len(res['lines']), 'detail_lines': sum(1 for l in res['lines'] if l['type'] == 'D'),
        'rules': len(res['rules']), 'rules_not_executable': sum(1 for r in res['rules'] if not r['usable']),
        'conditions': sum(len(r['conditions']) for r in res['rules']), 'gl_mapping_rows': res['gl_mapping_rows'],
        'validation': dict(sev), 'signatures': len(res['signatures']), 'source_records': (res['source'] or {}).get('records', 0),
        'allocation_status': dict(by_status),
        'allocated_share': (alloc_amt.get('ALLOCATED', ZERO) / total_abs) if total_abs else None,
        'bo_keys': len(rb), 'bo_matched_before': sum(1 for r in rb if r['status'] == 'MATCHED'),
        'bo_open_before': sum(1 for r in rb if r['status'] != 'MATCHED'),
        'bo_abs_difference_before': sum((abs(r['difference']) for r in rb if r['line_type'] in ('D', '')), ZERO),
        'bo_matched_after_proposals': sum(1 for r in ra if r['status'] == 'MATCHED') if ra else None,
        'bo_abs_difference_after_proposals': sum((abs(r['difference']) for r in ra if r['line_type'] in ('D', '')), ZERO) if ra else None,
        'proposals': dict(conf), 'residuals': len(res['residuals']),
        'unresolved': sum(1 for r in res['residuals'] if r['confidence'] == 'UNRESOLVED'),
    }


# ------------------------------------------------------------------ stored projects / runs
def new_project(store, data_root, label, workbook, bo=None, sources=(), config=None):
    pid = dt.datetime.now().strftime('%Y%m%d-%H%M%S-') + secrets.token_hex(3)
    folder = Path(data_root) / 'studio' / 'projects' / pid
    (folder / 'uploads').mkdir(parents=True, exist_ok=True)
    files = {'workbook': _copy(workbook, folder), 'bo': _copy(bo, folder) if bo else None, 'sources': [_copy(s, folder) for s in sources]}
    store.add_project(pid, label, folder, files, config)
    return pid


def _copy(src, folder):
    src = Path(src)
    dst = folder / 'uploads' / src.name
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
    return str(dst)


def run_project(store, data_root, export_root, pid, workbook=None, kind='ANALYSIS', parent=None, progress=None):
    from . import exports
    prj = store.project(pid)
    cfg = {**load_config(), **(prj['config'] or {})}
    progress and progress('compiling and analysing')
    res = analyse(workbook or prj['files']['workbook'], prj['files']['bo'], prj['files']['sources'], cfg)
    rid = dt.datetime.now().strftime('%Y%m%d-%H%M%S-') + secrets.token_hex(3)
    folder = Path(export_root) / rid
    folder.mkdir(parents=True, exist_ok=True)
    res['run_id'], res['project'], res['kind'], res['parent'] = rid, pid, kind, parent
    res['workbook_path'] = str(workbook or prj['files']['workbook'])
    if parent:
        pr = store.run(parent)
        res['parent_summary'] = pr['summary'] if pr else None
    (folder / 'result.json').write_text(json.dumps(res, default=jsonable), encoding='utf-8')
    store.add_run(rid, pid, kind, parent, res['workbook']['sha256'], folder, res['summary'], res['proposals'])
    progress and progress('writing reports')
    exports.write_analysis(store, rid, folder, res)
    return rid, folder, res


def load_result(folder):
    return json.loads((Path(folder) / 'result.json').read_text(encoding='utf-8'))


def rerun(store, data_root, export_root, rid, progress=None):
    """Step 11: re-run the reconciliation on the corrected copy (same BO report and source records)."""
    r = store.run(rid)
    corrected = Path(r['folder']) / 'CORRECTED_MAPPING_PREVIEW.xlsx'
    if not corrected.exists():
        raise ValueError('Approve corrections and export the corrected mapping first')
    return run_project(store, data_root, export_root, r['project_id'], workbook=str(corrected), kind='RERUN', parent=rid, progress=progress)
