import copy,json,unittest
from pathlib import Path
from nbs_control.workbook_validation import verify_report_workbook

ROOT=Path(__file__).resolve().parent.parent
BOOK=ROOT/'exports/NBS_Generated_September_2026.xlsx'
RESULT=ROOT/'exports/NBS_generated_review.json'

@unittest.skipUnless(BOOK.exists() and RESULT.exists(),'generated bank workbook not available')
class WorkbookDeliveryTests(unittest.TestCase):
    def test_all_generated_reference_and_difference_values_match_run(self):
        result=json.loads(RESULT.read_text(encoding='utf-8'))
        checked=verify_report_workbook(BOOK,result)
        self.assertGreater(checked['numeric_cells_verified'],10000)
        self.assertGreater(checked['compared_rows_verified'],10000)
    def test_stale_or_wrong_amount_is_refused(self):
        result=json.loads(RESULT.read_text(encoding='utf-8'))
        row=next(x for x in result['rows'] if x['row']==33)
        row['values']['J']+=100
        with self.assertRaisesRegex(ValueError,'amount mismatch'):verify_report_workbook(BOOK,result)
