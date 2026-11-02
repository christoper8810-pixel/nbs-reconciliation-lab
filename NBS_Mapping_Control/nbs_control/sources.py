"""Source registry: which input file is used for each source type, on any computer.

Files live in <app>/inputs. The registry (config/source_files.json) records the chosen file per type with its hash,
who chose it and when. Nothing refers to the original laptop's Downloads folder. Imports run from the registry.
"""
from __future__ import annotations
import json
import shutil
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from .rebuild_store import connect, sha256

TYPES = {
    'ECB': {'label': 'ECB balances (asset type wise)', 'pattern': ['ECB*.xlsx'], 'group': 'account database',
            'what': 'T24 balance per account and balance type, CONSOL.KEY (category, sector, residence)'},
    'LOAN': {'label': 'All Loan', 'pattern': ['All Loan*.xlsx'], 'group': 'account database',
             'what': 'Loan attributes: residency, SIC, customer type, product, maturity, risk, RIM'},
    'DEPOSIT': {'label': 'All Deposit', 'pattern': ['All Deposit*.xlsx'], 'group': 'account database',
                'what': 'Deposit attributes: residency, SIC, customer type, product, maturity, RIM'},
    'TB': {'label': 'Trial balance (Ethix GL)', 'pattern': ['Historical_Trial_Balance*.xlsx', '*Trial*Balance*.xlsx'], 'group': 'account database',
           'what': 'Ethix GL balances by account and currency'},
    'GL_MAPPING': {'label': 'GL mapping workbook', 'pattern': ['GL mapping*.xlsx', 'GL_mapping*.xlsx'], 'group': 'reference',
                   'what': 'GL Report line criteria, T24 category and sector dictionaries, Ethix GL -> Transact mapping (migration reference)'},
    'CATEG_ENTRY': {'label': 'Category entries', 'pattern': ['*Categ*Entry*.xlsx'], 'group': 'events',
                    'what': 'T24 category accounting entries (PL category, product category, event type)'},
    'BO': {'label': 'BO QCB NBS report (reference)', 'pattern': ['BO_QCB_NBS*.xlsx'], 'group': 'reference',
           'what': 'Ethix BO NBS figures by QCB item code: comparison only, never a generation input'},
    'LIVE': {'label': 'Earlier live NBS report (reference)', 'pattern': ['NBS01*.xlsx'], 'group': 'reference',
             'what': 'Earlier live NBS01 report: comparison only'},
    'QCB_RULES': {'label': 'QCB validation-rule workbooks', 'pattern': ['*NBS active validations*.xlsx'], 'group': 'reference', 'multiple': True,
                  'what': 'QCB cross-table validation rules (checks and QCB-derived definitions)'},
}
REGISTRY = 'source_files.json'


def inputs_dir(root):
    d = Path(root) / 'inputs'
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_registry(root):
    p = Path(root) / 'config' / REGISTRY
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'schema_version': 1, 'files': {}}


def save_registry(root, reg):
    p = Path(root) / 'config' / REGISTRY
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(reg, indent=1), encoding='utf-8')
    tmp.replace(p)


def discover(root, kind):
    """Candidate files for a type in inputs/ (and data/qcb_validations for QCB rules)."""
    found = []
    dirs = [inputs_dir(root)] + ([Path(root) / 'data' / 'qcb_validations'] if kind == 'QCB_RULES' else [])
    for d in dirs:
        for pat in TYPES[kind]['pattern']:
            found += [x for x in d.glob(pat) if x.is_file() and not x.name.startswith('~$')]
    return sorted(set(found))


