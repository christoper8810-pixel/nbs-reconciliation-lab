import json, zipfile
from pathlib import Path
import openpyxl

paths=list(Path('data/bank_sources').glob('*.xlsx'))+[Path(r'C:\Users\Test\Downloads\ECB_BALANCE Asset type wise (30.09.2026).xlsx')]
out={}
for p in paths:
    w=openpyxl.load_workbook(p,read_only=True,data_only=True)
    sheets=[]
    for s in w:
        samples=[]
        for row in s.iter_rows():
            vals=[c.value for c in row]
            if any(v is not None for v in vals):
                samples.append({'row':row[0].row,'values':vals})
            if len(samples)>=8: break
        sheets.append({'name':s.title,'rows':s.max_row,'columns':s.max_column,'samples':samples})
    out[str(p)]=sheets
    w.close()
Path('data/bank_inspection.json').write_text(json.dumps(out,default=str,indent=2),encoding='utf-8')
print(json.dumps(out,default=str,indent=2))
