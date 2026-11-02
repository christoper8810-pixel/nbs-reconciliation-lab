from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from docx import Document
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
base=Path(__file__).resolve().parent
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
log=json.loads((base/'change_register.json').read_text(encoding='utf-8'))
checks=[]
for item in log:
    path=base/'revised'/item['revised']
    src=base/'originals'/item['original']
    assert hashlib.sha256(src.read_bytes()).hexdigest()==item['original_sha256']
    with ZipFile(path) as z:
        assert z.testzip() is None
        root=E.fromstring(z.read('word/document.xml'))
        text='\n'.join(''.join(p.xpath('.//w:t/text()',namespaces=ns)) for p in root.xpath('//w:body//w:p',namespaces=ns))
        comments=E.fromstring(z.read('word/comments.xml'))
        assert len(comments)==1
        for tag in ['commentRangeStart','commentRangeEnd','commentReference']:
            assert len(root.xpath('//w:'+tag+'[@w:id="0"]',namespaces=ns))==1
        assert b'/word/comments.xml' in z.read('[Content_Types].xml')
        assert b'/comments' in z.read('word/_rels/document.xml.rels')
        assert not root.xpath('//w:ins|//w:del',namespaces=ns)
        policy=['ACCPRINCIPALPFT','RECPRINCIPALPFT','GRCPRINCIPALPFT','DUEPRINCIPALPFT',
                'NABPRINCIPALPFT','DELPRINCIPALPFT','PREPRINCIPALPFT',
                'linked category 6050 CREDIT','ACCCRPROFIT','ACCDEPOSITPFT',
                'Exclude it from all deposit reporting','LCR deposit outflows','NSFR deposit funding',
                'All changes proposed in NBS01','direct CAL/ECB rules','Implementation checks',
                'do not remove repeated source entries without investigating']
        for phrase in policy: assert phrase in text,(path.name,phrase)
        for forbidden in ['CREDIT to OUTSTANDING is proposed pending owner review',
                          'Approve the conditional CLS relationship',
                          'Remove the profit types; leave the line empty',
                          'Add the missing SP types to the suspended income tables',
                          'Include the conditional linked CLS6050']:
            assert forbidden not in text,(path.name,forbidden)
        # Existing paragraphs were retained or explicitly replaced. No original
        # paragraph can disappear silently during table/formatting edits.
        original=json.loads((base/(item['original']+'.json')).read_text(encoding='utf-8'))
        changed={x['paragraph']:x['after'] for x in item['changes']}
        for i,p in enumerate(original['paragraphs']):
            expected=changed.get(i,p['text'])
            if i==1: expected=p['text'].rstrip()+' Revised 22 October 2026.'
            assert expected in text,(path.name,'lost paragraph',i)
        assert len(Document(path).tables)==len(Document(src).tables)
        # A row taller than a page is avoided by retaining normal automatic
        # row heights; check for content clipping via an explicit exact height.
        assert not root.xpath('//w:trHeight[@w:hRule="exact"]',namespaces=ns)
        (base/'qa'/(path.stem+'.txt')).write_text(text,encoding='utf-8')
    checks.append({'document':path.name,'result':'PASS',
                   'checks':['original hash unchanged','DOCX ZIP integrity and reader load',
                             'one general comment with valid anchors and relationships',
                             'all requested policies present','contradictory recommendations removed',
                             'unmodified source paragraphs preserved','table structures preserved'],
                   'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(base/'qa'/'document_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
