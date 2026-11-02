"""SYNTHETIC mapping workbook, source records and BO report for Mapping Studio tests and demonstrations.

No bank data. The workbook follows the layout the existing adapter (gl_mapping.py) reads - GL Report with
named-range table, CATEGORY, SEGMENT, COA, GL Mapping - plus BRANCH, a defined name, a cross-sheet formula,
comments, number formats and merged cells, so preservation of the original can be verified.
The generator computes the TRUE BO allocation itself (truth.json), independently of the Studio engine.

Workbook defects (scenario 'defects'):
  W1 DKBGL1020 CATEGORY '3700-3748' (true 3700-3749)          W2 DKBGL1040 CATEGORY lacks 3901
  W3 GL Mapping fixed-asset row sends to DKBGL1070 (true 1060) W4 DKBGL2030 CATEGORY '6099-6001' (reversed)
  W7 DKBGL1030 SECTOR '1999-2999' (true 2000-2999: overlap)    W8 DKBGL1050 refers to unknown category 3955
  W9 GL Mapping line 'DKBGL 1065' (true 'DKBGL1065')          W12 DKBGL1080 product 4101 written in SECTOR
BO report defects: W5 duplicated row on DKBGL2010 QAR, W6 DKBGL5010 sign reversed, W10 line DKBGL9999 not in
the workbook, W11 DKBGL2040 reported without any source record.
"""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font
from openpyxl.workbook.defined_name import DefinedName

Q = Decimal('0.01')
DATE = '2026-09-30'


def _amt(rng, lo, hi):
    return (Decimal(rng.randint(lo * 100, hi * 100)) / 100).quantize(Q)


