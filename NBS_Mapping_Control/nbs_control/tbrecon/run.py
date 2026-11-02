"""Run orchestration, input discovery, reproducibility check and persistent run / rule versioning."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sqlite3
from decimal import Decimal
from pathlib import Path

from . import ENGINE_VERSION, controls, engine_a, engine_b, engine_c, rootcause, tb
from .keys import layouts
from .tables import TableError, read_table, require

INPUT_KINDS = {
    'legacy_tb': (['LEGACY_GL', 'CURRENCY', 'BALANCE'], 'Legacy cut-off trial balance (source of expected balances)'),
    'actual_tb': (['TARGET_GL', 'CURRENCY', 'BALANCE'], 'Temenos actual TB (pre-COB or correctly dated)'),
    'gl_mapping': (['LEGACY_GL', 'TARGET_GL'], 'Authorised legacy GL -> target GL(s) mapping'),
    'asset_balances': (['CONSOL_KEY'], 'Engine A: PRODUCT_S3 asset-type balances (<TYPE>_BAL_QAR columns)'),
    'gl_rules': (['RULE_ID', 'TARGET_GL', 'BALANCE_TYPE'], 'Engine A: GL allocation rules, GL Report H/D/T layout'),
    'internal_balances': (['ACCOUNT_NO', 'CURRENCY', 'BALANCE'], 'Engine B: INTERNAL_CUS_ACC source balances'),
    'internal_mapping': (['ACCOUNT_NO'], 'Engine B: one-to-one internal account mapping'),
    'customer_account_mapping': (['ACCOUNT_NO'], 'Engine B: authoritative customer account mapping (Nostro / Vostro refs)'),
    'target_accounts': (['TARGET_ACCOUNT', 'BALANCE'], 'Engine B: actual Temenos target-account balances (optional)'),
    'pl_balances': (['BALANCE'], 'Engine C: PL source balances (PL CONSOL_KEY and / or explicit PL dimensions)'),
    'pl_rules': (['RULE_ID', 'TARGET_GL'], 'Engine C: PL mapping rules'),
    'post_cob_movements': (['TARGET_GL', 'CURRENCY', 'BALANCE', 'BUSINESS_DATE'], 'Validated post-COB Transact movements'),
    'benchmark': (['TARGET_GL', 'CURRENCY', 'BALANCE'], 'Independent benchmark, e.g. TrialBalance_withConsolKey.csv (never a source)'),
}
BENCHMARK_NAMES = ('trialbalance_withconsolkey',)
DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / 'config' / 'tb_recon.json'


def load_config(path=None):
    return json.loads(Path(path or DEFAULT_CONFIG).read_text(encoding='utf-8'))


def discover(folder):
    """Find inputs in a folder by conventional names (<kind>.csv|xlsx) or a manifest.json {kind: path}."""
    folder = Path(folder)
    if not folder.is_dir():
        raise TableError(f'Input folder not found: {folder}')
    found = {}
    man = folder / 'manifest.json'
    if man.exists():
        for k, p in json.loads(man.read_text(encoding='utf-8')).items():
            if k in INPUT_KINDS and p:
                found[k] = (folder / p) if not Path(p).is_absolute() else Path(p)
    for f in sorted(folder.iterdir()):
        stem = f.stem.lower()
        if f.suffix.lower() not in ('.csv', '.xlsx', '.xlsm'):
            continue
        if stem in INPUT_KINDS and stem not in found:
            found[stem] = f
        elif stem in BENCHMARK_NAMES and 'benchmark' not in found:
            found['benchmark'] = f
    return found


def load_inputs(paths):
    data, metas = {}, {}
    for kind, (cols, _desc) in INPUT_KINDS.items():
        p = paths.get(kind)
        if not p:
            data[kind], metas[kind] = None, None
            continue
        rows, meta = read_table(p)
        require(meta, kind, cols)
        if kind in ('internal_mapping', 'customer_account_mapping') and not ({'TARGET_ACCOUNT', 'TARGET_GL'} & set(meta['headers'])):
            raise TableError(f'{kind} needs TARGET_ACCOUNT and / or TARGET_GL')
        if kind == 'pl_balances' and not ({'CONSOL_KEY', 'PL_CATEGORY'} & set(meta['headers'])):
            raise TableError('pl_balances needs CONSOL_KEY (PL layout) or explicit PL_CATEGORY')
        data[kind], metas[kind] = rows, meta
    return data, metas


def _canon(o):
    if isinstance(o, Decimal):
        return str(o.normalize()) if o != 0 else '0'
    if isinstance(o, dict):
        return {str(k): _canon(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_canon(x) for x in (sorted(o) if isinstance(o, set) else o)]
    return o


def digest(o):
    return hashlib.sha256(json.dumps(_canon(o), sort_keys=True, separators=(',', ':'), default=str).encode()).hexdigest()


def execute(data, metas, cfg, legacy=False):
    """Pure computation (no persistence)."""
    lay = layouts(cfg)
    tol = tb.tolerance(cfg)
    engines = {
        'A': engine_a.run(data['asset_balances'], metas['asset_balances'], data['gl_rules'], metas['gl_rules'], cfg, lay['AC'], legacy=legacy),
        'B': engine_b.run(data['internal_balances'], metas['internal_balances'], data['internal_mapping'],
                          data['customer_account_mapping'], data['target_accounts'], cfg),
        'C': engine_c.run(data['pl_balances'], metas['pl_balances'], data['pl_rules'], metas['pl_rules'], cfg, lay['PL']),
    }
    recon = tb.reconstruct(data, engines, cfg)
    comp_exc = rootcause.classify_components(engines)
    gl_exc = rootcause.classify_gl(recon, tol, engines)
    exceptions = recon['exceptions'] + comp_exc + gl_exc
    for i, e in enumerate(exceptions, 1):
        e['exception_id'] = f'EX{i:06d}'
        e.setdefault('engine', 'TB')
    ctrls = controls.build(engines, recon, exceptions, cfg, tol)
    issues = rootcause.systemic(exceptions)
    work = rootcause.worklist(engines, recon, exceptions)
    result_hash = digest({'gl': recon['gl_rows'], 'exc': exceptions, 'work': work,
                          'contrib': engines['A'].get('contributions') or []})
    return {'engines': engines, 'recon': recon, 'exceptions': exceptions, 'controls': ctrls, 'issues': issues,
            'worklist': work, 'result_hash': result_hash, 'legacy_semantics': legacy}


def statistics(res):
    """Headline statistics used for BEFORE / AFTER comparisons."""
    A = res['engines']['A']
    gl = res['recon']['gl_rows']
    stat = {s: 0 for s in ('RECONCILED', 'DIFFERENCE', 'EXPECTED_ONLY', 'ACTUAL_ONLY', 'INCOMPLETE', 'SOURCE_PENDING')}
    for r in gl:
        stat[r['recon_status']] = stat.get(r['recon_status'], 0) + 1
    unmatched = sum((abs(c['amount']) for e in res['engines'].values() for c in e.get('components') or [] if c['status'] != 'MAPPED'),
                    Decimal(0)) + sum((abs(u['amount']) for u in res['recon']['unallocated'] if not u.get('engine')), Decimal(0))
    return {
        'gl_lines': len(gl), **{f'gl_{k.lower()}': v for k, v in stat.items()},
        'unresolved_gl_lines': sum(v for k, v in stat.items() if k != 'RECONCILED'),
        'net_difference': sum((r['difference'] for r in gl), Decimal(0)),
        'absolute_difference': sum((r['abs_difference'] for r in gl), Decimal(0)),
        'unmatched_balance_abs': unmatched,
        'components_total': sum(len(e.get('components') or []) for e in res['engines'].values()),
        'components_unmapped': sum(1 for e in res['engines'].values() for c in e.get('components') or [] if c['status'] != 'MAPPED'),
        'ambiguous_allocations': sum(1 for e in res['engines'].values() for c in e.get('components') or [] if c['status'] == 'AMBIGUOUS'),
        'multi_target_unresolved': sum(1 for e in res['engines'].values() for c in e.get('components') or []
                                       if c['status'] == 'MULTI_TARGET_UNRESOLVED') +
        sum(1 for u in res['recon']['unallocated'] if u['status'] == 'MULTI_TARGET_UNRESOLVED' and not u.get('engine')),
        'unsupported_balance_types': len(A.get('unsupported_balance_types') or []),
        'misalignment_findings': len(A.get('misalignment') or []),
        'exceptions': len(res['exceptions']),
        'systemic_issues': len([i for i in res['issues'] if not i['informational']]),
        'controls_failed': [c['id'] for c in res['controls'] if c['status'] == 'FAIL'],
    }


def top_exceptions(res, n=20):
    rows = [e for e in res['exceptions'] if e['amount'] is not None and not e.get('informational')]
    rows.sort(key=lambda e: (-abs(e['amount']), e['exception_id']))
    return rows[:n]


# ---------------------------------------------------------------- persistence
SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, created TEXT, label TEXT, engine_version TEXT, input_hashes TEXT,
  config_hash TEXT, rules_hash TEXT, result_hash TEXT, reproducible TEXT, summary TEXT, folder TEXT, legacy_semantics INTEGER);
CREATE TABLE IF NOT EXISTS rule_versions(content_hash TEXT PRIMARY KEY, kind TEXT, file_name TEXT, first_seen TEXT, rows INTEGER, content TEXT);
CREATE TABLE IF NOT EXISTS run_rules(run_id TEXT, kind TEXT, content_hash TEXT);
"""
RULE_KINDS = ('gl_rules', 'pl_rules', 'gl_mapping', 'internal_mapping', 'customer_account_mapping')


