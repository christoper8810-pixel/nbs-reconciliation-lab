"""Rebuild orchestration: setup, versioned runs, controls, reconciliation, coverage and export."""
from __future__ import annotations
import csv
import hashlib
import json
import secrets
import shutil
import sqlite3
from collections import defaultdict
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from . import bo_reference, categ_data, legacy_gl, policies, qcb_validations as qcb, rebuild_compare as cmp, rebuild_engine as eng, target_mappings as tm
from .bank_data import load_manifest
from .generation import rebuild_settings
from .money import POLICY as MONEY_POLICY, from_micro, text as micro_text
from .rebuild_store import connect, open_bank_readonly, sha256, sources as list_sources, now

REVIEW = Path('exports/rebuild_review_20261017')
DEFAULT_INPUTS = {}  # no machine-specific paths: inputs come from config/source_files.json or the inputs folder (see sources.py)
EXPECTED_SHA = {'categ': 'a9dc0021a2cd9551802129fbb2277161178b971c38cbede07d93824d9a2f6ac1',
                'bo': 'ad30f4607a615e7d671143ee1244e6eb179b6e53ffb429e397d76ab0cb607ebf'}

DATA_REQUESTS = [
    ('P&L completeness', 'Complete September or required YTD category/consolidated P&L data and the documented opening/movement/closing equation (CONSOLIDATE.PRFT.LOSS BALANCE / DEBIT.MOVEMENT / CREDIT.MOVEMENT / BALANCE.YTD overlap).', 'Tables 400/500 and P&L-dependent cells stay unavailable/partial'),
    ('Event grain', 'Source subentry/multivalue sequence for repeated category IDs (1,440 IDs; 24,515 identical exported observations, -60,216,695.11 LCY sensitivity) and the accounting role of the 2,335 DC postings (+8.869bn LCY) and 51008 charge-off events.', 'Duplicate treatment remains UNRESOLVED_RETAIN_ALL'),
    ('Unheaded column', 'Definition of unheaded column U (SDB-CHARGE / DEBIT-INTEREST / LOAN-ACCOUNT) and the complete PL CONSOL.KEY token dictionary (tokens 5-12).', 'Field kept as UNHEADED_U; no business meaning assigned'),
    ('BO derivation', 'Source query/procedure or transformation behind the BO NBS item aggregates, including manual adjustments. The financial BS SQL alone is insufficient.', 'BO kept as comparison reference only'),
    ('Legacy SQL semantics', 'Meaning of *_bal_Begin at bdate and the missing Crystal total formulas (16 literal-zero lines).', 'Legacy model totals are LEGACY_LITERAL_ZERO_NOT_CERTIFIED'),
    ('Presentation basis', 'Confirmed reporting unit, geography/sector/country basis and gross/net NBS presentation (e.g. intangibles gross 896,109 vs net 292,410).', 'Unit recorded as QAR thousands (assumed); gross/net differences stay visible'),
    ('Maturity convention', 'Actual Ethix maturity boundary logic (calendar months vs fixed day counts) and the list of products that are genuinely open-ended.', 'Convention is a named provisional setting; no product treated as open-ended'),
    ('Loan components', 'T24 loan-fee definition and the missing owner components NABACCOUNT, NABDEFERREDPFT, RECPRINCIPALPFT, DEFERREDPFT.', 'Carrying amounts that use Ethix fees are labelled HYBRID'),
    ('Absent feeds', 'Treasury, collateral, indirect-risk, guarantee/commitment, acquisition (Table-020) and other feed definitions.', 'Affected tables unavailable, never zero-filled'),
]


class Paths:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.config = self.root / 'config'
        self.data = self.root / 'data' / 'rebuild'
        self.store = self.data / 'rebuild_store.sqlite'
        self.runs = self.data / 'runs'
        self.bank = self.root / 'data' / 'bank_20260930.sqlite'
        self.catalogue = self.config / 'bo_measure_catalogue.json'
        self.rules = self.config / 'generation_rules.json'
        self.review = self.root / REVIEW


def discover_inputs(root):
    """Inputs placed in <app>/inputs (portable install) take precedence over the original machine's Downloads paths."""
    inp = Path(root) / 'inputs'
    found = {}
    if inp.exists():
        categ = sorted(str(x) for x in inp.glob('*Categ*Entry*.xlsx'))
        bo = sorted(str(x) for x in inp.glob('BO_QCB_NBS*.xlsx'))
        live = sorted(str(x) for x in inp.glob('NBS01*.xlsx'))
        if categ:
            found['categ'] = categ
        if bo:
            found['bo'] = bo[0]
        if live:
            found['live'] = live[0]
    return found


