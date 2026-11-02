import json
from nbs_control.service import ControlService
from nbs_control.reconciliation import evaluate_accounts
r=evaluate_accounts('data/bank_20260930.sqlite',ControlService().config['balance_rules'],'exports',product_policies=json.load(open('config/report_product_policies.json')))
print(json.dumps(r,indent=2))
