"""TB reconciliation pages inside the existing local Flask app (127.0.0.1 only)."""
from __future__ import annotations

import json
import secrets
import sqlite3
import threading
from pathlib import Path

from flask import abort, flash, redirect, render_template, request, send_from_directory, url_for

from . import compare, run as tbrun, synthetic

JOBS = {}
DOWNLOADS = ('report.html', 'reconciliation.xlsx', 'audit.json', 'tb_reconciliation.csv', 'exceptions.csv', 'root_causes.csv',
             'proposed_mapping_corrections.csv', 'components.csv', 'contributions.csv', 'gl_report.csv', 'rollforward.csv',
             'controls.csv', 'legacy_lines.csv', 'unallocated.csv', 'benchmark.csv', 'misalignment.csv', 'rule_diagnostics.csv',
             'account_recon.csv', 'applied_proposals.json')
PAGE = 200


def register_tb_routes(app, root):
    root = Path(root)
    data_root, export_root = root / 'data', root / 'exports' / 'tb_recon'

    def run_or_404(rid):
        r = tbrun.get_run(data_root, rid)
        if not r:
            abort(404)
        return r

    def q(r, sql, args=()):
        c = sqlite3.connect(Path(r['folder']) / 'run.sqlite')
        c.row_factory = sqlite3.Row
        try:
            return [dict(x) for x in c.execute(sql, args)]
        finally:
            c.close()

    def meta(r):
        rows = {x['key']: json.loads(x['value']) for x in q(r, 'SELECT key, value FROM meta')}
        return rows

    @app.route('/tb', methods=['GET'])
    def tb_home():
        return render_template('tb_home.html', runs=tbrun.list_runs(data_root), kinds=tbrun.INPUT_KINDS,
                               prefill=request.args.get('inputs', ''))

    @app.route('/tb/synthetic', methods=['POST'])
    def tb_synthetic():
        scenario = request.form.get('scenario', 'defects')
        folder = synthetic.build(data_root / 'tbrecon' / f'synthetic_{scenario}', scenario)
        flash(f'SYNTHETIC {scenario} dataset written to {folder}', 'ok')
        return redirect(url_for('tb_home', inputs=str(folder)))

    @app.route('/tb/start', methods=['POST'])
    def tb_start():
        folder = request.form.get('inputs', '').strip().strip('"')
        try:
            paths = tbrun.discover(folder)
        except Exception as exc:  # noqa: BLE001 - shown to the user
            flash(str(exc), 'error')
            return redirect(url_for('tb_home'))
        cfg = request.form.get('config', '').strip().strip('"') or compare.folder_config(folder)
        label, mode = request.form.get('label', ''), request.form.get('mode', 'normal')
        jid = secrets.token_hex(6)
        JOBS[jid] = {'status': 'RUNNING', 'message': 'queued', 'run_id': None, 'error': None}

        def work():
            try:
                prog = lambda m: JOBS[jid].update(message=m)  # noqa: E731
                if mode == 'proposals':
                    rid, *_ = compare.run_with_proposals(paths, data_root, export_root, cfg, None, label)
                else:
                    rid, _f, _r = tbrun.run_and_store(paths, data_root, export_root, label=label, cfg_path=cfg,
                                                      legacy=mode == 'legacy', progress=prog)
                JOBS[jid].update(status='DONE', run_id=rid)
            except Exception as exc:  # noqa: BLE001
                JOBS[jid].update(status='ERROR', error=str(exc))
        threading.Thread(target=work, daemon=True).start()
        return redirect(url_for('tb_job', jid=jid))

    @app.route('/tb/job/<jid>')
    def tb_job(jid):
        job = JOBS.get(jid) or abort(404)
        if job['status'] == 'DONE':
            return redirect(url_for('tb_run', rid=job['run_id']))
        return render_template('tb_job.html', job=job, jid=jid)

    @app.route('/tb/run/<rid>')
    def tb_run(rid):
        r = run_or_404(rid)
        m = meta(r)
        where, args = [], []
        for f in ('class', 'currency', 'recon_status'):
            if request.args.get(f):
                where.append(f'"{f}"=?')
                args.append(request.args[f])
        if request.args.get('gl'):
            where.append('target_gl LIKE ?')
            args.append(request.args['gl'] + '%')
        sql = 'SELECT * FROM gl_rows' + (' WHERE ' + ' AND '.join(where) if where else '') + ' ORDER BY abs_difference DESC, target_gl'
        rows = q(r, sql, args)
        page = int(request.args.get('page', 0))
        facets = {f: [x[f] for x in q(r, f'SELECT DISTINCT "{f}" FROM gl_rows ORDER BY 1')] for f in ('class', 'currency', 'recon_status')}
        def page_url(n):
            return url_for('tb_run', rid=rid, **{**{k: v for k, v in request.args.items() if k != 'page'}, 'page': n})
        return render_template('tb_run.html', r=r, m=m, page_url=page_url, rows=rows[page * PAGE:(page + 1) * PAGE], total=len(rows), page=page,
                               pages=(len(rows) + PAGE - 1) // PAGE, facets=facets, controls=q(r, 'SELECT * FROM controls ORDER BY id'),
                               legacy=q(r, 'SELECT * FROM legacy_lines ORDER BY legacy_gl, currency'), downloads=DOWNLOADS,
                               files={f for f in DOWNLOADS if (Path(r['folder']) / f).exists()})

    @app.route('/tb/run/<rid>/gl/<gl>/<ccy>')
    def tb_gl(rid, gl, ccy):
        r = run_or_404(rid)
        row = q(r, 'SELECT * FROM gl_rows WHERE target_gl=? AND currency=?', (gl, ccy))
        comps = q(r, 'SELECT * FROM components WHERE target_gl=? AND currency=? ORDER BY ABS(amount) DESC LIMIT 2000', (gl, ccy))
        cands = q(r, "SELECT * FROM components WHERE status!='MAPPED' AND currency=? AND candidates LIKE ? ORDER BY ABS(amount) DESC LIMIT 500",
                  (ccy, f'%"{gl}"%'))
        grain = q(r, 'SELECT balance_type, rule_id, COUNT(*) n, SUM(amount) amount FROM components WHERE target_gl=? AND currency=? '
                     'GROUP BY balance_type, rule_id ORDER BY 1, 2', (gl, ccy))
        exc = q(r, 'SELECT * FROM exceptions WHERE target_gl=? AND (currency=? OR currency IS NULL OR currency="")', (gl, ccy))
        roll = q(r, 'SELECT * FROM rollforward WHERE target_gl=? AND currency=?', (gl, ccy))
        return render_template('tb_gl.html', r=r, gl=gl, ccy=ccy, row=row[0] if row else None, comps=comps, cands=cands,
                               grain=grain, exc=exc, roll=roll)

    @app.route('/tb/run/<rid>/account/<path:acct>')
    def tb_account(rid, acct):
        r = run_or_404(rid)
        comps = q(r, 'SELECT * FROM components WHERE account=? ORDER BY engine, balance_type', (acct,))
        exc = q(r, 'SELECT * FROM exceptions WHERE account=?', (acct,))
        return render_template('tb_account.html', r=r, acct=acct, comps=comps, exc=exc)

    @app.route('/tb/run/<rid>/exceptions')
    def tb_exceptions(rid):
        r = run_or_404(rid)
        cat = request.args.get('category', '')
        exc = q(r, 'SELECT * FROM exceptions' + (' WHERE category=?' if cat else '') + ' ORDER BY ABS(amount) DESC LIMIT 2000',
                (cat,) if cat else ())
        return render_template('tb_exceptions.html', r=r, issues=q(r, 'SELECT * FROM issues ORDER BY issue_id'), exc=exc, cat=cat,
                               cats=[x['category'] for x in q(r, 'SELECT DISTINCT category FROM exceptions ORDER BY 1')])

    @app.route('/tb/run/<rid>/worklist')
    def tb_worklist(rid):
        r = run_or_404(rid)
        return render_template('tb_worklist.html', r=r, items=q(r, 'SELECT * FROM worklist ORDER BY proposal_id'))

    @app.route('/tb/run/<rid>/rules')
    def tb_rules(rid):
        r = run_or_404(rid)
        return render_template('tb_rules.html', r=r, m=meta(r), diags=q(r, 'SELECT * FROM rule_diagnostics'),
                               mis=q(r, 'SELECT * FROM misalignment'), unsupported=q(r, 'SELECT * FROM unsupported_bt'),
                               report=q(r, 'SELECT * FROM gl_report'), roll=q(r, 'SELECT * FROM rollforward'),
                               bench=q(r, 'SELECT * FROM benchmark WHERE status!="AGREES"'),
                               accounts=q(r, 'SELECT * FROM account_recon WHERE status!="RECONCILED"'))

    @app.route('/tb/run/<rid>/file/<name>')
    def tb_file(rid, name):
        r = run_or_404(rid)
        if name not in DOWNLOADS:
            abort(404)
        return send_from_directory(r['folder'], name, as_attachment=not name.endswith('.html'))

    @app.route('/tb/compare')
    def tb_compare():
        a, b = request.args.get('before', ''), request.args.get('after', '')
        try:
            res = compare.compare_runs(data_root, export_root, a, b)
        except ValueError as exc:
            flash(str(exc), 'error')
            return redirect(url_for('tb_home'))
        return render_template('tb_compare.html', res=res)