def setup(root, categ_paths=None, bo_path=None, live_path=None, log=print, qcb_paths=None):
    from . import sources as src
    p = Paths(root)
    first = lambda kind: (src.resolved(root, kind) or [None])[0]
    categ_paths = categ_paths or [str(x) for x in src.resolved(root, 'CATEG_ENTRY')]
    bo_path = bo_path or first('BO')
    live_path = live_path or first('LIVE')
    qcb_paths = qcb_paths or [str(x) for x in src.resolved(root, 'QCB_RULES')]
    gl_path = first('GL_MAPPING')
    p.runs.mkdir(parents=True, exist_ok=True)
    out = {'hashes': {}}
    with closing(connect(p.store)) as c:
        for path in categ_paths or []:
            if path and Path(path).exists():
                log(f'Importing category events {Path(path).name}')
                r = categ_data.import_categ(c, path)
                out['hashes'][str(path)] = r['source_sha256']
                out.setdefault('categ', []).append({'path': str(path), 'sha256': r['source_sha256'], 'already_imported': r['already_imported'], 'rows': r['rows']})
        if bo_path and Path(bo_path).exists():
            log('Importing BO reference')
            catalogue = bo_reference.build_catalogue(bo_path, p.catalogue)
            r = bo_reference.import_bo(c, bo_path, catalogue)
            out['bo'] = {k: r[k] for k in ('ref_version', 'source_sha256', 'standard_item_rows', 'special_records', 'already_imported') if k in r}
        if live_path and Path(live_path).exists():
            out['live'] = bo_reference.import_live_reference(c, live_path)
        policies.ensure_basis_policy(p.config, p.review / 'reporting_basis_owner_confirmation.json')
        policies.ensure_duplicate_policy(p.config)
        settings = p.config / 'rebuild_settings.json'
        if not settings.exists():
            settings.write_text(json.dumps(rebuild_settings(), indent=1) + '\n', encoding='utf-8')
        if 'bo' in out:
            tm.ensure(p.config, c, out['bo']['ref_version'], p.review / 'bo_to_current_mapping_candidates.csv', json.loads(p.catalogue.read_text(encoding='utf-8')))
        if gl_path:
            from . import gl_mapping
            log('Importing GL mapping workbook')
            r = gl_mapping.import_gl_mapping(c, gl_path)
            out['gl_mapping'] = {k: r.get(k) for k in ('gl_lines', 'categories', 'sectors', 'gl_accounts', 'already_imported')}
        if qcb_paths:
            log('Importing QCB validation rules')
            r = qcb.import_rules(c, qcb_paths)
            out['qcb'] = {'rules': r['rules'], 'parse_errors': len(r['parse_errors']), 'files': len(qcb_paths)}
    return out


