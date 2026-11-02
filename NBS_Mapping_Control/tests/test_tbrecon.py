"""Regression tests for the whole-TB reconciliation (tbrecon) and the GL Report token fixes. SYNTHETIC data only."""
from __future__ import annotations

import csv
import json
import shutil
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path

from nbs_control.tbrecon import criteria as C, engine_a, engine_b, engine_c, rules as R, run as tbrun, synthetic, tb
from nbs_control.tbrecon import compare, rootcause
from nbs_control.tbrecon.keys import KeyLayout, layouts

ROOT = Path(__file__).resolve().parent.parent
CFG = tbrun.load_config(ROOT / 'config' / 'tb_recon.json')
D = Decimal


def rows(dicts):
    return [{**d, '_row': i + 2} for i, d in enumerate(dicts)]


def meta(dicts):
    hs = []
    for d in dicts:
        for k in d:
            if k not in hs and not k.startswith('_'):
                hs.append(k)
    return {'headers': hs, 'name': 'x', 'sha256': '0', 'rows': len(dicts)}


def ac(cat, prod='4101', sector='1000', ccy='QAR'):
    return synthetic.ac_key(ccy, cat, prod, sector)


class Criteria(unittest.TestCase):
    def test_range_or_list(self):
        c = C.parse('1000-1999, 6001, 7001')
        for v, ok in (('1000', True), ('1999', True), ('1500', True), ('2000', False), ('6001', True), ('7001', True), ('6002', False)):
            self.assertEqual(c.matches(v), ok, v)

    def test_newline_and_semicolon_alternatives_and_prefix(self):
        c = C.parse('3701\n3702; 38*')
        self.assertTrue(c.matches('3702') and c.matches('3850') and not c.matches('3900'))

    def test_blank_explicit_any_and_blank_token(self):
        self.assertFalse(C.parse('').restricted)
        self.assertTrue(C.parse('*').explicit and not C.parse('*').restricted)
        b = C.parse('<BLANK>')
        self.assertTrue(b.matches('') and not b.matches('X'))
        self.assertEqual(C.parse('', cfg={'blank_means': 'MUST_BE_BLANK'}).kind, 'BLANK')

    def test_malformed_and_reversed_ranges_fail_loudly(self):
        with self.assertRaises(C.CriteriaError):
            C.parse('1999-1000')
        with self.assertRaises(C.CriteriaError):
            C.parse('*UNDEFINED')

    def test_named_range(self):
        self.assertTrue(C.parse('*CASH', {'CASH': '1000-1009, 1020'}).matches('1020'))

    def test_legacy_mode_reproduces_old_literal_range(self):
        self.assertFalse(C.parse('1000-1999', legacy=True).matches('1500'))


class Keys(unittest.TestCase):
    def test_historical_ac_example(self):
        lay = layouts(CFG)['AC']
        dims, tokens, err = lay.parse('AC.1.TR.QAR.3717.5261.1000.14.QA.47004.2Y......QA0011014')
        self.assertIsNone(err)
        self.assertEqual((dims['currency'], dims['category'], dims['product'], dims['sector'], dims['department'], dims['residence'],
                          dims['industry'], dims['maturity'], dims['company']),
                         ('QAR', '3717', '5261', '1000', '14', 'QA', '47004', '2Y', 'QA0011014'))
        self.assertEqual(len(tokens), 17)
        self.assertIn('sector', lay.unverified())

    def test_pl_layout_is_separate(self):
        lay = layouts(CFG)['PL']
        dims, _t, err = lay.parse(synthetic.pl_key(52000, 'QAR', 3701, '14'))
        self.assertIsNone(err)
        self.assertEqual((dims['pl_category'], dims['currency'], dims['product'], dims['department'], dims['company']),
                         ('52000', 'QAR', '3701', '14', synthetic.COMPANY))
        self.assertTrue(lay.parse('AC.1.TR.QAR.3717')[2])     # AC key rejected by the PL layout

    def test_errors_and_cache(self):
        lay = KeyLayout('AC', CFG['consol_key_layouts']['AC'])
        self.assertEqual(lay.parse('')[2], 'EMPTY_KEY')
        self.assertTrue(lay.parse('AC.1.TR')[2].startswith('TOO_FEW_TOKENS'))
        self.assertTrue(lay.parse('PL' + '.x' * 15)[2].startswith('PREFIX'))
        k = ac('3701')
        self.assertIs(lay.parse(k), lay.parse(k))


RULE_COLS = ['RULE_ID', 'TYPE', 'TARGET_GL', 'BALANCE_TYPE', 'CATEGORY', 'SECTOR', 'PRODUCT', 'CURRENCY', 'PRIORITY', 'TOTAL_OF', 'RANGE_NAME', 'RANGE_VALUES']


