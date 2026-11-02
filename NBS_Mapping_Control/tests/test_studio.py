"""Mapping Studio regression tests (SYNTHETIC data only)."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook as XW, load_workbook

from nbs_control.studio import bo as B, conditions as C, exports, run as R, synthetic, validate
from nbs_control.studio.compiler import compile_workbook
from nbs_control.studio.engine import Allocation, expected
from nbs_control.studio.store import Store
from nbs_control.studio.workbook import Workbook

ROOT = Path(__file__).resolve().parent.parent
D = Decimal


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class Conditions(unittest.TestCase):
    def test_lists_ranges_comparisons_wildcards_exclusions(self):
        c = C.parse('1000-1999, 6001, 7001')
        self.assertEqual([c.matches(v) for v in ('1000', '1999', '2000', '6001', '7001', '6002')], [True, True, False, True, True, False])
        self.assertTrue(C.parse('6001 7001').matches('7001'))                 # whitespace-separated codes
        self.assertTrue(C.parse('3701\n3702').matches('3702'))                # newline alternatives
        self.assertTrue(C.parse('1000 - 1999').matches('1500'))               # spaced range kept together
        self.assertTrue(C.parse('>=5000').matches('5000') and not C.parse('<5000').matches('5000'))
        self.assertTrue(C.parse('37*').matches('3713') and C.parse('3?13').matches('3713'))
        ex = C.parse('NOT USD')
        self.assertTrue(ex.matches('QAR') and not ex.matches('USD'))
        both = C.parse('3700-3799, !3713')
        self.assertTrue(both.matches('3701') and not both.matches('3713') and not both.matches('3800'))

    def test_blank_any_and_must_be_blank(self):
        self.assertFalse(C.parse('').restricted)
        self.assertTrue(C.parse('ALL').explicit_any)
        b = C.parse('<BLANK>')
        self.assertTrue(b.matches('') and not b.matches('X'))
        self.assertIsNone(C.parse('3701').matches(None))                     # dimension absent: undecided, never a match

    def test_named_and_errors(self):
        self.assertTrue(C.parse('*CASH', {'CASH': '10000-10099'}).matches('10050'))
        for bad in ('6099-6001', '*UNDEFINED', '12-'):
            with self.assertRaises(C.ConditionError):
                C.parse(bad)

    def test_intersects(self):
        self.assertTrue(C.intersects(C.parse('1000-1999'), C.parse('1999-2999')))
        self.assertFalse(C.intersects(C.parse('1000-1998'), C.parse('1999-2999')))


class Scenario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='studio-'))
        cls.clean = synthetic.build(cls.tmp / 'clean', 'clean')
        cls.defects = synthetic.build(cls.tmp / 'defects', 'defects')
        cls.res_clean = R.analyse(cls.clean / 'mapping_workbook.xlsx', cls.clean / 'bo_report.csv', [cls.clean / 'source_records.csv'])
        cls.res = R.analyse(cls.defects / 'mapping_workbook.xlsx', cls.defects / 'bo_report.csv', [cls.defects / 'source_records.csv'])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_workbook_roles_columns_and_cross_sheet_reference(self):
        wb = Workbook(self.defects / 'mapping_workbook.xlsx')
        self.assertEqual(set(wb.roles), {'GL_REPORT', 'GL_MAPPING', 'CATEGORY', 'COA', 'SEGMENT', 'BRANCH'})
        hr, cols, ev = wb.column_map('GL_REPORT')
        self.assertEqual((hr, cols['category'], cols['product']), (1, 7, 19))
        self.assertTrue(any('used as range_name by position' in e for e in ev))     # fallback is disclosed
        m = compile_workbook(wb)
        ijara = next(r for r in m.rules if r.line == 'DKBGL1050')
        self.assertEqual((ijara.raw['category'], ijara.formulas['category']), ('3800', '=CATEGORY!B6'))
        self.assertIn('IJARA_STAFF', m.named)
        self.assertEqual(m.named['IJARA_STAFF']['source'], 'workbook defined name')

    def test_continuation_and_inheritance(self):
        m = compile_workbook(Workbook(self.clean / 'mapping_workbook.xlsx'))
        r2 = next(r for r in m.rules if r.id == 'DKBGL1020#2')
        self.assertEqual((r2.raw['sector'], r2.cells['sector']), ('1000-1999', "'GL Report'!J4"))   # '^' inherits J4
        self.assertTrue(r2.match({'category': '3901', 'sector': '1500', 'balance_type': 'DUEACCOUNT'}))
        self.assertEqual(m.lines['T1090']['total_basis'], 'INFERRED_SECTION')

    def test_uncached_formula_is_resolved_or_flagged(self):
        p = self.tmp / 'f.xlsx'
        w = XW()
        ws = w.active
        ws.title = 'GL Report'
        ws.append(['LINE', 'TYPE', 'DESCRIPTION', '', '', 'CURRENCY', 'CATEGORY'])
        ws.append(['L1', 'D', 'a', '', '', '', '=CATEGORY!A2'])
        ws.append(['L2', 'D', 'b', '', '', '', '=SUM(CATEGORY!A2:A3)'])
        cs = w.create_sheet('CATEGORY')
        cs.append(['CATEGORY'])
        cs.append([3701])
        w.save(p)
        m = compile_workbook(Workbook(p))
        self.assertEqual(m.rules[0].raw['category'], '3701')
        self.assertFalse(m.rules[1].usable)                                   # never read as blank / unrestricted
        self.assertIn('UNRESOLVED_FORMULA', {i['type'] for i in m.issues})

    def test_clean_expected_equals_independent_truth(self):
        truth = json.loads((self.clean / 'truth.json').read_text())['expected']
        exp = {f"{r['key'][0]}|{r['key'][1]}": r['expected'] for r in self.res_clean['recon_before'] if r['line_type'] == 'D'}
        self.assertEqual({k: D(v) for k, v in truth.items()}, {k: v for k, v in exp.items() if v})
        self.assertEqual(self.res_clean['summary']['bo_open_before'], 0)
        self.assertEqual(self.res_clean['proposals'], [])

    def test_every_injected_defect_gets_the_right_cell_and_confidence(self):
        got = {(e['cell'], e['existing'], e['proposed'], p['confidence']) for p in self.res['proposals'] for e in p['edits']}
        expected_edits = {
            ("'GL Report'!G4", '3700-3748', '3700-3749', 'HIGH'),                 # W1 range off by one
            ("'GL Report'!G7", '3700-3749', '3700-3749, 3901', 'HIGH'),           # W2 missing list value
            ("'GL Mapping'!W2", 'DKBGL1070', 'DKBGL1060', 'HIGH'),                # W3 wrong report line
            ("'GL Report'!G18", '6099-6001', '6001-6099', 'HIGH'),                # W4 reversed range
            ("'GL Report'!J6", '1999-2999', '2000-2999', 'HIGH'),                 # W7 overlap
            ("'GL Mapping'!W3", 'DKBGL 1065', 'DKBGL1065', 'HIGH'),               # W9 line reference
            ("'GL Report'!J13", '4101', '', 'HIGH'), ("'GL Report'!S13", '', '4101', 'HIGH'),   # W12 PRODUCT in SECTOR
        }
        self.assertEqual(got, expected_edits)
        resid = {r['key']: (r['category'], r['responsibility']) for r in self.res['residuals']}
        self.assertEqual(resid, {'DKBGL2010 / QAR': ('DUPLICATE_BO_ROWS', 'BO_REPORT'), 'DKBGL5010 / QAR': ('SIGN_PRESENTATION', 'BO_REPORT'),
                                 'DKBGL9999 / QAR': ('LINE_NOT_IN_MAPPING', 'MAPPING_OR_BO'),
                                 'DKBGL2040 / QAR': ('NO_SOURCE_RECORDS_FOR_LINE', 'SOURCE_DATA')})
        checks = {v['check'] for v in self.res['validation']}
        self.assertTrue({'UNKNOWN_CATEGORY', 'MALFORMED_RANGE', 'OVERLAPPING_CONDITIONS', 'GLMAP_UNKNOWN_LINE',
                         'POSSIBLE_MAPPING_COLUMN_MISALIGNMENT'} <= checks)
        self.assertTrue(any(t['category'] == 'BO_TOTAL_NOT_SUM_OF_DETAILS' for t in self.res['bo_internal_totals']))

    def test_proposals_carry_evidence_and_impact(self):
        p = next(p for p in self.res['proposals'] if p['edits'][0]['cell'] == "'GL Report'!G4")
        self.assertEqual(p['affected_records'], 14)
        self.assertEqual(p['lines'], {'DKBGL1020 / QAR': {'before': '2311029.93', 'after': '0.00'}})
        self.assertEqual(p['alternatives'], ["'GL Report'!G5"])
        self.assertFalse(p['finance_required'])

    def test_overlap_policy_and_undecided(self):
        wb = Workbook(self.defects / 'mapping_workbook.xlsx')
        from nbs_control.studio import sources
        sigs, _ = sources.load([self.defects / 'source_records.csv'])
        al = Allocation(compile_workbook(wb), sigs, {'overlap_policy': 'ALL'})
        self.assertTrue(any(al.status(s) == 'OVERLAP' for s in sigs))
        al2 = Allocation(compile_workbook(Workbook(self.defects / 'mapping_workbook.xlsx')), sigs, {'overlap_policy': 'MOST_SPECIFIC'})
        self.assertFalse(any(len(al2.lines_of[s.id]) > 1 for s in sigs))

    def test_bo_without_source_records_states_missing_evidence(self):
        res = R.analyse(self.defects / 'mapping_workbook.xlsx', self.defects / 'bo_report.csv', [])
        self.assertTrue(all(r['confidence'] in ('UNRESOLVED', 'MEDIUM') for r in res['residuals']))
        self.assertTrue(any('source records are needed' in r['evidence_needed'] for r in res['residuals']))
        self.assertFalse([p for p in res['proposals'] if p['origin'] == 'BO_RECONCILIATION'])

    def test_scale_detection(self):
        E = {('L1', 'QAR'): D('1000000'), ('L2', 'QAR'): D('5000'), ('L3', 'QAR'): D('70000')}
        A = {k: v / 1000 for k, v in E.items()}
        self.assertIn('scale', B.detect_scale_sign(E, A, D('0.01')))


class Workflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='studio-wf-'))
        cls.ds = synthetic.build(cls.tmp / 'in', 'defects')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_approve_export_preserve_and_rerun(self):
        st = Store(self.tmp / 'data')
        original_hash = sha(self.ds / 'mapping_workbook.xlsx')
        pid = R.new_project(st, self.tmp / 'data', 'wf', self.ds / 'mapping_workbook.xlsx', self.ds / 'bo_report.csv', [self.ds / 'source_records.csv'])
        rid, folder, res = R.run_project(st, self.tmp / 'data', self.tmp / 'exports', pid)
        for f in ('BO_RECONCILIATION.xlsx', 'PROPOSED_MAPPING_PATCH.xlsx', 'FINANCE_DECISION_WORKLIST.xlsx', 'MAPPING_VALIDATION_REPORT.xlsx',
                  'PATCH_AUDIT_LOG.xlsx', 'EXECUTIVE_SUMMARY.html'):
            self.assertTrue((folder / f).exists(), f)
        with self.assertRaises(ValueError):
            st.decide(rid, ['P0001'], 'APPROVED', '', 'no name')
        high = [p['id'] for p in st.proposals(rid) if p['confidence'] == 'HIGH']
        self.assertEqual(st.decide(rid, high, 'APPROVED', 'Tester', 'deterministic'), len(high))
        corr = exports.write_corrected(st, rid, folder, res, 'Tester')
        self.assertEqual((len(corr['applied']), corr['conflicts'], corr['verification']['preserved']), (8, [], True))
        self.assertEqual(sha(self.ds / 'mapping_workbook.xlsx'), original_hash)            # original untouched
        wb = load_workbook(folder / 'CORRECTED_MAPPING_PREVIEW.xlsx')
        self.assertEqual(wb['GL Report']['G4'].value, '3700-3749')
        self.assertEqual(wb['GL Report']['G7'].value, '3700-3749, 3901')
        self.assertEqual(wb['GL Report']['G8'].value, '=CATEGORY!B6')                       # formula preserved
        self.assertEqual(wb['GL Report']['N8'].comment.text, 'Category taken from the CATEGORY sheet (cross-sheet reference)')
        self.assertIn('A1:D1', [str(r) for r in wb['README'].merged_cells.ranges])
        self.assertEqual(wb['README']['A2'].value, "=COUNTA('GL Report'!A:A)")
        self.assertTrue((folder / 'CORRECTED_MAPPING_PREVIEW.xlsx').exists())
        log = load_workbook(folder / 'PATCH_AUDIT_LOG.xlsx')['Audit_Log']
        self.assertGreaterEqual(log.max_row, 10)
        wl = load_workbook(folder / 'FINANCE_DECISION_WORKLIST.xlsx')['Finance_Decisions']
        types = {wl.cell(row=i, column=2).value for i in range(2, wl.max_row + 1)}
        self.assertNotIn('PROPOSED CORRECTION', types)                                     # all HIGH were approved
        rid2, folder2, res2 = R.rerun(st, self.tmp / 'data', self.tmp / 'exports', rid)
        self.assertEqual(res2['summary']['bo_matched_before'], 16)
        self.assertLess(res2['summary']['bo_abs_difference_before'], res['summary']['bo_abs_difference_before'])
        self.assertEqual(res2['proposals'], [])
        self.assertEqual(res2['parent'], rid)

    def test_conflicting_cell_is_refused(self):
        from nbs_control.studio import patchbook
        out = patchbook.write_corrected(self.ds / 'mapping_workbook.xlsx', [{'sheet': 'GL Report', 'row': 4, 'col': 7, 'cell': "'GL Report'!G4",
                                                                            'existing': 'NOT THE CURRENT VALUE', 'proposed': 'X'}],
                                        self.tmp / 'c.xlsx')
        self.assertEqual((len(out['applied']), len(out['conflicts']), out['verification']['preserved']), (0, 1, True))

    def test_unresolved_cannot_be_approved(self):
        st = Store(self.tmp / 'data2')
        st.add_run('r1', 'p', 'ANALYSIS', None, 'x', self.tmp, {}, [{'id': 'P0001', 'confidence': 'UNRESOLVED', 'edits': []}])
        with self.assertRaises(ValueError):
            st.decide('r1', ['P0001'], 'APPROVED', 'Tester', 'try')

    def test_cli(self):
        import contextlib
        import io
        import nbs_control.cli as cli
        old = cli.PROJECT_ROOT, cli.EXPORT_DIR
        cli.PROJECT_ROOT, cli.EXPORT_DIR = self.tmp / 'cliroot', self.tmp / 'cliroot' / 'exports'
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                rc = cli.main(['studio-analyse', '--workbook', str(self.ds / 'mapping_workbook.xlsx'), '--bo', str(self.ds / 'bo_report.csv'),
                               '--sources', str(self.ds / 'source_records.csv')])
            self.assertEqual(rc, 2)
            rid = json.loads(out.getvalue())['run_id']
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cli.main(['studio-decide', rid, '--all-high', '--actor', 'T', '--reason', 'r']), 0)
                self.assertEqual(cli.main(['studio-export', rid, '--actor', 'T']), 0)
                self.assertEqual(cli.main(['studio-rerun', rid]), 2)
                self.assertEqual(cli.main(['studio-analyse', '--workbook', str(self.tmp / 'missing.xlsx')]), 1)
        finally:
            cli.PROJECT_ROOT, cli.EXPORT_DIR = old

    def test_web_workflow(self):
        from nbs_control.service import ControlService
        from nbs_control.web import create_app
        root = self.tmp / 'web'
        shutil.copytree(ROOT / 'config', root / 'config', ignore=shutil.ignore_patterns('history', 'mapping_versions', 'policy_history'))
        app = create_app(ControlService(root / 'config', root / 'data', root / 'supplied'), export_dir=root / 'exports')
        cl = app.test_client()
        self.assertEqual(cl.get('/studio').status_code, 200)
        with cl.session_transaction() as s:
            token = s['csrf']
        with open(self.ds / 'mapping_workbook.xlsx', 'rb') as w, open(self.ds / 'bo_report.csv', 'rb') as b, open(self.ds / 'source_records.csv', 'rb') as s:
            r = cl.post('/studio/start', data={'csrf': token, 'label': 'web', 'workbook': (w, 'mapping_workbook.xlsx'), 'bo': (b, 'bo_report.csv'),
                                               'sources': [(s, 'source_records.csv')], 'tolerance': '0.01', 'bo_amount_scale': '1', 'bo_sign': '1',
                                               'overlap_policy': 'ALL'}, content_type='multipart/form-data')
        job = r.headers['Location']
        for _ in range(300):
            r = cl.get(job)
            if r.status_code == 302:
                break
            time.sleep(0.1)
        self.assertEqual(r.status_code, 302, r.data[:400])
        run_url = r.headers['Location']
        rid = run_url.rstrip('/').split('/')[-1]
        self.assertIn(b'Discrepancy dashboard', cl.get(run_url).data)
        for url in (f'{run_url}?status=OPEN', f'/studio/run/{rid}/key?k=DKBGL1020+/+QAR', f'/studio/run/{rid}/proposals?confidence=HIGH',
                    f'/studio/run/{rid}/validation?severity=ERROR', f'/studio/run/{rid}/rules', f'/studio/run/{rid}/file/EXECUTIVE_SUMMARY.html'):
            resp = cl.get(url)
            self.assertEqual(resp.status_code, 200, url)
            resp.close()
        r = cl.post(f'/studio/run/{rid}/decide', data={'csrf': token, 'all_high': '1', 'decision': 'APPROVED', 'actor': 'Web', 'reason': 'ok'})
        self.assertEqual(r.status_code, 302)
        r = cl.post(f'/studio/run/{rid}/export', data={'csrf': token, 'actor': 'Web'})
        self.assertEqual(r.status_code, 302)
        resp = cl.get(f'/studio/run/{rid}/file/CORRECTED_MAPPING_PREVIEW.xlsx')
        self.assertEqual(resp.status_code, 200)
        resp.close()
        self.assertEqual(cl.get(f'/studio/run/{rid}/file/..%2F..%2Fx').status_code, 404)


class Scale(unittest.TestCase):
    def test_large_population_runs_quickly(self):
        tmp = Path(tempfile.mkdtemp(prefix='studio-scale-'))
        try:
            ds = synthetic.build(tmp / 'in', 'defects')
            rows = list(csv.DictReader((ds / 'source_records.csv').open()))
            with (tmp / 'big.csv').open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                for i in range(40000):
                    r = dict(rows[i % len(rows)])
                    r['ACCOUNT_NO'] = f'X{i:06d}'
                    if r.get('CATEGORY') and r['CATEGORY'].startswith('37'):
                        r['SECTOR'] = str(1000 + i % 900)       # many distinct signatures
                    w.writerow(r)
            t = time.time()
            res = R.analyse(ds / 'mapping_workbook.xlsx', ds / 'bo_report.csv', [tmp / 'big.csv'])
            self.assertLess(time.time() - t, 120)
            self.assertEqual(res['summary']['source_records'], 40000)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
