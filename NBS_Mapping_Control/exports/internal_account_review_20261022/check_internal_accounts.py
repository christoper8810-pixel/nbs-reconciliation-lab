"""Read-only focus on old GL segment 6 and mapped INTERNAL accounts."""
import sys,json,gzip,re,csv,collections,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;OLD=P.parent/'cell_audit_20261021'
sys.path.insert(0,str(OLD))
from audit_mapping import gl_predicate,selected,numset,compact

def read(n):
 with gzip.open(OLD/(n+'_cells.json.gz'),'rt',encoding='utf-8') as f:return json.load(f)
def rows(book,sheet):
 out=collections.defaultdict(dict)
 for a,c in book.get(sheet,{}).items():out[int(re.sub(r'\D','',a))][re.sub(r'\d','',a)]=str(c.get('v') or '').strip()
 return dict(out)
def seg(gl):
 pp=gl.split('-')
 return pp[5] if len(pp)==6 and re.fullmatch(r'\d{10}',pp[5]) else None
def write(n,data):
 if not data:return
 heads=list(dict.fromkeys(k for r in data for k in r))
 with (P/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=heads);w.writeheader();w.writerows(data)

d=json.loads((OLD/'audit.json').read_text(encoding='utf-8'))
books={'Current v6':read('GL_CURRENT_BASE'),'9 September':read('GL_09SEP')}
rs={v:rows(b,'GL Mapping') for v,b in books.items()}
for c in d['gl_version']['changes']:
 rs['Current v6'].setdefault(c['row_no'],{})[c['col']]=c['new_value']
coa=rows(books['Current v6'],'COA');coacodes={r['G'] for r in coa.values() if re.fullmatch(r'\d{10}',r.get('G',''))}
internal={v:{n:r for n,r in rr.items() if r.get('H','').upper()=='INTERNAL'} for v,rr in rs.items()}
rules={x['ehab_cell']:{k:x[k] for k in ['ehab_cell','description','table','rule_text']} for x in d['trace'] if x['version']=='Current v6' and x['classification']=='INTERNAL'}
allcode=collections.defaultdict(list)
for n,r in rs['Current v6'].items():
 if seg(r.get('A','')):allcode[seg(r['A'])].append((n,r))
exact=collections.defaultdict(set);trace=[];summaries=[];categorychecks=[];accountgroups=collections.defaultdict(list)
for cell,spec in sorted(rules.items()):
 pred=gl_predicate(spec['rule_text']);assert pred is not None
 for sign,code in pred['terms']:
  if len(code)==10:exact[code].add(cell)
 for ver,rr in internal.items():
  grouped=collections.defaultdict(list);cats=set()
  for n,r in rr.items():
   code=seg(r.get('A',''))
   if not code or not selected(pred,code):continue
   cats|=numset(r.get('L')) or set()
   key=(code,r.get('A',''),r.get('B',''),r.get('I',''),r.get('E',''),r.get('L',''),r.get('M',''),r.get('S',''),r.get('P',''))
   grouped[key].append(n)
  for k,nn in grouped.items():trace.append({'ehab_cell':cell,'nbs_line':spec['description'],'schedule':spec['table'],'ehab_original_rule':spec['rule_text'],'gl_version':ver,'sixth_segment':k[0],'full_old_gl':k[1],'currency':k[2],'company':k[3],'transact_internal_account':k[4],'category_field':k[5],'department_column_M':k[6],'balance_type':k[7],'residence':k[8],'source_rows':', '.join(map(str,nn)),'classification':'INTERNAL','ehab_signed_legs':str(selected(pred,k[0])),'scope':'Mapping definition only; no balance or full NBS validation.'})
  summaries.append({'ehab_cell':cell,'description':spec['description'],'version':ver,'sixth_segments':len({k[0] for k in grouped}),'internal_mapping_rows':sum(len(nn) for nn in grouped.values()),'exact_internal_accounts':len({(k[3],k[4]) for k in grouped if k[4]}),'category_field_union':compact(cats),'scope':'INTERNAL only. Excludes CUSTOMER ACCOUNT, CLOSED and NOT TO BE MAPPED. Blank/range categories retained in the trace.'})
checks=[]
for code,cells in sorted(exact.items()):
 matches=allcode.get(code,[]);ir=[(n,r) for n,r in matches if r.get('H','').upper()=='INTERNAL']
 checks.append({'sixth_segment':code,'ehab_cells':', '.join(sorted(cells)),'present_in_current_coa':code in coacodes,'present_in_gl_mapping':bool(matches),'current_internal_rows':len(ir),'other_classifications':', '.join(sorted({r.get('H','') for n,r in matches if r.get('H','').upper()!='INTERNAL'})),'internal_categories':compact(set.union(*(numset(r.get('L')) or set() for n,r in ir))) if ir else '', 'result':'ID PRESENT; INTERNAL ROW FOUND' if code in coacodes and ir else 'REVIEW SOURCE COVERAGE','limits':'Presence confirms the identifier and mapping route, not the approved regulatory meaning of the report line.'})
