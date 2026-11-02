import json,sqlite3
from pathlib import Path
c=sqlite3.connect('data/bank_20260930.sqlite');c.row_factory=sqlite3.Row
groups={};samples={}
for r in c.execute("SELECT e.account,e.components,l.product,l.amount,l.fees,l.linked_account,l.currency FROM unique_records e JOIN unique_records l ON l.source='LOAN' AND l.account=e.account AND l.currency=e.currency WHERE e.source='ECB' AND l.product IN ('RCM','CLM')"):
    comp=json.loads(r['components']);p=r['product'];value=None
    if p=='RCM':
        principal=-sum(comp.get(t,0) for t in ['CURACCOUNT','PREACCOUNT','GRCACCOUNT','DELACCOUNT','DUEACCOUNT','NABACCOUNT'])
        profit=-comp.get('RECDEFERREDPFT',0)-comp.get('ACCDEFERREDPFT',0)
        value=principal+profit+(r['fees'] or 0)
    else:
        ch=c.execute("SELECT components FROM unique_records WHERE source='ECB' AND account=? AND currency=? AND category='6050'",(r['linked_account'],r['currency'])).fetchone()
        if not ch:continue
        child=json.loads(ch[0]);value=-sum(comp.get(t,0) for t in ['CURACCOUNT','PREACCOUNT','GRCACCOUNT','DELACCOUNT','DUEACCOUNT','NABACCOUNT'])-child.get('CREDIT',0)-sum(comp.get(t,0) for t in ['ACCPRINCIPALPFT','RECPRINCIPALPFT','GRCPRINCIPALPFT','DELPRINCIPALPFT','PREPRINCIPALPFT'])-child.get('ACCCRPROFIT',0)+(r['fees'] or 0)
    diff=value-r['amount'];g=groups.setdefault(p,{'accounts':0,'within_1_QAR':0,'difference_QAR':0,'max_absolute_difference':0})
    g['accounts']+=1;g['within_1_QAR']+=abs(diff)<=1;g['difference_QAR']+=diff;g['max_absolute_difference']=max(g['max_absolute_difference'],abs(diff))
    if abs(diff)>1:samples.setdefault(p,[]).append({'account':r['account'],'difference_QAR':diff})
out={'groups':groups,'exceptions':samples}
Path('data/candidate_policy_evaluation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
