"""Simple owner screens: Home, Load files, full NBS report, Balance types, Downloads."""
from __future__ import annotations
import csv
import json
import secrets
import threading
from collections import defaultdict
from contextlib import closing
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from flask import abort, flash, redirect, render_template, request, url_for, send_from_directory

from . import logic_text as lt, rebuild_run as rr, source_explorer as sx, sources as src, target_mappings as tm
from .rebuild_store import connect

BANK_KINDS = ('ECB', 'LOAN', 'DEPOSIT', 'TB')


def register_nbs_routes(app, root):
    p = rr.Paths(root)
    lock = threading.Lock()
    jobs = p.data / 'jobs'
    jobs.mkdir(parents=True, exist_ok=True)

    def start_job(fn):
        if not lock.acquire(blocking=False):
            raise ValueError('Another load or run is in progress; wait for it to finish')
        job = secrets.token_hex(6)
        f = jobs / (job + '.json')

        def state(phase, **kw):
            tmp = f.with_suffix('.tmp')
            tmp.write_text(json.dumps({'job': job, 'phase': phase, **kw}, default=str), encoding='utf-8')
            tmp.replace(f)
        state('Starting')

        def work():
            try:
                state('Complete', result=fn(lambda m: state(m)))
            except Exception as exc:
                state('Failed', error=f'{type(exc).__name__}: {exc}')
            finally:
                lock.release()
        threading.Thread(target=work, daemon=True).start()
        return job

    def latest_run_dir():
        m = rr.latest_run(root)
        return (p.runs / m['run_id'], m) if m else (None, None)

    @app.route('/nbs')
    def nbs_home():
        status = src.status(root)
        loaded = {s['kind']: bool(s['files']) and all(f['state'] in ('IMPORTED', 'IN ACCOUNT DATABASE') for f in s['files']) for s in status}
        d, m = latest_run_dir()
        return render_template('nbs_home.html', status=status, loaded=loaded, run=m, bank=p.bank.exists())

    @app.route('/nbs/load', methods=['GET', 'POST'])
    def nbs_load():
        if request.method == 'POST':
            try:
                chosen = []
                for kind in src.TYPES:
                    for up in request.files.getlist('file_' + kind):
                        if up and up.filename:
                            if not up.filename.lower().endswith('.xlsx'):
                                raise ValueError(f'{up.filename}: choose an .xlsx workbook')
                            dest = src.inputs_dir(root) / Path(up.filename).name
                            up.save(dest)
                            src.register(root, kind, dest, request.form.get('actor') or 'owner')
                            chosen.append(kind)
                    path = (request.form.get('path_' + kind) or '').strip().strip('"')
                    if path:
                        src.register(root, kind, path, request.form.get('actor') or 'owner')
                        chosen.append(kind)
                force = request.form.get('reload') == 'on'
                if not chosen and not force:
                    raise ValueError('Choose at least one file (or tick "reload everything")')
                bank_needed = force or any(k in BANK_KINDS for k in chosen) or not p.bank.exists()
                refs = [k for k in ('CATEG_ENTRY', 'BO', 'LIVE', 'GL_MAPPING', 'QCB_RULES') if force or k in chosen or not p.store.exists()]

                def work(log):
                    out = {}
                    if bank_needed and all(src.resolved(root, k) for k in BANK_KINDS):
                        out['account database'] = src.build_account_database(root, log)
                    elif bank_needed:
                        out['account database'] = 'waiting for: ' + ', '.join(src.TYPES[k]['label'] for k in BANK_KINDS if not src.resolved(root, k))
                    if refs:
                        out['references'] = src.import_references(root, refs, log)
                    return out
                job = start_job(work)
                return redirect(url_for('rebuild_job', job=job))
            except (ValueError, OSError) as exc:
                flash(str(exc), 'error')
                return redirect(url_for('nbs_load'))
        return render_template('nbs_load.html', status=src.status(root), types=src.TYPES, inputs=str(src.inputs_dir(root)))

    @app.route('/nbs/report')
    def nbs_report():
        catalogue = json.loads(p.catalogue.read_text(encoding='utf-8')) if p.catalogue.exists() else {'tables': {}}
        tables = sorted(catalogue['tables'])
        table = request.args.get('table') or (tables[0] if tables else '')
        compare = request.args.get('compare') == '1'
        d, m = latest_run_dir()
        doc = tm.load(p.config) if (p.config / tm.MAPPING_FILE).exists() else {'targets': {}}
        items = [t for t in doc['targets'].values() if t['table'] == table]
        with closing(connect(p.store)) as c:
            ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()
            order = {i: r for i, r in c.execute('SELECT item_code, row_no FROM bo_items WHERE ref_version=? AND table_code=?', (ref[0], table))} if ref else {}
        items.sort(key=lambda t: (order.get(t['item_code'], 10 ** 6), t['item_code']))
        values = defaultdict(dict)
        if d and (d / 'comparison_bo.csv').exists():
            for r in csv.DictReader(open(d / 'comparison_bo.csv', encoding='utf-8-sig')):
                if r['table'] == table:
                    values[r['target_id']][r['measure']] = r
        measures = catalogue['tables'].get(table, {}).get('measures', {})
        cols = [h for h, mm in measures.items() if mm.get('primary', True)] if request.args.get('all') != '1' else list(measures)
        ctx = lt.Context(root)
        rows = []
        for t in items:
            desc = lt.describe(t, ctx)
            depth = (len(t['item_code'].split('-')[-1]) - 1) // 2 if t['item_code'] != 'SPECIAL' else 0
            cells = []
            for h in cols:
                r = values[t['target_id']].get(h, {})
                cells.append({'gen': _num(r.get('generated')), 'bo': _num(r.get('reference')), 'diff': _num(r.get('difference')),
                              'kind': measures[h]['kind'], 'status':r.get('status','UNAVAILABLE')})
            rows.append({'t': t, 'depth': depth, 'cells': cells, 'logic': desc, 'types_text': lt.types_text(desc['types'])})
        return render_template('nbs_report.html', tables=tables, titles={k: v.get('title', '') for k, v in catalogue['tables'].items()},
                               table=table, cols=cols, rows=rows, compare=compare, run=m, show_all=request.args.get('all') == '1',
                               stale=rr.stale_reasons(root,m) if m else [])

    @app.route('/nbs/temenos')
    def nbs_temenos():
        from .temenos_review import REVIEW_DIR
        file=Path(root)/REVIEW_DIR/'NBS_Temenos_Mapping_Review.json'
        if not file.exists():
            return render_template('nbs_temenos.html', review=None, rows=[], tables=[], table='')
        review=json.loads(file.read_text(encoding='utf-8'))
        tables=sorted({r['table'] for r in review['mapping']})
        table=request.args.get('table') or '010'
        rows=[r for r in review['mapping'] if r['table']==table]
        return render_template('nbs_temenos.html',review=review,rows=rows,tables=tables,table=table)

    @app.route('/nbs/temenos/files/<name>')
    def nbs_temenos_file(name):
        from .temenos_review import REVIEW_DIR
        allowed={'NBS_Temenos_Presentation.html','NBS_Temenos_Mapping_for_21Oct2026.xlsx','NBS_Temenos_Mapping.csv'}
        if name not in allowed:
            abort(404)
        return send_from_directory((Path(root)/REVIEW_DIR).resolve(),name,as_attachment=name.endswith(('.xlsx','.csv')))

    @app.route('/nbs/balance-types', methods=['GET', 'POST'])
    def nbs_balance_types():
        bal_path = p.config / 'balance_rules.json'
        bal = json.loads(bal_path.read_text(encoding='utf-8'))
        if request.method == 'POST':
            try:
                actor, reason = request.form.get('actor', '').strip(), request.form.get('reason', '').strip()
                if not actor or not reason:
                    raise ValueError('Enter your name and a reason')
                new = json.loads(json.dumps(bal))
                for g in new['groups']:
                    new['groups'][g] = [x.strip().upper() for x in request.form.get('group_' + g, '').replace(',', ' ').split() if x.strip()]
                if new == bal:
                    raise ValueError('No change')
                hist = p.config / 'policy_history'
                hist.mkdir(exist_ok=True)
                (hist / f'balance-groups-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")}.json').write_text(
                    json.dumps({'at': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'actor': actor, 'reason': reason, 'before': bal['groups'], 'after': new['groups']}, indent=1), encoding='utf-8')
                tmp = bal_path.with_suffix('.tmp')
                tmp.write_text(json.dumps(new, indent=2) + '\n', encoding='utf-8')
                tmp.replace(bal_path)
                rr.FactCache._cache.clear()
                flash('Balance groups saved (previous version kept in config/policy_history). Generate a run to apply.', 'ok')
                return redirect(url_for('nbs_balance_types'))
            except ValueError as exc:
                flash(str(exc), 'error')
        try:
            rows, _ = sx.explore(root, 'ECB', 'balance_type', limit=500)
        except ValueError:
            rows = []
        ctx = lt.Context(root)
        doc = tm.load(p.config) if (p.config / tm.MAPPING_FILE).exists() else {'targets': {}}
        used = defaultdict(list)
        for t in doc['targets'].values():
            if t['method'] in ('LEGACY_RULE', 'QCB_POPULATION', 'SOURCE_RULE'):
                for b in lt.describe(t, ctx)['types']:
                    for x in b['types']:
                        used[x['type']].append(t)
        gl_use = _gl_usage(root)
        groups = {g: set(ts) for g, ts in bal['groups'].items()}
        listed = {r['value'] for r in rows}
        extra = sorted({t for ts in bal['groups'].values() for t in ts} - listed)
        out = []
        for r in rows + [{'value': t, 'records': 0, 'amount': None} for t in extra]:
            ty = r['value']
            out.append({'type': ty, 'records': r['records'], 'amount': r['amount'], 'in_extract': ty in listed,
                        'groups': [g for g, ts in groups.items() if ty in ts],
                        'policies': [k for k, v in ctx.policies.items() if ty in v.get('parent_coefficients', {}) or ty in v.get('linked_coefficients', {})],
                        'nbs_lines': len({x['target_id'] for x in used.get(ty, [])}), 'examples': sorted({x['target_id'] for x in used.get(ty, [])})[:4],
                        'gl_lines': gl_use.get(ty, [])})
        return render_template('nbs_balance_types.html', rows=out, groups=bal['groups'], measures=_measure_help(bal, ctx))

    @app.route('/nbs/downloads')
    def nbs_downloads():
        d, m = latest_run_dir()
        run_files = sorted(x.name for x in d.iterdir() if x.is_file() and x.suffix in ('.xlsx', '.csv', '.json')) if d else []
        spec_dir = p.root / 'exports' / 'mapping_specification'
        specs = sorted((x.name for x in spec_dir.glob('NBS_Mapping_Specification_*')), reverse=True)[:6] if spec_dir.exists() else []
        return render_template('nbs_downloads.html', run=m, run_files=run_files, specs=specs)


