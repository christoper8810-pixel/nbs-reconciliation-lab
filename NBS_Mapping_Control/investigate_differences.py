import sqlite3,json
from pathlib import Path
c=sqlite3.connect('data/bank_20260930.sqlite');c.row_factory=sqlite3.Row
loan={r['account']:dict(r) for r in c.execute("SELECT * FROM unique_records WHERE source='LOAN'")}
diffs=list(csv for csv in __import__('csv').DictReader(open('exports/loan_account_reconciliation.csv',encoding='utf-8-sig')) if csv['difference_QAR'] and abs(float(csv['difference_QAR']))>1)
out=[];rcm=[]
for row in diffs:
    a=row['account'];e=dict(c.execute("SELECT * FROM unique_records WHERE source='ECB' AND account=?",(a,)).fetchone());comp=json.loads(e['components']);ch=None
    if row['linked_account']:
        found=c.execute("SELECT * FROM unique_records WHERE source='ECB' AND account=?",(row['linked_account'],)).fetchone()
        if found:ch=json.loads(found['components'])
    if row['product']=='RCM':
        rec=comp.get('RECDEFERREDPFT',0);rcm.append({'account':a,'difference':float(row['difference_QAR']),'RECDEFERREDPFT':rec,'after_exclusion':float(row['difference_QAR'])+rec})
    if len(out)<20 or (row['product']=='CLM' and sum(x['product']=='CLM' for x in out)<4):
        out.append({'account':a,'product':row['product'],'difference':row['difference_QAR'],'ecb':comp,'child_ecb':ch,'ethix_outstanding':row['ethix_outstanding'],'ethix_earned':row['ethix_earned'],'generated_earned':row['generated_earned']})
r={'largest_differences':out,'RCM_exclusion_test':{'accounts':len(rcm),'within_1_QAR':sum(abs(x['after_exclusion'])<=1 for x in rcm),'remaining_difference':sum(x['after_exclusion'] for x in rcm),'samples':rcm[:5]}}
Path('data/difference_investigation.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r,indent=2))