def register(root, kind, path, actor='owner'):
    """Record a file for a type. Files outside inputs/ are copied in first, so the app never depends on another folder."""
    if kind not in TYPES:
        raise ValueError('Unknown source type')
    path = Path(path)
    if not path.is_file():
        raise ValueError(f'File not found: {path}')
    if path.suffix.lower() != '.xlsx':
        raise ValueError('Choose an .xlsx workbook')
    inp = inputs_dir(root)
    target = path if path.resolve().parent in (inp.resolve(), (Path(root) / 'data' / 'qcb_validations').resolve()) else inp / path.name
    if target != path:
        shutil.copy2(path, target)
    reg = load_registry(root)
    entry = {'file': str(target.resolve().relative_to(Path(root).resolve())).replace('\\', '/'), 'sha256': sha256(target),
             'bytes': target.stat().st_size, 'chosen_by': actor, 'chosen_at': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    if TYPES[kind].get('multiple'):
        lst = [e for e in reg['files'].get(kind, []) if e['sha256'] != entry['sha256']]
        reg['files'][kind] = lst + [entry]
    else:
        reg['files'][kind] = entry
    save_registry(root, reg)
    return entry


def resolved(root, kind):
    """Registered file(s) for a type, else whatever is found in inputs/. Returns a list of absolute paths."""
    reg = load_registry(root).get('files', {}).get(kind)
    if reg:
        entries = reg if isinstance(reg, list) else [reg]
        paths = [Path(root) / e['file'] for e in entries]
        return [p for p in paths if p.exists()]
    found = discover(root, kind)
    return found if TYPES[kind].get('multiple') else found[:1]


def status(root):
    from .rebuild_run import Paths
    p = Paths(root)
    imported = {}
    if p.store.exists():
        with closing(connect(p.store)) as c:
            for sha, ds, at, summ in c.execute('SELECT source_sha256, dataset, imported_at, summary FROM sources'):
                imported[sha] = {'dataset': ds, 'imported_at': at, 'summary': json.loads(summ) if summ else {}}
    bank = {}
    if p.bank.exists():
        from .bank_data import load_manifest
        try:
            m = load_manifest(p.bank)
            bank = {k: v for k, v in m.items() if isinstance(v, dict) and 'sha256' in v}
        except Exception:  # an unreadable DB shows as not built
            bank = {}
    out = []
    for kind, meta in TYPES.items():
        files = resolved(root, kind)
        rows = []
        for f in files:
            digest = sha256(f)
            if meta['group'] == 'account database':
                b = bank.get(kind)
                state = ('IN ACCOUNT DATABASE' if b and b['sha256'] == digest else 'DATABASE BUILT FROM A DIFFERENT FILE' if b else 'NOT BUILT')
                info = f'{b["rows"]:,} rows' if b and b['sha256'] == digest else ''
            else:
                imp = imported.get(digest)
                state = 'IMPORTED' if imp else 'NOT IMPORTED'
                s = (imp or {}).get('summary') or {}
                info = ', '.join(f'{k} {v:,}' for k, v in s.items() if isinstance(v, int))[:160]
            rows.append({'file': f.name, 'path': str(f), 'sha256': digest, 'size_mb': round(f.stat().st_size / 2 ** 20, 1), 'state': state, 'info': info})
        out.append({'kind': kind, **meta, 'files': rows, 'candidates': [x.name for x in discover(root, kind)]})
    return out


def build_account_database(root, log=print):
    """(Re)build the account database from the registered ECB, LOAN, DEPOSIT and TB files; the previous one is kept as a backup."""
    from .bank_data import build_database
    from .rebuild_run import Paths, FactCache
    p = Paths(root)
    files = {k: resolved(root, k) for k in ('ECB', 'LOAN', 'DEPOSIT', 'TB')}
    missing = [k for k, v in files.items() if not v]
    if missing:
        raise ValueError('Choose these files first: ' + ', '.join(TYPES[k]['label'] for k in missing))
    tmp = p.bank.with_name('bank_building.sqlite')
    if tmp.exists():
        tmp.unlink()
    log('Building the account database (several minutes)')
    m = build_database(files['ECB'][0], {'LOAN': files['LOAN'][0], 'DEPOSIT': files['DEPOSIT'][0], 'TB': files['TB'][0]}, tmp)
    if p.bank.exists():
        p.bank.replace(p.bank.with_name('bank_20260930.' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.bak.sqlite'))
    tmp.replace(p.bank)
    FactCache._cache.clear()
    return {k: v.get('rows') for k, v in m.items() if isinstance(v, dict) and 'rows' in v}


def import_references(root, kinds=None, log=print):
    """Import category entries, BO, live NBS, GL mapping and QCB rules from the registry."""
    from . import bo_reference, categ_data, gl_mapping, qcb_validations as qcb, policies, target_mappings as tm
    from .rebuild_run import Paths, rebuild_settings
    p = Paths(root)
    kinds = kinds or ['CATEG_ENTRY', 'BO', 'LIVE', 'GL_MAPPING', 'QCB_RULES']
    out = {}
    p.runs.mkdir(parents=True, exist_ok=True)
    with closing(connect(p.store)) as c:
        for kind in kinds:
            files = resolved(root, kind)
            if not files:
                out[kind] = 'no file chosen'
                continue
            log(f'Importing {TYPES[kind]["label"]}')
            if kind == 'CATEG_ENTRY':
                out[kind] = [categ_data.import_categ(c, f)['rows'] for f in files]
            elif kind == 'BO':
                cat = bo_reference.build_catalogue(files[0], p.catalogue)
                out[kind] = bo_reference.import_bo(c, files[0], cat).get('standard_item_rows')
            elif kind == 'LIVE':
                out[kind] = bo_reference.import_live_reference(c, files[0])
            elif kind == 'GL_MAPPING':
                r = gl_mapping.import_gl_mapping(c, files[0])
                out[kind] = {k: r.get(k) for k in ('gl_lines', 'categories', 'sectors', 'gl_accounts')}
            elif kind == 'QCB_RULES':
                out[kind] = qcb.import_rules(c, files)['rules']
        policies.ensure_basis_policy(p.config, p.review / 'reporting_basis_owner_confirmation.json')
        policies.ensure_duplicate_policy(p.config)
        if not (p.config / 'rebuild_settings.json').exists():
            (p.config / 'rebuild_settings.json').write_text(json.dumps(rebuild_settings(), indent=1) + '\n', encoding='utf-8')
        ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()
        if ref and p.catalogue.exists():
            tm.ensure(p.config, c, ref[0], p.review / 'bo_to_current_mapping_candidates.csv', json.loads(p.catalogue.read_text(encoding='utf-8')))
    return out
