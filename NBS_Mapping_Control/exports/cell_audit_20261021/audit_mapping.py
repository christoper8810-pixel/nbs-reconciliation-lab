"""Evidence audit only: no production mapping or source workbook is altered."""
import sys,json,gzip,re,csv,hashlib,collections,zipfile
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from nbs_control.temenos_review import context_cells

def load(label):
 with gzip.open(OUT/(label+'_cells.json.gz'),'rt',encoding='utf-8') as f:return json.load(f)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def col(a):return re.sub(r'\d','',a)
def row(a):return int(re.sub(r'\D','',a))
def compact(vals):
 vals=sorted(set(int(v) for v in vals));groups=[]
 for n in vals:
  if groups and n==groups[-1][-1]+1:groups[-1].append(n)
  else:groups.append([n])
 return ', '.join(str(g[0]) if len(g)==1 else f'{g[0]}–{g[-1]}' for g in groups)

def numset(s):
 """Strict list/range parser. Unknown syntax is unavailable, never a wildcard."""
 s=str(s or '').strip().replace('–','-').replace('—','-')
 if not s or not re.fullmatch(r'[\d\s,&;\-().]+',s):return None
 nums=set()
 for m in re.finditer(r'(\d+)\s*-\s*(\d+)|(\d+)',s):
  if m[1]:
   a,b=int(m[1]),int(m[2])
   if b<a or b-a>99999:return None
   nums.update(range(a,b+1))
  else:nums.add(int(m[3]))
 return nums or None

MARK=re.compile(r'(?<![A-Z])(?P<field>PLCATEGORY|PL\.CATEGORY|PL\s+CATEGORY|CATEGORY|CATEGRY|CATGORY|SECTOR|INDUSTRY|ASSET\s*TYPE|ASSTE\s*TYPE|ASSET|CUSTOMER\.STATUS|RESIDENCE|CURRENCY)\s*(?P<op>NOT\s+EQUAL\s+TO\s*=?|NOT\s+EQUAL\s*=?|EQUAL\s+TO\s*=?|IS\s+NOT\s+EQUAL\s+TO\s*=?|<>|=)\s*',re.I)
SPELL=re.compile(r'\b(?:CATEGRY|CATGORY|ASSTE\s+TYPE|DEBITANDCATEGORY|NOT\s+EUAL|ACCOUNT\.CUTOMER|CREDIIT)\b|\bEQUA;',re.I)
def clauses(text):
 ms=list(MARK.finditer(str(text or '')));out=[]
 for i,m in enumerate(ms):
  key=re.sub(r'[^A-Z]','',m['field'].upper());key={'CATEGRY':'CATEGORY','CATGORY':'CATEGORY','ASSTETYPE':'ASSETTYPE','ASSET':'ASSETTYPE','PLCATEGORY':'CATEGORY'}.get(key,key)
  val=str(text)[m.end():ms[i+1].start() if i+1<len(ms) else len(str(text))]
  val=re.split(r'\n\s*\d+\s*\.\s',val)[0].strip(' \n\r&>.,')
  out.append((key,m['op'].upper(),val))
 return out
def fields(text):
 out=collections.defaultdict(list)
 for k,op,v in clauses(text):
  if k in ('CATEGORY','SECTOR','INDUSTRY','CUSTOMERSTATUS'):
   # Explicit exclusion is permitted, but arbitrary prose is never interpreted.
   parts=re.split(r'\bBUT\s*<>|\bEXCEPT\b|\bEXCLUDE\b',v,flags=re.I)
   ns=numset(parts[0])
   if ns is not None and len(parts)>1:
    ex=numset(parts[1]);ns=ns-ex if ex is not None else None
   if ns is not None and op=='=':out[k].append(ns)
  elif k=='ASSETTYPE':
   v=re.split(r'\b(?:THEN|ANDCATEGORY)\b',v,flags=re.I)[0]
   v=re.split(r'\b(?:CUSTOMER|RESIDENCE|CURRENCY|TABLE|SECTOR)\b',v,flags=re.I)[0].strip(' ,&\n\r')
   if re.fullmatch(r'[A-Z0-9_,&\s]+',v,re.I):out[k].append(set(re.findall(r'[A-Z][A-Z0-9_]*',v.upper())))
 return dict(out)
def category_of(text):
 fs=fields(text);xx=fs.get('CATEGORY',[])
 return set.union(*xx) if xx else None

