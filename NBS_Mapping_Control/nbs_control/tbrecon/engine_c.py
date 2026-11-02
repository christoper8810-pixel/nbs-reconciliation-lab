"""Engine C - PL reconciliation with its own PL key layout and PL rules.

The PL CONSOL.KEY is parsed with the configured PL layout (never the AC positions). Dimensions not
present in that layout (for example sector, residence) are only available from explicit source
columns; a rule restricting a dimension the source cannot supply is DIMENSION_NOT_AVAILABLE.
No asset-type logic is applied. A missing PL source gives SOURCE_PENDING, never success.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal

from . import rules as R
from .tables import amount, text

DIMS = ['PL_CATEGORY', 'PRODUCT', 'DEPARTMENT', 'SECTOR', 'RESIDENCE', 'CURRENCY', 'COMPANY']
ZERO = Decimal(0)


def run(rows, meta, rule_rows, rule_meta, cfg, layout):
    out = {'engine': 'C', 'name': 'PL'}
    if rows is None:
        out.update(status='SOURCE_PENDING', reason='No PL source file supplied: PL GLs cannot be reconciled')
        return out
    if rule_rows is None:
        out.update(status='SOURCE_PENDING', reason='No PL mapping rule file supplied')
        return out
    explicit = [d for d in DIMS if d in meta['headers']]
    available = set(layout.segments) | {d.lower() for d in explicit}
    dim_cols = [d for d in DIMS if d in rule_meta['headers']]
    rs = R.load(rule_rows, dim_cols, cfg, with_bt=False, available_dims=available)
    rs.index()
    sign = Decimal(str((cfg.get('sign_convention') or {}).get('pl_balances', 1)))
    comps, stats = [], Counter()
    status_amt = defaultdict(lambda: ZERO)
    expected = defaultdict(lambda: ZERO)
    population = defaultdict(lambda: ZERO)
    unresolved_by_gl = defaultdict(lambda: ZERO)
    conflicts = Counter()
    raw_total = ZERO
    missing_amount = 0
    for row in rows:
        key = text(row.get('CONSOL_KEY'))
        a = amount(row.get('BALANCE'))
        if a is None:
            missing_amount += 1
            continue
        raw_total += a
        a = a * sign
        err = None
        dims = {}
        if key:
            dims, _tokens, err = layout.parse(key)
            dims = dict(dims)
        for d in explicit:
            v = text(row.get(d)).upper()
            dl = d.lower()
            if dl in dims and dims[dl] and v and dims[dl] != v:
                conflicts[dl] += 1
            elif v and not dims.get(dl):
                dims[dl] = v
        if not key and not explicit:
            err = 'NO_PL_KEY_OR_DIMENSIONS'
        ccy = (dims.get('currency') or text(row.get('CURRENCY'))).upper()
        if err:
            status, top = 'INVALID_KEY', []
        else:
            status, top = rs.match(dims, None, memo_key=key + '|' + '|'.join(dims.get(d.lower(), '') for d in explicit))
        c = {'engine': 'C', 'source_row': row['_row'], 'account': text(row.get('ACCOUNT_NO')), 'ref': key, 'legacy_gl': text(row.get('LEGACY_GL')),
             'currency': ccy, 'balance_type': '', 'amount': a, 'status': status, 'contra': False,
             'rule_id': top[0].id if status == 'MAPPED' else '', 'line': top[0].line if status == 'MAPPED' else '',
             'target_gl': top[0].targets[0] if status == 'MAPPED' else '',
             'candidates': sorted({t for r in top for t in r.targets}) if status != 'MAPPED' else [],
             'candidate_rules': [r.id for r in top] if status != 'MAPPED' else [], 'reason': err or '', 'dims': dims,
             'duplicate_source': False}
        if status == 'MAPPED':
            expected[(c['target_gl'], ccy)] += a
        else:
            for g in c['candidates']:
                unresolved_by_gl[(g, ccy)] += a
        stats[status] += 1
        status_amt[status] += a
        if c['legacy_gl']:
            population[(c['legacy_gl'], ccy)] += a
        comps.append(c)
    incomplete = defaultdict(set)
    for (g, _c) in unresolved_by_gl:
        incomplete[g].add('unresolved ambiguous / multi-target PL allocation candidates')
    for r in rs.rules:
        if r.unavailable:
            for g in r.targets:
                incomplete[g].add(f'PL rule {r.id} needs dimensions not in the PL source: {", ".join(r.unavailable)}')
    out.update(status='COMPLETE', components=comps, expected=dict(expected), population=dict(population), ruleset=rs,
               rule_diagnostics=rs.diagnostics, stats=dict(stats), status_amounts=dict(status_amt),
               unresolved_by_gl=dict(unresolved_by_gl), incomplete_gls={k: sorted(v) for k, v in incomplete.items()},
               controls_input={'rows': len(rows), 'raw_total': raw_total, 'missing_amount_rows': missing_amount,
                               'key_field_conflicts': dict(conflicts), 'sign': sign},
               layout=layout.describe(), explicit_dimension_columns=explicit)
    return out
