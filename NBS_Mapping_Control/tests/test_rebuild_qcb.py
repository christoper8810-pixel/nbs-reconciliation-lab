"""QCB validation rules, structural crosswalk, inherited dimensions, distinctness, QCB-derived mappings, GL evidence, export."""
import json
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from decimal import Decimal
from pathlib import Path

from nbs_control import crosswalk as cw, qcb_validations as q, rebuild_engine as eng, target_mappings as tm
from tests.rebuild_fixtures import write_xlsx

ROOT = Path(__file__).resolve().parents[1]
QCB_DIR = ROOT / 'data' / 'qcb_validations'
STORE = ROOT / 'data' / 'rebuild' / 'rebuild_store.sqlite'

CAT = {'tables': {
    '100': {'measures': {h: {'semantic': s, 'kind': 'money', 'primary': True, 'unit': 'K', 'additive': True}
                         for h, s in (('In Lc Amount', 'IN_LC'), ('In Fc Amount', 'IN_FC'), ('Out Lc Amount', 'OUT_LC'), ('Out Fc Amount', 'OUT_FC'))}},
    '001': {'measures': {h: {'semantic': s, 'kind': 'money', 'primary': True, 'unit': 'K', 'additive': True}
                         for h, s in (('In LC Amount', 'IN_LC'), ('In FC Amount', 'IN_FC'), ('Out LC Amount', 'OUT_LC'), ('Out FC Amount', 'OUT_FC'))}},
    '012': {'measures': {'Upto 100th': {'semantic': 'BAND_UPTO_100TH_COUNT', 'kind': 'count', 'primary': True, 'unit': 'COUNT'},
                         'Upto 100th Amt': {'semantic': 'BAND_UPTO_100TH_AMOUNT', 'kind': 'money', 'primary': True, 'unit': 'K'}}},
}}


class Parsing(unittest.TestCase):
    def test_terms_measures_and_precedence(self):
        n = q.parse_expr('$001{1-001-10101}#INSIDE_LC+INSIDE_FC#-($001{1-001-10102}#INSIDE_LC#+2)')
        vals = {('001', '1-001-10101', 'INSIDE_LC'): Decimal(5), ('001', '1-001-10101', 'INSIDE_FC'): Decimal(7), ('001', '1-001-10102', 'INSIDE_LC'): Decimal(1)}
        self.assertEqual(q.evaluate(n, lambda t, i, m: vals[(t, i, m)]), Decimal(9))
        r = q.parse_expr('($012{1-012-01}#UP_TO_100_AMT#/($012{1-012-01}#UP_TO_100_NO#+0.0001))')
        self.assertTrue(q.has_ratio(r))
        self.assertEqual(q.evaluate(q.parse_expr('2*3+4'), None), Decimal(10))

    def test_mechanical_repairs_are_flagged(self):
        a = q.parse_expr('$601{6-601-101}#THREE_TO_6_MONTHS#+$602{6-602-101}#THREE_TO_6_MONTHS+$602{6-602-201}#THREE_TO_6_MONTHS#')
        self.assertEqual([t['repaired'] for t in q.terms(a)], [False, True, False])
        b = q.parse_expr('$614{6-614-1}#SUBSTAND_DIR_PROV#+614{6-614-2}#SUBSTAND_DIR_PROV#')
        self.assertEqual([t['table'] for t in q.terms(b)], ['614', '614'])
        self.assertTrue(list(q.terms(b))[1]['repaired'])

    def test_unsupported_syntax_rejected(self):
        for bad in ("$001{1}#A# ; DROP", "exec('x')", '$001{1}#A# $001{2}#B#', '($001{1}#A#'):
            with self.assertRaises(q.RuleSyntaxError):
                q.parse_expr(bad)

    def test_measure_dictionary_uses_validated_headers(self):
        self.assertEqual(q.header_for('100', 'INSIDE_LC', CAT), 'In Lc Amount')
        self.assertEqual(q.header_for('001', 'OUTSIDE_FC', CAT), 'Out FC Amount')
        self.assertEqual(q.header_for('012', 'UP_TO_100_NO', CAT), 'Upto 100th')
        self.assertIsNone(q.header_for('100', 'GCC_BALANCE', CAT))

    def test_check_statuses_and_tolerance(self):
        rule = {'left_ast': q.parse_expr('$100{1-100-101}#INSIDE_LC#'), 'right_ast': q.parse_expr('$001{1-001-10101}#INSIDE_LC#+$001{1-001-10102}#INSIDE_LC#'), 'operator': '='}
        vals = {('100', '1-100-101', 'In Lc Amount'): Decimal(10), ('001', '1-001-10101', 'In LC Amount'): Decimal(9), ('001', '1-001-10102', 'In LC Amount'): Decimal('0.5')}
        lk = q.lookup_factory(vals, CAT, {'100', '001'})
        self.assertEqual(q.check(rule, lk)['status'], 'PASS_WITHIN_ROUNDING')
        vals[('001', '1-001-10102', 'In LC Amount')] = Decimal(1)
        self.assertEqual(q.check(rule, lk)['status'], 'PASS')
        vals[('001', '1-001-10102', 'In LC Amount')] = Decimal(5)
        self.assertEqual(q.check(rule, lk)['status'], 'FAIL')
        vals[('001', '1-001-10102', 'In LC Amount')] = None
        self.assertEqual(q.check(rule, lk)['status'], 'NOT_EVALUABLE')
        self.assertIn('not in this report version', q.check({**rule, 'right_ast': q.parse_expr('$601{6-601-1}#ONE_WEEK#')}, lk)['reason'])

    @unittest.skipUnless(QCB_DIR.exists() and len(list(QCB_DIR.glob('*.xlsx'))) == 5, 'QCB files not present')
    def test_real_files(self):
        rules, errors = q.load_rules(sorted(QCB_DIR.glob('*.xlsx')))
        self.assertEqual((len(rules), len(errors)), (2664, 0))
        self.assertTrue(all(r['provenance'] for r in rules))
        kinds = {r['kind'] for r in rules}
        self.assertIn('CROSS_DIMENSION_SAME_POPULATION', kinds)
        r1 = next(r for r in rules if r['left'] == '$100{1-100-101}#INSIDE_LC#')
        self.assertEqual(r1['kind'], 'BASE_SCHEDULE_TO_DETAIL')


