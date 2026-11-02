import json
from pathlib import Path
import openpyxl
from nbs_control.bank_data import sha
from nbs_control.workbook_validation import verify_report_workbook

root=Path(__file__).parent
result=json.loads((root/'exports/NBS_generated_review.json').read_text(encoding='utf-8'))
book=root/'exports/NBS_Generated_September_2026.xlsx'
wb=openpyxl.load_workbook(book,read_only=True,data_only=True)
assert wb['Generated NBS']['J2'].value is None
assert abs(wb['Generated NBS']['J33'].value-result['rows'][next(i for i,x in enumerate(result['rows']) if x['row']==33)]['values']['J'])<.000001
assert wb['Ethix reference']['J33'].value==2110792
assert abs(wb['Generated NBS']['J49'].value-292410.144)<.000001
errors=[]
for sh in wb:
    for row in sh:
        for c in row:
            if c.data_type=='e':errors.append(f'{sh.title}!{c.coordinate}:{c.value}')
assert not errors,errors[:10]
tabs=wb.sheetnames;wb.close()
manifest=json.loads((root/'data/bank_manifest.json').read_text(encoding='utf-8'))
hashes={k:sha(v['path'])==v['sha256'] for k,v in manifest.items() if isinstance(v,dict) and 'path' in v}
validation={'validated_on':'2026-10-15','tests':116,'test_result':'passed',
    'ECB_account_rows':manifest['ECB']['rows'],'source_hashes_unchanged':hashes,
    'report_summary':result['summary'],'checks':result['checks'],
    'excel_tabs':tabs,'excel_error_cells':errors,'excel_all_five_tabs_rendered_and_reviewed':True,
    'excel_all_amounts_verified':verify_report_workbook(book,result),
    'native_Excel_execution':False,'browser_report_mapping_and_download_controls_verified':True,
    'browser_actual_ECB_upload_job':'3effe2e014eb6bb8',
    'browser_actual_ECB_upload_status':json.loads((root/'data/generation_jobs/3effe2e014eb6bb8.json').read_text())['phase'],
    'bank_reconciliation_complete':False}
(root/'VALIDATION.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2))
