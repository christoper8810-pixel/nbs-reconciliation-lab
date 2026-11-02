"""BO-generated report: import and comparison with the expected allocation of the workbook conditions.

The comparison grain is the report line plus every dimension the BO report and the source both carry
(currency, branch, company ...). If the BO report has only line totals, the reconciliation is at line level
and causes that need detail are reported as evidence requests, never guessed. Amounts are never forced to agree.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal

from ..tbrecon.tables import amount, read_table, text
from .compiler import DIMS
from .sources import HEADER_DIMS

LINE_HEADERS = ('LINE', 'DKBGL', 'REPORT_LINE', 'LINE_ID', 'LINE_NO', 'GL_LINE', 'QCB_ITEM_CODE', 'ITEM_CODE', 'RULE_ID')
AMOUNT_HEADERS = ('BALANCE', 'VALUE', 'TOTAL', 'LCY_AMOUNT', 'AMOUNT_QAR', 'NET_AMOUNT')
ZERO = Decimal(0)


def load(path):
    rows, meta = read_table(path)
    hdr = meta['headers']
    line_col = next((h for h in LINE_HEADERS if h in hdr), None)
    amt_col = next((h for h in AMOUNT_HEADERS if h in hdr), None)
    if not line_col or not amt_col:
        raise ValueError(f'BO report {meta["name"]}: needs a report-line column ({", ".join(LINE_HEADERS[:4])} ...) and an amount column '
                         f'(AMOUNT / BALANCE / VALUE); found {", ".join(hdr)}')
    dims = {h: HEADER_DIMS[h] for h in hdr if h in HEADER_DIMS and h != line_col}
    out, dup = [], Counter()
    for r in rows:
        line = text(r.get(line_col))
        a = amount(r.get(amt_col))
        if not line:
            continue
        rec = {'line': line, 'amount': a, 'row': r['_row'], 'dims': {d: (text(r.get(h)).upper() or None) for h, d in dims.items()},
               'date': text(r.get('BUSINESS_DATE'))[:10]}
        dup[(line, tuple(sorted(rec['dims'].items())), a)] += 1
        out.append(rec)
    return out, {'name': meta['name'], 'sha256': meta['sha256'], 'rows': len(out), 'line_column': line_col, 'amount_column': amt_col,
                 'dimensions': sorted(set(dims.values())), 'exact_duplicate_rows': sum(n - 1 for n in dup.values() if n > 1),
                 'dates': sorted({x['date'] for x in out if x['date']}), 'missing_amounts': sum(1 for x in out if x['amount'] is None)}


def grain(bo_meta, src_dims):
    """Dimensions used for the comparison: those both in the BO report and in the source records."""
    return [d for d in DIMS if d in bo_meta['dimensions'] and d in src_dims]


def actual(bo_rows, key_dims, scale=Decimal(1), sign=Decimal(1)):
    A = defaultdict(lambda: ZERO)
    rows_of = defaultdict(list)
    dup = Counter()
    for r in bo_rows:
        k = (r['line'],) + tuple(r['dims'].get(d) or '' for d in key_dims)
        if r['amount'] is not None:
            A[k] += r['amount'] * scale * sign
        rows_of[k].append(r['row'])
        dup[(k, r['amount'])] += 1
    dups = defaultdict(lambda: ZERO)
    for (k, a), n in dup.items():
        if n > 1 and a is not None:
            dups[k] += a * (n - 1) * scale * sign
    return dict(A), rows_of, dict(dups)


def compare(model, E, A, tol):
    rows = []
    for k in sorted(set(E) | set(A), key=lambda x: tuple(str(y) for y in x)):
        e, a = E.get(k, ZERO), A.get(k)
        line = model.lines.get(k[0])
        d = (a or ZERO) - e
        if line is None:
            if a is None and not e:
                continue
            st = 'LINE_NOT_IN_MAPPING'
        elif a is None:
            st = 'MISSING_IN_BO' if e else 'MATCHED'
        elif abs(d) <= tol:
            st = 'MATCHED'
        elif k not in E:
            st = 'NOT_EXPECTED'
        else:
            st = 'DIFFERENCE'
        rows.append({'key': k, 'line': k[0], 'line_type': line['type'] if line else '', 'expected': e, 'actual': a,
                     'difference': d, 'status': st})
    return rows


def detect_scale_sign(E, A, tol):
    """Global presentation checks: thousands scaling and reversed sign (reported, never applied automatically)."""
    common = [k for k in A if k in E and E[k] and A[k]]
    out = {}
    if common:
        thousand = sum(1 for k in common if abs(A[k] * 1000 - E[k]) <= max(tol * 1000, abs(E[k]) * Decimal('0.0005')))
        rev = sum(1 for k in common if abs(A[k] + E[k]) <= tol)
        if thousand >= max(3, len(common) * 0.6):
            out['scale'] = {'finding': 'BO amounts are expected / 1000 on most lines', 'lines': thousand, 'of': len(common)}
        if rev >= max(3, len(common) * 0.6):
            out['sign'] = {'finding': 'BO amounts are the negative of expected on most lines', 'lines': rev, 'of': len(common)}
    return out
