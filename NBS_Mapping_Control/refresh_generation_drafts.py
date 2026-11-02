import json
from pathlib import Path
from nbs_control.generation import read_template
from nbs_control.report_mapping import draft_rules
from nbs_control.service import ControlService
p=Path('config/generation_rules.json')
old=json.loads(p.read_text(encoding='utf-8'))
draft=draft_rules(ControlService().catalog,read_template('data/bank_sources/NBS01 Sep 2026 English.xlsx'))
old['rules']=draft['rules']
p.write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
print(len(old['rules']))
