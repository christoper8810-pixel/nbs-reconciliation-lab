"""Portable source registry, GL mapping adapter, logic-builder parts and the SOURCE_RULE engine method."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from werkzeug.datastructures import MultiDict

from nbs_control import builder_web, gl_mapping, rebuild_engine as eng, sources, target_mappings as tm
from nbs_control.rebuild_store import connect
from tests.rebuild_fixtures import write_xlsx

ROOT = Path(__file__).resolve().parents[1]


class Registry(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / 'config').mkdir()
        self.outside = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(self.outside, ignore_errors=True)

    def test_files_are_copied_into_inputs_and_hashed(self):
        f = self.outside / 'BO_QCB_NBS_Report.xlsx'
        write_xlsx(f, [('S', [['x']])])
        e = sources.register(self.root, 'BO', f, 'tester')
        self.assertEqual(e['file'], 'inputs/BO_QCB_NBS_Report.xlsx')
        self.assertTrue((self.root / 'inputs' / 'BO_QCB_NBS_Report.xlsx').exists())
        shutil.rmtree(self.outside)  # the original location may disappear: the app no longer needs it
        self.assertEqual([p.name for p in sources.resolved(self.root, 'BO')], ['BO_QCB_NBS_Report.xlsx'])
        reg = json.loads((self.root / 'config' / 'source_files.json').read_text())
        self.assertNotIn(':\\', json.dumps(reg))  # no absolute machine paths stored

    def test_discovery_without_registry_and_rejections(self):
        (self.root / 'inputs').mkdir()
        write_xlsx(self.root / 'inputs' / 'All Loan 30.09.2026.xlsx', [('S', [['x']])])
        self.assertEqual([p.name for p in sources.resolved(self.root, 'LOAN')], ['All Loan 30.09.2026.xlsx'])
        with self.assertRaises(ValueError):
            sources.register(self.root, 'NOPE', self.root / 'x.xlsx')
        with self.assertRaises(ValueError):
            sources.register(self.root, 'BO', self.root / 'missing.xlsx')

    def test_no_machine_paths_in_code(self):
        for py in (ROOT / 'nbs_control').glob('*.py'):
            self.assertNotIn('C:\\Users\\Test\\Downloads', py.read_text(encoding='utf-8'), py.name)


def gl_workbook(path):
    report = [['LINE', 'TYPE', 'Description', 'App', 'Market', 'Currency', 'CATEGORY', 'PLCATEGORY', 'PLPRODUCT', 'SECTOR', 'PLSECTOR', 'PLDEPARTMENT', 'BALANCE', 'N', 'RANGE', 'P', 'Q', 'R'],
              ['DKBGL.1010', 'D', 'Cash', 'AC', '1', None, '*CASH', None, None, None, None, None, 'DEBIT', None, 'CASH', 'CATEGORY', ('n', '10000'), ('n', '10025')],
              ['DKBGL.1210', 'D', 'Financing - Retail', 'AC', '1', None, '*FIN', None, None, '*RETAIL', None, None, '*PRIN', None, 'RETAIL', 'SECTOR', ('n', '1000'), ('n', '1999')],
              [None, None, None, 'AC', None, None, '6513', None, None, '*RETAIL', None, None, 'DEBIT', None, 'FIN', 'CATEGORY', ('n', '3000'), ('n', '3999')],
              [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'PRIN', 'ASSET.TYPE', 'CURACCOUNT\nDUEACCOUNT', None],
              ['DKBGL.4320', 'D', 'Fees', 'PL', None, None, None, ('n', '52000'), None, None, None, None, None]]
    category = [['Range', 'Start', 'End', 'Module', 'Approved', 'Description', 'GL', 'Transact GL'],
                ['Demand', ('n', '1000'), ('n', '1999'), 'AC', ('n', '1000'), '***Demand Accounts'],
                [None, None, None, 'AC', ('n', '1001'), 'Current Account - Retail']]
    segment = [['First', 'GL', 'Second', 'Third'], ['1 - Retail', 'RETAIL', '1000 - Lower Mass', '1 - Staff']]
    mapping = [['Old GL_Number', 'Iso_Code', 'Description'], ['01-01-001-12-01-1000000010', 'QAR', 'Cash In Vault 1']]
    write_xlsx(path, [('GL Report', report), ('CATEGORY', category), ('SEGMENT', segment), ('GL Mapping', mapping)])


class GLMapping(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.c = connect(self.dir / 's.sqlite')

    def tearDown(self):
        self.c.close()
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_lines_named_ranges_and_parts(self):
        p = self.dir / 'gl.xlsx'
        gl_workbook(p)
        r = gl_mapping.import_gl_mapping(self.c, p)
        self.assertEqual((r['gl_lines'], r['categories'], r['sectors'], r['gl_accounts']), (3, 2, 1, 1))
        d = r['source_sha256']
        parts, notes = gl_mapping.line_parts(self.c, d, 'DKBGL.1010')
        self.assertEqual(parts[0]['filter'], {'field': 'category', 'op': 'range', 'values': [10000, 10025]})
        self.assertEqual(parts[0]['components'], ['DEBIT'])
        parts, notes = gl_mapping.line_parts(self.c, d, 'DKBGL.1210')
        self.assertEqual(parts[0]['components'], ['CURACCOUNT', 'DUEACCOUNT'])  # named balance group
        self.assertEqual(parts[0]['filter']['all'][1], {'field': 'sector', 'op': 'range', 'values': [1000, 1999]})
        self.assertEqual(parts[1]['filter']['all'][0], {'field': 'category', 'op': 'in', 'values': ['6513']})
        parts, notes = gl_mapping.line_parts(self.c, d, 'DKBGL.4320')
        self.assertEqual(parts, [])
        self.assertIn('P&L', notes[0])  # P&L criteria are reported, not computed from balances
        self.assertTrue(gl_mapping.import_gl_mapping(self.c, p)['already_imported'])


class BuilderParts(unittest.TestCase):
    def test_structured_fields_build_typed_filters(self):
        f = MultiDict([('part_source', 'ECB'), ('part_categories', '1001'), ('part_category_ranges', '3000-3999, 13410'),
                       ('part_sector_ranges', '1000-1999'), ('part_country', 'QA'), ('part_measure', 'components'),
                       ('part_balance_types', 'DEBIT'), ('part_sign', '-1')])
        p = builder_web.build_part(f)
        self.assertEqual(p['factor'], -1)
        self.assertEqual(p['components'], ['DEBIT'])
        cats = p['filter']['all'][0]['any']
        self.assertIn({'field': 'category', 'op': 'range', 'values': [3000, 3999]}, cats)
        self.assertIn({'field': 'country', 'op': 'eq', 'values': ['QA']}, p['filter']['all'])
        tm.validate_target({'target_id': 'x', 'table': '001', 'item_code': 'x', 'status': 'PROVISIONAL', 'method': 'SOURCE_RULE', 'parts': [p]},
                           {'tables': {'001': {'measures': {}}}})

    def test_whole_source_and_bad_input_rejected(self):
        with self.assertRaisesRegex(ValueError, 'never implicit'):
            builder_web.build_part(MultiDict([('part_source', 'ECB'), ('part_balance_types', 'DEBIT')]))
        with self.assertRaisesRegex(ValueError, 'reversed'):
            builder_web.build_part(MultiDict([('part_source', 'ECB'), ('part_category_ranges', '3999-3000')]))
        with self.assertRaises(ValueError):
            tm.validate_target({'target_id': 'x', 'table': '001', 'item_code': 'x', 'status': 'PROVISIONAL', 'method': 'SOURCE_RULE',
                                'parts': [{'kind': 'STOCK', 'source': 'ECB', 'measure': 'components', 'components': ['DEBIT'],
                                           'filter': {'field': 'category; DROP', 'op': 'in', 'values': ['1']}, 'factor': 1}]},
                               {'tables': {'001': {'measures': {}}}})


class SourceRuleEngine(unittest.TestCase):
    def test_parts_are_summed_and_double_counting_flagged(self):
        base = dict(account='a', currency='QAR', residency='Resident', country='QA', maturity='', product='', risk='', personal='',
                    industry='', unavailable=0, issue=None, rim=None, source='ECB')

        class Facts:
            def rows(self, spec):
                cat = spec['filter']['values'][0]
                return [dict(base, fid=int(cat), amount=float(cat) * (1 if spec['components'] == ['DEBIT'] else 10) * spec['factor'])], [], []
        part = lambda cat, comps, sign=1: {'kind': 'STOCK', 'source': 'ECB', 'measure': 'components', 'components': comps,
                                           'filter': {'field': 'category', 'op': 'in', 'values': [cat]}, 'factor': sign, 'label': cat}
        cat = {'tables': {'001': {'measures': {'In LC Amount': {'semantic': 'IN_LC', 'kind': 'money', 'primary': True}}}}}
        t = {'target_id': '001|x', 'table': '001', 'item_code': 'x', 'status': 'PROVISIONAL', 'method': 'SOURCE_RULE',
             'parts': [part('1', ['DEBIT']), part('2', ['DEBIT']), part('2', ['CREDIT'])]}
        settings = {'maturity_convention': 'DAY_COUNT', 'open_ended_products': [], 'hierarchy_predicates': None}
        res, contrib = eng.generate_targets({'targets': {'001|x': t}}, cat, Facts(), {'rules': {}}, None, None, {}, '2026-09-30', settings)
        self.assertEqual(res['001|x']['cells']['In LC Amount']['value'], (1 + 2 + 20) * 10 ** 6)
        self.assertEqual(res['001|x']['cells']['In LC Amount']['status'], 'PROVISIONAL')
        self.assertFalse(any('WARNING' in i for i in res['001|x']['issues']))  # same account, different balance types: additive
        t['parts'].append(part('1', ['DEBIT'], 1))
        res, _ = eng.generate_targets({'targets': {'001|x': dict(t, parts=[part('1', ['DEBIT']), dict(part('1', ['DEBIT']), label='again')])}},
                                      cat, Facts(), {'rules': {}}, None, None, {}, '2026-09-30', settings)
        self.assertTrue(any('counted twice' in i for i in res['001|x']['issues']))


if __name__ == '__main__':
    unittest.main()


class PlainLogic(unittest.TestCase):
    def ctx(self):
        from nbs_control import logic_text as lt

        class C:
            pass
        c = C()
        c.rules = {'R1': {'id': 'R1', 'row': 358, 'source': 'ECB', 'measure': 'components', 'components': ['DEBIT'], 'factor': -1, 'enabled': True,
                          'path': '01 Cash on hand', 'filter': {'field': 'category', 'op': 'range', 'values': [10000, 10025]}},
                   'R2': {'id': 'R2', 'row': 900, 'source': None, 'enabled': False, 'path': 'x', 'notes': ['n']}}
        c.settings = {'hierarchy_predicates': None, 'component_corrections': None}
        c.balance = {'groups': {'OUTSTANDING': ['CURACCOUNT', 'NABACCOUNT'], 'AMORTIZED_EARNED': ['ACCPRINCIPALPFT'], 'UNEARNED_PROFIT': ['ACCDEFERREDPFT']}}
        c.policies = {}
        c.available = {'CURACCOUNT', 'DEBIT', 'ACCPRINCIPALPFT'}
        return lt, c

    def test_lines_described_with_explicit_balance_types(self):
        lt, c = self.ctx()
        d = lt.describe({'method': 'LEGACY_RULE', 'legacy_rule_id': 'R1', 'layout': None}, c)
        self.assertEqual((d['source'], d['accounts']), ('ECB balances', 'T24 category is between 10000, 10025'))
        self.assertEqual(lt.types_text(d['types']), 'all selected accounts: -DEBIT')
        loan = lt.balance_types({'source': 'ECB_LOAN', 'measure': 'carrying', 'factor': 1}, c)
        self.assertIn('-NABACCOUNT*', lt.types_text(loan))  # owner type missing from the extract is marked, not hidden
        self.assertIn('Ethix loan fees', lt.types_text(loan))
        self.assertIn('Not calculated yet', lt.describe({'method': 'LEGACY_RULE', 'legacy_rule_id': 'R2'}, c)['how'])
        self.assertIn('Sum of its sub-items', lt.describe({'method': 'SUBTOTAL_OF_CHILDREN'}, c)['how'])
