from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
base=Path(__file__).resolve().parent
source=base.parent/'tracked_christopher_joseph'
target=base/'tracked_christopher_joseph'/'render_inputs';target.mkdir(exist_ok=True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in source.glob('*.docx'):
    with ZipFile(p) as z:parts={n:z.read(n) for n in z.namelist()}
    settings=E.fromstring(parts['word/settings.xml'])
    for e in settings.findall('w:trackRevisions',ns):settings.remove(e)
    parts['word/settings.xml']=E.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(target/p.name,'w',ZIP_DEFLATED) as z:
        for n,b in parts.items():z.writestr(n,b)
    with ZipFile(p) as z:
        assert all(parts[n]==z.read(n) for n in z.namelist() if n!='word/settings.xml')
print('Prepared three preview copies; pending revisions, comments and their metadata unchanged')
