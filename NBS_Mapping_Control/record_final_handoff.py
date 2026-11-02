import io,json,zipfile
from pathlib import Path
from nbs_control.service import ControlService
from nbs_control.web import create_app

root=Path(__file__).parent
job=json.loads((root/'data/generation_jobs/c50efda0cc6b5b95.json').read_text())
assert job['phase']=='Complete'
client=create_app(ControlService()).test_client()
response=client.get('/reports/download/NBS_Generated_September_2026.xlsx')
assert response.status_code==200
with zipfile.ZipFile(io.BytesIO(response.data)) as z:assert z.testzip() is None
validation=json.loads((root/'VALIDATION.json').read_text())
validation['browser_excel_export_job']='c50efda0cc6b5b95'
validation['browser_excel_export_result']=job
validation['workbook_download_verified']={'status':response.status_code,'bytes':len(response.data),'zip_CRC_valid':True}
(root/'VALIDATION.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
warning='The Windows spreadsheet helper reported process exit code 3221226505 after writing the workbook. The application accepts the file only after independently checking all 22,914 numeric source/generated cells and all 16,603 comparison rows against the immutable run. The checked workbook is downloadable; this process shutdown warning is retained in excel_export.log. Native Microsoft Excel execution was not performed.'
evaluation=root/'exports/NBS_EVALUATION.md'
text=evaluation.read_text(encoding='utf-8')+'\n## Excel export runtime note\n\n'+warning+'\n'
evaluation.write_text(text,encoding='utf-8')
latest=Path(json.loads((root/'data/latest_generation.json').read_text())['result'])
r=json.loads(latest.read_text(encoding='utf-8'))
for p in [root/'exports/generation_notes.json',latest.parent/'generation_notes.json']:
    notes=json.loads(p.read_text(encoding='utf-8'));notes['product_policies']=r.get('product_policies');notes['excel_export_runtime_note']=warning;notes['excel_verification']=job['summary']['verification']
    p.write_text(json.dumps(notes,indent=2),encoding='utf-8')
print('Workbook download verified:',len(response.data),'bytes. Final handoff recorded.')