def enhance_mappings(root, actor='system', log=print):
    """Upgrade system-drafted targets from the structural code crosswalk and QCB validation rules.
    Owner-edited targets are never changed. Writes one new mapping version."""
    from . import crosswalk
    p = Paths(root)
    catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
    rules = json.loads(p.rules.read_text(encoding='utf-8'))['rules']
    with closing(connect(p.store)) as c:
        ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()[0]
        bo = {}
        for t, i, d in c.execute('SELECT table_code, item_code, description FROM bo_items WHERE ref_version=?', (ref,)):
            bo.setdefault(t, {})[i] = d
        qrules = qcb.stored_rules(c)
    links, prefixes = crosswalk.structural_crosswalk(rules, bo)
    original = tm.load(p.config)
    work = json.loads(json.dumps(original))
    # 1. structural crosswalk, 2. withhold non-distinct selectors, 3. QCB-derived definitions; saved once as the net change.
    work['targets'].update(tm.reset_derived(work))
    work['targets'].update(tm.upgrade_from_evidence(work, links, [], rules, catalogue))
    hier = run_settings(p).get('hierarchy_predicates')
    withheld = 0
    for tid, why in tm.non_distinct_selectors(work, rules, hier).items():
        t = work['targets'][tid]
        if tm.is_system(t):
            work['targets'][tid] = dict(t, status='UNRESOLVED', method='NONE', suggested_legacy_rule_id=t['legacy_rule_id'], legacy_rule_id=None,
                                        candidate_basis='SELECTOR_NOT_DISTINCT', author='system: selector distinctness check',
                                        evidence=f'Draft rule {t["legacy_rule_id"]} cannot separate this item: {why}. Needs the SIC/sub-sector or product definition.')
            withheld += 1
    work['targets'].update(tm.upgrade_from_evidence(work, {}, qrules, rules, catalogue))
    with closing(connect(p.store)) as c:
        bo_values = bo_reference.reference_values(c, ref)
    subtotals = tm.propose_subtotals(work, rules, catalogue, bo_values)
    log(f'Hierarchy subtotals proposed: {len(subtotals)}')
    changed = {}
    for tid, t in work['targets'].items():
        old = original['targets'][tid]
        strip = lambda x: {k: v for k, v in x.items() if k not in ('author', 'reason', 'changed_at')}
        if strip(t) != strip(old):
            changed[tid] = t
    doc, n = original, 0
    if changed:
        by_author = {}
        for tid, t in changed.items():
            by_author.setdefault(t.get('author', 'system'), {})[tid] = {k: v for k, v in t.items() if k not in ('reason', 'changed_at')}
        merged = {}
        for a, ups in by_author.items():
            merged.update(ups)
        doc, n = tm.save_batch(p.config, merged, 'system: evidence-based drafting',
                               'Structural code crosswalk, selector distinctness check and QCB validation identities; unreviewed drafts', catalogue)
    total = n
    log(f'Targets changed: {n} (withheld for non-distinct selectors: {withheld})')
    (p.data / 'crosswalk_prefixes.json').write_text(json.dumps(prefixes, indent=1), encoding='utf-8')
    with open(p.data / 'structural_crosswalk.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['bo_item_code', 'bo_description', 'legacy_rule_id', 'legacy_row', 'legacy_path', 'text_score', 'basis'])
        for code, ms in sorted(links.items()):
            for m in ms:
                w.writerow([code, bo[code.split('-')[1]][code], m['rule_id'], m['row'], m['path'], m['text_score'], m['basis']])
    return {'updated_targets': total, 'structural_links': len(links), 'mapping_version': doc['version']}


def qcb_validation_rows(qrules, results, catalogue, bo_values, label_generated='generated'):
    """Every QCB rule evaluated on the BO reference and on generated values, side by side."""
    by_construction = {ref['rule_id'] for r in results.values() if r['target']['method'] == 'QCB_COMPOSITION'
                       for ref in r['target'].get('qcb_composition', {}).values()}
    by_construction |= {r['target'].get('qcb_rule_id') for r in results.values() if r['target']['method'] == 'QCB_POPULATION'}
    tables = set(catalogue['tables'])
    ref_vals = {k: Decimal(v) / Decimal(10 ** 6) for k, v in bo_values.items() if v is not None}
    gen_vals = {}
    for tid, r in results.items():
        t = r['target']
        for h, cell in r['cells'].items():
            m = catalogue['tables'][t['table']]['measures'][h]
            gen_vals[(t['table'], t['item_code'], h)] = cmp.display(cell['value'], m['kind'])
    ref_lookup = qcb.lookup_factory(ref_vals, catalogue, tables)
    gen_lookup = qcb.lookup_factory(gen_vals, catalogue, tables)
    out = []
    for r in qrules:
        a = qcb.check(r, ref_lookup)
        b = qcb.check(r, gen_lookup)
        out.append({'rule_id': r['rule_id'], 'qcb_code': r['qcb_code'], 'kind': r['kind'], 'description': r['description'],
                    'left': r['left'], 'operator': r['operator'], 'right': r['right'], 'repaired_syntax': r['repaired'],
                    'source_files': '; '.join(sorted({x['file'] for x in r['provenance']})),
                    'bo_status': a['status'], 'bo_left': a['left'], 'bo_right': a['right'], 'bo_difference': a['difference'], 'bo_reason': a['reason'],
                    'generated_status': 'PASS_BY_CONSTRUCTION' if r['rule_id'] in by_construction and b['status'].startswith('PASS') else b['status'],
                    'generated_left': b['left'], 'generated_right': b['right'], 'generated_difference': b['difference'], 'generated_reason': b['reason']})
    return out


def qcb_summary(rows):
    s = {'rules': len(rows), 'bo': defaultdict(int), 'generated': defaultdict(int), 'bo_by_kind': defaultdict(lambda: defaultdict(int)),
         'generated_by_kind': defaultdict(lambda: defaultdict(int))}
    for r in rows:
        s['bo'][r['bo_status']] += 1
        s['generated'][r['generated_status']] += 1
        s['bo_by_kind'][r['kind']][r['bo_status']] += 1
        s['generated_by_kind'][r['kind']][r['generated_status']] += 1
    return json.loads(json.dumps(s))


def run_settings(p):
    s = rebuild_settings()
    hp = p.config / 'hierarchy_predicates.json'
    s['hierarchy_predicates'] = json.loads(hp.read_text(encoding='utf-8')) if hp.exists() else None
    cc = p.config / 'component_corrections.json'
    s['component_corrections'] = json.loads(cc.read_text(encoding='utf-8')) if cc.exists() else None
    return s


def _file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).exists() else None


def current_inputs_fingerprint(p, categ_sha, bo_ref):
    return {'mapping_sha256': _file_hash(p.config / tm.MAPPING_FILE), 'rules_sha256': _file_hash(p.rules),
            'basis_policy_sha256': _file_hash(p.config / policies.BASIS_FILE), 'duplicate_policy_sha256': _file_hash(p.config / policies.DUPLICATE_FILE),
            'catalogue_sha256': _file_hash(p.catalogue), 'settings_sha256': _file_hash(p.config / 'rebuild_settings.json'),
            'product_policies_sha256': _file_hash(p.config / 'report_product_policies.json'),
            'balance_rules_sha256': _file_hash(p.config / 'balance_rules.json'), 'hierarchy_sha256': _file_hash(p.config / 'hierarchy_predicates.json'), 'component_corrections_sha256': _file_hash(p.config / 'component_corrections.json'),
            'categ_source': categ_sha, 'bo_reference': bo_ref}


class FactCache:
    """Prepared per-account stock facts, kept in-process for previews (read-only bank connection)."""
    _cache = {}

    @classmethod
    def get(cls, p, report_date):
        key = (str(p.bank), p.bank.stat().st_mtime if p.bank.exists() else None, report_date,
               _file_hash(p.config / 'report_product_policies.json'), _file_hash(p.config / 'balance_rules.json'))
        if key not in cls._cache:
            cls._cache.clear()
            bank = open_bank_readonly(p.bank, shared=True)
            manifest = load_manifest(p.bank)
            product = json.loads((p.config / 'report_product_policies.json').read_text(encoding='utf-8'))
            balance = json.loads((p.config / 'balance_rules.json').read_text(encoding='utf-8'))
            cls._cache[key] = eng.FactSource(bank, balance, manifest, report_date, product)
        return cls._cache[key]