def _num(v):
    if v in (None, ''):
        return None
    try:
        return Decimal(v)
    except Exception:
        return None


def _gl_usage(root):
    """Balance type -> GL Report lines whose criteria use it (from the GL mapping workbook)."""
    from . import gl_mapping
    p = rr.Paths(root)
    out = defaultdict(list)
    if not p.store.exists():
        return out
    with closing(connect(p.store)) as c:
        sha = gl_mapping.latest(c)
        if not sha:
            return out
        named = gl_mapping.named_ranges(c, sha)
        for line, bal in c.execute('SELECT DISTINCT line, balance FROM gl_criteria WHERE source_sha256=? AND balance IS NOT NULL', (sha,)):
            types, _ = gl_mapping._balance_types(bal, named)
            for ty in types:
                if line not in out[ty]:
                    out[ty].append(line)
    return out


def _measure_help(bal, ctx):
    g = bal['groups']
    return [('Loan balance (outstanding)', 'minus the sum of the OUTSTANDING group'),
            ('Loan earned profit', 'minus the sum of the AMORTIZED_EARNED group'),
            ('Loan carrying amount', 'outstanding + earned profit + Ethix loan fees (fees come from the loan file, not a T24 balance type)'),
            ('Carrying amount with product policies', 'as above, except ' + ', '.join(f'{k}: ' + ' '.join(f'{"-" if c < 0 else "+"}{t}' for t, c in v['parent_coefficients'].items())
                                                                                     for k, v in ctx.policies.items() if v.get('enabled'))),
            ('Deposit balance', '+CREDIT +CURACCOUNT'),
            ('Selected balance types', 'exactly the types listed on the line')]
