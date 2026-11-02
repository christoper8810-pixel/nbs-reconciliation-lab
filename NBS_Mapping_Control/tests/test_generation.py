import json,sqlite3,tempfile,unittest
from pathlib import Path
from nbs_control.bank_data import FIELDS,NUMERIC,date_value
from nbs_control.generation import prepare_facts,query,save_rule,initialize_rules
from nbs_control.report_mapping import compile_filter,term,validate_spec,numeric_selector

class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.c=sqlite3.connect(':memory:')
        self.c.execute('CREATE TABLE unique_records ('+','.join(k+(' REAL' if k in NUMERIC else ' TEXT') for k in FIELDS)+')')
        self.c.execute('CREATE UNIQUE INDEX unique_account_idx ON unique_records(source,account,currency)')
        self.rules={'groups':{'OUTSTANDING':['CURACCOUNT','NABACCOUNT'],'AMORTIZED_EARNED':['ACCPRINCIPALPFT'], 'UNEARNED_PROFIT':['ACCDEFERREDPFT']}}
        self.manifest={'ECB':{'component_columns':['CURACCOUNT','CREDIT','ACCPRINCIPALPFT','ACCDEPOSITPFT','ACCDEFERREDPFT']}}
        self.add(source='ECB',account='P',currency='QAR',category='3713',country='QA',industry='47004',components=json.dumps({'CURACCOUNT':-150000}))
        self.add(source='LOAN',account='P',currency='QAR',product='CLM',personal='Personal',residency='Resident',linked_account='CH',fees=0,maturity='2026-10-07',amount=18893.51)
        self.add(source='ECB',account='CH',currency='QAR',category='6050',country='QA',components=json.dumps({'CREDIT':131106.49}))
    def add(self,**kw):
        self.c.execute('INSERT INTO unique_records ('+','.join(kw)+') VALUES ('+','.join('?' for x in kw)+')',list(kw.values()))
    def tearDown(self):self.c.close()
    def test_excel_serial_dates_are_calendar_dates(self):
        self.assertEqual(date_value(46295),'2026-09-30')
        self.assertEqual(date_value(None),'')
    def test_wrong_workbook_cannot_generate_zero_reports(self):
        from unittest.mock import patch
        from nbs_control.bank_data import import_file
        with patch('nbs_control.bank_data.xlsx_rows',return_value=iter([(1,{'A':'Wrong header'})])):
            with self.assertRaisesRegex(ValueError,'missing required headers'):import_file(self.c,'wrong.xlsx','ECB')
    def test_verified_clm_is_signed_offset_once(self):
        checks=prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        amount=self.c.execute("SELECT outstanding FROM facts WHERE source='ECB_LOAN'").fetchone()[0]
        self.assertAlmostEqual(amount,18893.51,places=2)
        self.assertEqual(checks['clm_linked'],1)
        self.assertEqual(checks['missing_balance_columns']['OUTSTANDING'],['NABACCOUNT'])
    def test_separate_clm_report_policy_uses_exact_accrprofit_without_aliasing(self):
        from nbs_control.generation import validate_product_policies
        self.c.execute("UPDATE unique_records SET components=? WHERE account='P' AND source='ECB'",(json.dumps({'CURACCOUNT':-150000,'ACCPRINCIPALPFT':-1000}),))
        self.c.execute("UPDATE unique_records SET components=? WHERE account='CH'",(json.dumps({'CREDIT':131106.49,'ACCCRPROFIT':980}),))
        policy={'products':{'CLM':{'enabled':True,'parent_coefficients':{'CURACCOUNT':-1,'ACCPRINCIPALPFT':-1},'linked_coefficients':{'CREDIT':-1,'ACCCRPROFIT':-1},'add_ethix_fees':True}}}
        validate_product_policies(policy)
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30',policy)
        owner,report=self.c.execute("SELECT carrying,ethix_carrying FROM facts WHERE source='ECB_LOAN'").fetchone()
        self.assertAlmostEqual(owner,19893.51,places=2);self.assertAlmostEqual(report,18913.51,places=2)
    def test_rcm_policy_keeps_principal_and_net_earned_distinct_from_owner_sum(self):
        self.c.execute("UPDATE unique_records SET product='RCM' WHERE source='LOAN'")
        self.c.execute("UPDATE unique_records SET components=? WHERE account='P' AND source='ECB'",(json.dumps({'CURACCOUNT':-1000,'RECDEFERREDPFT':-200,'ACCDEFERREDPFT':180}),))
        policy={'products':{'RCM':{'enabled':True,'parent_coefficients':{'CURACCOUNT':-1,'RECDEFERREDPFT':-1,'ACCDEFERREDPFT':-1},'linked_coefficients':{},'add_ethix_fees':True}}}
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30',policy)
        owner,report=self.c.execute("SELECT carrying,ethix_carrying FROM facts WHERE source='ECB_LOAN'").fetchone()
        self.assertEqual(owner,1000);self.assertEqual(report,1020)
    def test_nonfinite_policy_values_are_rejected(self):
        from nbs_control.generation import validate_product_policies
        with self.assertRaises(ValueError):validate_product_policies({'products':{'RCM':{'enabled':True,'parent_coefficients':{'CURACCOUNT':float('nan')},'linked_coefficients':{},'add_ethix_fees':True}}})
    def test_missing_clm_child_does_not_become_full_parent_exposure(self):
        self.c.execute("DELETE FROM unique_records WHERE account='CH'")
        checks=prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        self.assertEqual(checks['unresolved_clm_links'],1)
        self.assertEqual(self.c.execute("SELECT unavailable FROM facts WHERE source='ECB_LOAN'").fetchone()[0],1)
    def test_currency_conflict_is_not_joined(self):
        self.c.execute("UPDATE unique_records SET currency='USD' WHERE source='LOAN'")
        checks=prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        self.assertEqual(checks['joined_loans'],0)
        self.assertEqual(checks['loan_currency_conflicts'],1)
    def test_sparse_missing_key_uses_exact_account_currency(self):
        self.c.execute("UPDATE unique_records SET currency=NULL,category=NULL WHERE account='P' AND source='ECB'")
        checks=prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        self.assertEqual(checks['joined_loans'],1)
        self.assertEqual(checks['unresolved_clm_links'],1)
    def test_maturity_date_direction_and_boundary(self):
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        self.assertEqual(self.c.execute("SELECT days FROM facts WHERE source='ECB_LOAN'").fetchone()[0],7)
    def test_unknown_fields_and_sql_are_refused(self):
        with self.assertRaises(ValueError):compile_filter(term("category); DROP TABLE facts;--",'eq',['1']),[])
        params=[];sql=compile_filter(term('category','eq',["1' OR 1=1 --"]),params)
        self.assertNotIn('OR 1=1',sql);self.assertEqual(params,["1' OR 1=1 --"])
    def test_numeric_selector_retains_range_and_exclusion(self):
        s=numeric_selector('CATEGORY=3000-3999 BUT NOT EQUAL TO CATEGORY 3713, 3702','category','CATEGORY')
        self.assertIn('all',s)
        params=[];compile_filter(s,params);self.assertEqual(params,[3000,3999,'3713','3702'])
    def test_unavailable_source_is_not_zero(self):
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        spec={'source':None,'measure':None,'filter':None,'components':[],'factor':1,'enabled':True}
        r=query(self.c,spec);self.assertEqual(r['values'],{});self.assertEqual(r['status'],'UNAVAILABLE')
    def test_disabling_mapping_also_disables_size_and_maturity_layouts(self):
        from nbs_control.generation import calc_row
        for layout in ('size','maturity_loan','maturity_deposit','risk','geo'):
            spec={'source':'ECB_LOAN','measure':'ethix_carrying','filter':None,'components':[],
                  'factor':1,'enabled':False,'layout':layout}
            result=calc_row(self.c,spec,self.manifest,1000,{})
            self.assertEqual(result['values'],{});self.assertEqual(result['status'],'UNAVAILABLE')
    def test_net_asset_contra_is_deducted_instead_of_omitted(self):
        self.add(source='TB',account='gross',currency='QAR',gl='1801000001',amount=1000)
        self.add(source='TB',account='contra',currency='QAR',gl='2801000001',amount=200)
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        spec={'source':'TB','measure':'amount','filter':term('gl','in',['1801000001','2801000001']),
              'negative_filter':term('gl','eq',['2801000001']),'components':[],'factor':1,'enabled':True}
        r=query(self.c,spec,dimension='total')
        self.assertAlmostEqual(r['values']['amount'],.8)
    def test_absent_balance_column_is_partial(self):
        prepare_facts(self.c,self.rules,self.manifest,'2026-09-30')
        spec={'source':'ECB','measure':'components','filter':term('account','eq',['P']), 'components':['CURACCOUNT','NABACCOUNT'],'factor':-1,'enabled':True}
        r=query(self.c,spec,component_columns=self.manifest['ECB']['component_columns'])
        self.assertEqual(r['status'],'PARTIAL');self.assertEqual(r['values']['J'],150)
        self.assertEqual(r['missing_components'],['NABACCOUNT'])
    def test_mapping_edits_are_versioned_and_identity_is_fixed(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            p=Path(directory)/'generation_rules.json'
            spec={'id':'A','row':5,'description':'Cash','path':'Cash','section':'Assets','table':None,'base':'Assets','fingerprint':'x',
                  'source':'ECB','measure':'components','filter':None,'components':['DEBIT'],'factor':-1,'enabled':True}
            p.write_text(json.dumps({'rules':{'A':spec}}))
            change={**spec,'factor':1}
            save_rule(p,'A',change,'Reviewer','Changed display sign')
            self.assertEqual(json.loads(p.read_text())['rules']['A']['factor'],1)
            self.assertEqual(len(list((p.parent/'generation_history').glob('*.json'))),1)
            with self.assertRaises(ValueError):save_rule(p,'A',{**change,'row':6},'Reviewer','Readdress')

if __name__=='__main__':unittest.main()