def resolve_categ(c, p, categ_sha, report_date):
    basis_doc = json.loads((p.config / policies.BASIS_FILE).read_text(encoding='utf-8'))
    booking = [r[0] for r in c.execute('SELECT DISTINCT booking_date FROM categ_events WHERE source_sha256=?', (categ_sha,))]
    processing = [r[0] for r in c.execute('SELECT DISTINCT processing_date FROM categ_events WHERE source_sha256=?', (categ_sha,))]
    return policies.resolve_effective_date(basis_doc, categ_data.DATASET, categ_sha, booking, processing, report_date), basis_doc


def run(root, report_date='2026-09-30', categ_sha=None, bo_ref=None, live_ref='LIVE_NBS01_2026-09', actor='owner',
        label='', log=print, with_stock=True, export_excel=True):
    p = Paths(root)
    date.fromisoformat(report_date)
    with closing(connect(p.store)) as c:
        srcs = list_sources(c)
        if categ_sha is None:
            cs = [s for s in srcs if s['dataset'] == 'CATEG_ENTRY']
            categ_sha = cs[-1]['source_sha256'] if cs else None
        if bo_ref is None:
            r = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()
            bo_ref = r[0] if r else None
        basis = None
        if categ_sha:
            basis, basis_doc = resolve_categ(c, p, categ_sha, report_date)
        settings = run_settings(p)
        catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
        mappings = tm.load(p.config)
        rules = json.loads(p.rules.read_text(encoding='utf-8'))
        dup_doc = json.loads((p.config / policies.DUPLICATE_FILE).read_text(encoding='utf-8'))
        weights = policies.row_weights(c, categ_sha, dup_doc) if categ_sha else {}
        run_id = date.today().strftime('%Y%m%d') + '-' + secrets.token_hex(4)
        out = p.runs / run_id
        out.mkdir(parents=True)
        snap = out / 'snapshots'
        snap.mkdir()
        for f in (tm.MAPPING_FILE, policies.BASIS_FILE, policies.DUPLICATE_FILE, 'bo_measure_catalogue.json', 'rebuild_settings.json',
                  'generation_rules.json', 'report_product_policies.json', 'balance_rules.json', 'hierarchy_predicates.json', 'component_corrections.json'):
            if (p.config / f).exists():
                shutil.copy2(p.config / f, snap / f)
        log('Preparing stock facts (read-only bank database)')
        facts = FactCache.get(p, report_date) if with_stock and p.bank.exists() else None
        log('Calculating targets')
        qrules = qcb.stored_rules(c)
        results, contributions = eng.generate_targets(mappings, catalogue, facts, rules, c, categ_sha, weights, report_date, settings, qcb_rules=qrules)
        log('Comparing with reference versions')
        bo_values = bo_reference.reference_values(c, bo_ref) if bo_ref else {}
        qrows = qcb_validation_rows(qrules, results, catalogue, bo_values) if qrules else []
        bo_rows = cmp.compare_bo(results, catalogue, bo_values, bo_ref)
        live = {(r, col): v for r, col, v in c.execute('SELECT row_no, col, value_micro FROM live_cells WHERE ref_version=?', (live_ref,))}
        live_rows = cmp.compare_live(results, rules, live, live_ref)
        controls = build_controls(c, p, categ_sha, weights, contributions, mappings, bo_ref, facts, dup_doc)
        if facts and bo_values:
            controls['maturity_convention_sensitivity'] = maturity_sensitivity(results, mappings, catalogue, facts, rules, c, report_date, settings, bo_values)
        manifest = {
            'run_id': run_id, 'label': label, 'created_at': now(), 'actor': actor,
            'period': {'report_date': report_date, 'period_start': report_date[:8] + '01', 'period_end': report_date,
                       'as_of_convention': 'Point-in-time stocks at report date close; category events at owner-confirmed effective date',
                       'flows': 'Monthly/YTD P&L completeness NOT established'},
            'monetary_unit': 'QAR; generated money stored in 1e-6 units, displayed in QAR thousands; counts are counts',
            'money_policy': MONEY_POLICY, 'tolerance': cmp.TOLERANCE_NOTE,
            'sources': [s for s in srcs if s['source_sha256'] in {categ_sha, _ref_sha(c, bo_ref), _ref_sha(c, live_ref)}],
            'bank_database': {'path': str(p.bank), 'sha256_recorded': None, 'opened': 'read-only (mode=ro)'},
            'category_reporting_basis': basis, 'reference_versions': {'bo': bo_ref, 'live': live_ref},
            'inputs': current_inputs_fingerprint(p, categ_sha, bo_ref), 'mapping_version': mappings['version'],
            'duplicate_policy_version': dup_doc['version'], 'settings': settings,
            'statuses': _status_counts(results), 'stock_facts_checks': facts.checks if facts else None,
            'qcb_validations': qcb_summary(qrows) if qrows else None,
        }
        if qrows:
            _csv(out / 'qcb_validation_results.csv', qrows)
        _write_run(out, manifest, results, contributions, bo_rows, live_rows, controls, catalogue, c, bo_ref, mappings)
        if export_excel:
            log('Writing Excel workbook')
            from .rebuild_excel import write_workbook, verify_workbook
            xl = out / f'NBS_Rebuild_{report_date}.xlsx'
            write_workbook(xl, manifest, results, catalogue, bo_rows, live_rows, controls, c, bo_ref)
            manifest['excel'] = {'file': xl.name, 'verification': verify_workbook(xl, results, catalogue, c, bo_ref)}
            (out / 'manifest.json').write_text(json.dumps(manifest, indent=1, default=str), encoding='utf-8')
        (p.runs / 'latest.json').write_text(json.dumps({'run_id': run_id}), encoding='utf-8')
        return manifest


