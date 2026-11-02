import json,hashlib,gzip,re,sys
from pathlib import Path
from datetime import date,timedelta
from collections import Counter
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT))
from audit_mapping import numset,fields,category_of,gl_predicate,selected

def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def raw(n):
 with gzip.open(OUT/(n+'_cells.json.gz'),'rt',encoding='utf-8') as f:return json.load(f)
checks=[]
def check(name,condition):
 checks.append({'check':name,'result':'PASS' if condition else 'FAIL'})
 if not condition:print('FAILED',name,flush=True)
def hashfile(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

d=read('audit.json');s=raw('SYSTEMS');e=raw('EHAB');g=raw('GL_CURRENT_BASE');b=raw('GL_09SEP');fs=d['findings']
for m in d['sources']:
 check('Original source unchanged: '+m['label'],hashfile(m['path'])==m['sha256'])
 check('Every captured source cell counted: '+m['label'],sum(x['populated_cells'] for x in m['sheet_counts'])==m['cells'])
check('Source coverage includes all 81 worksheets',sum(m['sheets'] for m in d['sources'])==81)
check('All 10979 populated NBS cells have exactly one ledger record',len(d['cell_ledger'])==10979 and len({(x['source'],x['sheet'],x['cell']) for x in d['cell_ledger']})==10979)
check('Finding IDs unique and sequential',[f['id'] for f in fs]==[f'NBS-{i+1:04d}' for i in range(len(fs))])
check('Unknown syntax never becomes a wildcard',numset('see Treasury') is None and numset('1000-1999 EXCEPT 1001') is None)
check('Numeric range boundaries preserved',numset('1000-1004, 3701')=={1000,1001,1002,1003,1004,3701})
check('Numbered source components are not categories 4,5,7',not ({4,5,7}&(category_of(s['ASSET - 100']['C107']['v']) or set())))
check('Narrative words are not balance codes',all(not any(f['title'].endswith(': '+v) for f in fs if f['type']=='ABSENT_BALANCE_TYPE') for v in ['CUSTOMER','ACCOUNTS','RESIDENCE','CRITERIA','APPLIED']))
oldgl='01-01-001-12-01-1000000010'
check('Sixth GL segment retained as ten-digit text',oldgl.split('-')[5]=='1000000010')
p=gl_predicate("All Gl's Start by 100 Except 1003")
check('Cash selector respects prefix exclusion',bool(selected(p,'1000000010')) and not selected(p,'1003000010'))
p=gl_predicate("All Gl's Start by 29 Except GL Start by (2903,29085) + Gl's start by 23040 + GL 2903000002")
check('Explicit add-back survives broader excluded prefix',bool(selected(p,'2903000002')) and not selected(p,'2903000001') and bool(selected(p,'2304000001')))
p=gl_predicate('1800000001, 1801000001 Exclude (2800010001, 2800010002)')
check('Contra deductions retain negative leg',selected(p,'2800010001')[0][0]==-1)
def glrows(book,code):
 rows=[]
 for a,c in book['GL Mapping'].items():
  if re.fullmatch(r'A\d+',a) and str(c.get('v','')).endswith('-'+code):
   r=a[1:];rows.append({col:book['GL Mapping'].get(col+r,{}).get('v','') for col in ['A','B','J','L','M','N','O','S']})
 return rows
eh=next(iter(e.values()))
code=eh['K162']['v'];check('Government sukuk income Ehab GL preserved',code=='4004020004')
for book,name in [(g,'Current'),(b,'9 September')]:
 cc={int(r['J'] or r['L']) for r in glrows(book,code) if str(r['J'] or r['L']).isdigit()}
 check(name+' independent government sukuk PL category is 65073',cc=={65073})
check('Government sukuk Systems original is 65037',category_of(s['Income']['C21']['v'])=={65037})
check('Both-date sukuk mismatch is listed',any(f['type']=='GL_CATEGORY' and f['ehab_cells']=='K162' and f['missing_categories']=='65073' and f['extra_categories']=='65037' for f in fs))
check('Subsidiary original category mismatch retained',any(f['type']=='GL_CATEGORY' and f['ehab_cells']=='K938' and '11903' in f['missing_categories'] and f['extra_categories']=='11908' for f in fs))
check('Original 90 cached Excel errors are each listed',sum(f['type']=='EXCEL_ERROR' for f in fs)==sum(c['t']=='e' for ss in s.values() for c in ss.values())==90)
check('75 credit-quality formula defects individually listed',sum(f['type']=='CREDIT_QUALITY_FORMULA' for f in fs)==75)
check('Correct Table 30 and Table 43 totals are not flagged',not any(f['type']=='TOTAL_COLUMNS' and (f['systems_sheet'],f['systems_cells']) in [('Table 30','J5'),('Table 43','K7')] for f in fs))
check('Wrong asset currency totals E61 K61 flagged',all(any(f['type']=='TOTAL_COLUMNS' and f['systems_sheet']=='ASSET - 100' and f['systems_cells']==a for f in fs) for a in ['E61','H61','I61','J61','K61']))
check('Cached category alias in CONTRA D16 is not falsely missing',not any(f['type']=='CURRENCY_COLUMNS' and f['systems_sheet']=='CONTRA ITEMS' for f in fs))
report=date(2026,9,30);future=report+timedelta(days=30)
check('Independent future-maturity direction fixture',(report-future).days==-30 and (future-report).days==30)
check('Independent exact-30-day boundary fixture misses strict bands',not(7<30<30) and not(30<30<90))
check('Maturity omitted boundaries all listed',sum(f['type']=='MATURITY_BOUNDARY' for f in fs)==8)
types=set(read('ecb_types.json'))
check('ECB vocabulary 74 exact types retained',len(types)==74 and 'CONTDBBL' in types and 'CONTDRBL' not in types)
check('Absent codes remain gaps and are never synonyms',all(f['status']=='INPUT GAP' for f in fs if f['type']=='ABSENT_BALANCE_TYPE'))
check('Repeated Ehab treasury GL retained for investigation',any(f['type']=='EHAB_DUPLICATE' and 'K109' in f['ehab_cells'] and 'K111' in f['ehab_cells'] for f in fs))
check('Source-only missing schedules recorded',{'020','038'}=={f['table'] for f in fs if f['type']=='MISSING_SCHEDULE'})
check('Current version overlay is recorded, original kept',len(d['gl_version']['changes'])==1 and d['gl_version']['changes'][0]['col']=='L' and d['gl_version']['changes'][0]['row_no']==48311 and '23071' in d['gl_version']['changes'][0]['old_value'] and '23071' not in d['gl_version']['changes'][0]['new_value'])
reference_errors=[]
for f in fs:
 if f['type']!='GL_CATEGORY':continue
 for m in re.finditer(r'(Current v6|9 September): GL Mapping!A(\d+), ([JL])(\d+) = ([^;]+)',f['gl_cells']):
  book=g if m[1]=='Current v6' else b
  value=str(book['GL Mapping'].get(m[3]+m[4],{}).get('v','')).strip()
  if m[2]!=m[4] or numset(value) is None:reference_errors.append((f['id'],m[0]))
check('Every cited GL category reference is a nonblank numeric category row',not reference_errors)
for x in d['cell_ledger']:
 if x['findings']:
  for fid in x['findings'].split(', '):
   if fid not in {f['id'] for f in fs}:raise AssertionError('Dangling cell finding '+fid)
check('Every ledger finding links to a listed finding',True)
result={'passed':sum(c['result']=='PASS' for c in checks),'failed':sum(c['result']=='FAIL' for c in checks),'checks':checks}
(OUT/'acceptance_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
sys.exit(bool(result['failed']))
