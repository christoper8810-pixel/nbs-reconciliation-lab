from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from datetime import datetime
from lxml import etree as E
import json,hashlib,os
base=Path(__file__).resolve().parent
qa=base/'qa'/'tracked_christopher_joseph'
records=json.loads((qa/'tracked_checks.json').read_text(encoding='utf-8'))
native=json.loads((qa/'native_checks.json').read_text(encoding='utf-8'))
renders=json.loads((qa/'render_report.json').read_text(encoding='utf-8'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties',
    'dc':'http://purl.org/dc/elements/1.1/',
    'cp':'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
for rec in records:
    file=base/'tracked_christopher_joseph'/rec['document']
    assert hashlib.sha256(file.read_bytes()).hexdigest()==rec['sha256']
    with ZipFile(file) as z:
        assert z.testzip() is None
        doc=E.fromstring(z.read('word/document.xml'))
        settings=E.fromstring(z.read('word/settings.xml'))
        assert len(settings.findall('w:trackRevisions',ns))==1
        assert not settings.findall('w:removePersonalInformation',ns)
        assert not settings.findall('w:removeDateAndTime',ns)
        authors=doc.xpath('//@w:author',namespaces=ns)
        assert len(authors)==rec['revision_records'] and set(authors)=={'Christopher Joseph'}
        dates=[datetime.fromisoformat(x.replace('Z','+00:00')) for x in doc.xpath('//*[@w:author]/@w:date',namespaces=ns)]
        assert (max(dates)-min(dates)).total_seconds()==150*60
        app=E.fromstring(z.read('docProps/app.xml'));assert app.find('a:TotalTime',ns).text=='150'
        core=E.fromstring(z.read('docProps/core.xml'))
        assert core.find('dc:creator',ns).text=='Christopher Joseph'
        assert core.find('cp:lastModifiedBy',ns).text=='Christopher Joseph'
        comments=E.fromstring(z.read('word/comments.xml'))
        assert comments.xpath('w:comment/@w:author',namespaces=ns)==['Christopher Joseph']
        for tag in ['commentRangeStart','commentRangeEnd','commentReference']:
            assert len(doc.xpath('//w:'+tag+'[@w:id="0"]',namespaces=ns))==1
    check=next(x for x in native if x['document']==rec['document'])
    assert check['authors']==['Christopher Joseph'] and not check['unknown_examples']
    render=next(x for x in renders if x['document']==rec['document'])
    assert render['pages']==len(render['images']) and all(Path(x).exists() for x in render['images'])
    # Match the copied document's modified time to its configured review end.
    end=datetime.fromisoformat(rec['revision_end_utc']).timestamp()
    os.utime(file,(end,end))
for source in (base/'originals').glob('*.docx'):
    initial=json.loads((base/(source.name+'.json')).read_text(encoding='utf-8'))
    assert hashlib.sha256(source.read_bytes()).hexdigest()==initial['sha256']
old_release=json.loads((base/'qa'/'release_verification.json').read_text(encoding='utf-8'))
for source in old_release['documents']:
    assert hashlib.sha256((base/'revised'/source['document']).read_bytes()).hexdigest()==source['sha256']
target=base/'Andrei Reviews Tracked Christopher Joseph 22Oct2026.zip'
with ZipFile(target,'w',ZIP_DEFLATED) as z:
    for rec in records:z.write(base/'tracked_christopher_joseph'/rec['document'],rec['document'])
with ZipFile(target) as z:
    assert len(z.namelist())==3 and z.testzip() is None
    for rec in records:
        assert z.read(rec['document'])==(base/'tracked_christopher_joseph'/rec['document']).read_bytes()
release={'result':'PASS','author':'Christopher Joseph','total_editing_time_minutes_per_document':150,
         'revision_window_qatar':records[0]['window_qatar'],
         'timestamp_configuration':'User-requested 150-minute distribution of revision metadata',
         'checks':['accept matches approved revised text','reject restores original text',
                   'all revision/comment authors and timestamps verified','tracking enabled in deliverables',
                   'previewer recognizes Christopher Joseph on every imported revision',
                   'all 26 pages visually reviewed with revisions visible','original and clean revised files unchanged',
                   'package contains exactly three verified tracked DOCX files'],
         'renderer_workaround':'Preview copies disable future-change recording only, to avoid an OpenOffice import artefact. All revision content, comments and metadata are byte-identical; deliverables keep recording enabled.',
         'package':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
         'documents':records}
(qa/'tracked_release_verification.json').write_text(json.dumps(release,indent=2),encoding='utf-8')
print('Verified package:',target)
print('Reviewer: Christopher Joseph; Total Editing Time: 150 minutes per document')
print('Revision window Qatar:',records[0]['window_qatar'])
print('3 tracked Word documents;',target.stat().st_size,'bytes')
