"""Read-only views of every source for the owner: totals by any dimension, with dictionary descriptions.

Amounts are source units (QAR). Nothing here changes data; results are cached per source version.
"""
from __future__ import annotations
import json
from collections import defaultdict
from contextlib import closing
from decimal import Decimal

from . import gl_mapping
from .rebuild_store import connect, open_bank_readonly

_CACHE = {}
DATASETS = {
    'ECB': {'label': 'ECB balances', 'dims': {'category': 'T24 category', 'sector': 'T24 sector', 'country': 'Residence country',
                                                'currency': 'Currency', 'balance_type': 'Balance type', 'company': 'Company'}},
    'LOAN': {'label': 'Loan file', 'dims': {'product': 'Account type', 'residency': 'Residency', 'industry': 'SIC code', 'personal': 'Customer type',
                                            'currency': 'Currency', 'gl': 'Ethix GL', 'risk': 'Risk grade'}},
    'DEPOSIT': {'label': 'Deposit file', 'dims': {'product': 'Account type', 'residency': 'Residency', 'industry': 'SIC code', 'personal': 'Customer type',
                                                  'currency': 'Currency', 'gl': 'Ethix GL'}},
    'TB': {'label': 'Trial balance (Ethix GL)', 'dims': {'gl': 'Ethix GL', 'dkbgl': 'DKBGL line (via GL mapping)', 'currency': 'Currency'}},
    'CATEG': {'label': 'Category entries', 'dims': {'pl_category': 'PL category', 'product_category': 'Product category', 'event_type': 'Event type',
                                                    'company': 'Company', 'system_id': 'System ID'}},
    'GL_LINES': {'label': 'GL Report lines (DKBGL)', 'dims': {'line': 'DKBGL line'}},
}


def _paths(root):
    from .rebuild_run import Paths
    return Paths(root)


def _key(root, *extra):
    p = _paths(root)
    return (str(p.bank), p.bank.stat().st_mtime if p.bank.exists() else None, p.store.stat().st_mtime if p.store.exists() else None) + extra


def dictionaries(root):
    """{'category': {code: desc}, 'category_ranges': [(lo, hi, desc)], 'sector': {code: name}, 'gl': {gl10: desc}, 'gl_dkbgl': {...}}"""
    p = _paths(root)
    k = _key(root, 'dict')
    if k in _CACHE:
        return _CACHE[k]
    out = {'category': {}, 'category_ranges': [], 'sector': {}, 'gl': {}, 'dkbgl_of_gl': {}, 'line': {}, 'gl_mapping_sha': None}
    if p.store.exists():
        with closing(connect(p.store)) as c:
            d = gl_mapping.latest(c)
            out['gl_mapping_sha'] = d
            if d:
                for code, to, desc, group in c.execute('SELECT code, code_to, description, range_group FROM t24_categories WHERE source_sha256=?', (d,)):
                    if to:
                        out['category_ranges'].append((int(code), int(to), f'{desc or group}'))
                    else:
                        out['category'][code] = desc or ''
                for code, name, ctype, gl in c.execute('SELECT code, name, customer_type, gl_class FROM t24_sectors WHERE source_sha256=?', (d,)):
                    out['sector'][code] = f'{name} ({gl or ctype})'
                for gl10, desc, dk in c.execute('SELECT gl10, max(description), max(dkbgl) FROM gl_accounts WHERE source_sha256=? AND gl10 IS NOT NULL GROUP BY gl10', (d,)):
                    out['gl'][gl10] = desc or ''
                    out['dkbgl_of_gl'][gl10] = dk
                for line, typ, desc in c.execute('SELECT line, type, description FROM gl_lines WHERE source_sha256=?', (d,)):
                    out['line'][line] = f'{desc or ""}'
    _CACHE[k] = out
    return out


def describe(root, dim, code):
    d = dictionaries(root)
    if code in (None, ''):
        return '(blank)'
    if dim == 'category':
        if code in d['category']:
            return d['category'][code]
        if str(code).isdigit():
            for lo, hi, desc in d['category_ranges']:
                if lo <= int(code) <= hi:
                    return desc + ' (range)'
    if dim in ('sector',):
        return d['sector'].get(code, '')
    if dim == 'gl':
        return d['gl'].get(code, '')
    if dim in ('line', 'dkbgl'):
        return d['line'].get(code, '')
    if dim in ('pl_category', 'product_category'):
        return describe(root, 'category', code)
    return ''


