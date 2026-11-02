import json,csv,re,zipfile,hashlib,collections
from pathlib import Path
P=Path(__file__).resolve().parent
OLD=P.parent/'cell_audit_20261021'
d=json.loads((P/'internal_review.json').read_text(encoding='utf-8'))
base=json.loads((P.parent/'systems_summary_20261022/summary_items.json').read_text(encoding='utf-8'))
c=d['counts'];ident=d['category_identity_checks']
groups=collections.defaultdict(list)
for r in ident:groups[(r['company'],re.sub(r'[-\s]','',r['internal_account_E']))].append(r)
repeated=[]
for (company,account),rr in groups.items():
 if len(rr)>1:
  for r in rr:repeated.append({**r,'group_rows':', '.join(str(x['row']) for x in rr),'explanation':'Different old full GLs share the same sixth segment and target internal account. Preserve mapping rows; investigate the consolidation and count the source balance once.'})
with (P/'Repeated_internal_accounts_investigated.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(repeated[0]));w.writeheader();w.writerows(repeated)
priority={
 'number':1,'topic':'Preserve Ehab internal account selections',
 'issue':'A category-only NBS rule can lose the internal accounts, GL prefixes and exclusions identified by Ehab. The same sixth segment can cover several departments, currencies and branches.',
 'fix':'Start with Ehab\'s sixth-segment ledger selection, including every prefix and exception. Trace it to the exact Transact internal account, company and currency, then to the NBS line and balance calculation. Show missing and additional accounts.',
 'reference':'Ehab GL rules; GL Mapping A/B/E/H/I/L; Internal_account_trace.csv'}
revised=[priority]+[{**r,'number':i+2} for i,r in enumerate(base)]
for r in revised:
 if r['topic']=='Mapping versions':
  r['issue']='QCB clearing now has different routes: foreign-currency INTERNAL rows use 18062; the QAR CUSTOMER ACCOUNT row uses 5002. A combined category list hides this distinction.'
  r['fix']='Confirm the deployed mapping and effective date. Keep the INTERNAL and CUSTOMER ACCOUNT routes separate and preserve their currency and account conditions.'
intro='Please review the following issues against the 6 October NBS mapping. Give priority to preserving the internal-account population identified by Ehab, using the sixth segment of the old GL as the starting ledger reference.'
lines=['# NBS mapping summary for Systems Limited','','22 October 2026','',intro,'','For each selected old ledger, show: Ehab selection -> exact Transact account and source balance -> NBS line and reporting split. The category alone is not enough to demonstrate that the same accounts have been captured.','','| No. | Issue | Action requested |','|---|---|---|']
for r in revised:lines.append(f'| {r["number"]}. {r["topic"]} | {r["issue"]} | {r["fix"]} |')
lines+=['','Please return the corrected mapping, a response against each item, and a rerun for 30 September 2026. Identify Finance decisions separately and keep the old and new rules with their effective dates.']
summary=P/'NBS_Systems_Limited_Summary_With_Internal_Account_Focus_22Oct2026.md';summary.write_text('\n'.join(lines),encoding='utf-8')
focus=[
 '# Internal accounts and the sixth GL segment','',
 'Priority request for Systems Limited','',
 'Please demonstrate that the NBS preserves the internal-account population selected in Ehab\'s mapping. The sixth segment is the ten-digit ledger reference, not a complete Transact account or a complete NBS rule. Retain Ehab\'s exact ledgers, prefixes, exclusions and signed deductions.','',
 '## What the focused check establishes','',
 f'- {c["ehab_rule_cells_with_current_internal_rows"]} Ehab rule cells select current INTERNAL mapping rows.',
 f'- {c["explicit_segments_found_in_coa_and_internal"]} of {c["explicit_sixth_segments_in_those_rules"]} distinct explicit ledger codes in those rules are present in the supplied COA and have current INTERNAL mapping rows. This validates identifier coverage, not every NBS classification.',
 f'- {c["explicit_segments_needing_review"]} codes require clarification. They are listed below and have not been removed.',
 f'- {c["other_t24_internal_rows"]} rows in Other T24 Account are INTERNAL and have no corresponding Ethix GL. They need a separate NBS decision; an old-ledger-only review cannot establish their treatment.',
 '- The review uses the frozen supplied GL v6 mapping and 9 September source versions recorded in the detailed audit. It does not establish what is currently deployed in the bank.', '',
 '## Specific issues and requested handling','',
 '| Issue | Evidence | Action requested |','|---|---|---|',
 '| Reserve accounts | Ehab ledgers 1003000010 and 1003000011 map to categories 18060 and 18061. Table 2 includes these, but the repeated reserve rule in Assets C64/D64/F64/G64 still says 5003/5004. | Preserve the correct detail population and align the base Assets rule to it. |',
 '| Cash population | Ehab\'s 100 prefix, excluding 1003, also selects internal petty cash and cash-in-transit categories 12903-12907. Table 1 cash specifies 10000-10025. | Confirm the intended NBS line for each additional cash category. Do not lose these accounts or automatically move them into Cash on hand without confirming the reporting classification. |',
 '| Clearing routes | Current foreign-currency INTERNAL rows for ledger 1003000020 use 18062. Its QAR CUSTOMER ACCOUNT row uses 5002. | Keep both routes distinct. Do not classify the customer-account row as an internal account or apply one broad category change to both. |',
 '| Investment properties | Ehab ledger 1700000001 maps to internal account QAR-13337-1149-1900, category 13337. Table 15 B10 says 11320. | Confirm the correct NBS property classification and correct the category/account selection. |',
 '| Intangible amortisation | Ehab ledger 2801000001 maps to 11570. Category 11550 maps to ledger 2802000001, accumulated depreciation of the main building. | Review Table 18 C16 and keep building depreciation separate from intangible amortisation unless Finance documents a different reporting requirement. |',
 '| Department changes during migration | In 3,081 INTERNAL rows, column M differs from the department encoded in the actual target account in E. Example: row 2 has M=1201 but E=AED-10011-9999-1001. | Use the actual recorded target account. Do not construct it by assuming the old/mapping department is the target department. These differences are not automatically mapping errors. |',
 '| Repeated target cash accounts | Five company/account keys have two mapping rows each. Both old GLs have sixth segment 1000000010 but different departments, 3601 and 5260, and converge on department 9999 in the target account. | Preserve both old-to-new links. Confirm the consolidation and ensure the same target balance is counted once when the NBS is calculated. |',
 '| New internal accounts | The Other T24 Account sheet contains INTERNAL rows explicitly labelled No corresponding Ethix GL. | Define their NBS treatment separately; do not exclude them just because Ehab has no sixth-segment reference. |',
 '| Internal account reporting split | An internal account may have no customer-residency attribute. | Use the approved entity/account basis for inside/outside Qatar. Do not drop it or invent customer residency. Keep the currency, source balance type and reporting sign explicit. |','',
 '## Five ledger codes requiring clarification','',
 '| Sixth segment | Ehab cells | Current supplied evidence | Requested clarification |','|---|---|---|---|']
for r in d['explicit_codes']:
 if r['result']=='ID PRESENT; INTERNAL ROW FOUND':continue
 status='Not found in the supplied COA or GL Mapping' if not r['present_in_current_coa'] and not r['present_in_gl_mapping'] else 'No INTERNAL row; classifications: '+r['other_classifications']
 focus.append(f'| {r["sixth_segment"]} | {r["ehab_cells"]} | {status} | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |')
focus+=['','## Evidence to return','',
 'For every internal-account NBS line, provide Ehab cell and ledger rule, full old GL, exact Transact account, company, currency, source balance type, reporting sign and NBS line. Show exclusions, unmapped records and new internal accounts separately. Compare the old-ledger selection with the account selection at one reporting date and explain missing or additional balances.','',
 'No source rows or mapping entries were removed. This focused review refines the earlier all-class category comparison, particularly for clearing: 5002 and 18062 belong to different account routes.']
(P/'Internal_Accounts_Sixth_Segment_Issue_and_Fix.md').write_text('\n'.join(focus),encoding='utf-8')
checks=[]
def check(n,ok):
 checks.append({'check':n,'result':'PASS' if ok else 'FAIL'})
 assert ok,n
check('All focused trace rows are INTERNAL',all(r['classification']=='INTERNAL' for r in d['internal_trace']))
check('Sixth segment always ten text digits',all(re.fullmatch(r'\d{10}',r['sixth_segment']) for r in d['internal_trace']))
check('Explicit code counts reconcile',len(d['explicit_codes'])==c['explicit_segments_found_in_coa_and_internal']+c['explicit_segments_needing_review'])
check('Current INTERNAL clearing selects only 18062',{r['category_L'] for r in ident if r['sixth_segment']=='1003000020'}=={'18062'})
check('All reserve internal rows use 18060 or 18061',{r['category_L'] for r in ident if r['sixth_segment'] in ['1003000010','1003000011']}=={'18060','18061'})
check('Internal account category matches every comparable numeric category field',not any(r['result']=='CATEGORY FIELD DIFFERS FROM INTERNAL ACCOUNT' for r in ident))
check('Department example preserves distinct field meanings',any(r['row']==2 and r['department_column_M']=='1201' and r['internal_account_department']=='9999' for r in ident))
check('Five repeated keys investigated without row removal',sum(len(v)>1 for v in groups.values())==5 and len(repeated)==10 and len(ident)==8170)
check('Five code exceptions listed without removal',c['explicit_segments_needing_review']==5)
check('All 897 Other T24 INTERNAL rows retained',len(d['other_t24_internal'])==897)
manifest=json.loads((OLD/'source_manifest.json').read_text(encoding='utf-8'))
for s in manifest:
 with Path(s['path']).open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 check('Original unchanged '+s['label'],digest==s['sha256'])
(P/'focus_validation.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2),encoding='utf-8')
names=[summary.name,'Internal_Accounts_Sixth_Segment_Issue_and_Fix.md','Ehab_internal_rule_summary.csv','Ehab_sixth_segment_validation.csv','Internal_account_trace.csv','Internal_account_identity_checks.csv','Repeated_internal_accounts_investigated.csv','New_internal_accounts_without_Ehab_GL.csv','focus_validation.json']
with zipfile.ZipFile(P/'NBS_Internal_Account_Review_for_Systems_Limited_22Oct2026.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:z.write(P/n,n)
print(json.dumps({'summary_items':len(revised),'focused_validation_checks':len(checks),'repeated_mapping_rows_retained':len(repeated),'pack_bytes':(P/'NBS_Internal_Account_Review_for_Systems_Limited_22Oct2026.zip').stat().st_size}))
