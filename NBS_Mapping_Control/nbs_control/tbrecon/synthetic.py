"""Deterministic SYNTHETIC datasets for regression tests and demonstrations. No bank data.

Every account, GL, key and amount is invented (company SYN0010001, accounts SYN...). The generator
computes the TRUE expected balance of every target GL itself, from its own design, independently of
the reconciliation engine; tests compare the engine's reconstruction with that truth.

Scenarios:
* clean   - correct rules and mappings; everything reconciles after the post-COB roll-forward.
* defects - the same bank with injected mapping / data defects (D01..D19 below) and a correct actual TB.
"""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

COMPANY = 'SYN0010001'
CUTOVER = '2026-09-30'
TB_DATE = '2026-10-01'
Q = Decimal('0.01')

DEFECTS = {
    'D01': 'PRODUCT / SECTOR misalignment: corporate rule L120 has product codes in its SECTOR column, PRODUCT blank',
    'D02': 'Ambiguous rule L170 (QAR principal, category 3700-3799) as specific as L110',
    'D03': 'Multi-target continuation rule on L130 (category 3800-3899) without allocation evidence',
    'D04': 'Unsupported balance type GRCACCOUNT added to the *PRINCIPAL group',
    'D05': 'Source balance type PDODEFERREDPFT has no rule',
    'D06': 'Contra rule L150 (BLCURACCOUNT) removed',
    'D07': 'Two asset rows with a truncated CONSOL_KEY',
    'D08': 'One asset row duplicated in the extract',
    'D09': 'Actual TB holds capital GL 3001000010 with the opposite sign',
    'D10': 'Actual TB books part of fixed assets to 1501000020 instead of 1501000010',
    'D11': 'Internal accounts: one missing mapping, one conflicting duplicate mapping, one wrong-currency target account',
    'D12': 'Nostro customer reference not in the authoritative customer-account mapping',
    'D13': 'Legacy GL LG-1600-001 maps to two target GLs and has no account-level population',
    'D14': 'One internal account missing from the internal-balance extract (present in the legacy TB)',
    'D15': 'Post-COB movements: one dated on cutover, one not validated (both in the actual TB)',
    'D16': 'Actual TB books part of OBS GL 9001000010 in USD instead of QAR',
    'D17': 'Legacy GL LG-1700-001 has no GL mapping and no population',
    'D18': 'PL record with a PL category no rule covers; PL rule restricting SECTOR (not in the PL layout)',
    'D19': 'Deposit continuation rule targets 2101000011, outside the authorised GL mapping of LG-2100-001',
}


def ac_key(ccy, cat, prod, sector, dept='14', res='QA', ind='47004', mat='2Y'):
    return '.'.join(['AC', '1', 'TR', ccy, str(cat), str(prod), str(sector), dept, res, ind, mat, '', '', '', '', '', COMPANY])


def pl_key(plcat, ccy, prod, dept='14'):
    return '.'.join(['PL', str(plcat), ccy, str(prod), dept] + [''] * 8 + [COMPANY])


def _amt(rng, lo, hi):
    return (Decimal(rng.randint(lo * 100, hi * 100)) / 100).quantize(Q)


def _write(path, cols, rows):
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow(['' if r.get(c) is None else (format(r[c], 'f') if isinstance(r[c], Decimal) else r[c]) for c in cols])


BT_COLS = ['CURACCOUNT', 'DUEACCOUNT', 'ACCPRINCIPALPFT', 'BLCURACCOUNT', 'CREDIT']


