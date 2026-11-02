"""Before / after comparison of two stored runs, and the apply-proposals workflow (original mapping untouched)."""
from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

from . import rootcause
from .run import discover, execute, get_run, load_config, load_inputs, run_and_store


def _rows(folder, sql):
    c = sqlite3.connect(Path(folder) / 'run.sqlite')
    c.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in c.execute(sql)]
    finally:
        c.close()


def compare_runs(data_root, export_root, before_id, after_id):
    a, b = get_run(data_root, before_id), get_run(data_root, after_id)
    if not a or not b:
        raise ValueError('Unknown run id')
    q = 'SELECT target_gl, currency, class, expected, actual_opening, amount_exact AS difference, recon_status FROM gl_rows'
    ra = {(r['target_gl'], r['currency']): r for r in _rows(a['folder'], q)}
    rb = {(r['target_gl'], r['currency']): r for r in _rows(b['folder'], q)}
    lines = []
    for k in sorted(set(ra) | set(rb)):
        x, y = ra.get(k, {}), rb.get(k, {})
        lines.append({'target_gl': k[0], 'currency': k[1], 'class': y.get('class') or x.get('class'),
                      'before_status': x.get('recon_status', '-'), 'after_status': y.get('recon_status', '-'),
                      'before_difference': x.get('difference', ''), 'after_difference': y.get('difference', ''),
                      'change': 'RESOLVED' if x.get('recon_status') not in (None, 'RECONCILED') and y.get('recon_status') == 'RECONCILED'
                      else 'REGRESSED' if x.get('recon_status') == 'RECONCILED' and y.get('recon_status') != 'RECONCILED'
                      else 'NEW' if not x else 'REMOVED' if not y else 'CHANGED' if x.get('difference') != y.get('difference') else 'SAME'})
    stats = {k: {'before': a['summary'].get(k), 'after': b['summary'].get(k)} for k in a['summary']}
    out_dir = Path(export_root) / f'compare_{before_id}__{after_id}'
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / 'comparison.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(lines[0]) if lines else ['target_gl'])
        w.writeheader()
        w.writerows(lines)
    result = {'before': before_id, 'after': after_id, 'before_label': a['label'], 'after_label': b['label'],
              'statistics': stats, 'lines': lines,
              'summary': {c: sum(1 for l in lines if l['change'] == c) for c in ('RESOLVED', 'REGRESSED', 'NEW', 'REMOVED', 'CHANGED', 'SAME')}}
    (out_dir / 'comparison.json').write_text(json.dumps(result, indent=1, default=str), encoding='utf-8')
    result['folder'] = str(out_dir)
    return result


def run_with_proposals(paths, data_root, export_root, cfg_path=None, only=None, label=''):
    """Compute proposals on the supplied rules, apply the auto-applicable ones to a COPY and store a new run."""
    cfg = load_config(cfg_path)
    data, metas = load_inputs(paths)
    res = execute(data, metas, cfg)
    if data['gl_rules'] is None:
        raise ValueError('No gl_rules file: nothing to apply')
    rows, applied = rootcause.apply_worklist(data['gl_rules'], res['worklist'], only)
    if not applied:
        raise ValueError('No auto-applicable proposal to apply')
    run_id, folder, res2 = run_and_store(paths, data_root, export_root, label=label or f'after proposals {", ".join(applied)}',
                                         cfg_path=cfg_path, rule_overrides={'gl_rules': rows})
    (Path(folder) / 'applied_proposals.json').write_text(json.dumps(
        [w for w in res['worklist'] if w['proposal_id'] in applied], indent=1, default=str), encoding='utf-8')
    return run_id, folder, res2, applied


def folder_config(folder):
    p = Path(folder) / 'tb_recon.json'
    return str(p) if p.exists() else None


__all__ = ['compare_runs', 'run_with_proposals', 'folder_config', 'discover']
