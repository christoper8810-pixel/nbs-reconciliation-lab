"""Engine B - INTERNAL_CUS_ACC: one-to-one account mapping.

Source internal account -> exact account mapping -> target account / GL -> expected -> actual.
CONSOL_KEY is never generated, required or read here, and no AC / PRODUCT_S3 rule or asset-type
allocation applies. A missing CONSOL_KEY is not an internal-account defect.

When CUSTOMER_ACCOUNT_REF is populated (for example Nostro / Vostro), the reference is resolved
through the authoritative customer-account mapping - no extra flag is needed.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from decimal import Decimal

from .tables import amount, text
from .criteria import split_items

ZERO = Decimal(0)


def _index(rows, key_col, kind):
    idx = defaultdict(list)
    for r in rows or []:
        k = text(r.get(key_col)).upper()
        if k:
            idx[k].append(r)
    return idx


def _resolve(entries):
    """Return (status, target_account, target_gl, detail) from the mapping rows for one source account."""
    if not entries:
        return 'MISSING_MAPPING', '', '', 'No mapping row for this account'
    targets = {(text(e.get('TARGET_ACCOUNT')).upper(), text(e.get('TARGET_GL')).upper()) for e in entries}
    if len(targets) > 1:
        return 'DUPLICATE_MAPPING', '', '', 'Conflicting mapping rows: ' + '; '.join(f'{a or "-"} / {g or "-"}' for a, g in sorted(targets))
    acct, gl = targets.pop()
    gls = split_items(gl) if gl else []
    if len(gls) > 1:
        return 'INVALID_TARGET', acct, '', f'One-to-one mapping lists several target GLs: {gl}'
    if not gls and not acct:
        return 'INVALID_TARGET', '', '', 'Mapping row has neither target account nor target GL'
    note = 'Duplicate identical mapping rows' if len(entries) > 1 else ''
    return 'MAPPED', acct, gls[0] if gls else '', note


def run(rows, meta, mapping_rows, customer_rows, actual_account_rows, cfg):
    out = {'engine': 'B', 'name': 'INTERNAL_CUS_ACC one-to-one accounts'}
    if rows is None:
        out.update(status='SOURCE_PENDING', reason='No internal-account balance file supplied')
        return out
    if mapping_rows is None and customer_rows is None:
        out.update(status='SOURCE_PENDING', reason='No internal-account mapping file supplied')
        return out
    imap = _index(mapping_rows, 'ACCOUNT_NO', 'internal')
    cmap = _index(customer_rows, 'ACCOUNT_NO', 'customer')
    acct_gl = {}
    actual_acct = defaultdict(lambda: ZERO)
    for r in actual_account_rows or []:
        ta = text(r.get('TARGET_ACCOUNT')).upper()
        if ta:
            actual_acct[ta] += amount(r.get('BALANCE')) or ZERO
            if text(r.get('TARGET_GL')):
                acct_gl[ta] = text(r.get('TARGET_GL')).upper()
    sign = Decimal(str((cfg.get('sign_convention') or {}).get('internal_balances', 1)))
    comps, stats = [], Counter()
    status_amt = defaultdict(lambda: ZERO)
    expected = defaultdict(lambda: ZERO)
    expected_acct = defaultdict(lambda: ZERO)
    population = defaultdict(lambda: ZERO)
    seen = Counter()
    raw_total = ZERO
    missing_amount = 0
    target_sources = defaultdict(set)
    for row in rows:
        acct = text(row.get('ACCOUNT_NO')).upper()
        ccy = text(row.get('CURRENCY')).upper()
        a = amount(row.get('BALANCE'))
        if a is None:
            missing_amount += 1
            continue
        raw_total += a
        a = a * sign
        seen[acct] += 1
        cref = text(row.get('CUSTOMER_ACCOUNT_REF')).upper()
        if cref:
            status, tacct, tgl, detail = _resolve(cmap.get(cref))
            via = 'CUSTOMER_ACCOUNT_MAPPING'
            if status == 'MISSING_MAPPING':
                status, detail = 'CUSTOMER_REF_UNRESOLVED', f'Customer account reference {cref} not in the authoritative account mapping'
        else:
            status, tacct, tgl, detail = _resolve(imap.get(acct))
            via = 'INTERNAL_ACCOUNT_MAPPING'
        if status == 'MAPPED' and not tgl and tacct in acct_gl:
            tgl = acct_gl[tacct]
            detail = (detail + '; ' if detail else '') + 'target GL taken from the actual target-account list'
        if status == 'MAPPED' and not tgl:
            status, detail = 'INVALID_TARGET', 'Target GL cannot be determined for the mapped target account'
        flags = []
        m = re.match(r'^([A-Z]{3})\d', tacct or '')
        if status == 'MAPPED' and m and ccy and m.group(1) != ccy:
            flags.append('TARGET_ACCOUNT_CURRENCY_MISMATCH')
        if status == 'MAPPED' and tacct in acct_gl and acct_gl[tacct] != tgl:
            flags.append('TARGET_ACCOUNT_GL_DIFFERS_FROM_ACTUAL')
        c = {'engine': 'B', 'source_row': row['_row'], 'account': acct, 'ref': cref or acct, 'legacy_gl': text(row.get('LEGACY_GL')),
             'currency': ccy, 'balance_type': '', 'amount': a, 'status': status, 'contra': False, 'rule_id': via if status == 'MAPPED' else '',
             'line': '', 'target_gl': tgl if status == 'MAPPED' else '', 'target_account': tacct if status == 'MAPPED' else '',
             'candidates': [], 'candidate_rules': [], 'reason': detail, 'flags': flags, 'via': via,
             'customer_ref': cref}
        if status == 'MAPPED':
            expected[(tgl, ccy)] += a
            if tacct:
                expected_acct[tacct] += a
                target_sources[tacct].add(acct)
        stats[status] += 1
        status_amt[status] += a
        if c['legacy_gl']:
            population[(c['legacy_gl'], ccy)] += a
        comps.append(c)
    dups = {k for k, n in seen.items() if n > 1}
    for c in comps:
        c['duplicate_source'] = c['account'] in dups
    account_recon = []
    tol = Decimal(str((cfg.get('tolerance') or {}).get('absolute', '0.01')))
    if actual_account_rows is not None:
        for ta in sorted(set(expected_acct) | set(actual_acct)):
            e, ac = expected_acct.get(ta, ZERO), actual_acct.get(ta, ZERO)
            d = ac - e
            account_recon.append({'target_account': ta, 'expected': e, 'actual': ac, 'difference': d,
                                  'status': 'RECONCILED' if abs(d) <= tol else ('EXPECTED_ONLY' if ta not in actual_acct else
                                                                               'ACTUAL_ONLY' if ta not in expected_acct else 'DIFFERENCE'),
                                  'sources': sorted(target_sources.get(ta, ()))})
    many_to_one = {k: sorted(v) for k, v in target_sources.items() if len(v) > 1}
    out.update(status='COMPLETE', components=comps, expected=dict(expected), population=dict(population),
               stats=dict(stats), status_amounts=dict(status_amt), account_reconciliation=account_recon,
               many_to_one_targets=many_to_one,
               controls_input={'rows': len(rows), 'raw_total': raw_total, 'missing_amount_rows': missing_amount,
                               'duplicate_source_accounts': len(dups), 'sign': sign,
                               'consol_key_used': False},
               mapping_rows=sum(len(v) for v in imap.values()), customer_mapping_rows=sum(len(v) for v in cmap.values()))
    return out
