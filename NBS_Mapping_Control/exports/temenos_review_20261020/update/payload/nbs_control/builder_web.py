"""Owner pages: Sources (portable file selection), Explore (every source by any dimension), Logic builder."""
from __future__ import annotations
import json
import re
import secrets
import threading
from contextlib import closing
from decimal import Decimal
from pathlib import Path

from flask import abort, flash, redirect, render_template, request, url_for

from . import gl_mapping, rebuild_run as rr, source_explorer as sx, sources as src, target_mappings as tm
from .rebuild_engine import correct_components, inherit_hierarchy
from .rebuild_store import connect

SOURCE_LABELS = {'ECB': 'ECB balances (any T24 category)', 'ECB_LOAN': 'ECB balances of loan accounts (with loan-file attributes)',
                 'ECB_DEPOSIT': 'ECB balances of deposit accounts (with deposit-file attributes)', 'TB': 'Trial balance (Ethix GL)',
                 'GL_LINE': 'GL Report line (DKBGL) - expands to its T24 criteria', 'CATEG': 'Category entries (PL category / event)'}
MEASURES = {'components': 'Selected balance types', 'ethix_carrying': 'Carrying amount (owner groups + RCM/CLM policy + Ethix fees)',
            'carrying': 'Owner OUTSTANDING + AMORTIZED_EARNED + Ethix fees', 'outstanding': 'Owner OUTSTANDING group', 'earned': 'Owner AMORTIZED_EARNED group',
            'unearned': 'Owner UNEARNED_PROFIT group', 'deposit': 'Deposit balance (CREDIT + CURACCOUNT)', 'amount': 'Source amount'}


def _codes(text):
    return [x for x in re.split(r'[\s,;]+', text or '') if x]


def _ranges(text, field):
    terms = []
    singles = []
    for tok in _codes(text):
        m = re.fullmatch(r'(\d+)-(\d+)', tok)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                raise ValueError(f'Range {tok} is reversed')
            terms.append({'field': field, 'op': 'range', 'values': [lo, hi]})
        else:
            singles.append(tok)
    if singles:
        terms.append({'field': field, 'op': 'in', 'values': singles})
    return terms


def build_part(form):
    """Structured form fields -> one part (typed filter tree, no free SQL)."""
    s = form.get('part_source', '')
    sign = -1 if form.get('part_sign') == '-1' else 1
    if s == 'CATEG':
        parts = []
        for field, key in (('pl_category', 'part_pl'), ('event_type', 'part_events'), ('product_category', 'part_prodcat')):
            vals = form.getlist(key) + _codes(form.get(key + '_text', ''))
            if vals:
                parts.append({'field': field, 'op': 'in', 'values': list(dict.fromkeys(vals))})
        if not parts:
            raise ValueError('Choose at least one PL category or event type')
        return {'kind': 'CATEG', 'filter': parts[0] if len(parts) == 1 else {'all': parts}, 'sign': sign,
                'geography': form.get('part_geography', 'UNKNOWN'), 'label': form.get('part_label') or 'Category entries'}
    if s not in ('ECB', 'ECB_LOAN', 'ECB_DEPOSIT', 'TB'):
        raise ValueError('Choose a source')
    conds = []
    cat_terms = [{'field': 'category', 'op': 'in', 'values': form.getlist('part_categories')}] if form.getlist('part_categories') else []
    cat_terms += _ranges(form.get('part_category_ranges', ''), 'category')
    if cat_terms:
        conds.append(cat_terms[0] if len(cat_terms) == 1 else {'any': cat_terms})
    sec_terms = [{'field': 'sector', 'op': 'in', 'values': form.getlist('part_sectors')}] if form.getlist('part_sectors') else []
    sec_terms += _ranges(form.get('part_sector_ranges', ''), 'sector')
    if sec_terms:
        conds.append(sec_terms[0] if len(sec_terms) == 1 else {'any': sec_terms})
    if form.get('part_country') == 'QA':
        conds.append({'field': 'country', 'op': 'eq', 'values': ['QA']})
    elif form.get('part_country') == 'NOT_QA':
        conds.append({'not': {'field': 'country', 'op': 'eq', 'values': ['QA']}})
    if form.get('part_currency') == 'QAR':
        conds.append({'field': 'currency', 'op': 'eq', 'values': ['QAR']})
    elif form.get('part_currency') == 'FC':
        conds.append({'not': {'field': 'currency', 'op': 'eq', 'values': ['QAR']}})
    if form.get('part_residency') in ('Resident', 'NonResident'):
        conds.append({'field': 'residency', 'op': 'eq', 'values': [form['part_residency']]})
    if form.get('part_personal') in ('Personal', 'NonPersonal'):
        conds.append({'field': 'personal', 'op': 'eq', 'values': [form['part_personal']]})
    if _codes(form.get('part_sic', '')):
        conds.append({'field': 'industry', 'op': 'prefix', 'values': _codes(form['part_sic'])})
    if form.getlist('part_products'):
        conds.append({'field': 'product', 'op': 'in', 'values': form.getlist('part_products')})
    gls = form.getlist('part_gls') + [x for x in _codes(form.get('part_gl_text', '')) if len(x) == 10]
    glp = [x for x in _codes(form.get('part_gl_text', '')) if len(x) != 10]
    if gls or glp:
        g = ([{'field': 'gl', 'op': 'in', 'values': gls}] if gls else []) + ([{'field': 'gl', 'op': 'prefix', 'values': glp}] if glp else [])
        conds.append(g[0] if len(g) == 1 else {'any': g})
    flt = None if not conds else conds[0] if len(conds) == 1 else {'all': conds}
    measure = form.get('part_measure') or ('amount' if s == 'TB' else 'components')
    comps = [c.upper() for c in form.getlist('part_balance_types')] if measure == 'components' else []
    if s == 'TB':
        measure, comps = 'amount', []
    if flt is None:
        raise ValueError('Choose at least one selection (category, sector, GL, ...); a whole source is never implicit')
    return {'kind': 'STOCK', 'source': s, 'measure': measure, 'components': comps, 'filter': flt, 'factor': sign,
            'label': form.get('part_label') or SOURCE_LABELS[s]}