def _ref_sha(c, ref):
    r = c.execute('SELECT source_sha256 FROM ref_versions WHERE ref_version=?', (ref,)).fetchone()
    return r[0] if r else None


def _status_counts(results):
    out = defaultdict(int)
    for r in results.values():
        for cell in r['cells'].values():
            out[cell['status']] += 1
    return dict(out)


def build_controls(c, p, categ_sha, weights, contributions, mappings, bo_ref, facts, dup_doc):
    ctl = {}
    if categ_sha:
        ctl['category_source'] = categ_data.source_controls(c, categ_sha)
        groups = categ_data.repeated_groups(c, categ_sha)
        by_state = defaultdict(lambda: [0, 0])
        for (row_no, amt) in c.execute('SELECT row_no, amount_micro FROM categ_events WHERE source_sha256=?', (categ_sha,)):
            w, state = weights[row_no]
            by_state[state][0] += 1
            by_state[state][1] += amt
        ctl['duplicates'] = {
            'policy_version': dup_doc['version'], 'default_treatment': dup_doc['default_treatment'],
            'decisions': len(dup_doc.get('decisions', {})), 'repeated_groups': len(groups),
            'excess_observations': sum(g['excess'] for g in groups),
            'excess_signed_lcy': micro_text(sum(g['excess_micro'] for g in groups)),
            'rows_by_state': {k: {'rows': v[0], 'lcy': micro_text(v[1])} for k, v in by_state.items()},
            'sensitivity_if_count_once_lcy': micro_text(-sum(g['excess_micro'] for g in groups)),
        }
        if p.bank.exists():
            with closing(open_bank_readonly(p.bank)) as bank:
                ctl['category_account_links'] = categ_data.account_links(c, categ_sha, bank)
        ctl['category_reconciliation'] = reconcile_categ(c, categ_sha, weights, contributions, mappings)
    if facts:
        ctl['stock_population'] = reconcile_stock(facts)
    parts = eng.partition_diagnostics(mappings, contributions)
    ctl['partition_diagnostics'] = {'parents_with_findings': len(parts),
                                    'parents_with_overlap': sum(1 for x in parts if x['overlap_records']),
                                    'parents_with_uncovered_population': sum(1 for x in parts if x['uncovered_parent_records']),
                                    'items': [dict(x, overlap_amount_qar=micro_text(x.pop('overlap_amount_micro')),
                                                   uncovered_amount_qar=micro_text(x.pop('uncovered_amount_micro'))) for x in parts[:300]]}
    if bo_ref:
        ctl['reference_controls'] = reference_controls(c, bo_ref)
    if p.bank.exists() and (p.review / 'balance_sheet_case_rules.csv').exists():
        ctl['legacy_gl_reference_model'] = legacy_reference(p)
    return ctl


def maturity_sensitivity(results, mappings, catalogue, facts, rules, c, report_date, settings, bo_values):
    """Recalculate maturity targets under each named convention and show the BO difference for each."""
    ids = {tid for tid, r in results.items() if r['layout'] in ('maturity_loan', 'maturity_deposit')}
    sub = {'targets': {k: mappings['targets'][k] for k in ids}}
    out = {'targets': len(ids), 'current_convention': settings['maturity_convention'], 'by_convention': {}}
    for conv in ('DAY_COUNT', 'CALENDAR', 'CALENDAR_EOM'):
        res, _ = eng.generate_targets(sub, catalogue, facts, rules, c, None, {}, report_date, dict(settings, maturity_convention=conv))
        rows = [r for r in cmp.compare_bo(res, catalogue, bo_values, None) if r['difference'] is not None]
        out['by_convention'][conv] = {'compared_cells': len(rows), 'abs_difference_thousands': str(sum(abs(r['difference']) for r in rows)),
                                      'within_tolerance': sum(r['category'] in ('WITHIN_TOLERANCE', 'ROUNDING') for r in rows)}
    out['note'] = 'Boundary convention is provisional; if both conventions differ similarly, population/measure (not boundaries) drives the gap'
    return out


