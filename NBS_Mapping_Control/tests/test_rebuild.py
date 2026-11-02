"""Acceptance tests for the code-keyed NBS rebuild (brief of 17 Oct 2026). Fixtures are independent of the generator."""
import json
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from nbs_control import bo_reference, categ_data, legacy_gl, maturity as mat, money, policies, rebuild_compare as cmp
from nbs_control import rebuild_engine as eng, target_mappings as tm
from nbs_control.rebuild_store import connect, sha256
from tests.rebuild_fixtures import BO_STD, bo_sheet, categ_row, categ_workbook, write_xlsx, col

ROOT = Path(__file__).resolve().parents[1]
REAL_CATEG = Path(r'C:\Users\Test\Downloads\Mock3_UAT3 Categ Entry Extract (1).xlsx')
REAL_CATEG_COPY = Path(r'C:\Users\Test\Downloads\Mock3_UAT3 Categ Entry Extract.xlsx')
REAL_BO = Path(r'C:\Users\Test\Downloads\BO_QCB_NBS_Report.xlsx')
STORE = ROOT / 'data' / 'rebuild' / 'rebuild_store.sqlite'
CATEG_SHA = 'a9dc0021a2cd9551802129fbb2277161178b971c38cbede07d93824d9a2f6ac1'


class Temp(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.c = connect(self.dir / 'store.sqlite')

    def tearDown(self):
        self.c.close()
        shutil.rmtree(self.dir, ignore_errors=True)


class T12Money(unittest.TestCase):
    def test_decimal_policy(self):
        self.assertEqual(money.to_micro('-594.59000000000003'), -594590000)
        self.assertEqual(money.to_micro('8868772428.0799999237060547'), 8868772428080000)
        self.assertEqual(money.to_micro('0'), 0)
        self.assertIsNone(money.to_micro(''))  # blank is missing, not zero
        self.assertEqual(money.to_micro('0.0000005'), 0)  # half-even at the 1e-6 scale
        self.assertEqual(money.to_micro('0.0000015'), 2)
        for bad in ('NaN', 'inf', '-Infinity', 'abc'):
            with self.assertRaises(ValueError):
                money.to_micro(bad)
        # float drift does not reach controls: 0.1+0.2 summed as micro is exact
        self.assertEqual(sum(money.to_micro(x) for x in ['0.1', '0.2']), money.to_micro('0.3'))
        big = ['123456789012.123456'] * 1000
        self.assertEqual(sum(money.to_micro(x) for x in big), 123456789012123456000)


class T1T2T3Categ(Temp):
    def make(self, name, rows, **kw):
        p = self.dir / name
        categ_workbook(p, rows, **kw)
        return p

    def rows(self):
        return [categ_row('100', '400'), categ_row('100', '400'), categ_row('100', '-12.345678901'),  # repeated ID, 2 identical
                categ_row('200', '391420.98', pl='61001', ref=None, value=None, system='DC', soft=None, u=None, product=None),
                categ_row('300', '-7', value='20261001')]

    def test_identical_copy_imported_once_and_original_unchanged(self):
        a = self.make('a.xlsx', self.rows())
        b = self.dir / 'copy.xlsx'
        shutil.copy(a, b)
        before = sha256(a)
        r1 = categ_data.import_categ(self.c, a)
        r2 = categ_data.import_categ(self.c, b)
        self.assertFalse(r1['already_imported'])
        self.assertTrue(r2['already_imported'])
        self.assertEqual(self.c.execute('SELECT count(*) FROM categ_events').fetchone()[0], 5)
        self.assertEqual(sha256(a), before)
        aliases = json.loads(self.c.execute('SELECT aliases FROM sources').fetchone()[0])
        self.assertEqual(aliases, ['a.xlsx', 'copy.xlsx'])

    def test_raw_preservation_unheaded_u_dc_dates_signs(self):
        r = categ_data.import_categ(self.c, self.make('a.xlsx', self.rows()))
        self.assertEqual(r['rows'], 5)
        self.assertEqual(r['unheaded_columns'], {'U': 'UNHEADED_U'})
        issue = self.c.execute("SELECT field, issue FROM categ_schema WHERE column='U'").fetchone()
        self.assertEqual(issue, ('unheaded_u', 'MISSING_HEADER_POPULATED_COLUMN'))
        rows = {r[0]: r for r in self.c.execute('SELECT row_no, amount_raw, value_date, exposure_date, booking_date, processing_date, unheaded_u, our_reference, event_type, system_id FROM categ_events')}
        self.assertEqual(rows[4][1], '-12.345678901')  # raw text, sign intact
        self.assertEqual(rows[2][2:6], ('2026-09-15', '2026-09-15', '2026-10-01', '2026-10-01'))
        self.assertEqual(rows[2][6], 'SDB-CHARGE')
        self.assertIsNone(rows[5][7])  # DC blank reference kept
        self.assertEqual(rows[5][8], 'DC_WITHOUT_SOFT_DETAILS')
        self.assertEqual(self.c.execute('SELECT count(*) FROM categ_raw').fetchone()[0], 5)

    def test_missing_required_header_is_specific(self):
        hdr = [h for h in categ_data.REQUIRED if h != 'BOOKING.DATE']
        p = self.dir / 'bad.xlsx'
        write_xlsx(p, [('Sheet1', [hdr, ['1'] * len(hdr)])])
        with self.assertRaisesRegex(ValueError, 'BOOKING.DATE'):
            categ_data.import_categ(self.c, p)

    def test_nonfinite_amount_rejected(self):
        with self.assertRaisesRegex(ValueError, 'not'):
            categ_data.import_categ(self.c, self.make('a.xlsx', [categ_row('1', 'NaN')]))

    def test_nonunique_id_and_duplicate_treatment_transparent_and_order_independent(self):
        r = categ_data.import_categ(self.c, self.make('a.xlsx', self.rows()))
        sha = r['source_sha256']
        ctl = categ_data.source_controls(self.c, sha)
        self.assertEqual(ctl['ids_with_multiple_rows'], 1)
        self.assertEqual(ctl['ids_with_multiple_variants'], 1)
        groups = categ_data.repeated_groups(self.c, sha)
        self.assertEqual([(g['occurrences'], g['excess_micro']) for g in groups], [(2, 400_000_000)])
        doc = {'default_treatment': 'UNRESOLVED_RETAIN_ALL', 'decisions': {}}
        w = policies.row_weights(self.c, sha, doc)
        self.assertEqual(sum(x[0] for x in w.values()), 5)
        doc['decisions'][groups[0]['fingerprint']] = {'treatment': 'COUNT_ONCE'}
        w2 = policies.row_weights(self.c, sha, doc)
        amounts = dict(self.c.execute('SELECT row_no, amount_micro FROM categ_events'))
        delta = sum(amounts[k] * (w[k][0] - w2[k][0]) for k in w)
        self.assertEqual(delta, 400_000_000)  # exactly the reported excess, no hidden adjustment
        self.assertEqual([s for _, s in w2.values()].count('EXCLUDED_DUPLICATE_EXPORT'), 1)
        # Reordered source rows: same fingerprint, same decision, same amount effect.
        c2 = connect(self.dir / 'store2.sqlite')
        try:
            rr = self.rows()
            rr.reverse()
            sha2 = categ_data.import_categ(c2, self.make('b.xlsx', rr))['source_sha256']
            g2 = categ_data.repeated_groups(c2, sha2)
            self.assertEqual(g2[0]['fingerprint'], groups[0]['fingerprint'])
            w3 = policies.row_weights(c2, sha2, doc)
            am2 = dict(c2.execute('SELECT row_no, amount_micro FROM categ_events'))
            self.assertEqual(sum(am2[k] * w3[k][0] for k in w3), sum(amounts[k] * w2[k][0] for k in w2))
        finally:
            c2.close()


class T4ReportingBasis(Temp):
    def policy(self, sha=CATEG_SHA, enabled=True):
        return {'version': 3, 'policies': [{'policy_id': 'P', 'dataset': 'CATEG_ENTRY', 'source_sha256': sha, 'raw_booking_date': '2026-10-01',
                                            'raw_processing_date': '2026-10-01', 'effective_reporting_date': '2026-09-30', 'enabled': enabled,
                                            'authority': 'owner'}]}

    def test_confirmed_source_gets_september_and_keeps_raw_dates(self):
        r = policies.resolve_effective_date(self.policy(), 'CATEG_ENTRY', CATEG_SHA, ['2026-10-01'], ['2026-10-01'], '2026-09-30')
        self.assertEqual(r['effective_reporting_date'], '2026-09-30')
        self.assertEqual(r['raw_booking_dates'], ['2026-10-01'])
        self.assertEqual((r['policy_id'], r['policy_version']), ('P', 3))

    def test_unrelated_october_file_does_not_inherit(self):
        with self.assertRaisesRegex(policies.ReportingBasisError, 'no owner policy'):
            policies.resolve_effective_date(self.policy(), 'CATEG_ENTRY', 'f' * 64, ['2026-10-01'], ['2026-10-01'], '2026-09-30')

    def test_mixed_dates_and_disabled_policy_rejected(self):
        with self.assertRaisesRegex(policies.ReportingBasisError, 'mixes'):
            policies.resolve_effective_date(self.policy(), 'CATEG_ENTRY', 'f' * 64, ['2026-09-30', '2026-10-01'], ['2026-10-01'], '2026-09-30')
        with self.assertRaisesRegex(policies.ReportingBasisError, 'disabled'):
            policies.resolve_effective_date(self.policy(enabled=False), 'CATEG_ENTRY', CATEG_SHA, ['2026-10-01'], ['2026-10-01'], '2026-09-30')

    def test_historical_value_dates_do_not_set_reporting_date(self):
        # booking 2026-09-30 source with old value dates is a September source by booking date, not by value date
        r = policies.resolve_effective_date({'policies': []}, 'CATEG_ENTRY', 'e' * 64, ['2026-09-30'], ['2026-09-30'], '2026-09-30')
        self.assertEqual(r['basis'], 'RAW_BOOKING_DATE')

    def test_policy_change_is_new_version_without_touching_raw(self):
        cfg = self.dir / 'cfg'
        cfg.mkdir()
        conf = ROOT / 'exports/rebuild_review_20261017/reporting_basis_owner_confirmation.json'
        doc = policies.ensure_basis_policy(cfg, conf)
        self.assertTrue(doc['policies'][0]['enabled'])
        self.assertEqual(doc['policies'][0]['source_sha256'], CATEG_SHA)
        doc['policies'][0]['enabled'] = False
        new = policies.save_basis_policy(cfg, doc, 'tester', 'disable for test')
        self.assertEqual(new['version'], 2)
        self.assertEqual(len(list((cfg / 'policy_history').glob('basis-*.json'))), 2)
        with self.assertRaises(ValueError):
            policies.save_basis_policy(cfg, doc, '', '')

    @unittest.skipUnless((ROOT / 'data/rebuild/runs/latest.json').exists(), 'no real run yet')
    def test_real_run_manifest_records_policy_and_hash(self):
        from nbs_control.rebuild_run import latest_run
        m = latest_run(ROOT)
        b = m['category_reporting_basis']
        self.assertEqual((b['effective_reporting_date'], b['basis'], b['raw_booking_dates'], b['raw_processing_dates']),
                         ('2026-09-30', 'OWNER_CONFIRMED_SOURCE_POLICY', ['2026-10-01'], ['2026-10-01']))
        self.assertEqual(m['inputs']['categ_source'], CATEG_SHA)
        self.assertIn(CATEG_SHA, [s['source_sha256'] for s in m['sources']])


class T5Grain(unittest.TestCase):
    def test_one_ecb_account_three_events_counts_balance_once(self):
        spec = {'source': 'ECB_LOAN', 'factor': 1, 'layout': None}
        stock = [{'fid': 1, 'source': 'ECB_LOAN', 'account': 'A1', 'currency': 'QAR', 'residency': 'Resident', 'country': 'QA', 'maturity': '',
                  'product': 'X', 'risk': '1', 'personal': 'Personal', 'industry': '', 'unavailable': 0, 'issue': None, 'amount': 1000.0}]
        s = eng.legacy_semantic(spec, stock, '2026-09-30', {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(s['semantic']['IN_LC'], 1000 * 10 ** 6)
        events = [{'row_no': i, 'source_id': 'E', 'amount': a, 'currency': 'QAR', 'event_type': 't', 'weight': 1, 'state': 'UNIQUE_OBSERVATION'}
                  for i, a in enumerate([10 ** 6, 2 * 10 ** 6, 3 * 10 ** 6])]
        e = eng.categ_semantic({'categ': {'sign': 1, 'geography': 'IN'}}, events)
        self.assertEqual(e['semantic']['IN_LC'], 6 * 10 ** 6)
        # balance still once: the stock calculation is independent of the event count
        self.assertEqual(len([x for x in s['contributions'] if x[5]]), 1)

    def test_links_conflicts_do_not_fan_out(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            store = connect(tmp / 's.sqlite')
            p = tmp / 'c.xlsx'
            categ_workbook(p, [categ_row('1', '5', ref='A1'), categ_row('2', '6', ref='A1'), categ_row('3', '7', ref='A1'),
                               categ_row('4', '8', ref='A2'), categ_row('5', '9', ref='A3')])
            sha = categ_data.import_categ(store, p)['source_sha256']
            bank = sqlite3.connect(':memory:')
            bank.execute('CREATE TABLE unique_records(source TEXT, account TEXT, currency TEXT)')
            bank.executemany('INSERT INTO unique_records VALUES(?,?,?)', [('ECB', 'A1', 'QAR'), ('ECB', 'A2', 'USD'), ('ECB', 'A3', 'QAR'), ('ECB', 'A3', 'QAR')])
            r = categ_data.account_links(store, sha, bank)
            self.assertEqual(r['matched_rows'], 3)
            self.assertEqual(r['matched_distinct_accounts'], 1)
            self.assertEqual(r['ambiguous_or_conflicting_rows'], 2)  # currency conflict A2 + duplicate key A3
            store.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def bo_workbook(path, reorder=False, dup=False, pad=True):
    items = [['001' if pad else '1', '1-001-10101', 'Cash on hand', ('n', '417680'), ('n', '76581'), ('n', '0'), ('n', '0')],
             ['001' if pad else '1', '1-001-10102', 'Precious Metals', ('n', '5'), ('n', '0'), ('n', '0'), ('n', '0')],
             ['001' if pad else '1', '1-001-1010201', 'Gold', ('n', '5'), ('n', '0'), ('n', '0'), ('n', '0')]]
    if dup:
        items.append(items[0])
    hdr = list(BO_STD)
    if reorder:
        items.reverse()
        order = [0, 1, 2, 6, 5, 4, 3]  # swap measure columns
        items = [[it[i] for i in order] for it in items]
        hdr = [hdr[i] for i in order] + ['Report Date']
    t022 = bo_sheet('022', [['022', '1-022-201', 'Due to banks', ('n', '1'), ('n', '2'), ('n', '3'), ('n', '4'), ('n', '5'), ('n', '6'), ('n', '7'), ('n', '8')]],
                    headers=['Table Code', 'Qcb Item Code', 'Qcb Item Description', 'One Week', 'Week To 1 Month', 'One To 3 Month', 'Three To 6 Month',
                             'Six To 12 Month', 'One To 2 Year', 'Two To 5 Year', 'Greater 5 Year', 'Rep Date'])
    t031 = bo_sheet('031', [['031', '1-031-01', 'Others', ('n', '1'), ('n', '2'), ('n', '3'), ('n', '4'), ('n', '5'), ('n', '6')]],
                    headers=['Table Code', 'Qcb Item Code', 'Qcb Item Desc', 'In Amount Lc', 'In Amount Fc', 'Out Amount Lc', 'Out Amount Fc', 'Gcc Amount Lc', 'Gcc Amount Fc', 'Report Date'])
    t009 = bo_sheet('009', [['009', '1-009-01', 'X', ('n', '1'), ('n', '2'), ('n', '3'), ('n', '4'), ('n', '11'), ('n', '22')]],
                    headers=['Table Code', 'Qcb Item Code', 'Qcb Item Description', 'In Amount Lc', 'In Amount Fc', 'Out Amount Lc', 'Out Amount Fc', 'Uae Fc', 'Uae Lc', 'Report Date'])
    t020 = ('Table-020', [[], [None, None, 'Table (20) '], [], [None, 'Table Code', 'Acquistion No', 'Provision Amount', 'Net Value', 'Report Date'],
                          [None, '020', ('n', '0'), ('n', '0'), ('n', '0'), ('n', '46295')]])
    write_xlsx(path, [bo_sheet('001', items, headers=hdr), t009, t020, t022, t031])


class T6T7BO(Temp):
    def load(self, name, **kw):
        p = self.dir / name
        bo_workbook(p, **kw)
        cat = bo_reference.build_catalogue(p, self.dir / (name + '.cat.json'))
        return p, cat

    def test_schema_variants_and_special_table(self):
        p, cat = self.load('bo.xlsx')
        r = bo_reference.import_bo(self.c, p, cat, 'V1')
        self.assertEqual((r['standard_item_rows'], r['special_records'], r['report_date']), (6, 1, '2026-09-30'))
        self.assertEqual(cat['tables']['009']['measures']['Uae Fc']['semantic'], 'SUBSET_AE_FC')
        self.assertEqual(self.c.execute("SELECT raw FROM bo_cells WHERE table_code='009' AND measure='Uae Lc'").fetchone()[0], '22')
        self.assertFalse(cat['tables']['009']['measures']['Uae Lc']['primary'])
        self.assertIn('Qcb Item Desc', json.loads(self.c.execute("SELECT headers FROM bo_headers WHERE table_code='031'").fetchone()[0]).values())
        self.assertNotIn('Rep Date', cat['tables']['022']['measures'])
        self.assertEqual(self.c.execute("SELECT count(*) FROM bo_cells WHERE measure IN ('Report Date','Rep Date')").fetchone()[0], 0)
        self.assertEqual(json.loads(self.c.execute('SELECT fields FROM bo_special').fetchone()[0])['Net Value']['cell'], 'E5')
        self.assertEqual(self.c.execute("SELECT parent_code, depth FROM bo_items WHERE item_code='1-001-1010201'").fetchone(), ('1-001-10102', 1))

    def test_reordering_preserves_identity(self):
        p1, cat = self.load('a.xlsx')
        p2 = self.dir / 'b.xlsx'
        bo_workbook(p2, reorder=True)
        bo_reference.import_bo(self.c, p1, cat, 'A')
        bo_reference.import_bo(self.c, p2, cat, 'B')
        a = {k[1:]: v for k, v in ((r[:1] + r[1:4], r[4]) for r in self.c.execute("SELECT ref_version, table_code, item_code, measure, value_micro FROM bo_cells WHERE ref_version='A'"))}
        b = {k[1:]: v for k, v in ((r[:1] + r[1:4], r[4]) for r in self.c.execute("SELECT ref_version, table_code, item_code, measure, value_micro FROM bo_cells WHERE ref_version='B'"))}
        self.assertEqual(a, b)

    def test_duplicate_key_and_leading_zero_fail(self):
        p, cat = self.load('d.xlsx', dup=True)
        with self.assertRaisesRegex(ValueError, 'Duplicate BO key'):
            bo_reference.import_bo(self.c, p, cat, 'D')
        p2 = self.dir / 'z.xlsx'
        bo_workbook(p2, pad=False)
        with self.assertRaisesRegex(ValueError, 'leading zeroes'):
            bo_reference.import_bo(self.c, p2, cat, 'Z')

    @unittest.skipUnless(STORE.exists(), 'real store not built')
    def test_real_bo_import(self):
        with closing(sqlite3.connect(STORE)) as c:
            ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS'").fetchone()[0]
            self.assertEqual(c.execute('SELECT count(*) FROM bo_headers WHERE ref_version=?', (ref,)).fetchone()[0], 50)
            self.assertEqual(c.execute('SELECT count(*) FROM bo_items WHERE ref_version=?', (ref,)).fetchone()[0], 1648)
            self.assertEqual(c.execute('SELECT count(*) FROM bo_special WHERE ref_version=?', (ref,)).fetchone()[0], 1)
            self.assertEqual(c.execute("SELECT DISTINCT report_date FROM bo_items WHERE ref_version=? AND table_code='022'", (ref,)).fetchall(), [('2026-09-30',)])
            self.assertEqual(c.execute("SELECT count(DISTINCT table_code) FROM bo_items WHERE ref_version=? AND table_code LIKE '0%'", (ref,)).fetchone()[0], 44)
            m009 = json.loads(c.execute("SELECT headers FROM bo_headers WHERE ref_version=? AND table_code='009'", (ref,)).fetchone()[0])
            self.assertEqual((m009['M'], m009['N']), ('Uae Fc', 'Uae Lc'))
            self.assertEqual(c.execute("SELECT count(*) FROM bo_cells WHERE ref_version=? AND measure IN ('Report Date','Rep Date')", (ref,)).fetchone()[0], 0)


class T9Maturity(unittest.TestCase):
    R = '2026-09-30'

    def test_each_loan_band_calendar(self):
        expected = [('2026-09-29', 'OVERDUE'), ('2026-09-30', 'MAT_1W'), ('2026-10-07', 'MAT_1W'), ('2026-10-08', 'MAT_1M'),
                    ('2026-10-30', 'MAT_1M'), ('2026-10-31', 'MAT_3M'), ('2026-12-30', 'MAT_3M'), ('2026-12-31', 'MAT_6M'),
                    ('2027-03-30', 'MAT_6M'), ('2027-03-31', 'MAT_12M'), ('2027-09-30', 'MAT_12M'), ('2027-10-01', 'MAT_2Y'),
                    ('2028-09-30', 'MAT_2Y'), ('2028-10-01', 'MAT_5Y'), ('2031-09-30', 'MAT_5Y'), ('2031-10-01', 'MAT_10Y'),
                    ('2036-09-30', 'MAT_10Y'), ('2036-10-01', 'MAT_20Y'), ('2046-09-30', 'MAT_20Y'), ('2046-10-01', 'MAT_GT20Y'),
                    ('2099-12-31', 'MAT_GT20Y')]
        for d, b in expected:
            self.assertEqual(mat.bucket(d, self.R, convention='CALENDAR'), b, d)

    def test_day_count_and_leap_years(self):
        self.assertEqual(mat.bucket('2026-10-30', self.R, convention='DAY_COUNT'), 'MAT_1M')  # 30 days
        self.assertEqual(mat.bucket('2026-10-31', self.R, convention='DAY_COUNT'), 'MAT_3M')
        self.assertEqual(mat.add_months(date(2028, 2, 29), 12), date(2029, 2, 28))
        self.assertEqual(mat.bucket('2029-02-28', '2028-02-29', convention='CALENDAR'), 'MAT_12M')
        self.assertEqual(mat.bucket('2029-03-01', '2028-02-29', convention='CALENDAR'), 'MAT_2Y')
        self.assertEqual(mat.bucket('2027-09-30', self.R, convention='DAY_COUNT'), 'MAT_12M')  # 365 days

    def test_missing_open_ended_overdue_distinct(self):
        self.assertEqual(mat.bucket(None, self.R), 'MISSING')
        self.assertEqual(mat.bucket('', self.R, open_ended=True), 'MAT_NONE')
        self.assertEqual(mat.bucket('2020-01-01', self.R, open_ended=True), 'OVERDUE')

    def test_engine_total_and_exceptions(self):
        rows = [dict(fid=i, source='ECB_LOAN', account=f'A{i}', currency='QAR', residency='Resident', country='QA', maturity=m, product=p,
                     risk='', personal='', industry='', unavailable=0, issue=None, amount=a)
                for i, (m, p, a) in enumerate([('2026-10-03', 'X', 1000.0), ('2050-01-01', 'X', 2000.0), ('2020-01-01', 'X', 4000.0),
                                               ('', 'X', 8000.0), ('', 'OD', 16000.0)])]
        s = eng.legacy_semantic({'source': 'ECB_LOAN', 'factor': 1, 'layout': 'maturity_loan'}, rows, self.R,
                                {'maturity_convention': 'CALENDAR', 'open_ended_products': ['OD']})
        v = s['semantic']
        self.assertEqual((v['MAT_1W'], v['MAT_GT20Y'], v['MAT_NONE']), (10 ** 9, 2 * 10 ** 9, 16 * 10 ** 9))
        self.assertEqual(v['TOTAL'], 19 * 10 ** 9)  # overdue 4000 and missing 8000 excluded
        self.assertNotIn('OVERDUE', v)
        self.assertTrue(any('OVERDUE' in i for i in s['issues']) and any('MISSING' in i for i in s['issues']))
        cols = cmp.template_columns('maturity_loan', v)
        self.assertEqual(cols['M'], Decimal(19))  # total in M, not J
        self.assertEqual(cols['J'], Decimal(0))  # J is the 5-10 year bucket
        self.assertEqual(cols['C'], Decimal(1))

    @unittest.skipUnless((ROOT / 'data/bank_sources/NBS01 Sep 2026 English.xlsx').exists(), 'template missing')
    def test_template_headers_match_semantic_map(self):
        from nbs_control.bank_data import xlsx_rows
        rows = dict(xlsx_rows(ROOT / 'data/bank_sources/NBS01 Sep 2026 English.xlsx'))
        self.assertEqual({k: v for k, v in rows[769].items() if k != 'A'}, mat.TEMPLATE_T10_HEADERS)
        self.assertEqual((rows[1240]['B'], rows[1240]['C'], rows[1240]['K']), ('Current and Call', 'Saving', 'Total Amount'))

    def test_legacy_calc_row_writes_total_in_m(self):
        from nbs_control.generation import calc_row
        c = sqlite3.connect(':memory:')
        c.execute('CREATE TABLE facts(source TEXT, account TEXT, maturity TEXT, product TEXT, unavailable INTEGER, ethix_carrying REAL, category TEXT)')
        c.executemany('INSERT INTO facts VALUES(?,?,?,?,?,?,?)', [('ECB_LOAN', 'a', '2026-10-03', 'X', 0, 1000.0, '1'),
                                                                   ('ECB_LOAN', 'b', '2033-01-01', 'X', 0, 3000.0, '1'),
                                                                   ('ECB_LOAN', 'c', '2020-01-01', 'X', 0, 500.0, '1')])
        spec = {'source': 'ECB_LOAN', 'filter': None, 'measure': 'ethix_carrying', 'components': [], 'factor': 1, 'enabled': True,
                'notes': [], 'layout': 'maturity_loan', 'negative_filter': None}
        r = calc_row(c, spec, {'ECB': {'component_columns': []}}, 1000, {'as_of': '2026-09-30', 'missing_balance_columns': {}})
        self.assertEqual(r['values']['M'], 4.0)
        self.assertEqual(r['values']['C'], 1.0)
        self.assertEqual(r['values']['J'], 3.0)  # 2033 is in 5-10 years under both conventions
        self.assertEqual(r['values']['B'], 0.0)


class T10Units(unittest.TestCase):
    def test_counts_and_rates(self):
        self.assertEqual(bo_reference.classify('012', 'Upto 100th')['kind'], 'count')
        self.assertEqual(bo_reference.classify('012', 'Upto 100th Amt')['kind'], 'money')
        r = bo_reference.classify('017', 'Rate Depre In Qatar')
        self.assertEqual((r['kind'], r['additive']), ('rate', False))
        self.assertEqual(cmp.display(7, 'count'), Decimal(7))  # never divided by 1000
        self.assertEqual(cmp.display(7 * 10 ** 9, 'money'), Decimal(7))
        rows = [dict(fid=1, source='ECB_LOAN', account='a', currency='QAR', residency='', country='', maturity='', product='', risk='',
                     personal='', industry='', unavailable=0, issue=None, amount=150000.0)]
        s = eng.legacy_semantic({'source': 'ECB_LOAN', 'factor': 1, 'layout': 'size'}, rows, '2026-09-30', {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(s['semantic']['BAND_HUN_TO_1000TH_COUNT'], 1)
        self.assertEqual(s['semantic']['BAND_HUN_TO_1000TH_AMOUNT'], 150000 * 10 ** 6)

    def test_subtotal_skips_rates(self):
        cat = {'tables': {'017': {'measures': {'Cost In Qatar': {'kind': 'money', 'additive': True, 'semantic': 'C', 'primary': True},
                                               'Rate Depre In Qatar': {'kind': 'rate', 'additive': False, 'semantic': 'R', 'primary': True}}}}}
        mk = lambda tid, item, par, method='NONE': {'target_id': tid, 'table': '017', 'item_code': item, 'parent_code': par, 'status': 'PROVISIONAL', 'method': method}
        maps = {'targets': {'017|1': mk('017|1', '1', None, 'SUBTOTAL_OF_CHILDREN'), '017|11': mk('017|11', '11', '1'), '017|12': mk('017|12', '12', '1')}}
        res = {k: {'cells': {'Cost In Qatar': {'value': v, 'status': 'PROVISIONAL', 'issues': []}, 'Rate Depre In Qatar': {'value': 5, 'status': 'PROVISIONAL', 'issues': []}}}
               for k, v in (('017|1', None), ('017|11', 10), ('017|12', 20))}
        eng._subtotals(maps, res, cat)
        self.assertEqual(res['017|1']['cells']['Cost In Qatar']['value'], 30)
        self.assertEqual(res['017|1']['cells']['Rate Depre In Qatar']['status'], 'NOT_APPLICABLE')


class T11GrossNet(unittest.TestCase):
    def test_parent_plus_children_rejected(self):
        with self.assertRaisesRegex(ValueError, 'descendant'):
            tm.check_disjoint_codes(['1-018-1090203', '1-018-109020301'])
        tm.check_disjoint_codes(['1-018-1090201', '1-018-1090202', '1-018-1090203'])

    @unittest.skipUnless(STORE.exists(), 'real store not built')
    def test_real_intangibles(self):
        from nbs_control.rebuild_run import reference_controls
        with closing(sqlite3.connect(STORE)) as c:
            ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS'").fetchone()[0]
            r = reference_controls(c, ref)
        g = r['intangibles_gross_net']
        self.assertEqual((Decimal(g['table_018_top_level_gross']), Decimal(g['signed_amortization']), Decimal(g['net'])),
                         (Decimal(896109), Decimal(-603699), Decimal(292410)))
        self.assertEqual(Decimal(g['table_100_cell_E50']), Decimal(896109))
        self.assertEqual(Decimal(r['assets_vs_liabilities_capital']['difference']), Decimal(5747560))


class T13LegacyGL(unittest.TestCase):
    CSV = ROOT / 'exports/rebuild_review_20261017/balance_sheet_case_rules.csv'
    OUT = ROOT / 'exports/rebuild_review_20261017/balance_sheet_output_lines.csv'

    def test_ordered_rules_signs_fallback_and_omissions(self):
        rules = legacy_gl.load_rules(self.CSV)
        outs = legacy_gl.load_outputs(self.OUT)
        self.assertEqual(legacy_gl.classify(rules, {'ledger': '1302000010', 'account': ''}), 6)  # exact before broad prefix
        self.assertEqual(legacy_gl.classify(rules, {'ledger': '1101010015', 'account': ''}), 5)  # excluded from group 8
        self.assertEqual(legacy_gl.classify(rules, {'ledger': '1502000001', 'account': '01-01-900-60-01-2305550001'}), 4)
        self.assertEqual(legacy_gl.classify(rules, {'ledger': '2305550001', 'account': '01-01-900-60-01-2305550001'}), 4)
        self.assertEqual(legacy_gl.classify(rules, {'ledger': '9999999999', 'account': ''}), 38)
        self.assertEqual((legacy_gl.legacy_sign('2300000001'), legacy_gl.legacy_sign('2309000001'), legacy_gl.legacy_sign('2309050001')), (-1, -1, 1))
        res = legacy_gl.run(rules, outs, [{'ledger': '1504010001', 'account': '', 'amount': Decimal(5000)},
                                          {'ledger': '9999999999', 'account': '', 'amount': Decimal(7000)},
                                          {'ledger': '1000000001', 'account': '', 'amount': Decimal(1000)}])
        self.assertEqual(sorted(res['omitted_nonzero']), [17, 38])
        total = next(x for x in res['lines'] if x['description'] == 'TOTAL ASSETS')
        self.assertEqual((total['value'], total['status']), (None, 'LEGACY_LITERAL_ZERO_NOT_CERTIFIED'))
        cash = next(x for x in res['lines'] if x['line'] == 2)
        self.assertEqual(cash['value'], Decimal(1))

    def test_unsupported_sql_fails(self):
        with self.assertRaises(legacy_gl.LegacyRuleError):
            legacy_gl.parse("(A.ledger_no LIKE '10%')")
        with self.assertRaises(legacy_gl.LegacyRuleError):
            legacy_gl.parse("(Exec('x'))")


class T14Loans(unittest.TestCase):
    def test_owner_groups_unchanged_and_no_alias(self):
        rules = json.loads((ROOT / 'config/balance_rules.json').read_text(encoding='utf-8'))
        flat = [t for g in rules['groups'].values() for t in g]
        for name in ('NABACCOUNT', 'NABDEFERREDPFT', 'RECPRINCIPALPFT', 'DEFERREDPFT'):
            self.assertIn(name, flat)
        pol = json.loads((ROOT / 'config/report_product_policies.json').read_text(encoding='utf-8'))
        self.assertIn('ACCCRPROFIT', json.dumps(pol['products']['CLM']))
        self.assertNotIn('ACCDEPOSITPFT', json.dumps(pol['products']['CLM'].get('linked_coefficients', {})))

    def test_sdb_charges_are_category_events_not_fees(self):
        rows = [{'row_no': 1, 'source_id': 'x', 'amount': 800 * 10 ** 6, 'currency': 'QAR', 'event_type': 'CHARGE-MAKE.DUE-DUE / SDB-CHARGE', 'weight': 1, 'state': 'UNIQUE_OBSERVATION'}]
        s = eng.categ_semantic({'categ': {'sign': 1, 'geography': 'UNKNOWN'}}, rows)
        self.assertNotIn('IN_LC', s['semantic'])  # no residency -> primary columns unavailable
        cat = {'tables': {'008': {'measures': {'In Amount Lc': {'kind': 'money', 'semantic': 'IN_LC', 'primary': True}}}}}
        s['source_kind'] = 'T24_CATEG_ENTRY'
        cells = eng.cell_values({'table': '008'}, s, cat, 'PROVISIONAL')
        self.assertIsNone(cells['In Amount Lc']['value'])
        self.assertEqual(cells['In Amount Lc']['status'], 'UNAVAILABLE')

    def test_hybrid_fee_lineage_labelled(self):
        import inspect
        self.assertIn('HYBRID', inspect.getsource(eng.generate_targets))


class T15Partitions(unittest.TestCase):
    def test_overlap_and_uncovered_detected_unknown_sector_kept(self):
        maps = {'targets': {'044|1': {'table': '044', 'parent_code': None}, '044|11': {'table': '044', 'parent_code': '1'},
                            '044|12': {'table': '044', 'parent_code': '1'}}}
        mk = lambda fids: [(f, 'ECB_LOAN', 'a', 'IN_LC', 10, 1, None) for f in fids]
        d = eng.partition_diagnostics(maps, {'044|1': mk([1, 2, 3]), '044|11': mk([1, 2]), '044|12': mk([2])})
        self.assertEqual((d[0]['overlap_records'], d[0]['uncovered_parent_records']), (1, 1))
        rows = [dict(fid=1, source='ECB_LOAN', account='a', currency='QAR', residency='', country='', maturity='', product='', risk='',
                     personal=None, industry=None, unavailable=0, issue=None, amount=5.0)]
        s = eng.legacy_semantic({'source': 'ECB_LOAN', 'factor': 1, 'layout': 'sector_columns'}, rows, '2026-09-30', {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(s['semantic']['TOTAL'], 0)
        self.assertEqual(s['contributions'][0][3], 'UNKNOWN_SECTOR')
        g = eng.legacy_semantic({'source': 'ECB', 'factor': 1, 'layout': None}, rows, '2026-09-30', {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(g['contributions'][0][3], 'UNKNOWN_DIMENSION')


class T8T16T17T18EndToEnd(unittest.TestCase):
    """Fixture project: upload/import -> preview -> owner edit -> regenerate -> compare both references -> Excel."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp())
        (cls.root / 'config').mkdir()
        for f in ('balance_rules.json', 'report_product_policies.json', 'generation_rules.json'):
            shutil.copy(ROOT / 'config' / f, cls.root / 'config' / f)
        rev = cls.root / 'exports/rebuild_review_20261017'
        rev.mkdir(parents=True)
        for f in ('reporting_basis_owner_confirmation.json', 'balance_sheet_case_rules.csv', 'balance_sheet_output_lines.csv'):
            shutil.copy(ROOT / 'exports/rebuild_review_20261017' / f, rev / f)
        cls.categ = cls.root / 'categ.xlsx'
        categ_workbook(cls.categ, [categ_row('1', '400'), categ_row('1', '400'), categ_row('2', '-1000.5', pl='51008', soft='ACCOUNT-CHARGEOFF-DUE', u='LOAN-ACCOUNT'),
                                   categ_row('3', '2500', pl='61001', ref=None, value=None, system='DC', soft=None, u=None, product=None)])
        cls.bo = cls.root / 'bo.xlsx'
        bo_workbook(cls.bo)
        cls.live = cls.root / 'live.xlsx'
        write_xlsx(cls.live, [('S', [['Description', 'X'], ['Cash', ('n', '1')]])])
        from nbs_control import rebuild_run as rr
        cls.rr = rr
        cls.setup = rr.setup(cls.root, [str(cls.categ)], str(cls.bo), str(cls.live), log=lambda *_: None)
        cls.sha = cls.setup['categ'][0]['sha256']
        # Fixture source gets its own owner policy (the real policy must not apply to it).
        doc = json.loads((cls.root / 'config' / policies.BASIS_FILE).read_text())
        doc['policies'].append(dict(doc['policies'][0], policy_id='FIXTURE', source_sha256=cls.sha))
        policies.save_basis_policy(cls.root / 'config', doc, 'test', 'fixture policy')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def run_(self, **kw):
        return self.rr.run(self.root, '2026-09-30', live_ref='LIVE_NBS01_2026-09', with_stock=False, log=lambda *_: None, **kw)

    def target(self):
        return dict(tm.load(self.root / 'config')['targets']['001|1-001-10101'])

    def test_a_flow(self):
        cat = json.loads((self.root / 'config/bo_measure_catalogue.json').read_text())
        t = self.target()
        t.update(status='PROVISIONAL', method='CATEG_EVENTS', date_basis='EVENTS_EFFECTIVE_PERIOD',
                 categ={'filter': {'field': 'pl_category', 'op': 'in', 'values': ['52258']}, 'sign': 1, 'geography': 'IN'})
        prev = self.rr.preview_target(self.root, t['target_id'], t)
        self.assertEqual(next(r for r in prev['rows'] if r['measure'] == 'In LC Amount')['new'], Decimal('0.8'))
        prev2 = self.rr.preview_target(self.root, t['target_id'], t)
        self.assertEqual(prev, prev2)  # deterministic
        m1 = self.run_(label='before')
        tm.save_target(self.root / 'config', t['target_id'], t, 'owner', 'map SDB charges for test', cat)
        self.assertEqual(self.rr.stale_reasons(self.root, m1), ['mapping_sha256'])
        m2 = self.run_(label='after')
        self.assertNotEqual(m1['mapping_version'], m2['mapping_version'])
        self.assertTrue((self.root / 'data/rebuild/runs' / m1['run_id'] / 'manifest.json').exists())  # previous run intact
        with closing(sqlite3.connect(self.root / 'data/rebuild/runs' / m2['run_id'] / 'run.sqlite')) as db:
            v, st = db.execute("SELECT value_micro, status FROM cells WHERE target_id='001|1-001-10101' AND measure='In LC Amount'").fetchone()
            self.assertEqual((v, st), (800 * 10 ** 6, 'UNRESOLVED_DUPLICATE_BASIS'))
            n = db.execute("SELECT count(*) FROM contributions WHERE target_id='001|1-001-10101' AND included=1").fetchone()[0]
            self.assertEqual(n, 2)
        # Both reference versions compared; Excel written and validated against BO headers.
        self.assertEqual(m2['reference_versions'], {'bo': 'BO_' + sha256(self.bo)[:12], 'live': 'LIVE_NBS01_2026-09'})
        self.assertEqual(m2['excel']['verification']['status'], 'PASS', m2['excel']['verification'])
        self.assertEqual(m2['category_reporting_basis']['policy_id'], 'FIXTURE')
        ctl = json.loads((self.root / 'data/rebuild/runs' / m2['run_id'] / 'controls.json').read_text())
        rec = ctl['category_reconciliation']
        self.assertEqual(rec['status'], 'PASS')
        self.assertEqual(rec['parts']['contributed']['rows'], 2)
        self.assertEqual(Decimal(rec['source_total']), Decimal('2299.5'))
        # Web: drilldown and Excel download through the owner interface
        from flask import Flask
        from nbs_control.rebuild_web import register_rebuild_routes
        app = Flask('t', template_folder=str(ROOT / 'nbs_control/templates'))
        app.secret_key = 'x'
        app.jinja_env.globals.update(json=json)

        @app.context_processor
        def inj():
            return {'csrf_token': ''}
        for name in ('dashboard', 'mappings', 'decisions', 'unresolved', 'findings', 'sections', 'config_index', 'run', 'reports', 'exports', 'setup', 'report_mapping'):
            app.add_url_rule('/' + name + '/<path:key>' if name == 'report_mapping' else '/' + name, name, lambda **k: '')
        register_rebuild_routes(app, self.root)
        cl = app.test_client()
        self.assertEqual(cl.get('/rebuild').status_code, 200)
        r = cl.get(f'/rebuild/runs/{m2["run_id"]}/cell?target=001|1-001-10101&measure=In+LC+Amount')
        self.assertIn(b'400.000000', r.data)
        self.assertEqual(cl.get(f'/rebuild/runs/{m2["run_id"]}/table/001').status_code, 200)
        self.assertEqual(cl.get('/rebuild/mapping/001|1-001-10101').status_code, 200)
        self.assertEqual(cl.get('/rebuild/policies').status_code, 200)
        x = cl.get(f'/rebuild/runs/{m2["run_id"]}/download/NBS_Rebuild_2026-09-30.xlsx')
        self.assertEqual(x.status_code, 200)
        self.assertTrue(x.data[:2] == b'PK')
        x.close()

    def test_b_reference_change_does_not_change_generation(self):
        m1 = self.run_()
        db = self.root / 'data/rebuild/rebuild_store.sqlite'
        with closing(sqlite3.connect(db)) as c:
            c.execute("UPDATE bo_cells SET value_micro=value_micro+999000000 WHERE item_code='1-001-10101'")
            c.execute("UPDATE live_cells SET value_micro=value_micro+5")
            c.commit()
        m2 = self.run_()
        g = lambda m: dict(((r[0], r[1]), r[2]) for r in sqlite3.connect(self.root / 'data/rebuild/runs' / m['run_id'] / 'run.sqlite').execute('SELECT target_id, measure, value_micro FROM cells'))
        self.assertEqual(g(m1), g(m2))
        import inspect
        src = inspect.getsource(eng)
        self.assertNotIn('bo_cells', src)
        self.assertNotIn('live_cells', src)
        with closing(sqlite3.connect(db)) as c:
            c.execute("UPDATE bo_cells SET value_micro=value_micro-999000000 WHERE item_code='1-001-10101'")
            c.commit()

    def test_c_zero_override_differs_from_empty(self):
        cat = json.loads((self.root / 'config/bo_measure_catalogue.json').read_text())
        t = self.target()
        t['overrides'] = {'Out LC Amount': {'value': '0', 'reason': 'deliberate zero'}, 'Out FC Amount': {'value': None, 'reason': 'intentionally blank'}}
        res, _ = eng.generate_targets({'targets': {t['target_id']: t}}, cat, None, {'rules': {}}, None, None, {}, '2026-09-30',
                                      {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        cells = res[t['target_id']]['cells']
        self.assertEqual((cells['Out LC Amount']['value'], cells['Out LC Amount']['status']), (0, 'MANUAL_OVERRIDE'))
        self.assertEqual((cells['Out FC Amount']['value'], cells['Out FC Amount']['status']), (None, 'MANUAL_OVERRIDE_EMPTY'))
        with self.assertRaises(ValueError):
            tm.validate_target(dict(t, overrides={'Out LC Amount': {'value': '0', 'reason': ''}}), cat)

    def test_d_dropped_population_fails(self):
        from nbs_control import rebuild_run as rr
        with closing(connect(self.root / 'data/rebuild/rebuild_store.sqlite')) as c:
            w = policies.row_weights(c, self.sha, {'default_treatment': 'UNRESOLVED_RETAIN_ALL', 'decisions': {}})
            ok = rr.reconcile_categ(c, self.sha, w, {}, {'targets': {}})
            self.assertEqual(ok['status'], 'PASS')
            c.execute('DELETE FROM categ_events WHERE source_sha256=? AND row_no=(SELECT max(row_no) FROM categ_events WHERE source_sha256=?)', (self.sha, self.sha))
            bad = rr.reconcile_categ(c, self.sha, w, {}, {'targets': {}})
            c.rollback()
        self.assertEqual(bad['status'], 'FAIL_POPULATION_DROPPED_OR_ADDED')

    def test_e_filter_validation_blocks_unknown_fields_and_sql(self):
        for bad in ({'field': 'amount_micro', 'op': 'in', 'values': ['1']}, {'field': 'pl_category', 'op': 'sql', 'values': ['1']},
                    {'field': "pl_category; DROP TABLE x", 'op': 'in', 'values': ['1']}, {'field': 'category', 'op': 'in', 'values': ['1']}):
            with self.assertRaises(ValueError):
                tm.validate_filter(bad)
        params = []
        sql = tm.compile_filter({'all': [{'field': 'pl_category', 'op': 'in', 'values': ["x' OR 1=1 --"]}, {'field': 'product_category', 'op': 'prefix', 'values': ['39']}]}, params)
        self.assertNotIn("OR 1=1", sql)
        self.assertIn("x' OR 1=1 --", params)


@unittest.skipUnless(REAL_CATEG.exists() and STORE.exists(), 'real category source not available')
class RealCategory(unittest.TestCase):
    def test_real_counts(self):
        self.assertEqual(sha256(REAL_CATEG), CATEG_SHA)
        if REAL_CATEG_COPY.exists():
            self.assertEqual(sha256(REAL_CATEG_COPY), CATEG_SHA)
        with closing(sqlite3.connect(STORE)) as c:
            self.assertEqual(c.execute('SELECT count(*) FROM sources WHERE dataset="CATEG_ENTRY"').fetchone()[0], 1)
            ctl = categ_data.source_controls(c, CATEG_SHA)
            self.assertEqual((ctl['rows'], ctl['distinct_ids'], ctl['ids_with_multiple_variants'], ctl['blank_reference_rows'], ctl['unheaded_u_rows']),
                             (81722, 1711, 1440, 2335, 79387))
            self.assertEqual(ctl['value_date_profile'], {'blank': 2335, 'october_or_later': 652, 'on_or_before_2026-09-30': 78735})
            self.assertEqual(ctl['by_booking_date'].keys(), {'2026-10-01'})
            g = categ_data.repeated_groups(c, CATEG_SHA)
            self.assertEqual(sum(x['excess'] for x in g), 24515)
            self.assertEqual(sum(x['excess_micro'] for x in g), -60216695110000)
            self.assertEqual(c.execute('SELECT count(*) FROM categ_events WHERE source_sha256=? AND pl_category="51008"', (CATEG_SHA,)).fetchone()[0], 79097)


if __name__ == '__main__':
    unittest.main()