class Crosswalk(unittest.TestCase):
    def test_codes_from_ordinals_with_learned_prefix(self):
        bo = {'044': {'1-044-01': 'Inside Qatar', '1-044-0102': 'II - INDUSTRY', '1-044-01020401': '1. Food'},
              '007': {'1-007-10401': 'Debt Securities', '1-007-1040101': 'Issued by Governments'}}
        rules = {'A': {'table': 44, 'section': 'ETHIX|T44|R105', 'path': '01 Inside Qatar > ....02 INDUSTRY > ......04 MANUFACTURING > ........01 Food'},
                 'B': {'table': 44, 'section': 'ETHIX|T44|R105', 'path': '01 Inside Qatar'},
                 'C': {'table': 7, 'section': 'ETHIX|T7|R-', 'path': '01 Debt Securities > .......01 Issued by Governments'},
                 'D': {'table': 7, 'section': 'ETHIX|T7|R-', 'path': '01 Debt Securities'}}
        links, prefixes = cw.structural_crosswalk(rules, bo)
        self.assertEqual(prefixes['007'][0], '104')
        self.assertEqual(links['1-044-01020401'][0]['rule_id'], 'A')
        self.assertEqual(links['1-007-1040101'][0]['basis'], 'STRUCTURAL_CODE_TEXT_CONFIRMED')

    def test_text_score_variants_and_real_changes(self):
        self.assertGreaterEqual(cw.text_score('........08 Aluminum', '8. Aluminium'), 0.5)
        self.assertGreaterEqual(cw.text_score("........02 Istisna'a", 'Istisnaa'), 0.5)
        self.assertLess(cw.text_score('.........05 Personal Against Salary', 'Consumers'), 0.5)

    @unittest.skipUnless(STORE.exists(), 'real store not built')
    def test_real_crosswalk_agrees_with_review_candidates(self):
        import csv
        rules = json.loads((ROOT / 'config/generation_rules.json').read_text())['rules']
        with closing(sqlite3.connect(STORE)) as c:
            ref = c.execute("SELECT ref_version FROM ref_versions WHERE kind='ETHIX_BO_NBS'").fetchone()[0]
            bo = {}
            for t, i, d in c.execute('SELECT table_code, item_code, description FROM bo_items WHERE ref_version=?', (ref,)):
                bo.setdefault(t, {})[i] = d
        links, _ = cw.structural_crosswalk(rules, bo)
        self.assertGreaterEqual(len(links), 1560)
        self.assertTrue(all(len(v) == 1 for v in links.values()))
        cand = {r['bo_item_code']: r['candidate_ids'] for r in csv.DictReader(open(ROOT / 'exports/rebuild_review_20261017/bo_to_current_mapping_candidates.csv', encoding='utf-8-sig'))
                if r['status'] == 'UNREVIEWED_EXACT_PATH_CANDIDATE'}
        self.assertEqual(sum(links.get(k, [{}])[0].get('rule_id') == v for k, v in cand.items()), len(cand))


