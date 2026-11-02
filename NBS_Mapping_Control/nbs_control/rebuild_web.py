"""Owner interface for the code-keyed NBS rebuild: import, policies, mappings, preview, runs, drilldown."""
from __future__ import annotations
import csv
import io
import json
import secrets
import sqlite3
import threading
from contextlib import closing
from pathlib import Path

from flask import abort, flash, redirect, render_template, request, send_from_directory, url_for, Response

from . import policies, rebuild_run as rr, target_mappings as tm
from .categ_data import FILTER_FIELDS, repeated_groups
from .money import text as micro_text
from .rebuild_store import connect, sources as list_sources

CATEG_FORM_FIELDS = [('pl_category', 'PL.CATEGORY (P&L category)'), ('product_category', 'PRODUCT.CATEGORY (product, different namespace)'),
                     ('transaction_code', 'TRANSACTION.CODE'), ('system_id', 'SYSTEM.ID'), ('event_type', 'Event type (SOFT.ACCTNG.DTLS / U)'),
                     ('company', 'COMPANY.CODE'), ('unheaded_u', 'Unheaded column U (meaning not defined)')]


def register_rebuild_routes(app, root):
    register_spec_routes(app, root)
    from .builder_web import register_builder_routes
    register_builder_routes(app, root)
    from .nbs_web import register_nbs_routes
    register_nbs_routes(app, root)
    p = rr.Paths(root)
    jobs = p.data / 'jobs'
    jobs.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()

    def catalogue():
        return json.loads(p.catalogue.read_text(encoding='utf-8')) if p.catalogue.exists() else None

    def run_dir(run_id):
        if not run_id or not all(ch.isalnum() or ch == '-' for ch in run_id):
            abort(404)
        d = p.runs / run_id
        if not (d / 'manifest.json').exists():
            abort(404)
        return d

    def latest_id():
        f = p.runs / 'latest.json'
        return json.loads(f.read_text())['run_id'] if f.exists() else None

    def state(job, phase, **extra):
        f = jobs / (job + '.json')
        tmp = f.with_suffix('.tmp')
        tmp.write_text(json.dumps({'job': job, 'phase': phase, **extra}, default=str), encoding='utf-8')
        tmp.replace(f)

    def background(job, fn):
        def work():
            try:
                result = fn(lambda msg: state(job, msg))
                state(job, 'Complete', result=result)
            except Exception as exc:  # surfaced to the owner, never swallowed
                state(job, 'Failed', error=f'{type(exc).__name__}: {exc}')
            finally:
                lock.release()
        threading.Thread(target=work, daemon=True).start()

    @app.route('/rebuild')
    def rebuild_home():
        srcs, refs = [], []
        if p.store.exists():
            with closing(connect(p.store)) as c:
                srcs = list_sources(c)
                refs = c.execute('SELECT ref_version, kind, filename, report_date, unit FROM ref_versions ORDER BY imported_at').fetchall()
        basis = json.loads((p.config / policies.BASIS_FILE).read_text(encoding='utf-8')) if (p.config / policies.BASIS_FILE).exists() else None
        dup = json.loads((p.config / policies.DUPLICATE_FILE).read_text(encoding='utf-8')) if (p.config / policies.DUPLICATE_FILE).exists() else None
        latest = rr.latest_run(root)
        runs = sorted((json.loads((d / 'manifest.json').read_text(encoding='utf-8')) for d in p.runs.glob('*') if (d / 'manifest.json').exists()),
                      key=lambda m: m['created_at'], reverse=True) if p.runs.exists() else []
        mapping_counts = {}
        if (p.config / tm.MAPPING_FILE).exists():
            for t in tm.load(p.config)['targets'].values():
                mapping_counts[t['status']] = mapping_counts.get(t['status'], 0) + 1
        return render_template('rebuild_home.html', sources=srcs, refs=refs, basis=basis, dup=dup, latest=latest, runs=runs[:20],
                               stale=rr.stale_reasons(root, latest), mapping_counts=mapping_counts, defaults=rr.DEFAULT_INPUTS)

    @app.route('/rebuild/import', methods=['POST'])
    def rebuild_import():
        if not lock.acquire(blocking=False):
            flash('Another import or run is active.', 'error')
            return redirect(url_for('rebuild_home'))
        job = secrets.token_hex(6)
        work = p.data / 'uploads' / job
        try:
            work.mkdir(parents=True)
            categ, bo = [], None
            for f in request.files.getlist('categ_files'):
                if f and f.filename:
                    if not f.filename.lower().endswith('.xlsx'):
                        raise ValueError('Category files must be .xlsx')
                    dest = work / Path(f.filename).name
                    f.save(dest)
                    categ.append(str(dest))
            categ += [x.strip() for x in request.form.get('categ_paths', '').splitlines() if x.strip()]
            up = request.files.get('bo_file')
            if up and up.filename:
                bo = str(work / Path(up.filename).name)
                up.save(bo)
            bo = bo or request.form.get('bo_path', '').strip() or None
            for x in categ + ([bo] if bo else []):
                if not Path(x).exists():
                    raise ValueError(f'File not found: {x}')
            state(job, 'Importing')
            background(job, lambda log: rr.setup(root, categ or None, bo, None, log=log))
            return redirect(url_for('rebuild_job', job=job))
        except (ValueError, OSError) as exc:
            lock.release()
            flash(str(exc), 'error')
            return redirect(url_for('rebuild_home'))

    @app.route('/rebuild/run', methods=['POST'])
    def rebuild_start():
        if not lock.acquire(blocking=False):
            flash('Another import or run is active.', 'error')
            return redirect(url_for('rebuild_home'))
        job = secrets.token_hex(6)
        args = dict(report_date=request.form.get('report_date') or '2026-09-30', label=request.form.get('label', ''),
                    actor=request.form.get('actor') or 'owner', bo_ref=request.form.get('bo_ref') or None)
        state(job, 'Starting run')
        background(job, lambda log: {k: v for k, v in rr.run(root, log=log, **args).items() if k in ('run_id', 'statuses', 'excel')})
        return redirect(url_for('rebuild_job', job=job))

    @app.route('/rebuild/jobs/<job>')
    def rebuild_job(job):
        if not job.isalnum():
            abort(404)
        f = jobs / (job + '.json')
        if not f.exists():
            abort(404)
        return render_template('rebuild_job.html', state=json.loads(f.read_text(encoding='utf-8')))

    @app.route('/rebuild/runs/<run_id>')
    def rebuild_runview(run_id):
        d = run_dir(run_id)
        m = json.loads((d / 'manifest.json').read_text(encoding='utf-8'))
        controls = json.loads((d / 'controls.json').read_text(encoding='utf-8'))
        return render_template('rebuild_run.html', m=m, controls=controls, files=sorted(x.name for x in d.iterdir() if x.is_file()),
                               tables=sorted((catalogue() or {'tables': {}})['tables']), stale=rr.stale_reasons(root, m) if run_id == latest_id() else None)

    @app.route('/rebuild/runs/<run_id>/table/<table>')
    def rebuild_table(run_id, table):
        d = run_dir(run_id)
        if not table.isdigit():
            abort(404)
        rows = [r for r in csv.DictReader(open(d / 'comparison_bo.csv', encoding='utf-8-sig')) if r['table'] == table]
        items = {}
        for r in rows:
            items.setdefault(r['target_id'], {'target_id': r['target_id'], 'item_code': r['item_code'], 'description': r['description'],
                                              'mapping_status': r['mapping_status'], 'cells': []})['cells'].append(r)
        cat = catalogue()
        return render_template('rebuild_table.html', run_id=run_id, table=table, items=list(items.values()),
                               measures=list(cat['tables'][table]['measures']), meta=cat['tables'][table])

    @app.route('/rebuild/runs/<run_id>/cell')
    def rebuild_cell(run_id):
        d = run_dir(run_id)
        tid, measure = request.args.get('target', ''), request.args.get('measure', '')
        cat = catalogue()
        with closing(sqlite3.connect(d / 'run.sqlite')) as db:
            row = db.execute('SELECT value_micro, status, source_kind, issues FROM cells WHERE target_id=? AND measure=?', (tid, measure)).fetchone()
            if not row:
                abort(404)
            res = db.execute('SELECT layout, mapping FROM results WHERE target_id=?', (tid,)).fetchone()
            target = json.loads(res[1])
            sem = cat['tables'][target['table']]['measures'][measure]['semantic']
            # Totals are drilled to every included record (with the currency suffix where the total has one).
            if sem.startswith('TOTAL'):
                cond, arg = "(semantic LIKE ? OR included=0)", '%' + sem[5:] if sem != 'TOTAL' else '%'
            else:
                cond, arg = '(semantic=? OR included=0)', sem.replace('_COUNT', '_AMOUNT')
            contrib = db.execute(f'SELECT fact_id, source, record, semantic, amount_micro, included, reason FROM contributions WHERE target_id=? AND {cond} ORDER BY included DESC, abs(amount_micro) DESC LIMIT 2000',
                                 (tid, arg)).fetchall()
            totals = db.execute(f'SELECT included, count(*), sum(amount_micro) FROM contributions WHERE target_id=? AND {cond} GROUP BY included',
                                (tid, arg)).fetchall()
        if request.args.get('format') == 'csv':
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(['fact_or_row_id', 'source', 'record', 'semantic', 'amount_qar', 'included', 'reason'])
            for x in contrib:
                w.writerow(list(x[:4]) + [micro_text(x[4]), x[5], x[6]])
            return Response(buf.getvalue(), mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename=contributions_{tid.replace("|", "_")}.csv'})
        return render_template('rebuild_cell.html', run_id=run_id, target=target, measure=measure, semantic=sem, cell=row,
                               issues=json.loads(row[3]), contrib=contrib, totals=totals, micro_text=micro_text)

    @app.route('/rebuild/runs/<run_id>/download/<name>')
    def rebuild_download(run_id, name):
        d = run_dir(run_id)
        if name not in {x.name for x in d.iterdir() if x.is_file()} or name == 'run.sqlite':
            abort(404)
        return send_from_directory(d.resolve(), name, as_attachment=True)

    @app.route('/rebuild/mappings')
    def rebuild_mappings():
        doc = tm.load(p.config)
        table = request.args.get('table', '')
        status = request.args.get('status', '')
        q = request.args.get('q', '').lower()
        rows = [t for t in doc['targets'].values() if (not table or t['table'] == table) and (not status or t['status'] == status)
                and (not q or q in (t['description'] + ' ' + t['item_code']).lower())]
        return render_template('rebuild_mappings.html', rows=sorted(rows, key=lambda t: t['target_id'])[:500], total=len(rows), table=table,
                               status=status, q=q, statuses=tm.STATUSES, version=doc['version'], tables=sorted({t['table'] for t in doc['targets'].values()}))

    def form_target(old):
        f = request.form
        new = json.loads(json.dumps(old))
        for k in ('status', 'method', 'date_basis'):
            new[k] = f.get(k, old.get(k))
        new['legacy_rule_id'] = f.get('legacy_rule_id', '').strip() or None
        new['evidence'] = f.get('evidence', '').strip()
        new['effective_from'] = f.get('effective_from') or None
        new['effective_to'] = f.get('effective_to') or None
        if new['method'] == 'CATEG_EVENTS':
            if f.get('advanced_filter', '').strip():
                filt = json.loads(f['advanced_filter'])
            else:
                parts = []
                for field, _ in CATEG_FORM_FIELDS:
                    vals = [v.strip() for v in f.get('inc_' + field, '').split(',') if v.strip()]
                    if vals:
                        parts.append({'field': field, 'op': 'in', 'values': vals})
                    exc = [v.strip() for v in f.get('exc_' + field, '').split(',') if v.strip()]
                    if exc:
                        parts.append({'not': {'field': field, 'op': 'in', 'values': exc}})
                filt = parts[0] if len(parts) == 1 else {'all': parts} if parts else None
            new['categ'] = {'filter': filt, 'sign': int(f.get('sign', '1')), 'geography': f.get('geography', 'UNKNOWN')}
        else:
            new['categ'] = None
        overrides = {}
        for m in catalogue()['tables'][old['table']]['measures']:
            mode = f.get('ov_mode_' + m, '')
            if mode == 'value':
                overrides[m] = {'value': f.get('ov_value_' + m, '').strip(), 'reason': f.get('ov_reason_' + m, '').strip()}
            elif mode == 'empty':
                overrides[m] = {'value': None, 'reason': f.get('ov_reason_' + m, '').strip()}
        new['overrides'] = overrides
        return new

    @app.route('/rebuild/mapping/<path:tid>', methods=['GET', 'POST'])
    def rebuild_mapping(tid):
        doc = tm.load(p.config)
        t = doc['targets'].get(tid)
        if t is None:
            abort(404)
        cat = catalogue()
        preview = None
        proposed = t
        if request.method == 'POST':
            try:
                proposed = form_target(t)
                if request.form.get('action') == 'preview':
                    preview = rr.preview_target(root, tid, proposed)
                else:
                    tm.save_target(p.config, tid, proposed, request.form.get('actor', ''), request.form.get('reason', ''), cat)
                    flash('Saved as a new mapping version. Earlier runs are unchanged; the latest run is now stale until you regenerate.', 'ok')
                    return redirect(url_for('rebuild_mapping', tid=tid))
            except (ValueError, KeyError, json.JSONDecodeError) as exc:
                flash('Not saved: ' + str(exc), 'error')
        rules = json.loads(p.rules.read_text(encoding='utf-8'))['rules']
        rule = rules.get(proposed.get('legacy_rule_id') or '')
        return render_template('rebuild_mapping.html', t=proposed, saved=t, measures=cat['tables'][t['table']]['measures'], rule=rule,
                               history=tm.history(p.config, tid)[-15:], preview=preview, statuses=tm.STATUSES, methods=tm.METHODS,
                               date_bases=tm.DATE_BASES, geographies=tm.GEOGRAPHY, form_fields=CATEG_FORM_FIELDS,
                               filter_text=json.dumps((proposed.get('categ') or {}).get('filter'), indent=1),
                               categ_fields=sorted(FILTER_FIELDS))

    @app.route('/rebuild/policies', methods=['GET', 'POST'])
    def rebuild_policies():
        basis_path = p.config / policies.BASIS_FILE
        dup_path = p.config / policies.DUPLICATE_FILE
        basis = json.loads(basis_path.read_text(encoding='utf-8'))
        dup = json.loads(dup_path.read_text(encoding='utf-8'))
        if request.method == 'POST':
            try:
                actor, reason = request.form.get('actor', ''), request.form.get('reason', '')
                if request.form.get('kind') == 'basis':
                    pid = request.form['policy_id']
                    for pol in basis['policies']:
                        if pol['policy_id'] == pid:
                            pol['enabled'] = request.form.get('enabled') == 'on'
                            pol['effective_reporting_date'] = request.form['effective_reporting_date']
                    policies.save_basis_policy(p.config, basis, actor, reason)
                else:
                    dup['default_treatment'] = request.form.get('default_treatment', dup['default_treatment'])
                    fp = request.form.get('fingerprint', '').strip()
                    if fp:
                        if request.form.get('treatment') == 'CLEAR':
                            dup['decisions'].pop(fp, None)
                        else:
                            dup['decisions'][fp] = {'treatment': request.form['treatment'], 'actor': actor, 'reason': reason}
                    policies.save_duplicate_policy(p.config, dup, actor, reason)
                flash('Policy saved as a new version; raw source rows and dates are unchanged. Regenerate to apply.', 'ok')
                return redirect(url_for('rebuild_policies'))
            except (ValueError, KeyError) as exc:
                flash('Not saved: ' + str(exc), 'error')
        groups = []
        with closing(connect(p.store)) as c:
            cs = [s for s in list_sources(c) if s['dataset'] == 'CATEG_ENTRY']
            if cs:
                groups = sorted(repeated_groups(c, cs[-1]['source_sha256']), key=lambda g: -abs(g['excess_micro']))[:150]
        hist = sorted((p.config / 'policy_history').glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:12] if (p.config / 'policy_history').exists() else []
        return render_template('rebuild_policies.html', basis=basis, dup=dup, groups=groups, treatments=policies.TREATMENTS,
                               micro_text=micro_text, history=[json.loads(h.read_text(encoding='utf-8')) for h in hist])


def register_spec_routes(app, root):
    """Stakeholder mapping specification: build (with optional drafting refresh) and download."""
    from . import mapping_export
    p = rr.Paths(root)
    spec_dir = p.root / 'exports' / 'mapping_specification'

    @app.route('/rebuild/specification', methods=['GET', 'POST'])
    def rebuild_specification():
        if request.method == 'POST':
            try:
                if request.form.get('enhance') == 'on':
                    r = rr.enhance_mappings(root, log=lambda *_: None)
                    flash(f'Evidence-based drafting: {r["updated_targets"]} targets changed (mapping version {r["mapping_version"]}). Regenerate a run for new figures.', 'ok')
                if request.form.get('gl') == 'on' or not (p.data / 'gl_evidence.json').exists():
                    rr.gl_evidence_file(root)
                out = mapping_export.export(root)
                flash(f'Specification written: {Path(out["xlsx"]).name} ({out["targets"]} targets, check {out["verification"]["status"]}).', 'ok')
            except (ValueError, OSError, KeyError) as exc:
                flash('Not exported: ' + str(exc), 'error')
            return redirect(url_for('rebuild_specification'))
        files = sorted((x for x in spec_dir.glob('NBS_Mapping_Specification_*') if x.is_file()), key=lambda x: x.stat().st_mtime, reverse=True) if spec_dir.exists() else []
        return render_template('rebuild_specification.html', files=[x.name for x in files[:24]])

    @app.route('/rebuild/specification/<name>')
    def rebuild_specification_file(name):
        if not name.startswith('NBS_Mapping_Specification_') or '/' in name or '\\' in name or not (spec_dir / name).is_file():
            abort(404)
        return send_from_directory(spec_dir.resolve(), name, as_attachment=True)
