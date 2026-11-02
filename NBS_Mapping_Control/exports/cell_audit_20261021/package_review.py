import json,csv,hashlib,zipfile,re
from pathlib import Path
import openpyxl
P=Path(__file__).resolve().parent
d=json.loads((P/'audit.json').read_text(encoding='utf-8'));a=json.loads((P/'acceptance_results.json').read_text(encoding='utf-8'))
assert a['failed']==0 and a['passed']==40
p=P/'NBS_Ehab_Systems_GL_Cell_Audit_21Oct2026.xlsx'
w=openpyxl.load_workbook(p,data_only=False)
assert w.sheetnames==['Read first','Findings','GL comparison','Affected cells','Source coverage']
assert w['Findings'].max_row==len(d['findings'])+4
assert w['GL comparison'].max_row==len(d['comparisons'])+4
assert w['Affected cells'].max_row==sum(bool(x['findings']) for x in d['cell_ledger'])+4
assert w['Source coverage'].max_row==85
assert w['Read first']['B19'].value.startswith('40 acceptance')
assert all(c.data_type!='e' for s in w for row in s for c in row)
formula=[(s.title,c.coordinate,c.value) for s in w for row in s for c in row if c.data_type=='f']
assert len(formula)==5 and all(s=='Read first' for s,_,_ in formula)
for j,f in enumerate(d['findings'],5):
 assert w['Findings'].cell(j,1).value==f['id']
 assert w['Findings'].cell(j,8).value==(f['gl_cells'] or None)
 assert w['Findings'].cell(j,11).value==f['detail']
assert all(w['Findings'].cell(i,16).value is None and w['Findings'].cell(i,17).value is None for i in range(5,len(d['findings'])+5))
w.close()
cached=openpyxl.load_workbook(p,data_only=True)
for rr,status in [(10,'CONFIRMED'),(11,'DIFFERENCE'),(12,'INPUT GAP'),(13,'AMBIGUOUS'),(14,'REVIEW')]:
 assert cached['Read first'].cell(rr,2).value==d['counts']['status'][status],(rr,cached['Read first'].cell(rr,2).value)
cached.close()
for fname,key in [('All_findings.csv','findings'),('GL_category_comparison.csv','comparisons'),('GL_sixth_segment_trace.csv','trace'),('Referenced_GL_rows.csv','gl_evidence'),('NBS_cell_scan.csv','cell_ledger')]:
 with (P/fname).open(encoding='utf-8-sig',newline='') as f:assert sum(1 for _ in csv.DictReader(f))==len(d[key])
for src in d['sources']:
 h=hashlib.file_digest(Path(src['path']).open('rb'),'sha256').hexdigest()
 assert h==src['sha256']
versions={'sources':[{k:x[k] for k in ['label','filename','sha256','sheets','cells','sheet_counts']} for x in d['sources']], 'current_gl_run':d['gl_version']['run'],'mapping_versions':d['gl_version']['versions'],'recorded_changes':d['gl_version']['changes']}
(P/'Source_versions.json').write_text(json.dumps(versions,indent=2),encoding='utf-8')
validation={'acceptance_checks_passed':a['passed'],'acceptance_checks_failed':a['failed'],'delivery_checks':'All workbook rows, original evidence text, GL references, cached summary formulas, CSV row counts, editable decision cells and original source hashes verified. Offline HTML filters and evidence links exercised in browser. Every workbook sheet visually reviewed.','finding_occurrences':d['counts']['findings'],'source_nbs_cells':d['counts']['nbs_populated_cells'],'all_source_cells':sum(x['cells'] for x in d['sources']),'all_source_worksheets':sum(x['sheets'] for x in d['sources']),'status_counts':d['counts']['status'],'limits':'Counts are occurrences, not unique root causes or monetary misstatements. Capturing every source cell is not proof of complete semantic validation. No engine mapping was changed.'}
(P/'Validation_summary.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
names=['READ_ME_FIRST.txt','NBS_Ehab_Systems_GL_Cell_Audit_21Oct2026.xlsx','NBS_All_Mismatches_21Oct2026.html','All_findings.csv','All_findings_one_by_one.md','GL_category_comparison.csv','GL_sixth_segment_trace.csv','Referenced_GL_rows.csv','NBS_cell_scan.csv','Source_sheet_coverage.csv','acceptance_results.json','Source_versions.json','Validation_summary.json']
checksums={n:hashlib.file_digest((P/n).open('rb'),'sha256').hexdigest() for n in names}
(P/'SHA256SUMS.json').write_text(json.dumps(checksums,indent=2),encoding='utf-8');names.append('SHA256SUMS.json')
out=P/'NBS_Ehab_Systems_GL_Audit_Pack_21Oct2026.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:z.write(P/n,n)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for n,h in checksums.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
print(json.dumps({'archive':out.name,'bytes':out.stat().st_size,'files':len(names),'acceptance_checks':a['passed'],'delivery_verified':True}))
