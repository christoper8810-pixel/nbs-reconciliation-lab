from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
base=Path(__file__).resolve().parent
register=json.loads((base/'change_register.json').read_text(encoding='utf-8'))
checks=json.loads((base/'qa'/'document_checks.json').read_text(encoding='utf-8'))
renders=json.loads((base/'qa'/'render_report.json').read_text(encoding='utf-8'))
with ZipFile(r'C:\Users\Test\Downloads\OneDrive_1_10-22-2026.zip') as z:
    entries={Path(n).name:n for n in z.namelist()}
    for item in register:
        original=base/'originals'/item['original']
        initial=json.loads((base/(item['original']+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(original.read_bytes()).hexdigest()==initial['sha256']
        assert original.read_bytes()==z.read(entries[item['original']])
        revised=base/'revised'/item['revised']
        test=next(x for x in checks if x['document']==item['revised'])
        assert test['result']=='PASS'
        assert test['sha256']==hashlib.sha256(revised.read_bytes()).hexdigest()
        render=next(x for x in renders if x['document']==item['revised'])
        assert render['pages']==len(render['images'])
        assert all(Path(p).exists() for p in render['images'])
target=base/'Andrei Three Revised Mapping Reviews 22Oct2026.zip'
with ZipFile(target,'w',ZIP_DEFLATED) as z:
    for item in register:z.write(base/'revised'/item['revised'],item['revised'])
with ZipFile(target) as z:
    assert z.testzip() is None and len(z.namelist())==3
    for item in register:assert z.read(item['revised'])==(base/'revised'/item['revised']).read_bytes()
qa={'document_checks':'PASS','originals':'byte-for-byte match to supplied ZIP and initial hashes',
    'layout':'22 rendered pages visually reviewed',
    'renderer':'Apache OpenOffice 4.1.16 in a private local profile, then bundled Poppler PNG rendering',
    'packaged_renderer_diagnosis':'Bundled render_docx.py could not locate soffice.exe; local alternate conversion used',
    'calculations':'Document rules reviewed; financial impacts not recalculated and production mappings not changed',
    'package':str(target),'package_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'documents':checks}
(base/'qa'/'release_verification.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
print('Package verified:',target)
print('Size:',target.stat().st_size,'bytes; 3 revised DOCX files')