def explore(root, dataset, dim, contains='', limit=400):
    """Rows: value, description, records, amount (and per-balance-type totals for ECB)."""
    if dataset not in DATASETS or (dim not in DATASETS[dataset]['dims']):
        raise ValueError('Unknown dataset or dimension')
    k = _key(root, 'explore', dataset, dim)
    if k not in _CACHE:
        _CACHE[k] = _explore(root, dataset, dim)
    rows = _CACHE[k]
    if contains:
        c = contains.lower()
        rows = [r for r in rows if c in str(r['value']).lower() or c in (r['description'] or '').lower()]
    return rows[:limit], len(rows)


def _explore(root, dataset, dim):
    p = _paths(root)
    out = []
    if dataset in ('ECB', 'LOAN', 'DEPOSIT', 'TB'):
        if not p.bank.exists():
            raise ValueError('The account database has not been built yet (Sources page)')
        with closing(open_bank_readonly(p.bank)) as b:
            if dataset == 'ECB':
                agg = defaultdict(lambda: {'records': 0, 'types': defaultdict(float)})
                for row in b.execute("SELECT category, sector, country, currency, company, components FROM unique_records WHERE source='ECB'"):
                    comps = json.loads(row[5] or '{}')
                    if dim == 'balance_type':
                        for t, v in comps.items():
                            if v:
                                a = agg[t]
                                a['records'] += 1
                                a['types'][t] += v
                        continue
                    val = {'category': row[0], 'sector': row[1], 'country': row[2], 'currency': row[3], 'company': row[4]}[dim]
                    a = agg[val]
                    a['records'] += 1
                    for t, v in comps.items():
                        if v:
                            a['types'][t] += v
                for val, a in agg.items():
                    top = sorted(a['types'].items(), key=lambda x: -abs(x[1]))[:6]
                    out.append({'value': val, 'description': describe(root, dim, val) if dim != 'balance_type' else '', 'records': a['records'],
                                'amount': sum(a['types'].values()) if dim == 'balance_type' else None,
                                'balance_types': ', '.join(f'{t} {v:,.0f}' for t, v in top)})
            elif dataset in ('LOAN', 'DEPOSIT'):
                for val, n, amt in b.execute(f'SELECT {dim}, count(*), sum(amount) FROM unique_records WHERE source=? GROUP BY {dim}', (dataset,)):
                    out.append({'value': val, 'description': describe(root, 'gl' if dim == 'gl' else dim, val), 'records': n, 'amount': amt, 'balance_types': ''})
            else:
                d = dictionaries(root)
                agg = defaultdict(lambda: [0, 0.0])
                for gl, cur, amt in b.execute("SELECT gl, currency, amount FROM unique_records WHERE source='TB'"):
                    val = {'gl': gl, 'currency': cur, 'dkbgl': d['dkbgl_of_gl'].get(gl) or '(not in GL mapping)'}[dim]
                    agg[val][0] += 1
                    agg[val][1] += amt or 0
                for val, (n, amt) in agg.items():
                    out.append({'value': val, 'description': describe(root, 'gl' if dim == 'gl' else dim, val), 'records': n, 'amount': amt, 'balance_types': ''})
    elif dataset == 'CATEG':
        with closing(connect(p.store)) as c:
            sha = c.execute("SELECT source_sha256 FROM sources WHERE dataset='CATEG_ENTRY' ORDER BY imported_at DESC").fetchone()
            if not sha:
                raise ValueError('No category entries imported yet (Sources page)')
            for val, n, amt in c.execute(f'SELECT {dim}, count(*), sum(amount_micro) FROM categ_events WHERE source_sha256=? GROUP BY {dim}', (sha[0],)):
                out.append({'value': val, 'description': describe(root, dim, val), 'records': n, 'amount': (amt or 0) / 1e6, 'balance_types': ''})
    elif dataset == 'GL_LINES':
        out = gl_lines(root)
    if dataset != 'GL_LINES':
        out.sort(key=lambda r: -abs(r['amount'] or 0) if r.get('amount') is not None else -r['records'])
    return out


