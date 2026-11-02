from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from difflib import SequenceMatcher
from lxml import etree as E
import json,re,hashlib,sys

sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parent
OUT=BASE/'tracked_christopher_joseph'
QA=BASE/'qa'/'tracked_christopher_joseph'
OUT.mkdir(exist_ok=True);QA.mkdir(exist_ok=True)
AUTHOR='Christopher Joseph'
MINUTES=150
END=datetime(2026,10,22,16,49,12,tzinfo=timezone.utc)
START=END-timedelta(minutes=MINUTES)
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W14='http://schemas.microsoft.com/office/word/2010/wordml'
CP='http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
DC='http://purl.org/dc/elements/1.1/'
DT='http://purl.org/dc/terms/'
APP='http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
N={'w':W}
def q(n):return '{'+W+'}'+n
def bxml(r):return E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
def text(p):return ''.join(p.xpath('.//w:t/text()',namespaces=N))
def plain_doc(r):
    return [text(p) for p in r.xpath('//w:body//w:p',namespaces=N) if text(p).strip()]
def canon(e):return E.tostring(e,method='c14n') if e is not None else b''
def payload(p):
    # Include non-text run content (e.g. page breaks) when comparing paragraphs.
    runs=[]
    for ch in p:
        if ch.tag==q('pPr'):continue
        c=deepcopy(ch)
        for rp in c.findall('.//'+q('rPr')):rp.getparent().remove(rp)
        for x in c.iter():
            for a in list(x.attrib):
                if 'rsid' in a:del x.attrib[a]
        runs.append(canon(c))
    return runs
class Builder:
    def __init__(self):self.next_id=1;self.changed_paragraphs=0;self.inserted_paragraphs=0;self.inserted_rows=0
    def rev(self,tag):
        e=E.Element(q(tag));e.set(q('id'),str(self.next_id));self.next_id+=1
        e.set(q('author'),AUTHOR);e.set(q('date'),END.isoformat().replace('+00:00','Z'))
        return e
    def props(self,old,new,tag,change):
        a=old.find(q(tag));b=new.find(q(tag))
        if canon(a)==canon(b):return
        if b is None:b=E.Element(q(tag));new.insert(0,b)
        ch=self.rev(change);ch.append(deepcopy(a) if a is not None else E.Element(q(tag)));b.append(ch)
    def paragraph(self,old,new):
        self.props(old,new,'pPr','pPrChange')
        oldtext=text(old);newtext=text(new)
        if oldtext==newtext:
            oldruns=old.findall(q('r'));newruns=new.findall(q('r'))
            # Unchanged text preserves original runs; track formatting changes.
            if len(oldruns)==len(newruns) and all(text(a)==text(b) for a,b in zip(oldruns,newruns)):
                for a,b in zip(oldruns,newruns):self.props(a,b,'rPr','rPrChange')
                oldbreaks=old.xpath('.//w:br',namespaces=N);newbreaks=new.xpath('.//w:br',namespaces=N)
                if len(oldbreaks)==len(newbreaks):return
            elif payload(old)==payload(new):return
        self.changed_paragraphs+=1
        pp=new.find(q('pPr'))
        finalstyle=new.find('.//'+q('r')+'/'+q('rPr'))
        oldstyle=old.find('.//'+q('r')+'/'+q('rPr'))
        # Table issue paragraphs contain plain runs. Keep non-text annotation
        # anchors outside revisions, and retain exact token whitespace.
        anchors=[deepcopy(c) for c in new if c.tag not in {q('pPr'),q('r')}]
        for ch in list(new):
            if ch.tag!=q('pPr'):new.remove(ch)
        def run(s,style,deleted=False):
            r=E.Element(q('r'))
            if style is not None:r.append(deepcopy(style))
            t=E.SubElement(r,q('delText' if deleted else 't'))
            t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=s
            return r
        if not oldtext and not newtext:
            # Track removal/addition of standalone manual page-break runs.
            for oldrun in old.findall(q('r')):
                d=self.rev('del');d.append(deepcopy(oldrun));new.append(d)
        else:
            a=re.findall(r'\s+|\S+',oldtext);b=re.findall(r'\s+|\S+',newtext)
            matcher=SequenceMatcher(None,a,b,autojunk=False)
            for op,ai,aj,bi,bj in matcher.get_opcodes():
                if op=='equal':new.append(run(''.join(b[bi:bj]),finalstyle))
                else:
                    if ai!=aj:
                        d=self.rev('del');d.append(run(''.join(a[ai:aj]),oldstyle,True));new.append(d)
                    if bi!=bj:
                        ins=self.rev('ins');ins.append(run(''.join(b[bi:bj]),finalstyle));new.append(ins)
        for anchor in anchors:new.append(anchor)
    def newparagraph(self,p):
        self.inserted_paragraphs+=1
        pp=p.find(q('pPr'))
        if pp is None:pp=E.Element(q('pPr'));p.insert(0,pp)
        rp=pp.find(q('rPr'))
        if rp is None:rp=E.SubElement(pp,q('rPr'))
        rp.append(self.rev('ins'))  # inserted paragraph mark
        for run in list(p):
            if run.tag==q('r') and run.find(q('commentReference')) is None:
                at=p.index(run);p.remove(run);ins=self.rev('ins');ins.append(run);p.insert(at,ins)
    def table(self,old,new):
        self.props(old,new,'tblPr','tblPrChange')
        self.props(old,new,'tblGrid','tblGridChange')
        oldrows=old.findall(q('tr'));newrows=new.findall(q('tr'))
        assert len(newrows)>=len(oldrows)
        for ri,row in enumerate(newrows):
            if ri>=len(oldrows):
                self.inserted_rows+=1
                trpr=row.find(q('trPr'))
                if trpr is None:trpr=E.Element(q('trPr'));row.insert(0,trpr)
                trpr.append(self.rev('ins'))
                for p in row.xpath('./w:tc/w:p',namespaces=N):
                    for run in list(p):
                        if run.tag==q('r') and run.find(q('commentReference')) is None:
                            at=p.index(run);p.remove(run);ins=self.rev('ins');ins.append(run);p.insert(at,ins)
                continue
            before=oldrows[ri];self.props(before,row,'trPr','trPrChange')
            oc=before.findall(q('tc'));nc=row.findall(q('tc'));assert len(oc)==len(nc)
            for a,b in zip(oc,nc):
                self.props(a,b,'tcPr','tcPrChange')
                ap=a.findall(q('p'));bp=b.findall(q('p'));assert len(ap)==len(bp)
                for pa,pb in zip(ap,bp):self.paragraph(pa,pb)