def reconcile_categ(c, categ_sha, weights, contributions, mappings):
    """Every source row lands in exactly one of: contributed / excluded / unmapped. Totals from the raw layer."""
    raw = Decimal(categ_data.source_controls(c, categ_sha)['net_lcy'])
    used = set()
    for tid, rows in contributions.items():
        if mappings['targets'][tid]['method'] == 'CATEG_EVENTS':
            used.update(r[0] for r in rows if r[5])
    parts = defaultdict(int)
    n = defaultdict(int)
    for row_no, amt in c.execute('SELECT row_no, amount_micro FROM categ_events WHERE source_sha256=?', (categ_sha,)):
        w, state = weights[row_no]
        k = 'excluded_duplicate_export' if not w else 'contributed' if row_no in used else 'unmapped_or_unresolved'
        parts[k] += amt
        n[k] += 1
    return reconcile(raw, parts, n, 'CATEG_ENTRY whole-source net LCY (raw text) = contributed + excluded + unmapped/unresolved')


def reconcile(total, parts, counts, label):
    total_parts = sum(Decimal(v) / Decimal(10 ** 6) for v in parts.values())
    diff = total - total_parts
    return {'control': label, 'source_total': str(total), 'parts': {k: {'rows': counts.get(k), 'amount': micro_text(v)} for k, v in parts.items()},
            'parts_total': str(total_parts), 'difference': str(diff),
            'status': 'PASS' if abs(diff) < Decimal('0.000001') * max(1, sum(counts.values())) else 'FAIL_POPULATION_DROPPED_OR_ADDED'}


def reconcile_stock(facts):
    c = facts.c
    c.execute('CREATE INDEX IF NOT EXISTS temp.facts_source_account ON facts(source, account)')
    out = {}
    for src, kind in (('LOAN', 'ECB_LOAN'), ('DEPOSIT', 'ECB_DEPOSIT')):
        total = c.execute('SELECT count(*), sum(amount) FROM unique_records WHERE source=?', (src,)).fetchone()
        joined = c.execute(f"SELECT count(*), sum(m.amount) FROM unique_records m WHERE m.source=? AND EXISTS (SELECT 1 FROM facts f WHERE f.source=? AND f.account=m.account)", (src, kind)).fetchone()
        unavailable = c.execute('SELECT count(*) FROM facts WHERE source=? AND unavailable=1', (kind,)).fetchone()[0]
        dup = c.execute('SELECT count(*) FROM records WHERE source=?', (src,)).fetchone()[0] - total[0]
        out[src] = {'detail_unique_accounts': total[0], 'detail_amount_ethix_qar': repr(total[1]),
                    'joined_to_ecb_accounts': joined[0], 'joined_amount_ethix_qar': repr(joined[1]),
                    'not_joined_accounts': total[0] - joined[0], 'not_joined_amount_ethix_qar': repr((total[1] or 0) - (joined[1] or 0)),
                    'duplicate_key_rows_excluded_from_joins': dup, 'facts_flagged_unavailable': unavailable,
                    'status': 'PASS' if joined[0] <= total[0] else 'FAIL_FANOUT'}
    out['fanout_check'] = {'facts_rows_per_account_max': c.execute(
        "SELECT max(n) FROM (SELECT count(*) n FROM facts WHERE source IN ('ECB_LOAN','ECB_DEPOSIT') GROUP BY source, account, currency)").fetchone()[0]}
    return out


def reference_controls(c, ref):
    v = bo_reference.reference_values(c, ref)
    g = lambda t, i, m: Decimal(v[(t, i, m)]) / 10 ** 6 if v.get((t, i, m)) is not None else None
    items18 = c.execute("SELECT item_code, description, parent_code FROM bo_items WHERE ref_version=? AND table_code='018'", (ref,)).fetchall()
    if not items18:
        return {'note': 'Table-018 not present in this reference version'}
    top = [i for i, d, par in items18 if par is None]
    gross = sum(g('018', i, 'Orig Cost In Qatar') + g('018', i, 'Orig Cost Out Qatar') for i in top)
    amort = sum(g('018', i, 'Amor Impair In Qatar') + g('018', i, 'Amor Impair Out Qatar') for i in top)
    others = [i for i, d, par in items18 if d.strip().lower() == 'others' and par is None]
    kids = {o: [i for i, d, par in items18 if par == o] for o in others}
    t100_intang = c.execute("SELECT item_code FROM bo_items WHERE ref_version=? AND table_code='100' AND lower(description) LIKE '%intangible%' ORDER BY length(item_code) LIMIT 1", (ref,)).fetchone()
    out = {'intangibles_gross_net': {'table_018_top_level_gross': str(gross), 'signed_amortization': str(amort), 'net': str(gross + amort),
                                     'table_100_cell_E50': str(g('100', t100_intang[0], 'In Lc Amount')) if t100_intang else None,
                                     'note': 'BO Table-100 shows gross; earlier live report shows net 292,410. Both retained; no plug.'},
           'others_parent_children': {o: {'parent_gross': str(g('018', o, 'Orig Cost In Qatar')),
                                          'children': kids[o],
                                          'children_gross': str(sum(g('018', k, 'Orig Cost In Qatar') for k in kids[o])),
                                          'rule': 'Parent already contains children; parent+children summation is rejected'} for o in others}}
    roots = {}
    for t in ('100', '200'):
        root = c.execute('SELECT item_code FROM bo_items WHERE ref_version=? AND table_code=? ORDER BY row_no LIMIT 1', (ref, t)).fetchone()
        if root:
            roots[t] = (root[0], sum(g(t, root[0], m) or 0 for m in ('In Lc Amount', 'In Fc Amount', 'Out Lc Amount', 'Out Fc Amount')))
    if len(roots) == 2:
        out['assets_vs_liabilities_capital'] = {'table_100_root': roots['100'][0], 'assets': str(roots['100'][1]), 'table_200_root': roots['200'][0],
                                            'liabilities_capital': str(roots['200'][1]), 'difference': str(roots['100'][1] - roots['200'][1]),
                                            'treatment': 'Source control difference for investigation; never a balancing entry'}
    out['note'] = 'Reference-only controls; generated values are not adjusted to these'
    return out


