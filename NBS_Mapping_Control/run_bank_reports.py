from pathlib import Path
import json
from nbs_control.service import ControlService
from nbs_control.generation import initialize_rules,generate

s=ControlService();template=Path('data/bank_sources/NBS01 Sep 2026 English.xlsx')
config=Path('config/generation_rules.json')
initialize_rules(s,template,config)
r=generate('data/bank_20260930.sqlite',template,config,s.config['balance_rules'],'exports')
print(json.dumps(r['summary'],indent=2),flush=True)
print(json.dumps(r['checks'],indent=2),flush=True)
for row in [5,13,33,35,37,40,41,76,77,79,80,82,83,358,676,677,679]:
    x=next((v for v in r['rows'] if v['row']==row),None)
    if x:print(row,x['status'],x['values'].get('J'),x['reference'].get('J'),x['source'],x['issues'][:2],flush=True)