HIER = {'enabled': True, 'apply_to_leaf': True, 'namespace_corrections': {'industry_4digit_to_sector': True},
        'labels': {'inside qatar': {'ECB_LOAN': {'field': 'residency', 'op': 'eq', 'values': ['Resident']}},
                   'private sector': {'SECTOR': 'private sector'}, 'corporates': {'ECB_LOAN': {'field': 'personal', 'op': 'eq', 'values': ['NonPersonal']}},
                   'overdraft': {'ECB_LOAN': {'field': 'product', 'op': 'in', 'values': ['NONE_CONVENTIONAL_PRODUCT']}, 'FORCE': True, 'PROVISIONAL': 'Islamic bank'}}}


class Inheritance(unittest.TestCase):
    def spec(self, path, flt=None, source='ECB_LOAN'):
        return {'source': source, 'path': path, 'filter': flt, 'measure': 'outstanding', 'factor': 1}

    def test_parent_dimensions_added_unless_fixed(self):
        e, notes = eng.inherit_hierarchy(self.spec('01 Inside Qatar > 03 Private Sector > 01 Corporates'), HIER)
        flds = eng._fields(e['filter'], set())
        self.assertTrue({'residency', 'personal', 'industry'} <= flds)
        e2, _ = eng.inherit_hierarchy(self.spec('01 Inside Qatar > 01 X', {'field': 'residency', 'op': 'eq', 'values': ['NonResident']}), HIER)
        self.assertEqual(e2['filter'], {'field': 'residency', 'op': 'eq', 'values': ['NonResident']})  # own top-level condition wins

    def test_or_clause_does_not_block_leaf_label(self):
        own = {'any': [{'field': 'personal', 'op': 'eq', 'values': ['Personal']}, {'field': 'industry', 'op': 'prefix', 'values': ['4']}]}
        e, _ = eng.inherit_hierarchy(self.spec('03 Private Sector > 01 Corporates', own), HIER)
        self.assertIn({'field': 'personal', 'op': 'eq', 'values': ['NonPersonal']}, e['filter']['all'])

    def test_forced_empty_product_and_provisional_note(self):
        e, notes = eng.inherit_hierarchy(self.spec('01 X > 01 Overdraft', {'field': 'product', 'op': 'in', 'values': ['RCM']}), HIER)
        self.assertIn('NONE_CONVENTIONAL_PRODUCT', json.dumps(e['filter']))
        self.assertTrue(any('PROVISIONAL' in n for n in notes))

    def test_four_digit_sector_codes_move_to_sector(self):
        own = {'any': [{'field': 'industry', 'op': 'range', 'values': [1000, 1999]}, {'field': 'industry', 'op': 'eq', 'values': ['47004']}]}
        e, notes = eng.inherit_hierarchy(self.spec('X', own), {**HIER, 'labels': {}})
        self.assertEqual([x['field'] for x in e['filter']['any']], ['sector', 'industry'])
        self.assertTrue(notes and 'SECTOR' in notes[0])