def legacy_reference(p):
    rules = legacy_gl.load_rules(p.review / 'balance_sheet_case_rules.csv')
    outputs = legacy_gl.load_outputs(p.review / 'balance_sheet_output_lines.csv')
    with closing(open_bank_readonly(p.bank)) as bank:
        rows = [{'ledger': gl or '', 'account': acc or '', 'amount': Decimal(repr(a))} for acc, gl, a in
                bank.execute("SELECT account, gl, amount FROM unique_records WHERE source='TB' AND amount IS NOT NULL")]
    res = legacy_gl.run(rules, outputs, rows)
    return {'note': res['note'] + '. Applied to the Ethix trial balance (Equiv Cur Bal) as a proxy for Tbl_GL_Daily_Bo; *_bal_Begin semantics unknown.',
            'lines': [{'line': x['line'], 'description': x['description'], 'groups': x['groups'], 'status': x['status'],
                       'value_thousands': None if x['value'] is None else str(x['value'])} for x in res['lines']],
            'omitted_groups': {str(g): {'rows': v['rows'], 'amount_thousands': str(v['amount_thousands'])} for g, v in res['omitted_groups'].items()},
            'omitted_nonzero_groups': sorted(res['omitted_nonzero'])}


def coverage_rows(c, bo_ref, results, catalogue, bo_rows):
    comp = {(r['target_id'], r['measure']): r for r in bo_rows}
    out = []
    for tid, r in sorted(results.items()):
        t = r['target']
        for h, m in catalogue['tables'].get(t['table'], {}).get('measures', {}).items():
            cell = r['cells'].get(h, {})
            x = comp.get((tid, h), {})
            out.append({'target_id': tid, 'table': t['table'], 'item_code': t['item_code'], 'description': t['description'],
                        'measure': h, 'semantic': m['semantic'], 'kind': m['kind'], 'unit': m['unit'], 'primary': m.get('primary', True),
                        'mapping_status': t['status'], 'method': t['method'], 'legacy_rule_id': t.get('legacy_rule_id'),
                        'cell_status': cell.get('status'), 'source_kind': cell.get('source_kind'),
                        'generated': x.get('generated'), 'bo_reference': x.get('reference'), 'difference': x.get('difference'),
                        'category': x.get('category'), 'issues': ' | '.join(dict.fromkeys(cell.get('issues', [])))})
        if t['item_code'] == 'SPECIAL':
            out.append({'target_id': tid, 'table': t['table'], 'item_code': 'SPECIAL', 'description': t['description'],
                        'measure': 'Acquistion No / Provision Amount / Net Value', 'semantic': 'SPECIAL_SCHEMA', 'kind': 'special',
                        'unit': None, 'primary': True, 'mapping_status': t['status'], 'method': t['method'], 'legacy_rule_id': None,
                        'cell_status': 'UNAVAILABLE', 'source_kind': None, 'generated': None, 'bo_reference': 'record of zeros',
                        'difference': None, 'category': 'MISSING_FEED_OR_MAPPING', 'issues': 'Acquisition feed not supplied'})
    return out


def _csv(path, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else ['empty'])
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: ("'" + v if isinstance(v, str) and v[:1] in ('=', '+', '-', '@') else v) for k, v in r.items()})