def index_db(data_root):
    p = Path(data_root) / 'tbrecon' / 'runs.sqlite'
    p.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(p)
    c.executescript(SCHEMA)
    return c


def run_and_store(paths, data_root, export_root, label='', cfg_path=None, legacy=False, rule_overrides=None,
                  reproducibility_limit=300_000, progress=None):
    cfg = load_config(cfg_path)
    data, metas = load_inputs(paths)
    if rule_overrides:
        for k, rows in rule_overrides.items():
            data[k] = rows
            extra = sorted({h for r in rows for h in r if not h.startswith('_')} - set(metas[k]['headers']))
            metas[k] = {**metas[k], 'headers': metas[k]['headers'] + extra, 'overridden': True}
    progress and progress('computing')
    res = execute(data, metas, cfg, legacy=legacy)
    input_hashes = {k: {'sha256': m['sha256'], 'name': m['name'], 'rows': m['rows'], 'overridden': bool(m.get('overridden'))}
                    for k, m in metas.items() if m}
    config_hash = digest(cfg)
    rule_hashes = {k: digest([{kk: v for kk, v in r.items()} for r in data[k]]) for k in RULE_KINDS if data.get(k) is not None}
    rules_hash = digest(rule_hashes)
    total_rows = sum(m['rows'] for m in metas.values() if m)
    c = index_db(data_root)
    try:
        prev = c.execute('SELECT run_id, result_hash FROM runs WHERE input_hashes=? AND config_hash=? AND rules_hash=? AND engine_version=? '
                         'AND legacy_semantics=? ORDER BY created DESC LIMIT 1',
                         (json.dumps(input_hashes, sort_keys=True), config_hash, rules_hash, ENGINE_VERSION, int(legacy))).fetchone()
        if prev:
            repro = {'status': 'PASS' if prev[1] == res['result_hash'] else 'FAIL', 'compared_with': prev[0]}
        elif total_rows <= reproducibility_limit:
            progress and progress('reproducibility re-run')
            again = execute(*load_inputs(paths), cfg, legacy=legacy) if not rule_overrides else execute(data, metas, cfg, legacy=legacy)
            repro = {'status': 'PASS' if again['result_hash'] == res['result_hash'] else 'FAIL', 'compared_with': 'in-process re-run'}
        else:
            repro = {'status': 'NOT_TESTED', 'compared_with': f'first run with these inputs ({total_rows} rows > limit)'}
        res['controls'].append({'id': 'C10', 'control': 'Reproducibility between identical runs',
                                'status': 'PASS' if repro['status'] == 'PASS' else 'FAIL' if repro['status'] == 'FAIL' else 'INCOMPLETE',
                                'detail': f'Result hash {res["result_hash"][:16]}... compared with {repro["compared_with"]}: {repro["status"]}',
                                'values': repro})
        res['controls'].sort(key=lambda x: x['id'])
        now = dt.datetime.now()
        run_id = now.strftime('%Y%m%d-%H%M%S-') + f'{now.microsecond // 1000:03d}' + res['result_hash'][:5]
        folder = Path(export_root) / run_id
        folder.mkdir(parents=True, exist_ok=True)
        res['meta'] = {'run_id': run_id, 'created': now.isoformat(timespec='milliseconds'), 'label': label, 'engine_version': ENGINE_VERSION,
                       'inputs': input_hashes, 'missing_inputs': sorted(k for k, m in metas.items() if not m),
                       'config_hash': config_hash, 'rules_hash': rules_hash, 'rule_hashes': rule_hashes,
                       'result_hash': res['result_hash'], 'reproducibility': repro, 'legacy_semantics': legacy,
                       'tolerance': res['recon']['tolerance'], 'config': cfg}
        res['statistics'] = statistics(res)
        progress and progress('writing exports')
        from . import report
        report.write_all(res, folder)
        for k in RULE_KINDS:
            if data.get(k) is None:
                continue
            h = rule_hashes[k]
            c.execute('INSERT OR IGNORE INTO rule_versions VALUES(?,?,?,?,?,?)',
                      (h, k, metas[k]['name'], now.isoformat(timespec='seconds'), len(data[k]), json.dumps(data[k], default=str)))
            c.execute('INSERT INTO run_rules VALUES(?,?,?)', (run_id, k, h))
        c.execute('INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                  (run_id, res['meta']['created'], label, ENGINE_VERSION, json.dumps(input_hashes, sort_keys=True), config_hash,
                   rules_hash, res['result_hash'], repro['status'], json.dumps(_canon(res['statistics'])), str(folder), int(legacy)))
        c.commit()
    finally:
        c.close()
    return run_id, folder, res


def list_runs(data_root, limit=50):
    c = index_db(data_root)
    try:
        cols = ('run_id', 'created', 'label', 'engine_version', 'result_hash', 'reproducible', 'summary', 'folder', 'legacy_semantics', 'rules_hash')
        return [dict(zip(cols, r[:6] + (json.loads(r[6]),) + r[7:])) for r in
                c.execute(f'SELECT {", ".join(cols)} FROM runs ORDER BY created DESC, rowid DESC LIMIT ?', (limit,))]
    finally:
        c.close()


def get_run(data_root, run_id):
    return next((r for r in list_runs(data_root, 10_000) if r['run_id'] == run_id), None)
