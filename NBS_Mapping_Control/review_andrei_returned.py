from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from collections import Counter
import json

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS={'w':W}
Q=lambda t:'{'+W+'}'+t
ROOT=Path(r'C:\Users\Test\Desktop\NBS_Mapping_Control')
OUT=ROOT/'exports'/'andrei_returned_review_20261025'
OUT.mkdir(parents=True,exist_ok=True)
FILES=[
('LDR',r'C:\Users\Test\Downloads\LDR & LTD - Mapping Review.docx'),
('LCR',r'C:\Users\Test\Downloads\LCR_and_NSFR_Solo_Review_Tracked_CJ_22Oct2026_AV comments.docx'),
('NBS001',r'C:\Users\Test\Downloads\NBS001_Additional_Tables_Review_Tracked_CJ_22Oct2026_AV comments.docx'),
('NBS01',r'C:\Users\Test\Downloads\NBS01_Mapping_Review_Tracked_CJ_22Oct2026_AV comments v2.docx')]

def txt(n,view='accepted'):
    result=[]
    for x in n.iter():
        if x.tag not in (Q('t'),Q('delText'),Q('tab'),Q('br')):continue
        ancestors=list(x.iterancestors())
        if view=='accepted' and any(a.tag in (Q('del'),Q('moveFrom')) for a in ancestors):continue
        if view=='original' and any(a.tag in (Q('ins'),Q('moveTo')) for a in ancestors):continue
        result.append(x.text or '' if x.tag in (Q('t'),Q('delText')) else ('\t' if x.tag==Q('tab') else '\n'))
    return ''.join(result)

allresults=[]
for label,filename in FILES:
    with ZipFile(filename) as z:
        doc=E.fromstring(z.read('word/document.xml'))
        body=doc.find(Q('body'))
        ps=list(body.iter(Q('p')))
        index={p:i for i,p in enumerate(ps)}
        paras=[{'index':i,'accepted':txt(p),'original':txt(p,'original'),'all':txt(p,'all')} for i,p in enumerate(ps)]
        counts=Counter()
        revisions=[]
        for x in body.iter():
            if x.get(Q('author')) is not None:
                counts[(x.get(Q('author')),E.QName(x).localname)]+=1
                if E.QName(x).localname in ('ins','del','moveTo','moveFrom'):
                    p=next((a for a in x.iterancestors() if a.tag==Q('p')),None)
                    revisions.append({'type':E.QName(x).localname,'author':x.get(Q('author')),'date':x.get(Q('date')),'text':txt(x,'all'),'paragraph':index.get(p)})
        comments=[]
        if 'word/comments.xml' in z.namelist():
            for c in E.fromstring(z.read('word/comments.xml')).findall(Q('comment')):
                cid=c.get(Q('id'))
                starts=doc.xpath('//w:commentRangeStart[@w:id=$id]',namespaces=NS,id=cid)
                ends=doc.xpath('//w:commentRangeEnd[@w:id=$id]',namespaces=NS,id=cid)
                sp=next((a for a in starts[0].iterancestors() if a.tag==Q('p')),None) if starts else None
                ep=next((a for a in ends[0].iterancestors() if a.tag==Q('p')),None) if ends else sp
                si=index.get(sp);ei=index.get(ep)
                selected=[]; active=False
                for x in body.iter():
                    if x.tag==Q('commentRangeStart') and x.get(Q('id'))==cid:active=True
                    elif x.tag==Q('commentRangeEnd') and x.get(Q('id'))==cid:active=False
                    elif active and x.tag in (Q('t'),Q('delText')):selected.append(x.text or '')
                context=paras[max(0,si-2):min(len(paras),(ei if ei is not None else si)+3)] if si is not None else []
                comments.append({'id':cid,'author':c.get(Q('author')),'date':c.get(Q('date')),'text':'\n'.join(txt(p,'all') for p in c.findall(Q('p'))),'start':si,'end':ei,'selected':''.join(selected),'context':context})
        extra={n:z.read(n).decode('utf-8') for n in z.namelist() if n.startswith('word/comments') and n!='word/comments.xml'}
        props=z.read('docProps/core.xml').decode('utf-8') if 'docProps/core.xml' in z.namelist() else ''
        result={'label':label,'path':filename,'counts':[{'author':a,'type':t,'count':n} for (a,t),n in counts.items()],'paragraphs':paras,'comments':comments,'revisions':revisions,'extra':extra,'props':props}
        (OUT/(label+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        lines=[label+' '+filename,'REVISION COUNTS '+json.dumps(result['counts']),'CORE '+props,'COMMENTS']
        for c in comments:
            lines.extend([f"COMMENT {c['id']} | {c['author']} | {c['date']} | p{c['start']}-{c['end']}",c['text'],'SELECTED: '+c['selected'],'CONTEXT:']+[f"[{p['index']}] {p['accepted']}" for p in c['context']])
        lines.append('ACCEPTED BODY')
        lines.extend(f"[{p['index']}] {p['accepted']}" for p in paras if p['accepted'].strip())
        lines.append('NON CJ REVISIONS')
        lines.extend(json.dumps(r,ensure_ascii=False) for r in revisions if r['author']!='Christopher Joseph')
        (OUT/(label+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
        allresults.append({'label':label,'comments':len(comments),'counts':result['counts'],'paragraphs':len(paras),'chars':sum(len(p['accepted']) for p in paras)})
print(json.dumps(allresults,indent=2))