def resolve(root,accept):
    r=deepcopy(root)
    # Row and paragraph-mark changes have structural semantics, not run
    # semantics. Resolve them before the ordinary insertion/deletion runs.
    for row in list(r.xpath('//w:tr[w:trPr/w:ins]',namespaces=N)):
        if not accept:row.getparent().remove(row)
        else:
            for e in row.xpath('./w:trPr/w:ins',namespaces=N):e.getparent().remove(e)
    for p in list(r.xpath('//w:p[w:pPr/w:rPr/w:ins]',namespaces=N)):
        if not accept:p.getparent().remove(p)
        else:
            for e in p.xpath('./w:pPr/w:rPr/w:ins',namespaces=N):e.getparent().remove(e)
    propchanges=['pPrChange','rPrChange','tblPrChange','tblGridChange','trPrChange','tcPrChange']
    for tag in propchanges:
        for ch in reversed(r.findall('.//'+q(tag))):
            parent=ch.getparent()
            if accept:parent.remove(ch)
            else:
                prior=deepcopy(ch[0]);grand=parent.getparent();at=grand.index(parent)
                grand.remove(parent);grand.insert(at,prior)
    for tag in ['ins','del']:
        for e in reversed(r.findall('.//'+q(tag))):
            par=e.getparent()
            if (tag=='ins')==accept:
                at=par.index(e);children=list(e);par.remove(e)
                for j,c in enumerate(children):par.insert(at+j,c)
            else:par.remove(e)
    for t in r.findall('.//'+q('delText')):t.tag=q('t')
    return r

def add_metadata(parts):
    core=E.fromstring(parts['docProps/core.xml'])
    for tag,val in [('{'+DC+'}creator',AUTHOR),('{'+CP+'}lastModifiedBy',AUTHOR),
                    ('{'+DT+'}modified',END.isoformat().replace('+00:00','Z'))]:
        e=core.find(tag)
        if e is None:e=E.SubElement(core,tag)
        e.text=val
        if tag.endswith('modified'):e.set('{http://www.w3.org/2001/XMLSchema-instance}type','dcterms:W3CDTF')
    parts['docProps/core.xml']=bxml(core)
    app=E.fromstring(parts['docProps/app.xml'])
    tm=app.find('{'+APP+'}TotalTime')
    if tm is None:tm=E.SubElement(app,'{'+APP+'}TotalTime')
    tm.text=str(MINUTES);parts['docProps/app.xml']=bxml(app)
    settings=E.fromstring(parts['word/settings.xml'])
    for tag in ['trackRevisions','revisionView']:
        for e in settings.findall(q(tag)):settings.remove(e)
    view=E.Element(q('revisionView'))
    for k,v in [('markup','1'),('comments','1'),('insDel','1'),('formatting','0')]:view.set(q(k),v)
    anchor=settings.find(q('defaultTabStop'))
    at=settings.index(anchor) if anchor is not None else len(settings)
    settings.insert(at,view);settings.insert(at+1,E.Element(q('trackRevisions')))
    parts['word/settings.xml']=bxml(settings)