def parts_from_current(root, t, rules, settings):
    """Show the item's current logic as builder parts (corrections and inherited dimensions applied)."""
    ids = [t.get('legacy_rule_id')] if t['method'] == 'LEGACY_RULE' else (t.get('legacy_rule_ids') or []) if t['method'] == 'QCB_POPULATION' else []
    out = []
    for rid in ids:
        s = rules.get(rid or '')
        if not s or not s.get('source'):
            continue
        s, _ = correct_components(s, settings.get('component_corrections'))
        e, notes = inherit_hierarchy(s, settings.get('hierarchy_predicates'))
        out.append({'kind': 'STOCK', 'source': e['source'], 'measure': e['measure'], 'components': list(e.get('components') or []),
                    'filter': e.get('filter'), 'factor': e['factor'], 'label': f'From current rule {rid} (row {s.get("row")})'})
    if t['method'] == 'SOURCE_RULE':
        out = list(t.get('parts') or [])
    return out


def register_builder_routes(app, root):
    p = rr.Paths(root)
    lock = threading.Lock()
    jobs = p.data / 'jobs'
    jobs.mkdir(parents=True, exist_ok=True)

    def run_bg(fn):
        job = secrets.token_hex(6)
        f = jobs / (job + '.json')

        def state(phase, **kw):
            tmp = f.with_suffix('.tmp')
            tmp.write_text(json.dumps({'job': job, 'phase': phase, **kw}, default=str), encoding='utf-8')
            tmp.replace(f)
        if not lock.acquire(blocking=False):
            raise ValueError('Another import or calculation is running; wait for it to finish')
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

    @app.route('/rebuild/sources', methods=['GET', 'POST'])
    def rebuild_sources():
        if request.method == 'POST':
            try:
                action = request.form.get('action', '')
                kind = request.form.get('kind', '')
                if action == 'choose':
                    up = request.files.get('file')
                    if up and up.filename:
                        dest = src.inputs_dir(root) / Path(up.filename).name
                        up.save(dest)
                        e = src.register(root, kind, dest, request.form.get('actor') or 'owner')
                    elif request.form.get('existing'):
                        e = src.register(root, kind, src.inputs_dir(root) / Path(request.form['existing']).name, request.form.get('actor') or 'owner')
                    elif request.form.get('path'):
                        e = src.register(root, kind, request.form['path'].strip().strip('"'), request.form.get('actor') or 'owner')
                    else:
                        raise ValueError('Choose a file to upload, one already in the inputs folder, or type its full path')
                    flash(f'{src.TYPES[kind]["label"]}: {Path(e["file"]).name} recorded (SHA-256 {e["sha256"][:12]}...). Import or build to use it.', 'ok')
                elif action == 'build':
                    job = run_bg(lambda log: src.build_account_database(root, log))
                    return redirect(url_for('rebuild_job', job=job))
                elif action == 'import':
                    job = run_bg(lambda log: src.import_references(root, None, log))
                    return redirect(url_for('rebuild_job', job=job))
                elif action == 'gl_lines':
                    job = run_bg(lambda log: sx.compute_line_amounts(root, log))
                    return redirect(url_for('rebuild_job', job=job))
            except (ValueError, OSError) as exc:
                flash(str(exc), 'error')
            return redirect(url_for('rebuild_sources'))
        return render_template('rebuild_sources.html', status=src.status(root), inputs=str(src.inputs_dir(root)))

    @app.route('/rebuild/explore')
    def rebuild_explore():
        ds = request.args.get('dataset', 'ECB')
        if ds not in sx.DATASETS:
            abort(404)
        dim = request.args.get('dim') or next(iter(sx.DATASETS[ds]['dims']))
        q = request.args.get('q', '')
        rows, total, error = [], 0, None
        try:
            rows, total = sx.explore(root, ds, dim, q)
        except ValueError as exc:
            error = str(exc)
        return render_template('rebuild_explore.html', datasets=sx.DATASETS, ds=ds, dim=dim, q=q, rows=rows, total=total, error=error)

    @app.route('/rebuild/builder/<path:tid>', methods=['GET', 'POST'])
    def rebuild_builder(tid):
        doc = tm.load(p.config)
        t = doc['targets'].get(tid)
        if t is None:
            abort(404)
        catalogue = json.loads(p.catalogue.read_text(encoding='utf-8'))
        rules = json.loads(p.rules.read_text(encoding='utf-8'))['rules']
        settings = rr.run_settings(p)
        parts = parts_from_current(root, t, rules, settings)
        preview = None
        if request.method == 'POST':
            try:
                parts = json.loads(request.form.get('parts_json') or '[]')
                action = request.form.get('action')
                if action == 'original_temenos':
                    from .temenos_review import original_parts
                    parts = original_parts(root, t)
                    flash('Original Temenos category, sector and balance types loaded as an unsaved draft. Raw source signs are retained. Preview and review the presentation sign before saving.', 'ok')
                elif action == 'add':
                    if request.form.get('part_source') == 'GL_LINE':
                        with closing(connect(p.store)) as c:
                            sha = gl_mapping.latest(c)
                            if not sha:
                                raise ValueError('Import the GL mapping workbook first (Sources page)')
                            new, notes = gl_mapping.line_parts(c, sha, request.form.get('part_line', ''))
                        if not new:
                            raise ValueError('That GL line has no ECB balance criteria: ' + '; '.join(notes))
                        sign = -1 if request.form.get('part_sign') == '-1' else 1
                        parts += [dict(x, factor=sign) for x in new]
                        if notes:
                            flash('Not added from the GL line: ' + '; '.join(notes), 'error')
                    else:
                        parts.append(build_part(request.form))
                elif action and action.startswith('remove:'):
                    del parts[int(action.split(':')[1])]
                elif action == 'clear':
                    parts = []
                elif action in ('preview', 'save'):
                    proposed = dict(t, method='SOURCE_RULE', parts=parts, status=request.form.get('status') or 'PROVISIONAL',
                                    candidate_basis='OWNER_LOGIC_BUILDER', date_basis='STOCK_AS_OF',
                                    evidence=request.form.get('evidence') or t.get('evidence'))
                    if action == 'preview':
                        preview = rr.preview_target(root, tid, proposed)
                        preview['parts'] = []
                        for i, part in enumerate(parts):
                            one = rr.preview_target(root, tid, dict(proposed, parts=[part]))
                            preview['parts'].append({'label': part.get('label'), 'records': one['matched_records'],
                                                     'values': {r['measure']: r['new'] for r in one['rows'] if r['new'] is not None}})
                        with closing(connect(p.store)) as c:
                            ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS' ORDER BY imported_at DESC").fetchone()
                            bo = {m: v for m, v in c.execute('SELECT measure, value_micro FROM bo_cells WHERE ref_version=? AND table_code=? AND item_code=?',
                                                               (ref[0], t['table'], t['item_code']))} if ref else {}
                        for r in preview['rows']:
                            b = bo.get(r['measure'])
                            r['bo'] = None if b is None else Decimal(b) / Decimal(10 ** 6)
                            r['diff'] = None if r['new'] is None or r['bo'] is None else r['new'] - r['bo']
                    else:
                        tm.save_target(p.config, tid, dict(proposed), request.form.get('actor', ''), request.form.get('reason', ''), catalogue)
                        flash('Saved as a new mapping version. Generate a run to apply it.', 'ok')
                        return redirect(url_for('rebuild_builder', tid=tid))
            except (ValueError, KeyError, IndexError, json.JSONDecodeError) as exc:
                flash('Not done: ' + str(exc), 'error')
        try:
            opts = sx.options(root)
        except ValueError:
            opts = {}
        return render_template('rebuild_builder.html', t=t, parts=parts, parts_json=json.dumps(parts), preview=preview, opts=opts,
                               measures=catalogue['tables'][t['table']]['measures'], source_labels=SOURCE_LABELS, measure_labels=MEASURES,
                               readable=__import__('nbs_control.mapping_export', fromlist=['readable']).readable, statuses=tm.STATUSES)