def _write_run(out, manifest, results, contributions, bo_rows, live_rows, controls, catalogue, c, bo_ref, mappings):
    db = sqlite3.connect(out / 'run.sqlite')
    db.executescript("""CREATE TABLE cells(target_id TEXT, measure TEXT, value_micro INTEGER, status TEXT, source_kind TEXT, issues TEXT,
                        PRIMARY KEY(target_id, measure));
                        CREATE TABLE contributions(target_id TEXT, fact_id INTEGER, source TEXT, record TEXT, semantic TEXT,
                        amount_micro INTEGER, included INTEGER, reason TEXT);
                        CREATE TABLE results(target_id TEXT PRIMARY KEY, layout TEXT, semantic TEXT, issues TEXT, mapping TEXT);""")
    for tid, r in results.items():
        db.execute('INSERT INTO results VALUES(?,?,?,?,?)', (tid, r['layout'], json.dumps(r['semantic']), json.dumps(r['issues']), json.dumps(r['target'])))
        for h, cell in r['cells'].items():
            db.execute('INSERT INTO cells VALUES(?,?,?,?,?,?)', (tid, h, cell['value'], cell['status'], cell.get('source_kind'), json.dumps(cell['issues'])))
    for tid, rows in contributions.items():
        db.executemany('INSERT INTO contributions VALUES(?,?,?,?,?,?,?,?)', [(tid,) + tuple(x) for x in rows])
    db.execute('CREATE INDEX contrib_t ON contributions(target_id, semantic)')
    db.commit()
    db.close()
    _csv(out / 'comparison_bo.csv', bo_rows)
    _csv(out / 'comparison_live.csv', live_rows)
    cov = coverage_rows(c, bo_ref, results, catalogue, bo_rows)
    _csv(out / 'coverage_register.csv', cov)
    _csv(out / 'data_requests.csv', [{'topic': a, 'request': b, 'current_treatment': x} for a, b, x in DATA_REQUESTS])
    _csv(out / 'review_queue.csv', [{'target_id': tid, 'table': t['table'], 'item_code': t['item_code'], 'description': t['description'],
                                      'status': t['status'], 'candidates': '|'.join(t['candidate_ids']), 'evidence': t['evidence']}
                                     for tid, t in mappings['targets'].items() if t['status'] in ('UNRESOLVED', 'DRAFT_CANDIDATE')])
    summary = {'bo': cmp.materiality(bo_rows), 'live': cmp.materiality([dict(r, primary=True, kind='money') for r in live_rows]),
               'coverage': _coverage_summary(cov)}
    manifest['summary'] = summary
    (out / 'controls.json').write_text(json.dumps(controls, indent=1, default=str), encoding='utf-8')
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1, default=str), encoding='utf-8')


def _coverage_summary(cov):
    by_table = defaultdict(lambda: defaultdict(int))
    for r in cov:
        by_table[r['table']][r['cell_status'] or 'NONE'] += 1
    return {t: dict(v) for t, v in sorted(by_table.items())}


def preview_target(root, tid, proposed, report_date='2026-09-30'):
    """Old vs new values for one target under a proposed (unsaved) mapping."""
    p = Paths(root)
    catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
    tm.validate_target(proposed, catalogue)
    mappings = tm.load(p.config)
    rules = json.loads(p.rules.read_text(encoding='utf-8'))
    with closing(connect(p.store)) as c:
        cs = [s for s in list_sources(c) if s['dataset'] == 'CATEG_ENTRY']
        categ_sha = cs[-1]['source_sha256'] if cs else None
        dup_doc = json.loads((p.config / policies.DUPLICATE_FILE).read_text(encoding='utf-8'))
        weights = policies.row_weights(c, categ_sha, dup_doc) if categ_sha else {}
        needs_stock = any(x['method'] in ('LEGACY_RULE', 'QCB_POPULATION', 'SOURCE_RULE') for x in (mappings['targets'][tid], proposed))
        facts = FactCache.get(p, report_date) if needs_stock and p.bank.exists() else None
        settings = run_settings(p)
        old, _ = eng.generate_targets(mappings, catalogue, facts, rules, c, categ_sha, weights, report_date, settings, only={tid})
        alt = dict(mappings, targets=dict(mappings['targets'], **{tid: proposed}))
        new, contrib = eng.generate_targets(alt, catalogue, facts, rules, c, categ_sha, weights, report_date, settings, only={tid})
    rows = []
    for h in catalogue['tables'][proposed['table']]['measures']:
        o, n = old[tid]['cells'][h], new[tid]['cells'][h]
        kind = catalogue['tables'][proposed['table']]['measures'][h]['kind']
        rows.append({'measure': h, 'old': cmp.display(o['value'], kind), 'old_status': o['status'],
                     'new': cmp.display(n['value'], kind), 'new_status': n['status']})
    return {'rows': rows, 'matched_records': len(contrib.get(tid, [])),
            'included_records': sum(1 for x in contrib.get(tid, []) if x[5]), 'issues': new[tid]['issues']}


def latest_run(root):
    p = Paths(root)
    f = p.runs / 'latest.json'
    if not f.exists():
        return None
    rid = json.loads(f.read_text())['run_id']
    return json.loads((p.runs / rid / 'manifest.json').read_text(encoding='utf-8'))


def stale_reasons(root, manifest):
    if not manifest:
        return []
    p = Paths(root)
    now_ = current_inputs_fingerprint(p, manifest['inputs']['categ_source'], manifest['inputs']['bo_reference'])
    return [k for k, v in now_.items() if manifest['inputs'].get(k) != v]


def gl_evidence_file(root):
    """Compute and store the GL-mapping evidence (data/rebuild/gl_evidence.json) from the read-only bank files."""
    from . import gl_evidence
    p = Paths(root)
    catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
    with closing(connect(p.store)) as c:
        ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()[0]
        ev = gl_evidence.build(p.bank, catalogue, c, ref, qcb.stored_rules(c), legacy_gl.load_rules(p.review / 'balance_sheet_case_rules.csv'))
    (p.data / 'gl_evidence.json').write_text(json.dumps(ev, indent=1, default=list), encoding='utf-8')
    summary = {src: {k: f"{v['minimum_misplaced_pct']}% (QAR {v['minimum_misplaced_by_any_gl_mapping_qar']})" for k, v in ev['accounts'][src]['by_breakdown'].items()}
               for src in ('LOAN', 'DEPOSIT')}
    return {'evidence': ev, 'summary': summary}