class Distinctness(unittest.TestCase):
    def test_identical_non_nested_selectors_flagged_empty_exempt(self):
        rules = {r: {'enabled': True, 'source': 'ECB_LOAN', 'measure': 'outstanding', 'factor': 1, 'path': p, 'filter': f}
                 for r, p, f in (('P', '01 Public', {'field': 'industry', 'op': 'prefix', 'values': ['1']}),
                                 ('A', '01 Public > 01 Governments', {'field': 'industry', 'op': 'prefix', 'values': ['1']}),
                                 ('B', '01 Public > 05 Social Insurance', {'field': 'industry', 'op': 'prefix', 'values': ['1']}),
                                 ('C', '01 Public > 02 Overdraft', None), ('D', '01 Public > 03 Overdraft', None))}
        mk = lambda tid, item, par, rid: {'target_id': tid, 'table': '009', 'item_code': item, 'parent_code': par, 'status': 'DRAFT_CANDIDATE', 'method': 'LEGACY_RULE', 'legacy_rule_id': rid}
        doc = {'targets': {'009|1': mk('009|1', '1', None, 'P'), '009|11': mk('009|11', '11', '1', 'A'), '009|15': mk('009|15', '15', '1', 'B'),
                           '009|12': mk('009|12', '12', '1', 'C'), '009|13': mk('009|13', '13', '1', 'D')}}
        flagged = tm.non_distinct_selectors(doc, rules, HIER)
        self.assertEqual(sorted(flagged), ['009|11', '009|15'])