def rule_rows(*specs):
    return rows([{c: s.get(c, '') for c in RULE_COLS} for s in specs])


class Rules(unittest.TestCase):
    def load(self, rr, legacy=False):
        rs = R.load(rr, ['CATEGORY', 'SECTOR', 'PRODUCT', 'CURRENCY'], CFG, with_bt=True, legacy=legacy)
        rs.index()
        return rs

    def test_continuation_rows_and_inheritance(self):
        rs = self.load(rule_rows({'RULE_ID': 'L1', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '1000'},
                                 {'BALANCE_TYPE': '^', 'CATEGORY': '3901', 'SECTOR': '^'}))
        self.assertEqual([r.id for r in rs.rules], ['L1#1', 'L1#2'])
        r2 = rs.rules[1]
        self.assertEqual((r2.bt_names, r2.targets, r2.crit['sector'].values()), (['CURACCOUNT'], ['G1'], ['1000']))
        self.assertEqual(rs.match({'category': '3901', 'sector': '1000'}, 'CURACCOUNT')[0], 'MAPPED')

    def test_equal_specificity_conflict_is_ambiguous_never_first(self):
        rs = self.load(rule_rows({'RULE_ID': 'A', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '1000'},
                                 {'RULE_ID': 'B', 'TARGET_GL': 'G2', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'CURRENCY': 'QAR'}))
        st, top = rs.match({'category': '3701', 'sector': '1000', 'currency': 'QAR'}, 'CURACCOUNT')
        self.assertEqual((st, sorted(r.id for r in top)), ('AMBIGUOUS', ['A#1', 'B#1']))
        legacy = self.load(rule_rows({'RULE_ID': 'A', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '1000'},
                                     {'RULE_ID': 'B', 'TARGET_GL': 'G2', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '37*', 'CURRENCY': 'QAR'}), legacy=True)
        self.assertEqual(legacy.match({'category': '37*', 'currency': 'QAR', 'sector': '9'}, 'CURACCOUNT')[1][0].id, 'B#1')

    def test_specificity_and_priority(self):
        spec = [{'RULE_ID': 'A', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799'},
                {'RULE_ID': 'B', 'TARGET_GL': 'G2', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '1000'}]
        rs = self.load(rule_rows(*spec))
        self.assertEqual(rs.match({'category': '3701', 'sector': '1000'}, 'CURACCOUNT')[1][0].id, 'B#1')
        spec[0]['PRIORITY'] = '5'
        rs = self.load(rule_rows(*spec))
        self.assertEqual(rs.match({'category': '3701', 'sector': '1000'}, 'CURACCOUNT')[1][0].id, 'A#1')

    def test_multi_target_rule_never_allocates(self):
        rs = self.load(rule_rows({'RULE_ID': 'A', 'TARGET_GL': 'G1, G2', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3701'}))
        st, top = rs.match({'category': '3701'}, 'CURACCOUNT')
        self.assertEqual(st, 'MULTI_TARGET_UNRESOLVED')
        self.assertTrue(any(d['type'] == 'MULTI_TARGET_RULE' for d in rs.diagnostics))

    def test_duplicate_and_conflicting_duplicates(self):
        rs = self.load(rule_rows({'RULE_ID': 'A', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CREDIT', 'CATEGORY': '1001'},
                                 {'RULE_ID': 'B', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CREDIT', 'CATEGORY': '1001'},
                                 {'RULE_ID': 'C', 'TARGET_GL': 'G9', 'BALANCE_TYPE': 'DEBIT', 'CATEGORY': '1001'},
                                 {'RULE_ID': 'D', 'TARGET_GL': 'G8', 'BALANCE_TYPE': 'DEBIT', 'CATEGORY': '1001'}))
        types = {d['type'] for d in rs.diagnostics}
        self.assertTrue({'DUPLICATE_RULE', 'CONFLICTING_DUPLICATE_RULES'} <= types)
        self.assertEqual(rs.match({'category': '1001'}, 'CREDIT')[0], 'MAPPED')
        self.assertEqual(rs.match({'category': '1001'}, 'DEBIT')[0], 'AMBIGUOUS')

    def test_rule_without_atomic_balance_type_is_unusable(self):
        rs = self.load(rule_rows({'RULE_ID': 'A', 'TARGET_GL': 'G1', 'CATEGORY': '3701'}, {'RULE_ID': 'B', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CUR*'}))
        self.assertEqual([r.bt_error for r in rs.rules], ['NO_ATOMIC_BALANCE_TYPE', 'BALANCE_TYPE_NOT_ATOMIC'])


def run_a(asset, rr, cfg=CFG):
    return engine_a.run(rows(asset), meta(asset), rule_rows(*rr), {'headers': RULE_COLS}, cfg, layouts(cfg)['AC'])


class EngineA(unittest.TestCase):
    RULES = ({'RULE_ID': 'P', 'TARGET_GL': 'G_PRIN', 'BALANCE_TYPE': 'CURACCOUNT, DUEACCOUNT', 'CATEGORY': '3700-3799'},
             {'RULE_ID': 'A', 'TARGET_GL': 'G_ACC', 'BALANCE_TYPE': 'ACCPRINCIPALPFT', 'CATEGORY': '3700-3799'},
             {'RULE_ID': 'G', 'TARGET_GL': 'G_GRC', 'BALANCE_TYPE': 'GRCACCOUNT', 'CATEGORY': '3700-3799'})

    def asset(self):
        return [{'ACCOUNT_NO': 'S1', 'CONSOL_KEY': ac('3701'), 'LEGACY_GL': 'LG1', 'CURACCOUNT_BAL_QAR': '100.10', 'DUEACCOUNT_BAL_QAR': '0',
                 'ACCPRINCIPALPFT_BAL_QAR': '7.05', 'BLCURACCOUNT_BAL_QAR': '-3', 'UNKNOWNX_BAL_QAR': ''}]

    def test_unpivot_atomic_types_one_key_several_gls(self):
        a = run_a(self.asset(), self.RULES)
        self.assertEqual(a['expected'], {('G_PRIN', 'QAR'): D('100.10'), ('G_ACC', 'QAR'): D('7.05')})
        grain = {(c['consol_key'], c['balance_type'], c['target_gl']) for c in a['contributions']}
        self.assertEqual(grain, {(ac('3701'), 'CURACCOUNT', 'G_PRIN'), (ac('3701'), 'ACCPRINCIPALPFT', 'G_ACC')})
        ci = a['controls_input']
        self.assertEqual((ci['raw_total'], ci['component_total'], ci['zero_cells'], ci['missing_cells']), (D('104.15'), D('104.15'), 1, 1))

    def test_no_blanket_sum_contra_kept_separate(self):
        a = run_a(self.asset(), self.RULES)
        contra = [c for c in a['components'] if c['balance_type'] == 'BLCURACCOUNT']
        self.assertEqual((contra[0]['status'], contra[0]['amount'], contra[0]['contra']), ('CONTRA_UNRESOLVED', D('-3'), True))
        self.assertNotIn(D('101.15'), a['expected'].values())     # 100.10 + 7.05 - 3 would be a blanket sum

    def test_contra_allocates_only_when_named(self):
        a = run_a(self.asset(), self.RULES + ({'RULE_ID': 'C', 'TARGET_GL': 'G_CONTRA', 'BALANCE_TYPE': 'BLCURACCOUNT', 'CATEGORY': '3701'},))
        self.assertEqual(a['expected'][('G_CONTRA', 'QAR')], D('-3'))

    def test_unsupported_balance_type_reported_not_zero(self):
        a = run_a(self.asset(), self.RULES)
        self.assertEqual([u['balance_type'] for u in a['unsupported_balance_types']], ['GRCACCOUNT'])
        self.assertIn('G_GRC', a['incomplete_gls'])
        self.assertNotIn(('G_GRC', 'QAR'), a['expected'])

    def test_validated_alias_only(self):
        cfg = {**CFG, 'balance_type_aliases': {'CURACC': 'CURACCOUNT', 'BADALIAS': 'NOPE'}}
        rr = ({'RULE_ID': 'P', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACC', 'CATEGORY': '3701'},
              {'RULE_ID': 'Q', 'TARGET_GL': 'G2', 'BALANCE_TYPE': 'BADALIAS', 'CATEGORY': '3701'})
        a = run_a(self.asset(), rr, cfg)
        self.assertEqual(a['expected'][('G1', 'QAR')], D('100.10'))
        self.assertEqual({x['alias']: x['status'] for x in a['aliases']}['BADALIAS'], 'INVALID_TARGET_NOT_IN_SCHEMA')
        self.assertEqual([u['balance_type'] for u in a['unsupported_balance_types']], ['BADALIAS'])

    def test_invalid_key_and_balance_type_totals(self):
        asset = self.asset() + [{'ACCOUNT_NO': 'S2', 'CONSOL_KEY': 'AC.1.TR', 'CURACCOUNT_BAL_QAR': '5'}]
        a = run_a(asset, self.RULES)
        self.assertEqual(a['stats']['INVALID_KEY'], 1)
        self.assertEqual(a['column_totals']['CURACCOUNT'], sum(a['bt_totals']['CURACCOUNT'].values(), D(0)))

    def test_misalignment_detected_with_evidence(self):
        asset = [{'ACCOUNT_NO': f'C{i}', 'CONSOL_KEY': ac('3702', prod='5261', sector='2001'), 'CURACCOUNT_BAL_QAR': '10'} for i in range(3)]
        asset += [{'ACCOUNT_NO': 'R1', 'CONSOL_KEY': ac('3702', prod='4101', sector='1000'), 'CURACCOUNT_BAL_QAR': '1'}]
        rr = ({'RULE_ID': 'RET', 'TARGET_GL': 'G1', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '1000'},
              {'RULE_ID': 'CORP', 'TARGET_GL': 'G2', 'BALANCE_TYPE': 'CURACCOUNT', 'CATEGORY': '3700-3799', 'SECTOR': '5261'})
        a = run_a(asset, rr)
        f = a['misalignment']
        self.assertEqual(len(f), 1)
        self.assertEqual((f[0]['type'], f[0]['rule_column'], f[0]['observed_dimension'], f[0]['affected_rules'], f[0]['affected_rows'],
                          f[0]['net_amount']), ('POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', 'SECTOR', 'product', ['CORP#1'], 3, D('30')))
        self.assertEqual(sum(1 for c in a['components'] if c.get('misalignment')), 3)


class EngineB(unittest.TestCase):
    def test_one_to_one_without_consol_key_and_defects(self):
        src = [{'ACCOUNT_NO': 'I1', 'CURRENCY': 'QAR', 'BALANCE': '10', 'CONSOL_KEY': ''},
               {'ACCOUNT_NO': 'I2', 'CURRENCY': 'QAR', 'BALANCE': '20'},
               {'ACCOUNT_NO': 'I3', 'CURRENCY': 'QAR', 'BALANCE': '30'},
               {'ACCOUNT_NO': 'I4', 'CURRENCY': 'QAR', 'BALANCE': '40'},
               {'ACCOUNT_NO': 'N1', 'CURRENCY': 'USD', 'BALANCE': '50', 'CUSTOMER_ACCOUNT_REF': 'NOSTRO-1'},
               {'ACCOUNT_NO': 'N2', 'CURRENCY': 'USD', 'BALANCE': '60', 'CUSTOMER_ACCOUNT_REF': 'NOSTRO-X'}]
        imap = [{'ACCOUNT_NO': 'I1', 'TARGET_ACCOUNT': 'QAR1900100010001', 'TARGET_GL': 'G19'},
                {'ACCOUNT_NO': 'I3', 'TARGET_ACCOUNT': 'QAR1', 'TARGET_GL': 'G19'}, {'ACCOUNT_NO': 'I3', 'TARGET_ACCOUNT': 'QAR2', 'TARGET_GL': 'G20'},
                {'ACCOUNT_NO': 'I4', 'TARGET_ACCOUNT': 'USD1900100010004', 'TARGET_GL': 'G19'},
                {'ACCOUNT_NO': 'N1', 'TARGET_ACCOUNT': 'WRONG', 'TARGET_GL': 'G99'}]
        cmap = [{'ACCOUNT_NO': 'NOSTRO-1', 'TARGET_ACCOUNT': 'USD1200100010001', 'TARGET_GL': 'G12'}]
        b = engine_b.run(rows(src), meta(src), rows(imap), rows(cmap), None, CFG)
        st = {c['account']: c['status'] for c in b['components']}
        self.assertEqual(st, {'I1': 'MAPPED', 'I2': 'MISSING_MAPPING', 'I3': 'DUPLICATE_MAPPING', 'I4': 'MAPPED', 'N1': 'MAPPED',
                              'N2': 'CUSTOMER_REF_UNRESOLVED'})
        self.assertEqual(b['expected'], {('G19', 'QAR'): D('50'), ('G12', 'USD'): D('50')})   # N1 resolved by customer ref, not by I-map
        i4 = next(c for c in b['components'] if c['account'] == 'I4')
        self.assertIn('TARGET_ACCOUNT_CURRENCY_MISMATCH', i4['flags'])
        self.assertFalse(b['controls_input']['consol_key_used'])

    def test_pending_without_source(self):
        self.assertEqual(engine_b.run(None, None, [], [], None, CFG)['status'], 'SOURCE_PENDING')


class EngineC(unittest.TestCase):
    def test_pl_rules_and_unavailable_dimension(self):
        src = [{'CONSOL_KEY': synthetic.pl_key(51001, 'QAR', 3701), 'BALANCE': '-5'},
               {'CONSOL_KEY': synthetic.pl_key(52000, 'QAR', 3750), 'BALANCE': '-7'},
               {'CONSOL_KEY': synthetic.pl_key(52000, 'QAR', 6001), 'BALANCE': '-9'},
               {'CONSOL_KEY': 'AC.1.TR.QAR.3717', 'BALANCE': '-1'}]
        pr = [{'RULE_ID': 'P1', 'TARGET_GL': 'G51', 'PL_CATEGORY': '51000-51099', 'PRODUCT': '', 'SECTOR': ''},
              {'RULE_ID': 'P2', 'TARGET_GL': 'G52A', 'PL_CATEGORY': '52000', 'PRODUCT': '3700-3799', 'SECTOR': ''},
              {'RULE_ID': 'P3', 'TARGET_GL': 'G52B', 'PL_CATEGORY': '52000', 'PRODUCT': '', 'SECTOR': ''},
              {'RULE_ID': 'P4', 'TARGET_GL': 'G59', 'PL_CATEGORY': '59000', 'PRODUCT': '', 'SECTOR': '1000'}]
        c = engine_c.run(rows(src), meta(src), rows(pr), meta(pr), CFG, layouts(CFG)['PL'])
        self.assertEqual(c['expected'], {('G51', 'QAR'): D('-5'), ('G52A', 'QAR'): D('-7'), ('G52B', 'QAR'): D('-9')})
        self.assertEqual(c['stats']['INVALID_KEY'], 1)
        self.assertTrue(any(d['type'] == 'DIMENSION_NOT_AVAILABLE' for d in c['rule_diagnostics']))

    def test_missing_pl_source_is_pending(self):
        self.assertEqual(engine_c.run(None, None, [], {'headers': []}, CFG, layouts(CFG)['PL'])['status'], 'SOURCE_PENDING')


class Synthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='tbrecon-'))
        cls.clean = synthetic.build(cls.tmp / 'clean', 'clean')
        cls.defects = synthetic.build(cls.tmp / 'defects', 'defects')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def execute(self, folder, legacy=False, drop=(), cfg=None):
        cfg = cfg or tbrun.load_config(folder / 'tb_recon.json')
        paths = {k: v for k, v in tbrun.discover(folder).items() if k not in drop}
        data, metas = tbrun.load_inputs(paths)
        return tbrun.execute(data, metas, cfg, legacy=legacy)

    def test_clean_reconstruction_equals_independent_truth(self):
        res = self.execute(self.clean)
        truth = {tuple(k.split('|')): D(v) for k, v in json.loads((self.clean / 'truth.json').read_text())['expected'].items()}
        got = {(r['target_gl'], r['currency']): r['expected'] for r in res['recon']['gl_rows']}
        self.assertEqual(got, truth)
        self.assertEqual({r['recon_status'] for r in res['recon']['gl_rows']}, {'RECONCILED'})
        st = {c['id']: c['status'] for c in res['controls']}
        self.assertTrue(all(st[k] == 'PASS' for k in ('C01', 'C02', 'C03', 'C04', 'C05', 'C05B', 'C06', 'C07', 'C08', 'C09', 'C11')), st)
        self.assertEqual(st['C12'], 'WARN')      # unverified AC layout is never silently accepted
        self.assertFalse([i for i in res['issues'] if not i['informational']])

    def test_clean_gl_report_totals_from_details(self):
        res = self.execute(self.clean)
        rep = {r['line']: r for r in res['recon']['gl_report']}
        self.assertEqual(rep['H100']['amount'], None)
        self.assertEqual(rep['T190']['amount'], sum((rep[x]['amount'] for x in ('L110', 'L120', 'L130', 'L150')), D(0)))
        self.assertEqual(rep['T190']['amount'] + rep['T290']['amount'],
                         sum((c['amount'] for c in res['engines']['A']['components'] if c['status'] == 'MAPPED'), D(0)))

    def test_clean_rollforward_separates_post_cob(self):
        res = self.execute(self.clean)
        r = next(x for x in res['recon']['rollforward'] if x['target_gl'] == '1101000030' and x['currency'] == 'QAR')
        self.assertEqual(r['validated_post_cob_movements'], D('1234.56'))
        self.assertEqual(r['computed_closing'], r['actual_closing'])
        self.assertEqual(r['opening_migrated_expected'] + D('1234.56'), r['actual_closing'])

    def test_reproducible(self):
        self.assertEqual(self.execute(self.defects)['result_hash'], self.execute(self.defects)['result_hash'])

    def test_every_injected_defect_is_detected(self):
        res = self.execute(self.defects)
        exc = res['exceptions']
        cats = lambda **kw: [e for e in exc if all(e.get(k) == v for k, v in kw.items())]  # noqa: E731
        A = res['engines']['A']
        self.assertEqual([(m['rule_column'], m['observed_dimension'], m['affected_rules']) for m in A['misalignment']],
                         [('SECTOR', 'product', ['L120#1'])])                                                     # D01
        self.assertTrue(cats(category='PRODUCT_SECTOR_MISALIGNMENT', level='COMPONENT'))
        self.assertTrue(cats(category='AMBIGUOUS_MAPPING', level='COMPONENT'))                                     # D02
        self.assertTrue([c for c in A['components'] if c['status'] == 'MULTI_TARGET_UNRESOLVED'])                 # D03
        self.assertEqual({u['balance_type'] for u in A['unsupported_balance_types']}, {'GRCACCOUNT'})              # D04
        self.assertTrue(cats(category='WRONG_OR_MISSING_BALANCE_TYPE', balance_type='PDODEFERREDPFT'))             # D05
        self.assertTrue(cats(category='CONTRA_BL_TREATMENT', balance_type='BLCURACCOUNT'))                         # D06
        self.assertEqual(A['stats']['INVALID_KEY'], 6)                                                             # D07
        self.assertEqual(A['controls_input']['duplicate_source_keys'], 1)                                          # D08
        self.assertTrue(cats(category='SIGN_CONVENTION_MISMATCH', target_gl='3001000010'))                         # D09
        self.assertEqual({e['target_gl'] for e in cats(category='WRONG_TARGET_GL', level='GL')} >= {'1501000010', '1501000020'}, True)  # D10
        self.assertEqual({e['subtype'] for e in cats(category='INTERNAL_ACCOUNT_MAPPING_DEFECT', level='COMPONENT')},
                         {'MISSING_MAPPING', 'DUPLICATE_MAPPING', 'TARGET_ACCOUNT_CURRENCY_MISMATCH', 'CUSTOMER_REF_UNRESOLVED'})  # D11 D12
        multi = [l for l in res['recon']['legacy_lines'] if l['legacy_gl'] == 'LG-1600-001'][0]
        self.assertEqual(multi['status'], 'MULTI_TARGET_UNRESOLVED')                                               # D13
        self.assertTrue(cats(category='MISSING_SOURCE_RECORD', legacy_gl='LG-1900-001'))                           # D14
        self.assertEqual(len(res['recon']['movements_excluded']), 2)                                               # D15
        self.assertTrue(cats(category='WRONG_DIMENSION', target_gl='9001000010', level='GL'))                      # D16
        self.assertTrue(cats(category='MISSING_MAPPING', legacy_gl='LG-1700-001'))                                 # D17
        self.assertTrue(cats(category='PL_MAPPING_DEFECT'))                                                        # D18
        self.assertTrue(any(d['type'] == 'DIMENSION_NOT_AVAILABLE' for d in res['engines']['C']['rule_diagnostics']))
        self.assertTrue(cats(category='WRONG_TARGET_GL', level='RULE', rule_id='L210#2'))                          # D19

    def test_multi_target_never_split_or_first(self):
        res = self.execute(self.defects)
        gl = {(r['target_gl'], r['currency']): r for r in res['recon']['gl_rows']}
        for t in ('1601000010', '1601000020'):
            self.assertEqual(gl[(t, 'QAR')]['expected'], D(0))
            self.assertEqual(gl[(t, 'QAR')]['recon_status'], 'INCOMPLETE')

    def test_whole_tb_walk_ties_and_nothing_disappears(self):
        res = self.execute(self.defects)
        walk = next(c for c in res['controls'] if c['id'] == 'C05B')
        self.assertEqual(walk['status'], 'PASS')
        self.assertEqual(next(c for c in res['controls'] if c['id'] == 'C02')['status'], 'PASS')

    def test_no_false_success_when_pl_source_missing(self):
        res = self.execute(self.clean, drop=('pl_balances',))
        pl = [r for r in res['recon']['gl_rows'] if r['class'] == 'PL']
        self.assertTrue(pl and all(r['recon_status'] == 'SOURCE_PENDING' for r in pl))
        self.assertEqual(res['engines']['C']['status'], 'SOURCE_PENDING')
        self.assertTrue(all(l['status'] == 'SOURCE_PENDING' for l in res['recon']['legacy_lines'] if l['class'] == 'PL'))
        self.assertEqual(next(c for c in res['controls'] if c['id'] == 'C05B')['status'], 'PASS')
        self.assertNotEqual(next(c for c in res['controls'] if c['id'] == 'C05')['status'], 'PASS')

    def test_missing_actual_tb_is_incomplete(self):
        res = self.execute(self.clean, drop=('actual_tb',))
        self.assertEqual(next(c for c in res['controls'] if c['id'] == 'C05')['status'], 'INCOMPLETE')

    def test_tolerance_is_configurable_and_displayed(self):
        cfg = tbrun.load_config(self.defects / 'tb_recon.json')
        cfg['tolerance'] = {'absolute': '100', 'relative': '0'}
        res = self.execute(self.defects, cfg=cfg)
        self.assertEqual(res['recon']['tolerance'], {'absolute': '100', 'relative': '0'})
        self.assertEqual(next(r for r in res['recon']['gl_rows'] if r['target_gl'] == '5101000010')['recon_status'], 'RECONCILED')

    def test_proposals_are_a_copy_and_fix_the_misalignment(self):
        res = self.execute(self.defects)
        data, metas = tbrun.load_inputs(tbrun.discover(self.defects))
        original = json.dumps(data['gl_rules'], sort_keys=True)
        fixed, applied = rootcause.apply_worklist(data['gl_rules'], res['worklist'])
        self.assertEqual(json.dumps(data['gl_rules'], sort_keys=True), original)
        self.assertEqual(len(applied), 1)
        data['gl_rules'] = fixed
        after = tbrun.execute(data, metas, tbrun.load_config(self.defects / 'tb_recon.json'))
        self.assertFalse(after['engines']['A']['misalignment'])
        before_corp = sum(1 for c in res['engines']['A']['components'] if c['account'].startswith('SYNC') and c['status'] == 'MAPPED' and c['rule_id'].startswith('L120'))
        after_corp = sum(1 for c in after['engines']['A']['components'] if c['account'].startswith('SYNC') and c['rule_id'].startswith('L120'))
        self.assertEqual(before_corp, 0)
        self.assertGreater(after_corp, 0)

    def test_legacy_semantics_baseline_loses_inline_ranges(self):
        before = self.execute(self.clean, legacy=True)
        self.assertGreater(tbrun.statistics(before)['components_unmapped'], 0)
        self.assertEqual(tbrun.statistics(self.execute(self.clean))['components_unmapped'], 0)


class StoreExportsCliWeb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='tbrecon-store-'))
        cls.ds = synthetic.build(cls.tmp / 'in', 'defects')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_store_exports_and_compare(self):
        paths = tbrun.discover(self.ds)
        cfg = compare.folder_config(self.ds)
        a, fa, ra = tbrun.run_and_store(paths, self.tmp / 'store' / 'data', self.tmp / 'store' / 'exports', 'before', cfg)
        for f in ('run.sqlite', 'audit.json', 'report.html', 'reconciliation.xlsx', 'tb_reconciliation.csv', 'root_causes.csv',
                  'proposed_mapping_corrections.csv', 'components.csv'):
            self.assertTrue((fa / f).exists(), f)
        audit = json.loads((fa / 'audit.json').read_text())
        self.assertEqual(len(audit['top_20_exceptions']), 20)
        self.assertEqual(next(c for c in audit['controls'] if c['id'] == 'C10')['status'], 'PASS')
        import openpyxl
        wb = openpyxl.load_workbook(fa / 'reconciliation.xlsx', read_only=True)
        self.assertIn('Correction_Worklist', wb.sheetnames)
        wb.close()
        b, fb, rb, applied = compare.run_with_proposals(paths, self.tmp / 'store' / 'data', self.tmp / 'store' / 'exports', cfg)
        cmp = compare.compare_runs(self.tmp / 'store' / 'data', self.tmp / 'store' / 'exports', a, b)
        self.assertGreater(cmp['summary']['CHANGED'] + cmp['summary']['RESOLVED'], 0)
        self.assertEqual([r['run_id'] for r in tbrun.list_runs(self.tmp / 'store' / 'data')], [b, a])
        a2, *_ = tbrun.run_and_store(paths, self.tmp / 'store' / 'data', self.tmp / 'store' / 'exports', 'again', cfg)
        rerun = tbrun.get_run(self.tmp / 'store' / 'data', a2)
        self.assertEqual(rerun['reproducible'], 'PASS')
        self.assertEqual(rerun['result_hash'], tbrun.get_run(self.tmp / 'store' / 'data', a)['result_hash'])

    def test_cli_exit_codes(self):
        from nbs_control.cli import main
        import contextlib
        import io
        import nbs_control.cli as cli
        old = cli.PROJECT_ROOT, cli.EXPORT_DIR
        cli.PROJECT_ROOT, cli.EXPORT_DIR = self.tmp, self.tmp / 'exports'
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                clean = synthetic.build(self.tmp / 'clean', 'clean')
                self.assertEqual(main(['tb-recon', '--inputs', str(clean)]), 0)
                self.assertEqual(main(['tb-recon', '--inputs', str(self.ds)]), 2)
                self.assertEqual(main(['tb-recon', '--inputs', str(self.tmp / 'nowhere')]), 1)
        finally:
            cli.PROJECT_ROOT, cli.EXPORT_DIR = old

    def test_web_pages(self):
        from nbs_control.service import ControlService
        from nbs_control.web import create_app
        root = self.tmp / 'webroot'
        shutil.copytree(ROOT / 'config', root / 'config', ignore=shutil.ignore_patterns('history', 'mapping_versions', 'policy_history'))
        app = create_app(ControlService(root / 'config', root / 'data', root / 'supplied'), export_dir=root / 'exports')
        cl = app.test_client()
        self.assertEqual(cl.get('/tb').status_code, 200)
        with cl.session_transaction() as s:
            token = s['csrf']
        r = cl.post('/tb/synthetic', data={'csrf': token, 'scenario': 'defects'})
        self.assertEqual(r.status_code, 302)
        folder = root / 'data' / 'tbrecon' / 'synthetic_defects'
        r = cl.post('/tb/start', data={'csrf': token, 'inputs': str(folder), 'mode': 'normal', 'label': 'web'})
        job = r.headers['Location']
        for _ in range(200):
            r = cl.get(job)
            if r.status_code == 302:
                break
            time.sleep(0.1)
        self.assertEqual(r.status_code, 302, r.data[:500])
        run_url = r.headers['Location']
        rid = run_url.rstrip('/').split('/')[-1]
        page = cl.get(run_url)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Expected versus actual TB', page.data)
        for url in (f'/tb/run/{rid}/gl/1101000020/QAR', f'/tb/run/{rid}/account/SYNC000000', f'/tb/run/{rid}/exceptions',
                    f'/tb/run/{rid}/exceptions?category=AMBIGUOUS_MAPPING', f'/tb/run/{rid}/worklist', f'/tb/run/{rid}/rules',
                    f'/tb/run/{rid}/file/report.html', f'{run_url}?recon_status=INCOMPLETE', f'/tb/compare?before={rid}&after={rid}'):
            resp = cl.get(url)
            self.assertEqual(resp.status_code, 200, url)
            resp.close()
        self.assertEqual(cl.get(f'/tb/run/{rid}/file/../../x').status_code, 404)


class GLReportAdapterFixes(unittest.TestCase):
    def test_inline_ranges_and_lists(self):
        from nbs_control import gl_mapping as g
        f, err = g._token_filter('1000-1999, 6001, 7001', 'category', {})
        self.assertIsNone(err)
        self.assertEqual(f, {'any': [{'field': 'category', 'op': 'in', 'values': ['6001', '7001']},
                                     {'field': 'category', 'op': 'range', 'values': [1000, 1999]}]})
        self.assertEqual(g._token_filter('6001 7001', 'category', {})[0], {'field': 'category', 'op': 'in', 'values': ['6001', '7001']})
        self.assertIsNotNone(g._token_filter('1999-1000', 'category', {})[1])
        from nbs_control.report_mapping import compile_filter
        params = []
        self.assertIn('BETWEEN', compile_filter(f, params))

    def test_listed_balance_types_are_split(self):
        from nbs_control import gl_mapping as g
        self.assertEqual(g._balance_types('CURACCOUNT, DUEACCOUNT', {}), (['CURACCOUNT', 'DUEACCOUNT'], None))
        self.assertTrue(g._balance_types('CUR-ACCOUNT', {})[1])

    def test_ecb_loader_positions_from_config(self):
        from nbs_control import bank_data as b
        pos = b.ac_positions()
        parts = 'AC.1.TR.QAR.3717.5261.1000.14.QA.47004.2Y......QA0011014'.split('.')
        self.assertEqual({k: b.key_segment(parts, v, 10) for k, v in pos.items()},
                         {'currency': 'QAR', 'category': '3717', 'sector': '1000', 'residence': 'QA', 'industry': '47004', 'company': 'QA0011014'})
        self.assertEqual(b.ac_positions(Path('/nonexistent.json')), b.AC_DEFAULT_POSITIONS)


class Tables(unittest.TestCase):
    def test_header_aliases_xlsx_and_csv(self):
        from nbs_control.tbrecon.tables import read_table, amount
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / 't.csv'
            with p.open('w', newline='') as f:
                csv.writer(f).writerows([['Old GL', 'CCY', 'Amount'], ['LG1', 'QAR', '(1,234.50)'], ['', '', '']])
            rows_, m = read_table(p)
            self.assertEqual(m['headers'], ['LEGACY_GL', 'CURRENCY', 'BALANCE'])
            self.assertEqual(amount(rows_[0]['BALANCE']), D('-1234.50'))
            self.assertIsNone(amount(''))
            import openpyxl
            wb = openpyxl.Workbook()
            wb.active.append(['DKB GL', 'Currency', 'Balance'])
            wb.active.append(['G1', 'QAR', 12.5])
            wb.save(tmp / 't.xlsx')
            rows_, m = read_table(tmp / 't.xlsx')
            self.assertEqual((m['headers'], amount(rows_[0]['BALANCE'])), (['TARGET_GL', 'CURRENCY', 'BALANCE'], D('12.5')))
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
