"""Supporting source records (CSV / XLSX) -> signatures for the expected BO allocation.

Accepted layouts, detected from the headers:
* long: one amount per row (AMOUNT / BALANCE ...) with dimension columns (CATEGORY, SECTOR, BALANCE_TYPE, CURRENCY,
  COMPANY, BRANCH, DAO, DEPARTMENT, PRODUCT, RESIDENCE, SEGMENT, PL_CATEGORY ..., LEGACY_GL / OLD_GL);
* wide ECB / PRODUCT_S3: <TYPE>_BAL_QAR columns are unpivoted into BALANCE_TYPE rows (non-zero cells only);
  CONSOL_KEY fills dimensions that have no explicit column, using the configured AC layout (config/tb_recon.json).
Blank amounts are missing (never zero) and reported.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal

from ..tbrecon.tables import amount, read_table, text
from .compiler import DIMS
from .engine import Sig

HEADER_DIMS = {d.upper(): d for d in DIMS}
HEADER_DIMS.update({'BAL_TYPE': 'balance_type', 'BALANCETYPE': 'balance_type', 'ASSET_TYPE': 'balance_type', 'CCY': 'currency',
                    'CATEG': 'category', 'DEPT': 'department', 'ACCOUNT_OFFICER': 'dao', 'RESIDENCY': 'residence',
                    'PL_CATEGORY': 'pl_category', 'PLCATEGORY': 'pl_category', 'PL_PRODUCT': 'pl_product',
                    'PL_SECTOR': 'pl_sector', 'PL_DEPARTMENT': 'pl_department', 'CO_CODE': 'company', 'BRANCH_CODE': 'branch'})
SUFFIX = '_BAL_QAR'
ZERO = Decimal(0)


def load(paths, cfg=None, layout=None):
    """Return (sigs, report). layout: tbrecon KeyLayout for CONSOL_KEY (optional)."""
    groups, report = {}, {'files': [], 'rows': 0, 'records': 0, 'missing_amounts': 0, 'key_errors': Counter(), 'dates': Counter()}
    for p in paths:
        rows, meta = read_table(p)
        hdr = meta['headers']
        dims = {h: HEADER_DIMS[h] for h in hdr if h in HEADER_DIMS}
        bt_cols = [h for h in hdr if h.endswith(SUFFIX)]
        amount_col = 'BALANCE' if 'BALANCE' in hdr else None
        info = {'name': meta['name'], 'sha256': meta['sha256'], 'rows': meta['rows'], 'layout': 'WIDE' if bt_cols else 'LONG',
                'dimension_columns': sorted(set(dims.values())), 'unused_columns': [h for h in hdr if h not in dims and h not in bt_cols
                                                                                   and h not in ('BALANCE', 'ACCOUNT_NO', 'LEGACY_GL',
                                                                                                 'CONSOL_KEY', 'BUSINESS_DATE')]}
        if not bt_cols and not amount_col:
            raise ValueError(f'{meta["name"]}: no amount column (AMOUNT / BALANCE) and no <TYPE>{SUFFIX} columns')
        report['files'].append(info)
        for r in rows:
            report['rows'] += 1
            base = {d: text(r.get(h)).upper() for h, d in dims.items()}   # '' = column present but blank (known empty)
            if text(r.get('LEGACY_GL')):
                base['legacy_gl'] = text(r['LEGACY_GL']).upper()
            key = text(r.get('CONSOL_KEY'))
            if key and layout is not None:
                kd, _t, err = layout.parse(key)
                if err:
                    report['key_errors'][err] += 1
                for d, v in kd.items():
                    if d in DIMS and not base.get(d) and v:
                        base[d] = v
            if text(r.get('BUSINESS_DATE')):
                report['dates'][text(r['BUSINESS_DATE'])[:10]] += 1
            acct = text(r.get('ACCOUNT_NO'))
            ref = f'{meta["name"]}:{r["_row"]}'
            if bt_cols:
                for col in bt_cols:
                    a = amount(r.get(col))
                    if a is None or a == 0:
                        continue
                    _add(groups, {**base, 'balance_type': col[:-len(SUFFIX)]}, a, acct, ref)
            else:
                a = amount(r.get(amount_col))
                if a is None:
                    report['missing_amounts'] += 1
                    continue
                _add(groups, base, a, acct, ref)
    sigs = list(groups.values())
    for i, s in enumerate(sigs):
        s.id = i
    report['records'] = sum(s.count for s in sigs)
    report['signatures'] = len(sigs)
    report['key_errors'] = dict(report['key_errors'])
    report['dates'] = dict(report['dates'])
    report['total_amount'] = sum((s.amount for s in sigs), ZERO)
    return sigs, report


def _add(groups, dims, a, acct, ref):
    k = tuple(sorted((d, v) for d, v in dims.items() if v is not None))
    s = groups.get(k)
    if s is None:
        s = groups[k] = Sig(len(groups), dict(k))
    s.amount += a
    s.count += 1
    if acct and len(s.accounts) < 25:
        s.accounts.append(acct)
    if len(s.refs) < 25:
        s.refs.append(ref)