def writezip(path,parts):
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for n,b in parts.items():z.writestr(n,b)

report=[]
for item in json.loads((BASE/'change_register.json').read_text(encoding='utf-8')):
    original=BASE/'originals'/item['original'];clean=BASE/'revised'/item['revised']
    with ZipFile(original) as z:orig=E.fromstring(z.read('word/document.xml'))
    with ZipFile(clean) as z:parts={n:z.read(n) for n in z.namelist()}
    final=E.fromstring(parts['word/document.xml']);approved=deepcopy(final)
    builder=Builder()
    origbody=orig.find(q('body'));newbody=final.find(q('body'))
    oldparas={p.get('{'+W14+'}paraId'):p for p in origbody.findall(q('p'))}
    assert None not in oldparas and len(oldparas)==len(origbody.findall(q('p')))
    seen=set()
    for p in newbody.findall(q('p')):
        pid=p.get('{'+W14+'}paraId')
        if pid in oldparas:builder.paragraph(oldparas[pid],p);seen.add(pid)
        else:builder.newparagraph(p)
    assert seen==set(oldparas)
    oldtables=origbody.findall(q('tbl'));newtables=newbody.findall(q('tbl'));assert len(oldtables)==len(newtables)
    for a,b in zip(oldtables,newtables):builder.table(a,b)
    # Distribute the recorded revision timestamps through the requested span.
    revisions=final.xpath('//*[@w:author]',namespaces=N)
    for i,rev in enumerate(revisions):
        rev.set(q('date'),(START+(END-START)*(i/max(1,len(revisions)-1))).replace(microsecond=0).isoformat().replace('+00:00','Z'))
    comments=E.fromstring(parts['word/comments.xml'])
    for c in comments:
        c.set(q('author'),AUTHOR);c.set(q('initials'),'CJ');c.set(q('date'),END.isoformat().replace('+00:00','Z'))
    parts['word/comments.xml']=bxml(comments)
    parts['word/document.xml']=bxml(final);add_metadata(parts)
    name=item['revised'].replace('Revised 22Oct2026','Tracked Christopher Joseph 22Oct2026')
    target=OUT/name;writezip(target,parts)
    accepted=resolve(final,True);rejected=resolve(final,False)
    assert plain_doc(accepted)==plain_doc(approved),(name,'accept mismatch')
    assert plain_doc(rejected)==plain_doc(orig),(name,'reject mismatch')
    assert len(accepted.xpath('//w:tr',namespaces=N))==len(approved.xpath('//w:tr',namespaces=N))
    assert len(rejected.xpath('//w:tr',namespaces=N))==len(orig.xpath('//w:tr',namespaces=N))
    assert len(revisions)>0 and all(e.get(q('author'))==AUTHOR for e in revisions)
    ids=[e.get(q('id')) for e in revisions];assert len(set(ids))==len(ids)
    assert len(final.xpath('//w:del/w:r/w:delText',namespaces=N))>0
    assert not final.xpath('//w:del//w:t',namespaces=N)
    assert len(comments)==1
    times=[datetime.fromisoformat(e.get(q('date')).replace('Z','+00:00')) for e in revisions]
    assert min(times)==START and max(times)==END
    for state,r in [('accepted',accepted),('rejected',rejected)]:
        testparts=dict(parts);testparts['word/document.xml']=bxml(r)
        writezip(QA/(state+' '+name),testparts)
    record={'document':name,'author':AUTHOR,'editing_minutes':MINUTES,
            'revision_start_utc':START.isoformat(),'revision_end_utc':END.isoformat(),
            'window_qatar':[(d+timedelta(hours=3)).strftime('%d %B %Y %H:%M:%S') for d in [START,END]],
            'changed_paragraphs':builder.changed_paragraphs,'new_paragraphs':builder.inserted_paragraphs,
            'new_rows':builder.inserted_rows,'revision_records':len(revisions),
            'checks':['accept equals approved revised text and row count',
                      'reject restores original text and row count',
                      'unique revision IDs','author on every revision and comment',
                      'timestamps span exactly 150 minutes','TotalTime 150 minutes'],
            'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    report.append(record);print(name,len(revisions),'revision records',flush=True)
(QA/'tracked_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
