from pathlib import Path
import json
from nbs_control.bank_data import build_database
p=Path('data/bank_sources')
out=build_database(Path(r'C:\Users\Test\Downloads\ECB_BALANCE Asset type wise (30.09.2026).xlsx'),
    {'LOAN':p/'All Loan 30.09.2026.xlsx','DEPOSIT':p/'All Deposit 30.09.2026..xlsx','TB':p/'Historical_Trial_Balance  30.09.2026..xlsx'},
    'data/bank_20260930.sqlite')
Path('data/bank_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