class QcbDerived(unittest.TestCase):
    def test_composition_from_generated_cells_only(self):
        rule = {'rule_id': 'Q1', 'qcb_code': '1', 'left': '$100{1-100-101}#INSIDE_LC#', 'right': 'x',
                'left_ast': q.parse_expr('$100{1-100-101}#INSIDE_LC#'), 'right_ast': q.parse_expr('$001{1-001-10101}#INSIDE_LC#+$001{1-001-10102}#INSIDE_LC#')}
        target = {'target_id': '100|1-100-101', 'table': '100', 'item_code': '1-100-101', 'status': 'DRAFT_CANDIDATE', 'method': 'QCB_COMPOSITION',
                  'qcb_composition': {'INSIDE_LC': {'rule_id': 'Q1', 'qcb_code': '1', 'kind': 'BASE', 'side': 'left'}}}
        cells = lambda v: {h: {'value': v if h == 'In LC Amount' else None, 'status': 'DRAFT_CANDIDATE_PREVIEW', 'issues': []} for h in CAT['tables']['001']['measures']}
        results = {'100|1-100-101': {'target': target, 'cells': {h: {'value': None, 'status': 'UNAVAILABLE', 'issues': []} for h in CAT['tables']['100']['measures']}},
                   '001|1-001-10101': {'target': {'table': '001', 'method': 'LEGACY_RULE'}, 'cells': cells(7_000_000)},
                   '001|1-001-10102': {'target': {'table': '001', 'method': 'LEGACY_RULE'}, 'cells': cells(3_000_000)}}
        contrib = {}
        eng._compositions({'targets': {}}, results, contrib, CAT, [rule])
        c = results['100|1-100-101']['cells']['In Lc Amount']
        self.assertEqual((c['value'], c['status'], c['source_kind']), (10_000_000, 'DRAFT_CANDIDATE_PREVIEW', 'QCB_COMPOSITION'))
        self.assertEqual(results['100|1-100-101']['cells']['In Fc Amount']['status'], 'UNAVAILABLE')
        self.assertEqual(len(contrib['100|1-100-101']), 2)

    def test_population_union_counts_shared_accounts_once(self):
        rows = {'A': [dict(fid=1, source='ECB_LOAN', amount=10.0), dict(fid=2, source='ECB_LOAN', amount=20.0)], 'B': [dict(fid=2, source='ECB_LOAN', amount=20.0)]}
        base = dict(account='x', currency='QAR', residency='Resident', country='QA', maturity='', product='MUR', risk='', personal='Personal',
                    industry='47004', unavailable=0, issue=None, rim='R1')

        class Facts:
            def rows(self, spec):
                return [dict(base, **r) for r in rows[spec['id']]], [], []
        specs = {'A': {'id': 'A', 'enabled': True, 'source': 'ECB_LOAN', 'measure': 'outstanding', 'components': [], 'factor': 1, 'path': 'a', 'filter': None},
                 'B': {'id': 'B', 'enabled': True, 'source': 'ECB_LOAN', 'measure': 'outstanding', 'components': [], 'factor': 1, 'path': 'b', 'filter': None}}
        cat = {'tables': {'009': {'measures': {'In Amount Lc': {'semantic': 'IN_LC', 'kind': 'money', 'primary': True}}}}}
        t = {'target_id': '009|x', 'table': '009', 'item_code': 'x', 'status': 'DRAFT_CANDIDATE', 'method': 'QCB_POPULATION',
             'legacy_rule_ids': ['A', 'B'], 'qcb_rule_id': 'Q', 'qcb_code': '1', 'layout': 'geo'}
        res, _ = eng.generate_targets({'targets': {'009|x': t}}, cat, Facts(), {'rules': specs}, None, None, {}, '2026-09-30',
                                      {'maturity_convention': 'DAY_COUNT', 'open_ended_products': [], 'hierarchy_predicates': None})
        self.assertEqual(res['009|x']['cells']['In Amount Lc']['value'], 30 * 10 ** 6)
        self.assertTrue(any('counted once' in i for i in res['009|x']['issues']))

    def test_customer_grain_bands(self):
        rows = [dict(fid=i, source='ECB_DEPOSIT', account=f'A{i}', currency='QAR', residency='Resident', country='', maturity='', product='CUR',
                     risk='', personal='Personal', industry='', unavailable=0, issue=None, amount=a, rim=r)
                for i, (a, r) in enumerate([(60000.0, 'C1'), (60000.0, 'C1'), (5000.0, 'C2')])]
        s = eng.legacy_semantic({'source': 'ECB_DEPOSIT', 'factor': 1, 'layout': 'size', 'size_grain': 'customer'}, rows, '2026-09-30',
                                {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(s['semantic']['BAND_HUN_TO_1000TH_COUNT'], 1)  # customer C1 = 120k
        self.assertEqual(s['semantic']['BAND_UPTO_100TH_COUNT'], 1)
        a = eng.legacy_semantic({'source': 'ECB_DEPOSIT', 'factor': 1, 'layout': 'size'}, rows, '2026-09-30', {'maturity_convention': 'DAY_COUNT', 'open_ended_products': []})
        self.assertEqual(a['semantic']['BAND_UPTO_100TH_COUNT'], 3)  # account grain differs


class GlEvidence(unittest.TestCase):
    def test_minimum_misplacement_is_lower_bound(self):
        from nbs_control import gl_evidence as g
        tmp = Path(tempfile.mkdtemp())
        try:
            db = tmp / 'bank.sqlite'
            c = sqlite3.connect(db)
            c.execute('CREATE TABLE unique_records(source TEXT, gl TEXT, residency TEXT, currency TEXT, industry TEXT, personal TEXT, maturity TEXT, product TEXT, amount REAL, rim TEXT)')
            c.execute('CREATE TABLE records(source TEXT, residency TEXT, country TEXT, industry TEXT, maturity TEXT, rim TEXT, risk TEXT, currency TEXT, gl TEXT)')
            c.executemany('INSERT INTO unique_records VALUES(?,?,?,?,?,?,?,?,?,?)', [
                ('LOAN', 'G1', 'Resident', 'QAR', '47004', 'Personal', '2027-01-01', 'MUR', 70.0, 'a'),
                ('LOAN', 'G1', 'NonResident', 'QAR', '47004', 'Personal', '2027-01-01', 'MUR', 30.0, 'b'),
                ('LOAN', 'G2', 'Resident', 'USD', '47004', 'Personal', '2027-01-01', 'MUR', 50.0, 'c'),
                ('DEPOSIT', 'G3', 'Resident', 'QAR', '47004', 'Personal', '', 'CUR', 10.0, 'd')])
            c.commit()
            c.close()
            out = g.account_dispersion(db)
            r = out['LOAN']['by_breakdown']['residency (Inside/Outside Qatar)']
            self.assertEqual((Decimal(r['minimum_misplaced_by_any_gl_mapping_qar']), r['gls_spanning_several_cells']), (Decimal(30), 1))
            self.assertEqual(r['minimum_misplaced_pct'], 20.0)
            self.assertEqual(out['LOAN']['by_breakdown']['currency (LC/FC)']['minimum_misplaced_pct'], 0.0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless((ROOT / 'data/rebuild/runs/latest.json').exists(), 'no real run yet')
class Export(unittest.TestCase):
    def test_export_round_trip(self):
        from nbs_control import mapping_export as mx
        out = Path(tempfile.mkdtemp())
        try:
            r = mx.export(ROOT, out_dir=out)
            self.assertEqual(r['verification']['status'], 'PASS')
            self.assertEqual(r['targets'], 1649)
            j = json.loads(next(out.glob('*.json')).read_text(encoding='utf-8'))
            self.assertEqual(len(j['targets']), 1649)
            from openpyxl import load_workbook
            wb = load_workbook(next(out.glob('*.xlsx')), read_only=True)
            for sheet in ('README', 'Summary_by_table', 'Mapping', 'Measures', 'Hierarchy_rules', 'QCB_validations', 'Review_queue', 'Data_requests'):
                self.assertIn(sheet, wb.sheetnames)
            wb.close()
        finally:
            shutil.rmtree(out, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()


class LaterRules(unittest.TestCase):
    def test_month_end_convention(self):
        from nbs_control import maturity as m
        self.assertEqual(m.bucket('2026-12-31', '2026-09-30', convention='CALENDAR_EOM'), 'MAT_3M')
        self.assertEqual(m.bucket('2026-12-31', '2026-09-30', convention='CALENDAR'), 'MAT_6M')
        self.assertEqual(m.bucket('2027-01-31', '2026-09-30', convention='CALENDAR_EOM'), 'MAT_6M')
        self.assertEqual(m.bucket('2027-03-30', '2026-09-15', convention='CALENDAR_EOM'), 'MAT_12M')  # not a month-end report date

    def test_component_typos_and_words(self):
        corr = {'typos': {'CONTDRBL': {'to': 'CONTDBBL'}}, 'not_balance_types': {'words': ['FOR', 'WILL']}}
        s, notes = eng.correct_components({'components': ['CONTCR', 'CONTDRBL', 'FOR', 'WILL', 'NABACCOUNT']}, corr)
        self.assertEqual(s['components'], ['CONTCR', 'CONTDBBL', 'NABACCOUNT'])  # owner type untouched
        self.assertTrue(notes)

    def test_sector_labels_only_on_joined_sources(self):
        cfg = {'enabled': True, 'apply_to_leaf': True, 'labels': {'private sector': {'SECTOR': 'private sector'}}}
        s = {'source': 'ECB', 'path': '01 Guarantees > 02 Private Sector', 'filter': {'field': 'sector', 'op': 'range', 'values': [2000, 2003]}}
        e, notes = eng.inherit_hierarchy(s, cfg)
        self.assertEqual(e['filter'], s['filter'])

    def test_residual_others_excludes_named_siblings(self):
        base = dict(account='a', currency='QAR', residency='Resident', country='QA', maturity='', product='', risk='', personal='',
                    industry='', unavailable=0, issue=None, rim=None, source='ECB')
        rows = {'N': [dict(base, fid=1, amount=100.0)], 'O': [dict(base, fid=1, amount=100.0), dict(base, fid=2, amount=40.0)]}

        class Facts:
            def rows(self, spec):
                return [dict(r) for r in rows[spec['id']]], [], []
        spec = lambda i: {'id': i, 'enabled': True, 'source': 'ECB', 'measure': 'amount', 'components': [], 'factor': 1, 'path': i,
                          'filter': {'field': 'category', 'op': 'eq', 'values': [i]}}
        cat = {'tables': {'035': {'measures': {'In Lc Amount': {'semantic': 'IN_LC', 'kind': 'money', 'primary': True}}}}}
        mk = lambda tid, code, par, desc, rid: {'target_id': tid, 'table': '035', 'item_code': code, 'parent_code': par, 'description': desc,
                                                'status': 'DRAFT_CANDIDATE', 'method': 'LEGACY_RULE' if rid else 'NONE', 'legacy_rule_id': rid}
        maps = {'targets': {'035|1': mk('035|1', '1', None, 'Guarantees', None), '035|11': mk('035|11', '11', '1', 'Performance Bonds', 'N'),
                            '035|17': mk('035|17', '17', '1', 'Others', 'O')}}
        res, contrib = eng.generate_targets(maps, cat, Facts(), {'rules': {'N': spec('N'), 'O': spec('O')}}, None, None, {}, '2026-09-30',
                                            {'maturity_convention': 'DAY_COUNT', 'open_ended_products': [], 'hierarchy_predicates': None})
        self.assertEqual(res['035|17']['cells']['In Lc Amount']['value'], 40 * 10 ** 6)
        self.assertEqual(res['035|11']['cells']['In Lc Amount']['value'], 100 * 10 ** 6)
