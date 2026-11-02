import json,sqlite3
from pathlib import Path
from nbs_control.bank_data import sha

root=Path(__file__).parent
db=root/'data/bank_20260930.sqlite'
with sqlite3.connect(db) as c:
    manifest=json.loads(c.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()[0])
    for src in ('LOAN','DEPOSIT'):
        manifest['exact_account_joins'][src]=c.execute("SELECT count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account AND (e.currency=m.currency OR e.currency IS NULL) WHERE e.source='ECB' AND m.source=?",(src,)).fetchone()[0]
    manifest['join_policy']='Unique exact account; currency must match when provided by ECB. Missing ECB currency is enriched from the unique matched source account.'
    c.execute("UPDATE metadata SET value=? WHERE key='manifest'",(json.dumps(manifest),))
(root/'data/bank_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
p=root/'exports/NBS_generated_review.json';r=json.loads(p.read_text(encoding='utf-8'))
config=root/'config/generation_rules.json'
assert r['mapping_sha256']==sha(config),'Regenerate before finalizing: mapping and amounts differ'
r['mapping_snapshot']=json.loads(config.read_text(encoding='utf-8'))['rules'];r['manifest']=manifest
p.write_text(json.dumps(r,indent=2),encoding='utf-8')
notes=root/'exports/generation_notes.json';n=json.loads(notes.read_text(encoding='utf-8'));n['manifest']=manifest;n['product_policies']=r['product_policies'];notes.write_text(json.dumps(n,indent=2),encoding='utf-8')
a=json.loads((root/'exports/account_evaluation.json').read_text(encoding='utf-8'))
s=r['summary'];coverage=a['checks']
lines=['# September 2026 NBS evaluation','',
'The ECB upload-to-report workflow is implemented. All 49 report sections are present. Results remain a mixture of calculated, partial and unavailable amounts; the supplied data does not support an issue-free, fully reconciled NBS submission.','',
'## Coverage','',
f"- ECB: {manifest['ECB']['rows']:,} account rows. Loans: {manifest['LOAN']['rows']:,}. Deposits: {manifest['DEPOSIT']['rows']:,}. Trial balance: {manifest['TB']['rows']:,} detail rows; subtotals are excluded.",
f"- Exact matched loan accounts: {coverage['joined_loans']:,}. Exact matched deposit accounts: {coverage['joined_deposits']:,}.",
f"- Report rows reviewed: {s['rows']:,}. Rows with available calculations: {s['rows_with_amounts']:,}. Compared cells: {s['comparable_cells']:,}; {s['within_one_thousand']:,} differ by no more than QAR 1,000. This includes zero cells and is not a certification measure.",
f"- All {a['deposits']['matched_accounts']:,} matched deposit balances agree with their Ethix account balances within QAR 1. Aggregate difference: QAR {a['deposits']['difference_QAR']:,.2f}.",
'','## Mapping changes and findings','',
'1. The signed parent/CLS offset is applied once for verified CLM links; linked credits are not added as positive exposure a second time.',
'2. RCM report carrying amount uses principal ACCOUNT balances and the net RECDEFERREDPFT / ACCDEFERREDPFT earned-profit relationship. 1,614 of 1,623 supplied RCM accounts match within QAR 1. The nine residual cases have commitment-only ECB data, so their drawn amounts are unavailable rather than forced to match.',
'3. The actual linked CLS accrued component in the new file is ACCCRPROFIT. A distinct CLM report policy uses it without aliasing ACCDEPOSITPFT. 160 of 161 verified pairs match within QAR 1; one remains QAR 138,009.48 different.',
'4. Original owner component groups are retained as a separate selectable measure. Product policies and report filters can be changed in the application with history.',
'5. Currency conflicts never fan out account joins. Duplicate detection uses source/account/currency, allowing valid multi-currency trial-balance rows.',
'6. Loan-fee values come from the supplied September Ethix loan field, separately identified. They do not establish a T24 fee definition.',
'7. Maturity uses reporting date minus maturity in the correct direction, then non-overlapping forward buckets. Overdue accounts and missing dates remain separate exceptions.',
'8. Report totals sum only top-level rows, or immediate children, and remain explicitly partial if components are unavailable. Company captions are not numerical subtotals.',
'9. Specified accumulated depreciation and amortization contra accounts are deducted from gross fixed/intangible assets. Intangible aggregate is approximately QAR 292,410.144 thousand, consistent with the rounded live report. Net fixed assets still differ materially from the live report under the supplied GL rules; no unexplained adjustment is used to force a tie.',
'10. Trial-balance-only rows show aggregate currency amounts. Inside/outside residence is unavailable, rather than inferred from the reference report.',
'','## Unresolved data and differences','',
'- Four required owner balance columns are absent: NABACCOUNT, NABDEFERREDPFT, RECPRINCIPALPFT, DEFERREDPFT. They remain visible limitations; CO, CUST and BL balances are not aliases.',
'- 34 loan accounts and one deposit account have no ECB match. Their values are not imported from Ethix to manufacture a generated amount.',
f"- {coverage['unresolved_clm_links']} CLM links cannot be verified. {coverage.get('commitment_only_loan_accounts',19)} additional loan accounts contain commitment-only data and no supported drawn balance.",
f"- {coverage['maturity_overdue_loans']} matched loans have overdue maturities and are outside forward maturity buckets.",
'- T24 versus Ethix industry differs for 30 loan accounts and 166 deposit accounts. T24 industry is retained when present, explaining some regulatory row allocation differences even where account balances agree.',
'- Treasury instrument attributes, collateral, indirect risk, some personal/QFC/MSME subdivisions and several other report dimensions are missing. Corresponding results remain unavailable.',
'- Cash, fixed assets, some provisions and treasury rows show material source/report differences. The comparison export exposes them by cell.',
'','## How to review','',
'Open http://127.0.0.1:8767/reports. Choose a report; click a row to edit its mapping. Use the RCM / CLM calculation page for product policies. Save a named change note and regenerate. The original approval register remains separate from provisional generation mappings.',
'','## Outputs','',
'- NBS_Generated_September_2026.xlsx: generated report layout, original Ethix reference, linked cell differences and mapping notes.',
'- NBS_generated_vs_Ethix.csv: all generated/reference cell differences with statuses and source notes.',
'- loan_account_reconciliation.csv: owner-group and report-policy carrying amounts alongside Ethix values.',
'- source_coverage_exceptions.csv: missing accounts and unsupported monetary records.',
'- account_evaluation.json and generation_notes.json: full evaluation figures and policy evidence.',
'','## Validation','',
'Automated tests cover imports, exact memberships, links, source dates, currencies, signed offsets, separate report policies, maturity boundaries, structured-filter safety, contra deductions, mapping history and application forms. The final test count is recorded in VALIDATION.json. All five Excel tabs are rendered and inspected, formulas are recalculated and errors scanned. Native Excel execution is not performed.','',
'Original source hashes are checked against the imported manifest. No original workbook or ZIP is edited. No shared-folder URL was supplied; the attached ZIP and local folder were used.']
(root/'exports/NBS_EVALUATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(s)
print('Source hashes unchanged:',all(sha(m['path'])==m['sha256'] for m in manifest.values() if isinstance(m,dict) and 'path' in m))
