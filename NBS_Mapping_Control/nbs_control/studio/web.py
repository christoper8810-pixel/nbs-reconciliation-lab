"""Mapping Studio pages in the existing local Flask app (127.0.0.1 only). Steps 1-11 of the Studio workflow."""
from __future__ import annotations

import secrets
import tempfile
import threading
from collections import OrderedDict
from pathlib import Path

from flask import abort, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from . import exports, run as R, synthetic
from .store import Store

JOBS = {}
_CACHE = OrderedDict()


def register_studio_routes(app, root):
    app.config['STUDIO_ENABLED'] = True
    root = Path(root)
    data_root, export_root = root / 'data', root / 'exports' / 'studio'
    store = Store(data_root)

    def result(rid):
        r = store.run(rid) or abort(404)
        if rid not in _CACHE:
            _CACHE[rid] = R.load_result(r['folder'])
            while len(_CACHE) > 4:
                _CACHE.popitem(last=False)
        return r, _CACHE[rid]

    def start_job(fn):
        jid = secrets.token_hex(6)
        JOBS[jid] = {'status': 'RUNNING', 'message': 'queued', 'run_id': None, 'error': None}

        def work():
            try:
                rid = fn(lambda m: JOBS[jid].update(message=m))
                JOBS[jid].update(status='DONE', run_id=rid)
            except Exception as exc:  # noqa: BLE001 - shown to the user
                JOBS[jid].update(status='ERROR', error=f'{type(exc).__name__}: {exc}')
        threading.Thread(target=work, daemon=True).start()
        return redirect(url_for('studio_job', jid=jid))

    @app.route('/studio')
    def studio_home():
        return render_template('studio_home.html', projects=store.projects(), runs=store.runs())

    @app.route('/studio/synthetic', methods=['POST'])
    def studio_synthetic():
        sc = request.form.get('scenario', 'defects')
        folder = synthetic.build(data_root / 'studio' / f'synthetic_{sc}', sc)
        pid = R.new_project(store, data_root, f'SYNTHETIC {sc}', folder / 'mapping_workbook.xlsx', folder / 'bo_report.csv',
                            [folder / 'source_records.csv'])
        return start_job(lambda prog: R.run_project(store, data_root, export_root, pid, progress=prog)[0])

    @app.route('/studio/start', methods=['POST'])
    def studio_start():
        tmp = Path(tempfile.mkdtemp(prefix='studio-upload-'))

        def take(field, multiple=False):
            out = []
            for f in (request.files.getlist(field) if multiple else [request.files.get(field)]):
                if f and f.filename:
                    p = tmp / secure_filename(f.filename)
                    f.save(p)
                    out.append(p)
            for line in (request.form.get(field + '_path') or '').splitlines():
                line = line.strip().strip('"')
                if line:
                    if not Path(line).exists():
                        raise FileNotFoundError(line)
                    out.append(Path(line))
            return out if multiple else (out[0] if out else None)
        try:
            wb, bo, src = take('workbook'), take('bo'), take('sources', True)
            if not wb:
                raise ValueError('Step 1: choose the Excel mapping workbook')
            cfg = {'overlap_policy': request.form.get('overlap_policy', 'ALL'),
                   'tolerance': request.form.get('tolerance') or '0.01',
                   'bo_amount_scale': request.form.get('bo_amount_scale') or 1, 'bo_sign': request.form.get('bo_sign') or 1}
            pid = R.new_project(store, data_root, request.form.get('label', ''), wb, bo, src, cfg)
        except (ValueError, FileNotFoundError) as exc:
            flash(str(exc), 'error')
            return redirect(url_for('studio_home'))
        return start_job(lambda prog: R.run_project(store, data_root, export_root, pid, progress=prog)[0])

    @app.route('/studio/job/<jid>')
    def studio_job(jid):
        job = JOBS.get(jid) or abort(404)
        if job['status'] == 'DONE':
            return redirect(url_for('studio_run', rid=job['run_id']))
        return render_template('studio_job.html', job=job)

    @app.route('/studio/run/<rid>')
    def studio_run(rid):
        r, res = result(rid)
        status, q = request.args.get('status', ''), request.args.get('q', '').upper()
        after = {' / '.join(str(x) for x in a['key'] if x): a for a in res['recon_after']}
        rows = []
        for x in res['recon_before']:
            k = ' / '.join(str(y) for y in x['key'] if y)
            if (status == 'OPEN' and x['status'] == 'MATCHED') or (status and status != 'OPEN' and x['status'] != status) or (q and q not in k.upper()):
                continue
            rows.append({**x, 'k': k, 'after': (after.get(k) or {}).get('difference')})
        props = store.proposals(rid)
        return render_template('studio_run.html', r=r, res=res, s=res['summary'], rows=rows, props=props,
                               files=[f for f in exports.FILES if (Path(r['folder']) / f).exists()],
                               statuses=sorted({x['status'] for x in res['recon_before']}))

    @app.route('/studio/run/<rid>/key')
    def studio_key(rid):
        r, res = result(rid)
        k = request.args.get('k', '')
        line = k.split(' / ')[0]
        rec = next((x for x in res['recon_before'] if ' / '.join(str(y) for y in x['key'] if y) == k), None)
        ids = next((v for kk, v in res['contributions'].items() if ' / '.join(p for p in kk.split(' | ') if p) == k), [])
        sigs = [s for s in res['signatures'] if s['id'] in set(ids)]
        near = [s for s in res['signatures'] if s['status'] != 'ALLOCATED' and (line in s['lines'] or not s['lines'])][:200]
        props = [p for p in store.proposals(rid) if k in (p.get('lines') or {})]
        resid = [x for x in res['residuals'] if x['key'] == k]
        return render_template('studio_key.html', r=r, k=k, line=line, rec=rec, sigs=sigs, near=near, props=props, resid=resid,
                               rules=res['line_rules'].get(line, []), ln=next((l for l in res['lines'] if l['line'] == line), None))

    @app.route('/studio/run/<rid>/proposals')
    def studio_proposals(rid):
        r, res = result(rid)
        conf, st = request.args.get('confidence', ''), request.args.get('status', '')
        props = [p for p in store.proposals(rid) if (not conf or p['confidence'] == conf) and (not st or p['status'] == st)]
        return render_template('studio_proposals.html', r=r, props=props, conf=conf, st=st)

    @app.route('/studio/run/<rid>/decide', methods=['POST'])
    def studio_decide(rid):
        pids = request.form.getlist('pid')
        if request.form.get('all_high'):
            pids = [p['id'] for p in store.proposals(rid) if p['confidence'] == 'HIGH' and p['status'] == 'PROPOSED']
        try:
            n = store.decide(rid, pids, request.form.get('decision', ''), request.form.get('actor', '').strip(), request.form.get('reason', '').strip())
            flash(f'{n} proposal(s) {request.form.get("decision", "").lower()}', 'ok')
        except ValueError as exc:
            flash(str(exc), 'error')
        return redirect(request.referrer or url_for('studio_proposals', rid=rid))

    @app.route('/studio/run/<rid>/export', methods=['POST'])
    def studio_export(rid):
        r, res = result(rid)
        actor = request.form.get('actor', '').strip()
        if not actor:
            flash('Enter your name to export the corrected mapping', 'error')
            return redirect(url_for('studio_run', rid=rid))
        corr = exports.write_corrected(store, rid, r['folder'], res, actor)
        v = corr['verification']
        flash(f"Corrected copy written: {len(corr['applied'])} edit(s) applied, {len(corr['conflicts'])} refused; "
              f"{v['cells_compared']} cells compared, original preserved: {'yes' if v['preserved'] else 'NO - see PATCH_AUDIT_LOG.xlsx'}",
              'ok' if v['preserved'] else 'error')
        return redirect(url_for('studio_run', rid=rid))

    @app.route('/studio/run/<rid>/rerun', methods=['POST'])
    def studio_rerun(rid):
        try:
            result(rid)
            if not (Path(store.run(rid)['folder']) / 'CORRECTED_MAPPING_PREVIEW.xlsx').exists():
                raise ValueError('Approve corrections and export the corrected mapping first')
        except ValueError as exc:
            flash(str(exc), 'error')
            return redirect(url_for('studio_run', rid=rid))
        return start_job(lambda prog: R.rerun(store, data_root, export_root, rid, prog)[0])

    @app.route('/studio/run/<rid>/validation')
    def studio_validation(rid):
        r, res = result(rid)
        sev, chk = request.args.get('severity', ''), request.args.get('check', '')
        items = [v for v in res['validation'] if (not sev or v['severity'] == sev) and (not chk or v['check'] == chk)]
        return render_template('studio_validation.html', r=r, res=res, items=items, sev=sev, chk=chk,
                               checks=sorted({v['check'] for v in res['validation']}))

    @app.route('/studio/run/<rid>/rules')
    def studio_rules(rid):
        r, res = result(rid)
        return render_template('studio_rules.html', r=r, res=res)

    @app.route('/studio/run/<rid>/file/<name>')
    def studio_file(rid, name):
        r = store.run(rid) or abort(404)
        if name not in exports.FILES:
            abort(404)
        return send_from_directory(r['folder'], name, as_attachment=not name.endswith('.html'))
