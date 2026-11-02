import json
import unittest
from pathlib import Path
from nbs_control import temenos_review as review, rebuild_engine as eng


class OriginalTemenosReview(unittest.TestCase):
    def test_original_builder_uses_literal_types_and_refuses_missing_definition(self):
        targets=json.loads(Path('config/target_mappings.json').read_text())['targets']
        parts=review.original_parts('.',targets['035|3-035-3010102'])
        self.assertEqual(len(parts),1)
        self.assertEqual(parts[0]['components'],['CONTCR','CONTDRBL'])
        self.assertEqual(parts[0]['filter'],{'field':'category','op':'eq','values':['28002']})
        self.assertEqual(parts[0]['factor'],1)
        unchanged,notes=eng.correct_components(parts[0],{'typos':{'CONTDRBL':{'to':'CONTDBBL'}}})
        self.assertEqual(unchanged['components'],['CONTCR','CONTDRBL'])
        self.assertFalse(notes)
        original=dict(parts[0],path='01 Loans and advances')
        same,notes=eng.inherit_hierarchy(original,{'enabled':True,'apply_to_leaf':True,'labels':{'loans and advances':{'FORCE':True,'ECB':{'field':'category','op':'eq','values':['INVENTED']}}}})
        self.assertEqual(same['filter'],original['filter'])
        self.assertFalse(notes)
        with self.assertRaisesRegex(ValueError,'exact balance types'):
            review.original_parts('.',targets['010|1-010-10501'])
        with self.assertRaisesRegex(ValueError,'lookup or complex wording'):
            review.original_parts('.',targets['023|2-023-203030201'])

    def test_link_is_original_cell_not_ethix_row(self):
        catalog=json.loads(Path('data/catalogs/catalog-0001.json').read_text(encoding='utf-8'))
        by_id={m['business_id']:m for m in catalog['mappings']}
        rules=json.loads(Path('config/generation_rules.json').read_text())['rules']
        targets=json.loads(Path('config/target_mappings.json').read_text())['targets']
        rows=review.original_rows(targets['010|1-010-10501'],rules,by_id)
        self.assertEqual([(r['sheet'],r['source_row']) for r in rows],[('Table 10',7)])
        self.assertEqual(next(c['value'] for c in rows[0]['cells'] if c['column']=='B'),'SECTOR = 2004')
        self.assertEqual(rules[targets['010|1-010-10501']['legacy_rule_id']]['row'],770)

    def test_column_conditions_kept_separate(self):
        cells=[{'sheet':'Table 23','cell':'B8','text':'RESIDENCE = QA'},
               {'sheet':'Table 23','cell':'E8','text':'RESIDENCE NOT EQUAL TO QA'},
               {'sheet':'Table 35','cell':'B16','text':'CATEGORY = 28002\nASSET TYPE = CONTCR & CONTDRBL'}]
        f=review.extract_fields(cells)
        self.assertIn('B8: RESIDENCE = QA',f['residence'])
        self.assertIn('E8: RESIDENCE NOT EQUAL TO QA',f['residence'])
        self.assertIn('CONTDRBL',f['balance_types'])  # preserve original typo as evidence
        multi=review.extract_fields([{'sheet':'Table 10','cell':'B43','text':'CATEGORY = 3702, 3706 & ASSET TYPE = CURACCOUNT\nGRCACCOUNT\nPREACCOUNT'}])
        self.assertIn('PREACCOUNT',multi['balance_types'])

    def test_disabled_zero_rule_preserves_original_selection(self):
        spec={'path':'01 Loans and advances','source':'ECB','filter':{'field':'category','op':'range','values':[3000,3999]}}
        cfg={'enabled':True,'apply_to_leaf':True,'labels':{'loans and advances':{'enabled':False,'FORCE':True,
             'ECB':{'field':'category','op':'eq','values':['NONE_CONVENTIONAL_PRODUCT']}}}}
        new,notes=eng.inherit_hierarchy(spec,cfg)
        self.assertEqual(new['filter'],spec['filter'])
        self.assertFalse(notes)

    def test_missing_component_partial_not_complete(self):
        cat={'tables':{'001':{'measures':{'In LC Amount':{'semantic':'IN_LC','kind':'money'}}}}}
        sem={'semantic':{'IN_LC':0},'issues':['Absent balance columns: CONTDRBL'],'layout':'geo',
             'missing_components':['CONTDRBL'],'source_kind':'T24_ECB'}
        self.assertEqual(eng.cell_values({'table':'001'},sem,cat,'DRAFT_CANDIDATE')['In LC Amount']['status'],'PARTIAL')
        sem['semantic']={}
        self.assertIsNone(eng.cell_values({'table':'001'},sem,cat,'DRAFT_CANDIDATE')['In LC Amount']['value'])


if __name__=='__main__':
    unittest.main()