def build(folder, scenario='defects', seed=7):
    D = scenario == 'defects'
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    wb = Workbook()
    ws = wb.active
    ws.title = 'GL Report'
    hdr = ['LINE', 'TYPE', 'DESCRIPTION', 'APP', 'MARKET', 'CURRENCY', 'CATEGORY', 'PL CATEGORY', 'PL PRODUCT', 'SECTOR', 'PL SECTOR',
           'PL DEPARTMENT', 'BALANCE', 'NOTE', '', '', '', '', 'PRODUCT']
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)

    def row(line='', typ='', desc='', ccy='', cat='', plcat='', sector='', bal='', note='', product='', rn='', rf='', rs='', re=''):
        ws.append([line, typ, desc, '', '', ccy, cat, plcat, '', sector, '', '', bal, note, rn, rf, rs, re, product])
        return ws.max_row
    row('H001', 'H', 'ASSETS', rn='CASH', rf='CATEGORY', rs='10000', re='10099')
    row('DKBGL1010', 'D', 'Cash and balances', cat='*CASH', bal='CREDIT, DEBIT', rn='PRINCIPAL', rf='BALANCE', rs='CURACCOUNT, DUEACCOUNT')
    row('DKBGL1020', 'D', 'Murabaha - retail', cat='3700-3748' if D else '3700-3749', sector='1000-1999', bal='*PRINCIPAL',
        note='Retail sectors')
    row(cat='3901', sector='^', bal='^')
    row('DKBGL1030', 'D', 'Murabaha - corporate', cat='3700-3749', sector='1999-2999' if D else '2000-2999', bal='*PRINCIPAL')
    row('DKBGL1040', 'D', 'Accrued profit', cat='3700-3749' if D else '3700-3749, 3901', bal='ACCPRINCIPALPFT')
    r_ijara = row('DKBGL1050', 'D', 'Ijara', cat='=CATEGORY!B6', sector='2000-2999', bal='*PRINCIPAL')
    if D:
        row(cat='3955', bal='*PRINCIPAL')
    row('DKBGL1060', 'D', 'Fixed assets (GL Mapping)')
    row('DKBGL1065', 'D', 'Intangibles (GL Mapping)')
    row('DKBGL1070', 'D', 'Other assets (GL Mapping)')
    row('DKBGL1080', 'D', 'Staff financing', cat='*IJARA_STAFF', sector='4101' if D else '', product='' if D else '4101', bal='*PRINCIPAL')
    row('T1090', 'T', 'Total assets')
    row('H002', 'H', 'LIABILITIES')
    row('DKBGL2010', 'D', 'Current accounts - other currencies', ccy='NOT USD', cat='1001-1099', bal='CREDIT')
    row('DKBGL2020', 'D', 'Current accounts - USD', ccy='USD', cat='1001-1099', bal='CREDIT')
    row('DKBGL2030', 'D', 'Savings accounts', cat='6099-6001' if D else '6001-6099', bal='CREDIT')
    row('DKBGL2040', 'D', 'Margin deposits', cat='1500-1599', bal='CREDIT')
    row('T2090', 'T', 'Total liabilities')
    row('H005', 'H', 'INCOME')
    row('DKBGL5010', 'D', 'Profit income', plcat='51000-51999')
    ws.cell(row=r_ijara, column=14).comment = Comment('Category taken from the CATEGORY sheet (cross-sheet reference)', 'synthetic')
    # CATEGORY
    cs = wb.create_sheet('CATEGORY')
    cs.append(['GROUP', 'CATEGORY', 'TO', 'MODULE', '', 'DESCRIPTION', 'GL PARAM', 'TRANSACT GL', '', '', 'RANGE'])
    cats = [('CASH', 10000, 10099, 'AC', 'Cash', '1001000010'), ('CURRENT', 1001, 1099, 'AC', 'Current accounts', '2001000010'),
            ('MARGIN', 1500, 1599, 'AC', 'Margin', '2004000010'), ('MURABAHA', 3700, 3749, 'AA', 'Murabaha', '1101000010'),
            ('IJARA', 3800, None, 'AA', 'Ijara', '1102000010'), ('MURABAHA', 3901, None, 'AA', 'Murabaha 2', '1101000010'),
            ('SAVINGS', 6001, 6099, 'AC', 'Savings', '2002000010'), ('PL', 51000, 51999, 'PL', 'Profit income', '5001000010')]
    for g, lo, hi, mod, desc, gl in cats:
        cs.append([g, lo, hi, mod, None, desc, 'P' + str(lo), gl, None, None, g])
    cs['H2'].number_format = '@'
    # SEGMENT, COA, BRANCH
    ss = wb.create_sheet('SEGMENT')
    ss.append(['CUSTOMER TYPE', 'GL', 'SECTOR', 'SEGMENT'])
    for code, name in ((1000, 'Individuals'), (1500, 'Staff'), (1999, 'Other individuals'), (2001, 'Corporate'), (2500, 'SME')):
        ss.append(['RETAIL' if code < 2000 else 'CORPORATE', 'R' if code < 2000 else 'C', f'{code} - {name}', 'S' + str(code)[0]])
    co = wb.create_sheet('COA')
    co.append(['GL CODE', 'DESCRIPTION'])
    for gl in ('1001000010', '1101000010', '1102000010', '1501000010', '1502000010', '1901000010', '2001000010', '2002000010',
               '2004000010', '5001000010'):
        co.append([gl, 'GL ' + gl])
    br = wb.create_sheet('BRANCH')
    br.append(['BRANCH CODE', 'NAME'])
    for b in ('QA0010001', 'QA0010002'):
        br.append([b, 'Branch ' + b[-1]])
    # GL Mapping (letters A, B, C, E, H, L, W as read by the existing adapter)
    gm = wb.create_sheet('GL Mapping')
    head = [''] * 23
    for i, h in ((0, 'OLD GL'), (1, 'CCY'), (2, 'DESCRIPTION'), (4, 'TRANSACT GL'), (7, 'CLASSIFICATION'), (11, 'CATEGORY'), (22, 'DKBGL')):
        head[i] = h
    gm.append(head)
    glrows = [('01-01-000-10-01-1500000001', 'QAR', 'Fixed assets', '1501000010', 'ASSET', '', 'DKBGL1070' if D else 'DKBGL1060'),
              ('01-01-000-10-01-1500000002', 'QAR', 'Intangibles', '1502000010', 'ASSET', '', 'DKBGL 1065' if D else 'DKBGL1065'),
              ('01-01-000-10-01-1900000001', 'QAR', 'Other assets', '1901000010', 'ASSET', '', 'DKBGL1070'),
              ('01-01-000-10-01-3700000001', 'QAR', 'Murabaha GL', '1101000010', 'ASSET', '3701', 'DKBGL1020')]
    for old, ccy, desc, tgl, cls, cat, line in glrows:
        r = [''] * 23
        r[0], r[1], r[2], r[4], r[7], r[11], r[22] = old, ccy, desc, tgl, cls, cat, line
        gm.append(r)
    readme = wb.create_sheet('README')
    readme['A1'] = 'SYNTHETIC mapping workbook - no bank data'
    readme.merge_cells('A1:D1')
    readme['A2'] = '=COUNTA(\'GL Report\'!A:A)'
    wb.defined_names['IJARA_STAFF'] = DefinedName('IJARA_STAFF', attr_text='CATEGORY!$B$6')
    path = folder / 'mapping_workbook.xlsx'
    wb.save(path)
    _cache_formula_values(path, {('GL Report', f'G{r_ijara}'): 3800, ('README', 'A2'): 20})

    # ---------------- source records and truth
    truth = defaultdict(Decimal)
    src = []

    def rec(acct, cat, sector, bt, ccy, amount, line, product='', branch='QA0010001'):
        src.append({'ACCOUNT_NO': acct, 'CATEGORY': cat, 'SECTOR': sector, 'PRODUCT': product, 'BALANCE_TYPE': bt, 'CURRENCY': ccy,
                    'BRANCH': branch, 'AMOUNT': amount, 'BUSINESS_DATE': DATE})
        if line:
            truth[(line, ccy)] += amount
    for i in range(12):
        rec(f'SYNCASH{i:03d}', 10000 + i, 1000, 'DEBIT', 'QAR', _amt(rng, 1000, 90000), 'DKBGL1010')
    for i in range(30):
        cat = rng.choice([3701, 3720, 3749]) if i < 24 else 3901
        sec = rng.choice([1000, 1500, 1999]) if i % 3 else 1000
        ccy = 'USD' if i % 7 == 6 else 'QAR'
        rec(f'SYNRET{i:03d}', cat, sec, 'CURACCOUNT', ccy, _amt(rng, 10000, 400000), 'DKBGL1020')
        rec(f'SYNRET{i:03d}', cat, sec, 'ACCPRINCIPALPFT', ccy, _amt(rng, 100, 9000), 'DKBGL1040')
        if i % 4 == 0:
            rec(f'SYNRET{i:03d}', cat, sec, 'DUEACCOUNT', ccy, _amt(rng, 100, 20000), 'DKBGL1020')
    for i in range(10):
        rec(f'SYNCORP{i:03d}', rng.choice([3701, 3730]), rng.choice([2001, 2500]), 'CURACCOUNT', 'QAR', _amt(rng, 200000, 3000000), 'DKBGL1030')
    for i in range(6):
        rec(f'SYNIJR{i:03d}', 3800, 2001, 'CURACCOUNT', 'QAR', _amt(rng, 50000, 900000), 'DKBGL1050')
    for i in range(4):
        rec(f'SYNSTF{i:03d}', 3800, 1500, 'DUEACCOUNT', 'QAR', _amt(rng, 5000, 50000), None, product='4101')
    for i in range(20):
        ccy = 'USD' if i % 5 == 0 else 'QAR'
        rec(f'SYNCA{i:03d}', rng.choice([1001, 1050, 1099]), 1000, 'CREDIT', ccy, -_amt(rng, 1000, 500000),
            'DKBGL2020' if ccy == 'USD' else 'DKBGL2010', branch='QA0010002')
    for i in range(10):
        rec(f'SYNSAV{i:03d}', rng.choice([6001, 6050, 6099]), 1000, 'CREDIT', 'QAR', -_amt(rng, 1000, 300000), 'DKBGL2030')
    for i in range(8):
        a = -_amt(rng, 500, 60000)
        src.append({'ACCOUNT_NO': f'SYNPL{i:03d}', 'PL_CATEGORY': 51000 + i * 7, 'CURRENCY': 'QAR', 'AMOUNT': a, 'BUSINESS_DATE': DATE})
        truth[('DKBGL5010', 'QAR')] += a
    # staff financing: true line DKBGL1080 (category via defined name IJARA_STAFF -> CATEGORY!B6 = 3800, product 4101)
    for s in src:
        if str(s.get('ACCOUNT_NO', '')).startswith('SYNSTF'):
            truth[('DKBGL1080', 'QAR')] += s['AMOUNT']
    gl_src = [('01-01-000-10-01-1500000001', 'QAR', Decimal('750000.00'), 'DKBGL1060'),
              ('01-01-000-10-01-1500000002', 'QAR', Decimal('120000.00'), 'DKBGL1065'),
              ('01-01-000-10-01-1900000001', 'QAR', Decimal('33000.00'), 'DKBGL1070')]
    for gl, ccy, a, line in gl_src:
        src.append({'LEGACY_GL': gl, 'CURRENCY': ccy, 'AMOUNT': a, 'BUSINESS_DATE': DATE})
        truth[(line, ccy)] += a
    cols = ['ACCOUNT_NO', 'LEGACY_GL', 'CATEGORY', 'SECTOR', 'PRODUCT', 'BALANCE_TYPE', 'PL_CATEGORY', 'CURRENCY', 'BRANCH', 'AMOUNT', 'BUSINESS_DATE']
    with (folder / 'source_records.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for s in src:
            w.writerow({k: s.get(k, '') for k in cols})
    # ---------------- BO report (truth + BO-side defects)
    bo = [{'LINE': l, 'CURRENCY': c, 'AMOUNT': v, 'BUSINESS_DATE': DATE} for (l, c), v in sorted(truth.items())]
    totals = defaultdict(Decimal)
    for (l, c), v in truth.items():
        if l.startswith('DKBGL1'):
            totals[('T1090', c)] += v
        elif l.startswith('DKBGL2'):
            totals[('T2090', c)] += v
    if D:
        bo.append({'LINE': 'DKBGL2040', 'CURRENCY': 'QAR', 'AMOUNT': Decimal('-45000.00'), 'BUSINESS_DATE': DATE})   # W11
        totals[('T2090', 'QAR')] += Decimal('-45000.00')
        dup = next(b for b in bo if b['LINE'] == 'DKBGL2010' and b['CURRENCY'] == 'QAR')
        bo.append(dict(dup))                                                                                      # W5
        for b in bo:
            if b['LINE'] == 'DKBGL5010':
                b['AMOUNT'] = -b['AMOUNT']                                                                        # W6
        bo.append({'LINE': 'DKBGL9999', 'CURRENCY': 'QAR', 'AMOUNT': Decimal('1234.00'), 'BUSINESS_DATE': DATE})   # W10
    bo += [{'LINE': l, 'CURRENCY': c, 'AMOUNT': v, 'BUSINESS_DATE': DATE} for (l, c), v in sorted(totals.items())]
    with (folder / 'bo_report.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['LINE', 'CURRENCY', 'AMOUNT', 'BUSINESS_DATE'])
        w.writeheader()
        w.writerows(bo)
    (folder / 'truth.json').write_text(json.dumps({'scenario': scenario, 'synthetic': True,
                                                    'expected': {f'{l}|{c}': str(v) for (l, c), v in sorted(truth.items())}}, indent=1))
    (folder / 'README_SYNTHETIC.txt').write_text('SYNTHETIC Mapping Studio data - no bank data. Scenario: ' + scenario + '\n')
    return folder


def _cache_formula_values(path, values):
    """openpyxl writes formulas without cached results; add them (as Excel would) so data-only readers see the values."""
    import re
    import shutil
    import zipfile
    tmp = Path(str(path) + '.tmp')
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        wbxml = zin.read('xl/workbook.xml').decode()
        rels = zin.read('xl/_rels/workbook.xml.rels').decode()
        sheet_files = {}
        for name, rid in re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wbxml):
            target = re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels) or re.search(rf'Target="([^"]+)"[^>]*Id="{rid}"', rels)
            sheet_files[name] = 'xl/' + target.group(1).lstrip('/').replace('xl/', '')
        for item in zin.infolist():
            data = zin.read(item.filename)
            for (sheet, ref), val in values.items():
                if sheet_files.get(sheet) == item.filename:
                    s = data.decode()
                    s = re.sub(rf'(<c r="{ref}"[^>]*>)(<f>[^<]*</f>)(<v>[^<]*</v>)?', lambda m: m.group(1) + m.group(2) + f'<v>{val}</v>', s)
                    data = s.encode()
            zout.writestr(item, data)
    shutil.move(str(tmp), str(path))
