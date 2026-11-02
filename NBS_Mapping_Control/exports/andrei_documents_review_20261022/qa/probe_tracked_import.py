from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
base=Path(__file__).resolve().parent
folder=base/'tracked_christopher_joseph'/'probes';folder.mkdir(exist_ok=True)
source=next((base.parent/'tracked_christopher_joseph').glob('LCR*.docx'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
tests={
 'without_formatting_changes':'//w:pPrChange|//w:rPrChange|//w:tcPrChange|//w:trPrChange|//w:tblPrChange|//w:tblGridChange',
 'without_paragraph_mark_insertions':'//w:pPr/w:rPr/w:ins',
 'without_row_insertions':'//w:trPr/w:ins',
 'without_empty_deletions':'//w:del[not(.//w:delText)]',
 'without_comment_anchors':'//w:commentRangeStart|//w:commentRangeEnd|//w:commentReference',
}
with ZipFile(source) as z:parts={n:z.read(n) for n in z.namelist()}
for name,xpath in tests.items():
    root=E.fromstring(parts['word/document.xml']);els=root.xpath(xpath,namespaces=ns)
    print(name,'removed',len(els))
    for e in els:e.getparent().remove(e)
    copy=dict(parts);copy['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(folder/(name+'.docx'),'w',ZIP_DEFLATED) as z:
        for n,b in copy.items():z.writestr(n,b)
root=E.fromstring(parts['word/settings.xml'])
for e in root.xpath('//w:trackRevisions|//w:revisionView',namespaces=ns):e.getparent().remove(e)
copy=dict(parts);copy['word/settings.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(folder/'without_tracking_settings.docx','w',ZIP_DEFLATED) as z:
    for n,b in copy.items():z.writestr(n,b)