def gl_lines(root):
    """Every DKBGL line with its criteria in words, the trial balance mapped to it, and (when computed) the ECB amount."""
    p = _paths(root)
    d = dictionaries(root)
    if not d['gl_mapping_sha']:
        raise ValueError('No GL mapping workbook imported yet (Sources page)')
    tb = defaultdict(float)
    if p.bank.exists():
        with closing(open_bank_readonly(p.bank)) as b:
            for gl, amt in b.execute("SELECT gl, amount FROM unique_records WHERE source='TB'"):
                tb[d['dkbgl_of_gl'].get(gl)] += amt or 0
    ecb = load_line_amounts(root)
    out = []
    with closing(connect(p.store)) as c:
        crit = defaultdict(list)
        for line, seq, cat, plcat, sec, bal in c.execute('SELECT line, seq, category, plcategory, sector, balance FROM gl_criteria WHERE source_sha256=? ORDER BY line, seq', (d['gl_mapping_sha'],)):
            crit[line].append(' '.join(x for x in (f'category {cat}' if cat else '', f'PL {plcat}' if plcat else '', f'sector {sec}' if sec else '', f'balance {bal}' if bal else '') if x))
        for line, typ, desc, seq in c.execute('SELECT line, type, description, seq FROM gl_lines WHERE source_sha256=? ORDER BY seq', (d['gl_mapping_sha'],)):
            e = ecb.get(line)
            out.append({'value': line, 'description': f'{desc or ""} [{typ}]', 'records': len(crit[line]), 'amount': e['amount'] if e else None,
                        'tb_amount': tb.get(line), 'balance_types': ' | '.join(crit[line])[:400], 'seq': seq, 'notes': '; '.join(e['notes']) if e else ''})
    out.sort(key=lambda r: r['seq'])
    return out


def _line_file(root):
    return _paths(root).data / 'gl_line_amounts.json'


def load_line_amounts(root):
    f = _line_file(root)
    if not f.exists():
        return {}
    doc = json.loads(f.read_text(encoding='utf-8'))
    p = _paths(root)
    if doc.get('bank_mtime') != (p.bank.stat().st_mtime if p.bank.exists() else None):
        return {}
    return doc['lines']


def compute_line_amounts(root, log=print):
    """Evaluate every DKBGL line's criteria on the ECB balances (sum of the named balance types). Takes a few minutes."""
    from .rebuild_run import FactCache
    p = _paths(root)
    facts = FactCache.get(p, '2026-09-30')
    out = {}
    with closing(connect(p.store)) as c:
        sha = gl_mapping.latest(c)
        lines = [r[0] for r in c.execute("SELECT line FROM gl_lines WHERE source_sha256=? AND type='D' ORDER BY seq", (sha,))]
        for i, line in enumerate(lines, start=1):
            parts, notes = gl_mapping.line_parts(c, sha, line)
            total = 0.0
            n = 0
            for part in parts:
                spec = dict(part, negative_filter=None, notes=[], path='')
                rows, errs, missing = facts.rows(spec)
                total += sum(r['amount'] or 0 for r in rows)
                n += len(rows)
                if missing:
                    notes.append('balance types not in the ECB extract: ' + ', '.join(missing))
            out[line] = {'amount': total, 'records': n, 'notes': list(dict.fromkeys(notes))}
            if i % 25 == 0:
                log(f'{i} of {len(lines)} GL lines')
    _line_file(root).write_text(json.dumps({'bank_mtime': p.bank.stat().st_mtime, 'lines': out}), encoding='utf-8')
    _CACHE.clear()
    return {'lines': len(out)}


def options(root):
    """Pick-lists for the logic builder, with descriptions and sizes."""
    k = _key(root, 'options')
    if k in _CACHE:
        return _CACHE[k]
    o = {}
    for ds, dim, name in (('ECB', 'category', 'categories'), ('ECB', 'sector', 'sectors'), ('ECB', 'balance_type', 'balance_types'),
                          ('ECB', 'country', 'countries'), ('LOAN', 'product', 'loan_products'), ('DEPOSIT', 'product', 'deposit_products'),
                          ('TB', 'gl', 'gls'), ('CATEG', 'pl_category', 'pl_categories'), ('CATEG', 'event_type', 'event_types')):
        try:
            rows, _ = explore(root, ds, dim, limit=3000)
        except ValueError:
            rows = []
        o[name] = [{'value': r['value'], 'label': f"{r['value']} - {r['description'] or ''}".strip(' -') + f"  ({r['records']:,} rec{', ' + format(r['amount'], ',.0f') if r.get('amount') is not None else ''})"}
                   for r in rows if r['value'] not in (None, '')]
    try:
        o['gl_lines'] = [{'value': r['value'], 'label': f"{r['value']} - {r['description']}"} for r in gl_lines(root) if '[D]' in r['description']]
    except ValueError:
        o['gl_lines'] = []
    _CACHE[k] = o
    return o