def gl_predicate(text):
 """Compile Ehab's explicit GL prose; unsupported mixed loan/GL prose remains partial."""
 s=str(text or '').lower().replace('’',"'")
 toks=list(re.finditer(r'(?<![\d])\d{2,10}(?![\d])',s))
 if not any(len(m[0])==10 for m in toks) and not re.search(r'gl|starts?\s+(?:by|with)',s):return None
 if re.search(r'\bsic\b|all loan|all deposits|nonpersonal|\brim\b',s):return {'partial':True,'text':text,'terms':[(1,m[0]) for m in toks if len(m[0])==10]}
 terms=[];sign=1;prev=0;mode='include';block=[]
 # Plus/minus and exclusions are separate legs. Exclude(...) means a signed deduction.
 for m in toks:
  between=s[prev:m.start()]
  if '+' in between:mode='include';sign=1
  if 'minus' in between:mode='include';sign=-1
  if re.search(r'\bexclude\b',between):mode='include';sign=-1
  elif re.search(r'\bexcept\b',between):mode='exclude'
  if mode=='exclude':block.append(m[0])
  else:terms.append((sign,m[0]))
  prev=m.end()
 if not terms:return None
 return {'partial':False,'text':text,'terms':terms,'exclude':block}
def selected(p,code):
 return [(sign,pat) for sign,pat in p['terms'] if code.startswith(pat) and (len(pat)==10 or not any(code.startswith(x) for x in p.get('exclude',[])))]

