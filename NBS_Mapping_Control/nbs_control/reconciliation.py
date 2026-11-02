"""Independent account-to-account evaluation and coverage exceptions."""
import csv,json,sqlite3
from contextlib import closing
from pathlib import Path
from .bank_data import load_manifest
from .generation import prepare_facts

def evaluate_accounts(database,balance_rules,output_dir,as_of='2026-09-30',product_policies=None):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    with closing(sqlite3.connect(database)) as c:
        c.row_factory=sqlite3.Row
        checks=prepare_facts(c,balance_rules,load_manifest(database),as_of,product_policies)
        sql="""SELECT f.account,f.arrangement,f.currency,f.category,f.product,f.linked_account,f.unavailable,
            f.outstanding generated_outstanding,f.earned generated_earned,f.fees ethix_fees,f.carrying owner_carrying,f.ethix_carrying generated_carrying,
            l.outstanding ethix_outstanding,l.earned ethix_earned,l.amount ethix_carrying,
            f.ethix_carrying-l.amount difference_QAR, f.source_row ecb_row,l.source_row loan_row
            FROM facts f JOIN unique_records l ON l.source='LOAN' AND l.account=f.account AND l.currency=f.currency
            WHERE f.source='ECB_LOAN' ORDER BY abs(f.ethix_carrying-l.amount) DESC"""
        rows=[dict(r) for r in c.execute(sql)]
        for r in rows:
            if r['unavailable']:
                r['generated_outstanding']=r['generated_earned']=r['generated_carrying']=r['difference_QAR']=None
        with (output_dir/'loan_account_reconciliation.csv').open('w',newline='',encoding='utf-8-sig') as f:
            if rows:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        groups={}
        for r in rows:
            key=(r['product'],r['currency']);g=groups.setdefault(key,{'product':key[0],'currency':key[1],'accounts':0,'unavailable':0,'generated_carrying_QAR':0,'ethix_carrying_QAR_matched':0,'difference_QAR':0,'within_1_QAR':0})
            g['accounts']+=1
            if r['unavailable']:g['unavailable']+=1;continue
            g['generated_carrying_QAR']+=r['generated_carrying'] or 0;g['ethix_carrying_QAR_matched']+=r['ethix_carrying'] or 0
            g['difference_QAR']+=(r['difference_QAR'] or 0);g['within_1_QAR']+=abs(r['difference_QAR'] or 0)<=1
        grouped=sorted(groups.values(),key=lambda g:abs(g['difference_QAR']),reverse=True)
        unmatched=[]
        for src in ('LOAN','DEPOSIT'):
            for r in c.execute("""SELECT m.source,m.account,m.currency,m.product,m.source_row,m.amount,
                    'NO_ECB_ACCOUNT' reason FROM unique_records m WHERE m.source=? AND NOT EXISTS
                    (SELECT 1 FROM unique_records e WHERE e.source='ECB' AND e.account=m.account)""",(src,)):
                unmatched.append(dict(r))
        for r in c.execute("SELECT source,account,currency,product,source_row,reference amount,'UNVERIFIED_CLM_LINK' reason FROM facts WHERE source='ECB_LOAN' AND unavailable=1"):
            unmatched.append(dict(r))
        for r in unmatched:
            if r['reason']=='UNVERIFIED_CLM_LINK' and r['product']!='CLM':r['reason']='COMMITMENT_ONLY_NO_DRAWN_BALANCE'
        with (output_dir/'source_coverage_exceptions.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=['source','account','currency','product','source_row','amount','reason']);w.writeheader();w.writerows(unmatched)
        deposit=c.execute("SELECT count(*),sum(deposit),sum(reference),sum(deposit-reference),sum(CASE WHEN abs(deposit-reference)<=1 THEN 1 ELSE 0 END) FROM facts WHERE source='ECB_DEPOSIT'").fetchone()
        clm=c.execute("SELECT count(*),sum(CASE WHEN abs(ethix_carrying-reference)<=1 THEN 1 ELSE 0 END),sum(ethix_carrying-reference) FROM facts WHERE source='ECB_LOAN' AND product='CLM' AND unavailable=0").fetchone()
        result={'checks':checks,'loan_comparison_by_product':grouped,
                'deposits':dict(zip(['matched_accounts','ECB_net_QAR','Ethix_balance_QAR','difference_QAR','within_1_QAR'],deposit)),
                'verified_clm_comparison':dict(zip(['accounts','within_1_QAR','difference_QAR'],clm)),
                'unmatched_source_accounts':dict(c.execute("SELECT m.source,count(*) FROM unique_records m WHERE m.source IN ('LOAN','DEPOSIT') AND NOT EXISTS (SELECT 1 FROM unique_records e WHERE e.source='ECB' AND e.account=m.account) GROUP BY m.source")),
                'basis':'Per-account ECB owner component sum, CLM signed offsets, and dated Ethix fees; missing columns remain unresolved, not aliases.'}
        (output_dir/'account_evaluation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        return result