def build(folder, scenario='clean', seed=20261102):
    if scenario not in ('clean', 'defects'):
        raise ValueError('scenario must be clean or defects')
    D = scenario == 'defects'
    rng = random.Random(seed)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    truth = defaultdict(Decimal)             # (target_gl, ccy) -> correct migrated balance
    legacy = defaultdict(Decimal)            # (legacy_gl, ccy) -> legacy TB
    asset_rows = []
    bt_cols = BT_COLS + (['PDODEFERREDPFT'] if D else [])

    def asset(acct, key, lgl, ccy, comps, targets):
        row = {'ACCOUNT_NO': acct, 'ARRANGEMENT_ID': 'AA' + acct[-6:], 'CONSOL_KEY': key, 'LEGACY_GL': lgl}
        for bt in bt_cols:
            row[bt + '_BAL_QAR'] = comps.get(bt)
        asset_rows.append(row)
        for bt, a in comps.items():
            if a:
                legacy[(lgl, ccy)] += a
                if bt in targets:
                    truth[(targets[bt], ccy)] += a
    # retail murabaha (sector 1000, products 4101/4102)
    for i in range(40):
        ccy = 'USD' if i % 8 == 7 else 'QAR'
        cat = rng.choice([3701, 3713, 3755, 3799]) if i < 30 else rng.choice([3801, 3850, 3901])
        comps = {'CURACCOUNT': _amt(rng, 10_000, 500_000), 'ACCPRINCIPALPFT': _amt(rng, 100, 9_000)}
        if i % 3 == 0:
            comps['DUEACCOUNT'] = _amt(rng, 500, 20_000)
        if i % 5 == 0:
            comps['BLCURACCOUNT'] = -_amt(rng, 100, 5_000)
        if D and i in (4, 9, 14):
            comps['PDODEFERREDPFT'] = _amt(rng, 50, 2_000)
        asset(f'SYNR{i:06d}', ac_key(ccy, cat, 4101 + i % 2, 1000), 'LG-1100-001', ccy, comps,
              {'CURACCOUNT': '1101000010', 'DUEACCOUNT': '1101000010', 'ACCPRINCIPALPFT': '1101000030', 'BLCURACCOUNT': '1101000090',
               'PDODEFERREDPFT': '1101000070'})
    # corporate (sectors 2001-2005, products 5261/5262)
    for i in range(20):
        ccy = 'USD' if i % 4 == 3 else 'QAR'
        comps = {'CURACCOUNT': _amt(rng, 100_000, 2_000_000), 'ACCPRINCIPALPFT': _amt(rng, 1_000, 40_000)}
        if i % 4 == 0:
            comps['BLCURACCOUNT'] = -_amt(rng, 1_000, 20_000)
        asset(f'SYNC{i:06d}', ac_key(ccy, rng.choice([3702, 3720, 3790]), 5261 + i % 2, 2001 + i % 5), 'LG-1100-002', ccy, comps,
              {'CURACCOUNT': '1101000020', 'ACCPRINCIPALPFT': '1101000030', 'BLCURACCOUNT': '1101000090'})
    # deposits (credit balances are negative: debit-positive convention throughout)
    for i in range(30):
        ccy = 'USD' if i % 6 == 5 else 'QAR'
        cat = rng.choice([1001, 1010, 1049]) if i < 20 else rng.choice([1050, 1075, 1099])
        asset(f'SYND{i:06d}', ac_key(ccy, cat, 6001, 1000 if i % 2 else 2003), 'LG-2100-001', ccy,
              {'CREDIT': -_amt(rng, 1_000, 900_000)}, {'CREDIT': '2101000010'})
    if D:
        for r in asset_rows[5:7]:                                     # D07 truncated keys
            r['CONSOL_KEY'] = '.'.join(r['CONSOL_KEY'].split('.')[:6])
        asset_rows.append(dict(asset_rows[22]))                       # D08 duplicated extract row
    # ---------------- GL rules (GL Report H / D / T layout)
    R = []

    def rule(rid='', typ='', desc='', tgt='', bt='', cat='', prod='', sec='', ccy='', prio='', total='', rn='', rv=''):
        R.append({'RULE_ID': rid, 'TYPE': typ, 'DESCRIPTION': desc, 'TARGET_GL': tgt, 'BALANCE_TYPE': bt, 'CATEGORY': cat,
                  'PRODUCT': prod, 'SECTOR': sec, 'CURRENCY': ccy, 'PRIORITY': prio, 'TOTAL_OF': total,
                  'RANGE_NAME': rn, 'RANGE_VALUES': rv})
    rule(rn='PRINCIPAL', rv='CURACCOUNT, DUEACCOUNT' + (', GRCACCOUNT' if D else ''))   # D04
    rule('H100', 'H', 'Financing assets')
    rule('L110', 'D', 'Retail murabaha principal', '1101000010', '*PRINCIPAL', '3700-3799', sec='1000')
    rule(bt='*PRINCIPAL', cat='3800-3899, 3901', sec='1000')                            # continuation row
    if D:                                                                             # D01
        rule('L120', 'D', 'Corporate financing principal', '1101000020', '*PRINCIPAL', '3700-3799', sec='5261, 5262')
    else:
        rule('L120', 'D', 'Corporate financing principal', '1101000020', '*PRINCIPAL', '3700-3799', prod='5261, 5262')
    rule('L130', 'D', 'Accrued profit', '1101000030', 'ACCPRINCIPALPFT', '3700-3799')
    if D:                                                                             # D03
        rule(tgt='1101000030, 1101000031', bt='ACCPRINCIPALPFT', cat='3800-3899, 3901')
    else:
        rule(bt='ACCPRINCIPALPFT', cat='3800-3899, 3901')
    if not D:                                                                         # D06
        rule('L150', 'D', 'Contra: deferred / BL balances', '1101000090', 'BLCURACCOUNT', '3700-3899, 3901')
    if D:                                                                             # D02
        rule('L170', 'D', 'QAR financing (overlapping rule)', '1101000060', '*PRINCIPAL', '3700-3799', ccy='QAR')
    rule('T190', 'T', 'Total financing assets', total='L110..L170' if D else 'L110..L150')
    rule('H200', 'H', 'Customer deposits')
    rule('L210', 'D', 'Current and savings accounts', '2101000010', 'CREDIT', '1001-1049')
    rule(tgt='2101000011' if D else '', bt='CREDIT', cat='1050-1099')                 # D19
    rule('T290', 'T', 'Total customer deposits', total='L210')
    # ---------------- internal accounts (engine B)
    ib, imap, cmap, tacc = [], [], [], []
    for i in range(8):
        a = _amt(rng, 1_000, 80_000) * (1 if i % 2 else -1)
        src, tgt = f'SYNINT{i:04d}', f'QAR1900100010{i:03d}'
        legacy[('LG-1900-001', 'QAR')] += a
        truth[('1900000010', 'QAR')] += a
        if not (D and i == 6):                                                         # D14
            ib.append({'ACCOUNT_NO': src, 'CURRENCY': 'QAR', 'BALANCE': a, 'LEGACY_GL': 'LG-1900-001', 'CONSOL_KEY': ''})
        if not (D and i == 2):                                                         # D11 missing
            imap.append({'ACCOUNT_NO': src, 'TARGET_ACCOUNT': ('USD' if D and i == 4 else 'QAR') + tgt[3:],
                         'TARGET_GL': '1900000010'})
        if D and i == 3:                                                               # D11 conflicting duplicate
            imap.append({'ACCOUNT_NO': src, 'TARGET_ACCOUNT': f'QAR1900100099{i:03d}', 'TARGET_GL': '1900000020'})
        tacc.append({'TARGET_ACCOUNT': tgt, 'TARGET_GL': '1900000010', 'CURRENCY': 'QAR', 'BALANCE': a})
    for j in range(2):                                                                # Nostro via customer reference
        a = _amt(rng, 50_000, 3_000_000)
        ref = f'NOSTRO-SYN-{j:02d}'
        legacy[('LG-1200-001', 'USD')] += a
        truth[('1201000010', 'USD')] += a
        ib.append({'ACCOUNT_NO': f'SYNNOS{j:04d}', 'CURRENCY': 'USD', 'BALANCE': a, 'LEGACY_GL': 'LG-1200-001',
                   'CUSTOMER_ACCOUNT_REF': ref})
        if not (D and j == 1):                                                         # D12
            cmap.append({'ACCOUNT_NO': ref, 'TARGET_ACCOUNT': f'USD1200100010{j:03d}', 'TARGET_GL': '1201000010'})
        tacc.append({'TARGET_ACCOUNT': f'USD1200100010{j:03d}', 'TARGET_GL': '1201000010', 'CURRENCY': 'USD', 'BALANCE': a})
    # ---------------- PL (engine C)
    pl, plr = [], []
    for i in range(25):
        ccy = 'QAR'
        if i < 10:
            plcat, prod, tgt, lgl = 51001 + i * 5, 3701, '5101000010', 'LG-5100-001'
        elif i < 18:
            plcat, prod, tgt, lgl = 52000, rng.choice([3701, 3750, 3799]), '5201000010', 'LG-5200-001'
        else:
            plcat, prod, tgt, lgl = 52000, 6001, '5201000020', 'LG-5200-001'
        a = -_amt(rng, 1_000, 60_000)
        legacy[(lgl, ccy)] += a
        truth[(tgt, ccy)] += a
        pl.append({'CONSOL_KEY': pl_key(plcat, ccy, prod), 'BALANCE': a, 'LEGACY_GL': lgl})
    if D:                                                                             # D18
        a = -_amt(rng, 1_000, 9_000)
        legacy[('LG-5300-001', 'QAR')] += a
        truth[('5301000010', 'QAR')] += a
        pl.append({'CONSOL_KEY': pl_key(53010, 'QAR', 3701), 'BALANCE': a, 'LEGACY_GL': 'LG-5300-001'})
    plr.append({'RULE_ID': 'P510', 'TARGET_GL': '5101000010', 'PL_CATEGORY': '51000-51099', 'PRODUCT': '', 'DEPARTMENT': '', 'SECTOR': ''})
    plr.append({'RULE_ID': 'P520', 'TARGET_GL': '5201000010', 'PL_CATEGORY': '52000', 'PRODUCT': '3700-3799', 'DEPARTMENT': '', 'SECTOR': ''})
    plr.append({'RULE_ID': 'P521', 'TARGET_GL': '5201000020', 'PL_CATEGORY': '52000', 'PRODUCT': '', 'DEPARTMENT': '', 'SECTOR': ''})
    if D:
        plr.append({'RULE_ID': 'P590', 'TARGET_GL': '5901000010', 'PL_CATEGORY': '59000', 'PRODUCT': '', 'DEPARTMENT': '', 'SECTOR': '1000'})
    # ---------------- direct-stream legacy GLs (no account-level population)
    direct = [('LG-3000-001', 'QAR', '3001000010', -Decimal('5000000.00'), 'BS'),
              ('LG-1500-001', 'QAR', '1501000010', Decimal('750000.00'), 'BS'),
              ('LG-9000-001', 'QAR', '9001000010', Decimal('1200000.00'), 'OBS')]
    for lgl, ccy, tgt, a, _cls in direct:
        legacy[(lgl, ccy)] += a
        truth[(tgt, ccy)] += a
    if D:
        legacy[('LG-1600-001', 'QAR')] += Decimal('333000.00')                       # D13
        legacy[('LG-1700-001', 'QAR')] += Decimal('44000.00')                        # D17
        truth[('1601000010', 'QAR')] += Decimal('200000.00')
        truth[('1601000020', 'QAR')] += Decimal('133000.00')
        truth[('1701000010', 'QAR')] += Decimal('44000.00')
    gmap = [('LG-1100-001', '1101000010, 1101000030, 1101000090'), ('LG-1100-002', '1101000020, 1101000030, 1101000090'),
            ('LG-2100-001', '2101000010'), ('LG-1900-001', '1900000010'), ('LG-1200-001', '1201000010'),
            ('LG-5100-001', '5101000010'), ('LG-5200-001', '5201000010, 5201000020'), ('LG-3000-001', '3001000010'),
            ('LG-1500-001', '1501000010'), ('LG-9000-001', '9001000010')]
    if D:
        gmap += [('LG-1600-001', '1601000010, 1601000020'), ('LG-5300-001', '5301000010')]
        gmap = [(g, t + ', 1101000070' if g == 'LG-1100-001' else t) for g, t in gmap]
    cls_of = lambda gl: 'PL' if gl.startswith('5') else 'OBS' if gl.startswith('9') else 'BS'
    # ---------------- post-COB movements and actual TB (= truth + movements + actual-side defects)
    mov = [{'TARGET_GL': '1101000030', 'CURRENCY': 'QAR', 'BALANCE': Decimal('1234.56'), 'BUSINESS_DATE': TB_DATE,
            'MOVEMENT_TYPE': 'ACCRUAL', 'VALIDATED': 'Y'},
           {'TARGET_GL': '2101000010', 'CURRENCY': 'QAR', 'BALANCE': Decimal('-500.00'), 'BUSINESS_DATE': TB_DATE,
            'MOVEMENT_TYPE': 'POSTING', 'VALIDATED': 'Y'}]
    if D:                                                                             # D15
        mov += [{'TARGET_GL': '1501000010', 'CURRENCY': 'QAR', 'BALANCE': Decimal('-2500.00'), 'BUSINESS_DATE': CUTOVER,
                 'MOVEMENT_TYPE': 'POSTING', 'VALIDATED': 'Y'},
                {'TARGET_GL': '5101000010', 'CURRENCY': 'QAR', 'BALANCE': Decimal('-75.25'), 'BUSINESS_DATE': TB_DATE,
                 'MOVEMENT_TYPE': 'ACCRUAL', 'VALIDATED': 'N'}]
    actual = defaultdict(Decimal, truth)
    for m in mov:
        actual[(m['TARGET_GL'], m['CURRENCY'])] += m['BALANCE']
    if D:
        actual[('3001000010', 'QAR')] = -actual[('3001000010', 'QAR')]              # D09
        actual[('1501000010', 'QAR')] -= Decimal('50000.00')                         # D10
        actual[('1501000020', 'QAR')] += Decimal('50000.00')
        actual[('9001000010', 'QAR')] -= Decimal('70000.00')                         # D16
        actual[('9001000010', 'USD')] += Decimal('70000.00')
    actual_rows = [{'TARGET_GL': g, 'CURRENCY': c, 'BALANCE': v, 'BUSINESS_DATE': TB_DATE, 'CLASS': cls_of(g)}
                   for (g, c), v in sorted(actual.items())]
    legacy_rows = [{'LEGACY_GL': g, 'CURRENCY': c, 'BALANCE': v, 'CLASS': cls_of(g.split('-')[1])}
                   for (g, c), v in sorted(legacy.items())]
    bench = [{'CONSOL_KEY': '', 'TARGET_GL': g, 'CURRENCY': c, 'BALANCE': v} for (g, c), v in sorted(truth.items())]
    _write(folder / 'asset_balances.csv', ['ACCOUNT_NO', 'ARRANGEMENT_ID', 'CONSOL_KEY', 'LEGACY_GL'] + [b + '_BAL_QAR' for b in bt_cols], asset_rows)
    _write(folder / 'gl_rules.csv', list(R[0]), R)
    _write(folder / 'internal_balances.csv', ['ACCOUNT_NO', 'CURRENCY', 'BALANCE', 'LEGACY_GL', 'CUSTOMER_ACCOUNT_REF', 'CONSOL_KEY'], ib)
    _write(folder / 'internal_mapping.csv', ['ACCOUNT_NO', 'TARGET_ACCOUNT', 'TARGET_GL'], imap)
    _write(folder / 'customer_account_mapping.csv', ['ACCOUNT_NO', 'TARGET_ACCOUNT', 'TARGET_GL'], cmap)
    _write(folder / 'target_accounts.csv', ['TARGET_ACCOUNT', 'TARGET_GL', 'CURRENCY', 'BALANCE'], tacc)
    _write(folder / 'pl_balances.csv', ['CONSOL_KEY', 'BALANCE', 'LEGACY_GL'], pl)
    _write(folder / 'pl_rules.csv', ['RULE_ID', 'TARGET_GL', 'PL_CATEGORY', 'PRODUCT', 'DEPARTMENT', 'SECTOR'], plr)
    _write(folder / 'gl_mapping.csv', ['LEGACY_GL', 'TARGET_GL'], [{'LEGACY_GL': g, 'TARGET_GL': t} for g, t in gmap])
    _write(folder / 'legacy_tb.csv', ['LEGACY_GL', 'CURRENCY', 'BALANCE', 'CLASS'], legacy_rows)
    _write(folder / 'actual_tb.csv', ['TARGET_GL', 'CURRENCY', 'BALANCE', 'BUSINESS_DATE', 'CLASS'], actual_rows)
    _write(folder / 'post_cob_movements.csv', ['TARGET_GL', 'CURRENCY', 'BALANCE', 'BUSINESS_DATE', 'MOVEMENT_TYPE', 'VALIDATED'], mov)
    _write(folder / 'TrialBalance_withConsolKey.csv', ['CONSOL_KEY', 'TARGET_GL', 'CURRENCY', 'BALANCE'], bench)
    from .run import load_config
    cfg = load_config()
    cfg['cutover_date'] = CUTOVER
    (folder / 'tb_recon.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
    (folder / 'truth.json').write_text(json.dumps({'scenario': scenario, 'defects': DEFECTS if D else {},
                                                    'expected': {f'{g}|{c}': str(v) for (g, c), v in sorted(truth.items())},
                                                    'synthetic': True}, indent=1), encoding='utf-8')
    (folder / 'README_SYNTHETIC.txt').write_text('SYNTHETIC test data generated by nbs_control.tbrecon.synthetic. '
                                                 'No bank or customer data. Scenario: ' + scenario + '\n', encoding='utf-8')
    return folder