norm=lambda a:re.sub(r'[^A-Z0-9]','',str(a).upper())
pattern=re.compile(r'([A-Z]{3}(?:[A-Z]{3})?)(\d{5})(\d{4})(\d{4})$')
for n,r in internal['Current v6'].items():
 acct=norm(r.get('E',''));m=pattern.fullmatch(acct)
 if acct:accountgroups[(r.get('I',''),acct)].append((n,r))
 if not m:status='MISSING OR UNPARSED INTERNAL ACCOUNT'
 elif re.fullmatch(r'\d+',r.get('L','')) and int(m[2])!=int(r['L']):status='CATEGORY FIELD DIFFERS FROM INTERNAL ACCOUNT'
 else:status='NO STRICT CATEGORY CONTRADICTION'
 categorychecks.append({'row':n,'old_gl':r.get('A',''),'sixth_segment':seg(r.get('A','')) or '', 'currency':r.get('B',''),'company':r.get('I',''),'internal_account_E':r.get('E',''),'category_L':r.get('L',''),'internal_account_category':m[2] if m else '', 'department_column_M':r.get('M',''),'internal_account_department':m[3] if m else '', 'internal_account_branch':m[4] if m else '', 'result':status,'scope':'Exact INTERNAL rows only. Column M is retained separately from the department encoded in column E.'})
shared=[]
for (company,acct),nn in accountgroups.items():
 codes={seg(r.get('A','')) for n,r in nn if seg(r.get('A',''))}
 if len(codes)>1:shared.append({'company':company,'internal_account':acct,'old_sixth_segments':', '.join(sorted(codes)),'source_rows':', '.join(str(n) for n,r in nn),'required_handling':'Investigate whether the old GLs are meant to share one NBS line. Do not add the same T24 account balance once per old GL.'})
new=[]
for n,r in rows(books['Current v6'],'Other T24 Account').items():
 if r.get('H','').upper()=='INTERNAL':new.append({'source_sheet':'Other T24 Account','source_row':n,'old_gl_note':r.get('A',''),'description':r.get('C',''),'internal_account':r.get('E',''),'currency':r.get('B',''),'company':r.get('I',''),'category':r.get('L',''),'department_column_M':r.get('M',''),'review':'Requires a separate NBS decision when no old Ethix sixth segment exists.'})
counts={'ehab_rule_cells_with_current_internal_rows':len(rules),'explicit_sixth_segments_in_those_rules':len(checks),'explicit_segments_found_in_coa_and_internal':sum(x['result']=='ID PRESENT; INTERNAL ROW FOUND' for x in checks),'explicit_segments_needing_review':sum(x['result']!='ID PRESENT; INTERNAL ROW FOUND' for x in checks),'current_internal_mapping_rows':len(internal['Current v6']),'focused_trace_groups_both_versions':len(trace),'shared_internal_accounts_multiple_old_segments':len(shared),'other_t24_internal_rows':len(new),'category_identity_results':dict(collections.Counter(x['result'] for x in categorychecks))}
result={'scope':'Read-only internal account and sixth-segment focus, 22 October 2026. Uses the 21 October frozen source hashes and recorded v6 overlay.','counts':counts,'rules':summaries,'explicit_codes':checks,'internal_trace':trace,'category_identity_checks':categorychecks,'shared_accounts':shared,'other_t24_internal':new}
(P/'internal_review.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
for name,arr in [('Ehab_internal_rule_summary.csv',summaries),('Ehab_sixth_segment_validation.csv',checks),('Internal_account_trace.csv',trace),('Internal_account_identity_checks.csv',categorychecks),('Shared_internal_accounts_investigate.csv',shared),('New_internal_accounts_without_Ehab_GL.csv',new)]:write(name,arr)
assert all(x['classification']=='INTERNAL' for x in trace)
assert all(len(x['sixth_segment'])==10 for x in trace)
assert {'18062'}=={x['category_L'] for x in categorychecks if x['sixth_segment']=='1003000020'}
assert all('5002' not in x['category_field_union'] for x in summaries if x['ehab_cell']=='L380' and x['version']=='Current v6')
assert any(x['sixth_segment']=='1003000020' and x['currency']=='EUR' and x['internal_account_E']=='EUR-18062-1901-1900' for x in categorychecks)
assert any(x['sixth_segment']=='1700000001' and x['category_L']=='13337' for x in categorychecks)
assert len(checks)==len({x['sixth_segment'] for x in checks})
print(json.dumps(counts,indent=2))
print('EXPLICIT REVIEW',[x for x in checks if x['result']!='ID PRESENT; INTERNAL ROW FOUND'])
print('CATEGORY CONTRADICTIONS',[x for x in categorychecks if x['result']=='CATEGORY FIELD DIFFERS FROM INTERNAL ACCOUNT'][:12])