def main():
 cat=read(ROOT/'data/catalogs/catalog-0001.json');byid={r['business_id']:r for r in cat['mappings']};blocks=collections.defaultdict(list)
 for r in cat['mappings']:blocks[r['block_key']].append(r)
 raw=load('SYSTEMS');ehabraw=load('EHAB');glbase=load('GL_CURRENT_BASE');old=load('GL_09SEP');vm=read(OUT/'gl_version.json')
 current={s:dict(v) for s,v in glbase.items()}
 for e in vm['changes']:
  current.setdefault(e['sheet'],{})[e['col']+str(e['row_no'])]={'v':e['new_value'],'t':'s','overlay':e['id']}
 def make_rows(data,sheet):
  rows=collections.defaultdict(dict)
  for a,c in data.get(sheet,{}).items():rows[row(a)][col(a)]=c.get('v') or ''
  return dict(rows)
 glrows={'Current v6':make_rows(current,'GL Mapping'),'9 September':make_rows(old,'GL Mapping')}
 idx={};gl_stats=[]
 for ver,rr in glrows.items():
  ix=collections.defaultdict(list)
  for rn,r in rr.items():
   parts=str(r.get('A','')).split('-')
   if len(parts)==6 and re.fullmatch(r'\d{10}',parts[5]):ix[parts[5]].append((rn,r))
  idx[ver]=ix;gl_stats.append({'version':ver,'data_rows':sum(len(v) for v in ix.values()),'sixth_segments':len(ix)})
 systemsrows=[r for r in cat['mappings'] if r['source_system']=='T24'];ehabrows=[r for r in cat['mappings'] if r['source_system']=='ETHIX']
 sysbyloc={(r['sheet'],r['source_row']):r for r in systemsrows}
 findings=[];seen=set();affected=collections.defaultdict(list)
 def add(kind,status,title,sh,refs,detail,other='',action='',table='',ehab='',gl='',missing='',extra='',baseline='',limits=''):
  refs=list(dict.fromkeys(refs if isinstance(refs,list) else [refs]));key=(kind,sh,tuple(refs),title,detail)
  if key in seen:return
  seen.add(key);fid=f'NBS-{len(findings)+1:04d}'
  f={'id':fid,'status':status,'type':kind,'table':str(table),'title':title,'systems_sheet':sh,'systems_cells':', '.join(refs),'ehab_cells':ehab,'gl_cells':gl,'detail':detail,'other_evidence':other,'missing_categories':missing,'extra_categories':extra,'baseline_9sep':baseline,'action':action,'limits':limits,'stakeholder_decision':'','owner':''};findings.append(f)
  for a in refs:affected[('SYSTEMS',sh,a)].append(fid)
  for hit in re.finditer(r'\b[A-Z]+\d+\b',ehab):affected[('EHAB',next(iter(ehabraw)),hit[0])].append(fid)
  return fid
 def ci(a):
  n=0
  for x in re.sub(r'\d','',a):n=n*26+ord(x)-64
  return n
 def report_cell(r,c):
  hh=[ci(x['coord']) for h in blocks[r['block_key']] if h['kind']=='HEADER' for x in h['cells'] if x.get('header')]
  maximum=max(hh) if hh else 10
  return ci(c['cell'] if 'cell' in c else c['coord'])<=maximum
 def effective(c,sh):
  if c.get('alias',{}).get('status')=='RESOLVED':return c['alias']['value']
  cached=raw.get(sh,{}).get(c['coord'],{})
  if c.get('type')=='f' and cached.get('t')!='e' and cached.get('v') is not None:return cached['v']
  return c.get('value')
 
 # Direct original cross-reference trace, never Excel execution. Incomplete references remain explicit.
 refpat=re.compile(r"(?:'([^']+)'|([A-Za-z][A-Za-z0-9 _-]*))!\$?([A-Z]+)\$?(\d+)")
 def evidence(r,depth=0,visited=None):
  visited=set() if visited is None else visited
  key=(r['sheet'],r['source_row'])
  if key in visited or depth>5:return [],True
  visited=visited|{key}
  cells=context_cells(r,blocks[r['block_key']]);out=[];unresolved=False
  for c in cells:
   if not report_cell(r,c):continue
   out.append(c)
   if c['role']!='LINE':continue
   text=c['text'];refs=list(refpat.finditer(text))
   if not refs and ('!' in text) and not category_of(text):unresolved=True
   for m in refs:
    sh=m[1] or m[2];dest=sysbyloc.get((sh,int(m[4])))
    if dest:
     cc,uu=evidence(dest,depth+1,visited);out+=cc;unresolved|=uu
    else:unresolved=True
  return out,unresolved
 comparisons=[];glevidence={};trace=[]
 for e in ehabrows:
  if e['kind']!='RULE':continue
  for cell in e['cells']:
   if cell['column']==e.get('description_column'):continue
   text=cell.get('alias',{}).get('value',cell.get('value',''));p=gl_predicate(text)
   if not p:continue
   ers=cell['coord'];matches=[byid[x['business_id']] for x in e.get('nbs_row_candidates',[]) if x['business_id'] in byid and x.get('match')=='FULL_PATH']
   traces={};vercats={};uncertain=[]
   for ver in ['Current v6','9 September']:
    groups=collections.defaultdict(list);u=[]
    for code,rr in idx[ver].items():
     legs=selected(p,code)
     if not legs:continue
     for rn,gr in rr:
      cls=gr.get('H','').strip().upper();ispl=cls=='PL' or bool(gr.get('J','').strip())
      cv=(gr.get('J','').strip() or gr.get('L','').strip()) if ispl else gr.get('L','').strip()
      ns=numset(cv)
      key=(code,cv,gr.get('O',''),gr.get('M',''),gr.get('N',''),gr.get('S',''),gr.get('H',''),gr.get('P',''))
      groups[key].append(rn)
      glevidence[(ver,rn)]={'version':ver,'row':rn,'sixth_segment':code,'full_gl':gr.get('A',''),'currency':gr.get('B',''),'description':gr.get('C',''),'classification':cls,'migration_pl':gr.get('J',''),'category':gr.get('L',''),'sector':gr.get('O',''),'department':gr.get('M',''),'product':gr.get('N',''),'residence':gr.get('P',''),'balance_types':gr.get('S',''),'destination':gr.get('W',''),'terms':gr.get('Q',''),'dormancy':gr.get('R','')}
      if ns is None and cls not in ('NOT TO BE MAPPED','NO MIGRATION','NOT TO BE MIGRATED'):u.append((code,rn,cv,cls))
    traces[ver]=groups;vercats[ver]=set().union(*(numset(k[1]) or set() for k in groups)) if groups else set()
    uncertain.extend((ver,*x) for x in u)
   for ver,gg in traces.items():
    for k,rns in gg.items():
     trace.append({'ehab_cell':ers,'table':e.get('table_number') or e.get('base_report'),'description':e.get('description'),'version':ver,'sixth_segment':k[0],'category':k[1],'sector':k[2],'department':k[3],'product':k[4],'balance_types':k[5],'classification':k[6],'residence':k[7],'gl_rows':', '.join(map(str,rns)),'rule_text':text,'ehab_sign_legs':str(selected(p,k[0]))})
   if not matches:
    comparisons.append({'ehab_cell':ers,'table':e.get('table_number') or e.get('base_report'),'description':e.get('description'),'ehab_rule':text,'systems_reference':'','systems_categories':'','gl_current_categories':compact(vercats['Current v6']),'gl_9sep_categories':compact(vercats['9 September']),'missing_current':'','extra_current':'','status':'NO UNIQUE ROW LINK','note':'No FULL_PATH catalogue link. Not joined by row offset or fuzzy leaf description.'})
    add('ROW_LINK','REVIEW','Ehab GL rule has no exact Systems hierarchy link','',[],f'Ehab {ers}: {e.get("description")}. No FULL_PATH recorded match.',action='Confirm the target hierarchy before changing category logic.',table=e.get('table_number') or e.get('base_report'),ehab=ers)
    continue
   for s in matches:
    cc,unres=evidence(s);cs=[]
    # Use only actual criterion cells, not SQL/document text or explanatory notes.
    for c in cc:
     ns=category_of(c['text'])
     if ns is not None:cs.append((c,ns))
    scats=set().union(*(ns for _,ns in cs)) if cs else set()
    currentcats=vercats['Current v6'];basecats=vercats['9 September'];missing=currentcats-scats;extra=scats-currentcats
    missingbase=basecats-scats;extrabase=scats-basecats
    ext=any(re.search(r'OUTBOUND|CRS[A-Z]+T|TREASURY',c['text'],re.I) for c in cc)
    status='CATEGORY SET AGREES' if currentcats and scats and not missing and not extra else 'CATEGORY SET DIFFERS' if scats and currentcats else 'NO CATEGORY COMPARISON'
    note='Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.'
    if p['partial']:note+=' Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.'
    if uncertain:note+=' Some selected GL rows have no executable numeric category; see unresolved GL rows.'
    if ext:note+=' Systems uses treasury/outbound data; GL equivalence is not established.'
    if unres:note+=' Some original cross-references could not be resolved safely.'
    glrefparts=[]
    for ver in ['Current v6','9 September']:
     valid=[(k,rns) for k,rns in traces[ver].items() if numset(k[1]) is not None]
     wanted=missing if ver=='Current v6' else missingbase
     valid.sort(key=lambda z:0 if wanted and (numset(z[0][1]) or set())&wanted else 1)
     for k,rns in valid[:5]:
      rn=rns[0];gr=glrows[ver][rn];category_col='J' if gr.get('J','').strip() else 'L'
      glrefparts.append(f'{ver}: GL Mapping!A{rn}, {category_col}{rn} = {k[1]}')
    glrefs='; '.join(glrefparts)
    refs=[c['cell'] for c,ns in cs if c['sheet']==s['sheet']];reftext='; '.join(dict.fromkeys(c['sheet']+'!'+c['cell'] for c,ns in cs))
    comparisons.append({'ehab_cell':ers,'table':e.get('table_number') or e.get('base_report'),'description':e.get('description'),'ehab_rule':text,'systems_reference':s['sheet']+'!'+str(s['source_row']),'criterion_references':reftext,'systems_categories':compact(scats),'gl_current_categories':compact(currentcats),'gl_9sep_categories':compact(basecats),'missing_current':compact(missing),'extra_current':compact(extra),'missing_9sep':compact(missingbase),'extra_9sep':compact(extrabase),'status':status,'note':note})
    if status=='CATEGORY SET DIFFERS':
     add('GL_CATEGORY','DIFFERENCE',f'Ehab GL-to-category selection differs: {e.get("description")}',s['sheet'],refs or [s.get('description_column','A')+str(s['source_row'])],f'Ehab {ers} selects GL sixth segments whose current categories are {compact(currentcats)}. Systems criteria select {compact(scats)}.',other=reftext,action='Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.',table=e.get('table_number') or e.get('base_report'),ehab=ers,gl=glrefs,missing=compact(missing),extra=compact(extra),baseline=f'9 September missing: {compact(missingbase) or "none"}; extra: {compact(extrabase) or "none"}.',limits=note)
    elif status=='NO CATEGORY COMPARISON':
     add('MISSING_CRITERIA','REVIEW',f'No numeric category bridge: {e.get("description")}',s['sheet'],[s.get('description_column','A')+str(s['source_row'])],f'Ehab {ers}: {text}. Systems linked row has '+('treasury/outbound logic' if ext else 'no safely traceable explicit category selection')+'.',other='; '.join(dict.fromkeys(c['sheet']+'!'+c['cell'] for c in cc if c['role']=='LINE')),action='Obtain the source-specific bridge or complete the original category/balance definition.',table=e.get('table_number') or e.get('base_report'),ehab=ers,limits=note)
 
 # Independent scan of every Systems criterion cell and pair of comparable currency columns.
 for r in systemsrows:
  table=r.get('table_number') or r.get('base_report') or r['sheet'];cells=r['cells'];mapping={c['column']:c for c in cells};rn=r['source_row'];sh=r['sheet']
  for c in cells:
   text=str(c.get('value') or '');a=c['coord']
   if SPELL.search(text):
    bad=sorted(set(x[0] for x in SPELL.finditer(text)))
    if bad:add('FIELD_SPELLING','CONFIRMED',f'Malformed field or operator: {", ".join(bad)}',sh,a,text,action='Correct the specification spelling after preserving the original cell. Confirm the actual source field name.',table=table)
   if c.get('type')=='e' or '#REF!' in text:
    add('BROKEN_REFERENCE','CONFIRMED','Broken Excel reference in source',sh,a,text,action='Repair the intended reference in a reviewed mapping copy.',table=table)
   fs=fields(text)
   for k,sets in fs.items():
    if k!='ASSETTYPE' and len(sets)>1 and not set.intersection(*sets) and re.search(r'&\s*'+k+r'\s*=',text,re.I):
     add('DISJOINT_AND','AMBIGUOUS',f'Disjoint repeated {k} conditions joined by &',sh,a,text,action='State OR / separate additive components explicitly. Literal AND yields an empty selection.',table=table,limits='The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.')
  # Compare only LC/FC columns identified by the explicit source headers.
  headers={}
  for h in blocks[r['block_key']]:
   if h['source_row']>rn:continue
   for c in h['cells']:
    if c.get('header'):headers[c['column']]=c['header']
  pairs=[]
  for lc in mapping:
   hdr=headers.get(lc,'')
   if not re.search(r'(^| / )LC$',hdr):continue
   want=re.sub(r'LC$','FC',hdr)
   for fc in mapping:
    if headers.get(fc)==want:pairs.append((lc,fc))
  for lc,fc in pairs:
   ca,cb=mapping[lc],mapping[fc];fa,fb=fields(effective(ca,sh)),fields(effective(cb,sh))
   for field in ['CATEGORY','ASSETTYPE','SECTOR','INDUSTRY','CUSTOMERSTATUS']:
    a=fa.get(field);b=fb.get(field)
    if not a and not b:continue
    av=set.union(*a) if a else None;bv=set.union(*b) if b else None
    if av==bv:continue
    # Header/context rows set different currencies intentionally. This test concerns account populations only.
    if not r.get('description') or r['kind'] in ('HEADER','TITLE'):continue
    display=lambda ss:compact(ss) if ss and field!='ASSETTYPE' else ', '.join(sorted(ss)) if ss else '(not specified in this cell)'
    add('CURRENCY_COLUMNS','DIFFERENCE',f'LC/FC {field} criteria differ: {r.get("description")}',sh,[ca['coord'],cb['coord']],f'{headers.get(lc)}: {display(av)}. {headers.get(fc)}: {display(bv)}.',other=str(ca.get('value'))+'\nVERSUS\n'+str(cb.get('value')),action='Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.',table=table,limits='A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.')
 
 # ECB exact balance type vocabulary. Absence is evidence of missing input, never a synonym.
 import sqlite3
 db=ROOT/'data/bank_20260930.sqlite';con=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True)
 tables=[x[0] for x in con.execute("select name from sqlite_master where type='table'")];types=set()
 for t in tables:
  info=[x[1] for x in con.execute('pragma table_info("'+t+'")')]
  if t=='ecb_balance' and 'balance_type' in info:types={x[0] for x in con.execute('select distinct balance_type from ecb_balance')}
 if not types:
  manifest_record=con.execute("select value from metadata where key='manifest'").fetchone()
  if manifest_record:types.update(json.loads(manifest_record[0]).get('ECB',{}).get('component_columns',[]))
 con.close()
 (OUT/'ecb_types.json').write_text(json.dumps(sorted(types)),encoding='utf-8')
 for r in systemsrows:
  for c in r['cells']:
   ts=fields(c.get('value')).get('ASSETTYPE',[])
   for typ in sorted(set.union(*ts) if ts else set()):
    if types and typ not in types and typ not in ('AND','OR'):
     add('ABSENT_BALANCE_TYPE','INPUT GAP',f'Original balance type absent from supplied ECB: {typ}',r['sheet'],c['coord'],str(c.get('value')),action='Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.',table=r.get('table_number') or r.get('base_report'),limits='Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.')

 # Cached Excel errors are original workbook evidence, independent of catalogue parsing.
 for label,book in [('SYSTEMS',raw),('EHAB',ehabraw)]:
  for sh,ss in book.items():
   for a,c in ss.items():
    if c['t']=='e':
     fid=add('EXCEL_ERROR','CONFIRMED',f'Original cached Excel error: {c.get("v")}',sh if label=='SYSTEMS' else '',[a] if label=='SYSTEMS' else [],f'{label} {sh}!{a}: saved error {c.get("v")}; formula {c.get("f") or "shared formula / formula precedent"}.',action='Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.',table=sh,ehab=a if label=='EHAB' else '',limits='This is the saved source error. Source formulas were not executed during the audit.')

 # Inspect the actual expanded Table 11 formulas, including shared-formula children.
 import openpyxl
 formula_book=openpyxl.load_workbook(cat['sources']['T24']['file_path'],data_only=False)
 ts=formula_book['Table 11']
 expected={'F':lambda rr:{f'B{rr}',f'D{rr}'},'G':lambda rr:{f'C{rr}',f'E{rr}'},'N':lambda rr:{f'H{rr}',f'J{rr}',f'L{rr}'},'O':lambda rr:{f'I{rr}',f'K{rr}',f'M{rr}'},'P':lambda rr:{f'F{rr}',f'N{rr}'},'Q':lambda rr:{f'G{rr}',f'O{rr}'}}
 for rr in ts.iter_rows():
  for c in rr:
   if c.data_type!='f' or c.column_letter not in expected:continue
   formula=c.value;refs=set(re.findall(r'\b[A-Z]+\d+\b',formula));correct=expected[c.column_letter](c.row)
   if refs!=correct:
    add('CREDIT_QUALITY_FORMULA','CONFIRMED','Credit-quality total uses wrong buckets or direct/indirect columns','Table 11',c.coordinate,f'Original {formula}. The source headings require '+ '+'.join(sorted(correct))+'.',action='Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.',table='11')
 formula_book.close()

 # Remaining maturity must be positive for a future maturity, under the source future-band headers.
 for sh,ss in raw.items():
  for a,c in ss.items():
   text=str(c.get('v') or '')
   if re.search(r'SYSTEM\s*DATE\s*-\s*MATURITY\.DATE',text,re.I):
    add('MATURITY_DIRECTION','CONFIRMED','Remaining maturity subtraction runs backwards',sh,a,text,action='For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.',table=sh,limits='Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.')
 # Boundary gaps are independently demonstrable from the original adjacent strict inequalities.
 ss=raw['Table 10']
 add('NO_MATURITY','CONFIRMED','Without Maturity is defined as a one-day date band','Table 10','D6',ss['D6']['v'],other='Table 10!D4: Without Maturity',action='Select missing/open-ended maturity according to the approved source definition. Do not treat a near-term or overdue date as a missing date.',table='10')
 bands=[]
 for a,c in ss.items():
  if row(a)!=6:continue
  m=re.search(r'greater than\s*(\d+)\s*and less than\s*(\d+)',str(c.get('v')),re.I)
  if m:bands.append((a,int(m[1]),int(m[2])))
 for a,lo,hi in bands:
  nexts=[aa for aa,ll,hh in bands if ll==hi]
  if hi==7300:nexts=['N6']
  if nexts:
   add('MATURITY_BOUNDARY','CONFIRMED',f'Exact maturity boundary {hi} days is omitted','Table 10',[a,*nexts],f'{a} ends at less than {hi}; {nexts[0]} starts at greater than {hi}. A balance at exactly {hi} days reaches neither band.',action='Use mutually exclusive bands with one inclusive side at each shared boundary.',table='10')

 # Arithmetic written as mapping text must follow the labelled amount columns.
 for r in systemsrows:
  hh={}
  for h in blocks[r['block_key']]:
   if h['source_row']>r['source_row']:continue
   for c in h['cells']:
    if c.get('header'):hh[c['column']]=c['header']
  for c in r['cells']:
   expr=str(c.get('value') or '').strip();parts=re.fullmatch(r'([A-Z]+)\s*\+\s*([A-Z]+)',expr)
   if not parts:continue
   this=c['column'];hdr=hh.get(this,'');valid=[]
   if re.search(r' / (Total|Net)$',hdr):
    pref=hdr.rsplit(' / ',1)[0]+' / '
    children=[k for k,v in hh.items() if v.startswith(pref) and k!=this and v.split(' / ')[-1] not in ('Total','Net')]
    if len(children)==2:valid=[set(children)]
   if hdr.startswith('Grand Total / '):
    suffix=hdr.split(' / ')[-1];aa=[k for k,v in hh.items() if v=='Inside Qatar / '+suffix];bb=[k for k,v in hh.items() if v=='Outside Qatar / '+suffix]
    if aa and bb:valid.append({aa[0],bb[0]})
   if valid and set(parts.groups()) not in valid:
    add('TOTAL_COLUMNS','CONFIRMED','Total expression uses the wrong labelled columns',r['sheet'],c['coord'],f'{hdr} contains {expr}. Valid labelled components: '+ ' or '.join('+'.join(sorted(v,key=ci)) for v in valid)+'.',action='Correct the written total expression to the labelled source columns.',table=r.get('table_number') or r.get('base_report'))

 # Dictionary validation uses approved category identifiers, not numeric guessing.
 dictionaries={ver:make_rows(book,'CATEGORY') for ver,book in [('Current v6',current),('9 September',old)]}
 dictindex={ver:{int(z['E']):(rn,z) for rn,z in rr.items() if str(z.get('E','')).isdigit()} for ver,rr in dictionaries.items()}
 for r in systemsrows:
  for c in r['cells']:
   if c['column']==r.get('description_column'):continue
   for field,op,val in clauses(c.get('value')):
    if field!='CATEGORY':continue
    ns=numset(val)
    if ns is None:continue
    # Test individual list members only; unused members of legitimate ranges are not defects.
    indiv=re.sub(r'\d+\s*-\s*\d+','',val)
    for token in re.findall(r'(?<!\d)\d{4,6}(?!\d)',indiv):
     n=int(token)
     if n not in dictindex['Current v6'] and n not in dictindex['9 September']:
      add('UNKNOWN_CATEGORY','DIFFERENCE',f'Explicit category absent from both supplied dictionaries: {token}',r['sheet'],c['coord'],str(c.get('value')),action='Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.',table=r.get('table_number') or r.get('base_report'),limits='Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.')
     elif r['sheet'] in ('Income','Expense') and n in dictindex['Current v6']:
      rn,z=dictindex['Current v6'][n]
      # Source explicitly declares CONSOLIDATE.PRFT.LOSS. Product categories have a different namespace.
      if str(z.get('D','')).strip().upper() not in ('PL','P/L') and n<50000:
       add('CATEGORY_NAMESPACE','DIFFERENCE',f'Product category placed in a consolidated P&L selector: {token}',r['sheet'],c['coord'],f'Cell: {c.get("value")}. CATEGORY!D{rn}: {z.get("D")}; CATEGORY!F{rn}: {z.get("F")}.',gl=f'Current v6 CATEGORY!D{rn}:F{rn}',action='Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.',table=r.get('base_report') or r['sheet'])

 # Investigate duplicate Ehab selectors within one schedule; retain both originals.
 dup=collections.defaultdict(list)
 for e in ehabrows:
  if e['kind']!='RULE' or not e.get('description'):continue
  for c in e['cells']:
   text=c.get('alias',{}).get('value',c.get('value',''));p=gl_predicate(text)
   if p and not p['partial']:
    sig=(tuple(p['terms']),tuple(p.get('exclude',[])))
    dup[(e['block_key'],sig)].append((e,c))
 for vv in dup.values():
  if len(vv)<2:continue
  for i in range(len(vv)):
   e,ca=vv[i]
   for f,cb in vv[i+1:]:
    if e['source_row']==f['source_row']:continue
    add('EHAB_DUPLICATE','REVIEW','Same Ehab GL selector assigned to two lines','',[],f'{ca["coord"]} {e.get("description")}: {ca.get("value")}. {cb["coord"]} {f.get("description")}: {cb.get("value")}.',action='Investigate whether a split attribute or correction is missing. Retain both entries until evidenced.',table=e.get('table_number') or e.get('base_report'),ehab=ca['coord']+', '+cb['coord'])

 # Explicit cross-schedule overlap: both original selectors name the same component/population.
 a=raw['TABLE 19']['C10']['v'];b=raw['Table 30']['B7']['v']
 aa=fields(a);bb=fields(b)
 sharedcat=(category_of(a) or set())&(category_of(b) or set())
 sharedtypes=set.union(*aa.get('ASSETTYPE',[set()]))&set.union(*bb.get('ASSETTYPE',[set()]))
 if sharedcat and sharedtypes:
  add('CROSS_SCHEDULE_OVERLAP','REVIEW','Accrued asset and deferred liability select the same profit component','TABLE 19','C10',f'TABLE 19!C10 and Table 30!B7 both include categories {compact(sharedcat)} and {", ".join(sorted(sharedtypes))}.',other='Table 30!B7; GL review puts ACCDEFERREDPFT on deferred income 2610.',action='Determine the intended accounting side and measurement. Reconcile the asset and liability schedules without automatically deleting either source rule.',table='19 / 30',limits='Selector overlap is proven. Actual double counting depends on the complete source calculation and presentation sign.')

 # Retain the exact sector dictionary evidence for every conflicting NBFI criterion.
 segment=make_rows(current,'SEGMENT')
 salary=[(rn,z) for rn,z in segment.items() if str(z.get('C','')).startswith('2006 ')]
 if salary:
  dr,dv=salary[0]
  for r in systemsrows:
   if 'non-bank financial' not in r.get('path_key',''):continue
   for c in r['cells']:
    fs=fields(c.get('value'));secs=set.union(*fs.get('SECTOR',[set()]))
    sm=re.search(r'SECTOR\s*=\s*([0-9,\s-]+)',str(c.get('value')),re.I)
    if sm:secs|=numset(sm[1]) or set()
    if 2006 in secs:
     add('SECTOR_DICTIONARY','DIFFERENCE','NBFI criterion includes the salary-card sector','Table 11' if r['sheet']=='Table 11' else r['sheet'],c['coord'],f'Original criterion: {c.get("value")}. Current GL SEGMENT!C{dr}: {dv["C"]}.',gl=f'Current v6 SEGMENT!C{dr}',action='Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.',table=r.get('table_number'),limits='The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.')
 add('BREAKDOWN_LINK','CONFIRMED','Asset cash reference omits the Cash on hand row','ASSET - 100','B6',f'Original text: {raw["ASSET - 100"]["B6"]["v"]}. Table 1!A9 is Cash on hand; the written references are A10 Precious Metals and A11 Others.',other='Table 1!A9:A11; Ehab K5 / K358',action='Correct the linked breakdown rows after confirming which cash components belong in the base line.',table='100',ehab='K5, K358',limits='The written reference omission is confirmed. This cell is a specification string, not a working balance calculation.')
 targets=read(ROOT/'config/target_mappings.json')['targets'];target_tables=sorted(set(str(t['table']).zfill(3) for t in targets.values()))
 system_tables={str(r['table_number']).zfill(3) for r in systemsrows if r.get('table_number')}
 for t in target_tables:
  if int(t)<100 and t not in system_tables:
   add('MISSING_SCHEDULE','INPUT GAP',f'BO schedule {t} has no original Systems worksheet','',[],f'The BO target register includes table {t}; no table-number worksheet is present in the 6 October Systems source.',action='Obtain the original specification or write a separate reviewed mapping for the missing schedule.',table=t,limits='No original worksheet was supplied. This does not establish what is deployed in the bank report.')

 # Carry forward prior source-review issues only when the exact original cell still agrees.
 # Existing observed findings never become an error solely because a reviewer raised them.
 for f in cat['findings_queue']:
  if f.get('scope')!='CELL' or not f.get('cell_found') or not f.get('cell'):continue
  label='SYSTEMS' if f.get('source_system')=='T24' else 'EHAB';book=raw if label=='SYSTEMS' else ehabraw
  sh=f.get('sheet');a=f['cell'];c=book.get(sh,{}).get(a)
  if c is None:continue
  if affected.get((label,sh,a)):continue
  # These source review topics concern measurement/definitions beyond category-set comparison.
  add('PRIOR_SOURCE_REVIEW','REVIEW',f['finding_title'],sh if label=='SYSTEMS' else '',[a] if label=='SYSTEMS' else [],f.get('implication',''),other=f.get('finding_id',''),action=f.get('required_owner_decision') or 'Resolve the documented source definition.',table=sh,ehab=a if label=='EHAB' else '',limits='Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.')
 
 # Raw-cell ledger covers all populated NBS cells, including formulas and notes.
 ledger=[]
 for label,book in [('EHAB',ehabraw),('SYSTEMS',raw)]:
  for sh,cells in book.items():
   for a,c in cells.items():
    ids=affected.get((label,sh,a),[])
    ledger.append({'source':label,'sheet':sh,'cell':a,'type':c['t'],'formula':c.get('f',''),'value':c.get('v'),'findings':', '.join(ids),'scan_result':'FINDING' if ids else 'SCANNED; NO RULE-BASED FINDING','note':'No finding does not certify business correctness.'})
 def writecsv(name,rr):
  if not rr:return
  heads=list(dict.fromkeys(k for r in rr for k in r))
  with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=heads);w.writeheader();w.writerows(rr)
 manifest=read(OUT/'source_manifest.json')
 result={'created_at':datetime.now().isoformat(timespec='seconds'),'sources':manifest,'gl_version':vm,'gl_statistics':gl_stats,'counts':{'findings':len(findings),'status':dict(collections.Counter(x['status'] for x in findings)),'type':dict(collections.Counter(x['type'] for x in findings)),'comparisons':len(comparisons),'gl_trace_groups':len(trace),'gl_evidence_rows':len(glevidence),'nbs_populated_cells':len(ledger)},'findings':findings,'comparisons':comparisons,'trace':trace,'gl_evidence':list(glevidence.values()),'cell_ledger':ledger}
 (OUT/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 for n,rr in [('All_findings.csv',findings),('GL_category_comparison.csv',comparisons),('GL_sixth_segment_trace.csv',trace),('Referenced_GL_rows.csv',list(glevidence.values())),('NBS_cell_scan.csv',ledger),('Source_sheet_coverage.csv',[x for m in manifest for x in m['sheet_counts']])]:writecsv(n,rr)
 print(json.dumps(result['counts'],indent=2));print('ECB types',len(types))

if __name__=='__main__':main()
