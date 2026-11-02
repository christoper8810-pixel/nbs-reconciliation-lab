"""Read bank exports as data and retain source lineage. No workbook code runs."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import zipfile
from datetime import datetime,timedelta
from collections import Counter
from pathlib import Path
from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
FIELDS = ['source','account','arrangement','currency','country','company','category','sector','industry',
          'residency','personal','rim','product','risk','maturity','effective','gl','amount',
          'outstanding','earned','fees','unearned','suspense','components','source_row','linked_account']
NUMERIC = {'amount','outstanding','earned','fees','unearned','suspense'}

# AC CONSOL_KEY segment positions, read from config/tb_recon.json (consol_key_layouts.AC) so the layout is
# configurable and shared with the TB reconciliation. Defaults are the positions this loader always used; none of
# them is verified against the bank's CONSOLIDATE.COND record (see POSSIBLE_MAPPING_COLUMN_MISALIGNMENT).
AC_DEFAULT_POSITIONS = {'currency': 3, 'category': 4, 'sector': 6, 'residence': 8, 'industry': 9, 'company': -1}


def ac_positions(config_path=None):
    path = Path(config_path) if config_path else Path(__file__).resolve().parent.parent / 'config' / 'tb_recon.json'
    try:
        seg = json.loads(path.read_text(encoding='utf-8'))['consol_key_layouts']['AC']['segments']
        return {k: int(seg[k]['position']) for k in AC_DEFAULT_POSITIONS if k in seg} or dict(AC_DEFAULT_POSITIONS)
    except (OSError, KeyError, ValueError, TypeError):
        return dict(AC_DEFAULT_POSITIONS)


def key_segment(parts, pos, min_len=None):
    if pos < 0:
        return parts[pos] if len(parts) > (min_len or 0) else None
    return parts[pos] if len(parts) > pos else None


def code(v):
    if v is None: return ''
    if isinstance(v,float) and v.is_integer(): return str(int(v))
    return str(v).strip()

def number(v):
    if v is None or code(v) in ('','N/A','-'): return None
    try: return float(code(v).replace(',',''))
    except ValueError: return None

def date_value(v):
    if isinstance(v,(float,int)):
        return (datetime(1899,12,30)+timedelta(days=v)).date().isoformat()
    return code(v)[:10] if code(v) not in ('','N/A') else ''

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def xlsx_rows(path, sheet='xl/worksheets/sheet1.xml'):
    """Stream sparse OOXML cells; preserve numeric blanks; use cached values only."""
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                for _,el in etree.iterparse(f,events=('end',),tag=NS+'si'):
                    strings.append(''.join(el.itertext()))
                    el.clear()
                    while el.getprevious() is not None: del el.getparent()[0]
        with z.open(sheet) as f:
            for _,row in etree.iterparse(f,events=('end',),tag=NS+'row'):
                values={}
                for c in row:
                    if c.tag!=NS+'c': continue
                    coord=c.get('r'); t=c.get('t'); v=c.find(NS+'v')
                    if t=='inlineStr': value=''.join(c.find(NS+'is').itertext())
                    elif v is None or v.text is None: continue
                    elif t=='s': value=strings[int(v.text)]
                    elif t in ('str','e','b'): value=v.text
                    else:
                        try: value=float(v.text)
                        except ValueError: value=v.text
                    values[re.sub(r'\d','',coord)]=value
                yield int(row.get('r')),values
                row.clear()
                while row.getprevious() is not None: del row.getparent()[0]

def import_file(conn,path,source):
    pos=ac_positions()
    headers=None; batch=[]; n=0; duplicates=0; dates=Counter(); types=Counter(); component_counts=Counter()
    insert='INSERT INTO records ('+','.join(FIELDS)+') VALUES ('+','.join('?' for _ in FIELDS)+')'
    for row,values in xlsx_rows(path):
        if not values: continue
        if headers is None:
            if source=='TB' and 'Account No' not in values.values(): continue
            headers={col:code(v) for col,v in values.items()}
            required={
                'ECB':{'ACCOUNT_NO','ARRANGEMENT_ID','CONSOL_KEY'},
                'LOAN':{'Business_Date','Account_No','Account_Currency','Outstanding_QAR','Amortized_Earned_QAR','Loan_Fees_QAR'},
                'DEPOSIT':{'Business_Date','Account_No','iso_code','Balance_QAR'},
                'TB':{'Account No','Cur','Equiv Cur Bal'},
            }[source]
            missing=required-set(headers.values())
            if missing:raise ValueError(f'{source} workbook is missing required headers: '+', '.join(sorted(missing)))
            if source=='ECB' and not any(h.endswith('_BAL_QAR') for h in headers.values()):raise ValueError('ECB requires QAR balance columns ending _BAL_QAR')
            continue
        d={headers.get(k,k):v for k,v in values.items()}
        r={k:None for k in FIELDS};r.update(source=source,source_row=row)
        if source=='ECB':
            account=code(d.get('ACCOUNT_NO')); parts=code(d.get('CONSOL_KEY')).split('.')
            if account.lower() in ('','total','grand total'): continue
            r.update(account=account,arrangement=code(d.get('ARRANGEMENT_ID')),
                     currency=key_segment(parts,pos['currency']),category=key_segment(parts,pos['category']),
                     sector=key_segment(parts,pos['sector']),country=key_segment(parts,pos['residence']),
                     industry=key_segment(parts,pos['industry']),company=key_segment(parts,pos['company'],10))
            comp={k[:-8]:number(v) for k,v in d.items() if k.endswith('_BAL_QAR') and number(v) is not None}
            r['components']=json.dumps(comp,separators=(',',':'))
            for k,v in comp.items():
                if v: component_counts[k]+=1
            # No blanket sum: balance families can overlap. Metrics assembled in the report rules.
        elif source in ('LOAN','DEPOSIT'):
            r.update(account=code(d.get('Account_No')),currency=code(d.get('Account_Currency',d.get('iso_code'))),
                     industry=code(d.get('Sector_Code',d.get('Sic_Code'))).split(' ')[0],
                     residency=code(d.get('Residency',d.get('residency'))),personal=code(d.get('Rim_Type')),
                     rim=code(d.get('Rim_No')),product=code(d.get('Account_Type',d.get('Acct_Type'))),
                     risk=code(d.get('Risk_Rating')).split(' ')[0],maturity=date_value(d.get('Maturity_Date',d.get('Mat_Dt'))),
                     effective=date_value(d.get('Effective_Date',d.get('effective_dt'))),
                     gl=code(d.get('Gl_account',d.get('GL'))).split('-')[-1],
                     linked_account=code(d.get('CashLine_Dp_Account')))
            if source=='LOAN':
                for k,f in [('outstanding','Outstanding_QAR'),('earned','Amortized_Earned_QAR'),('fees','Loan_Fees_QAR'),
                            ('unearned','Unearned_Profit_QAR'),('suspense','Profit_In_Suspense_QAR')]:r[k]=number(d.get(f))
                r['amount']=None if any(r[k] is None for k in ('outstanding','earned','fees')) else sum(r[k] for k in ('outstanding','earned','fees'))
            else:r['amount']=number(d.get('Balance_QAR'))
            dates[date_value(d.get('Business_Date'))]+=1
            types[r['product']]+=1
        else:
            r.update(account=code(d.get('Account No')),currency=code(d.get('Cur')),
                     gl=code(d.get('Account No')).split('-')[-1],amount=number(d.get('Equiv Cur Bal')))
            if not r['gl'] or not re.fullmatch(r'\d{10}',r['gl']): continue
        if not r['account']: continue
        batch.append(tuple(r[k] for k in FIELDS)); n+=1
        if len(batch)>=10000:
            conn.executemany(insert,batch);batch=[]
            if n%50000==0:print(f'{source}: {n:,} rows imported',flush=True)
    if headers is None or n==0:raise ValueError(f'{source} workbook contains no usable detail records')
    if batch:conn.executemany(insert,batch)
    conn.commit()
    return {'path':str(Path(path).resolve()),'sha256':sha(path),'rows':n,'dates':dict(dates),
            'consol_key_positions':pos if source=='ECB' else None,
            'products':dict(types),'component_columns':[v[:-8] for v in headers.values() if v.endswith('_BAL_QAR')],
            'nonzero_components':dict(component_counts)}

def build_database(ecb,sources,output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists(): raise ValueError('Choose a new run database; existing evidence is retained')
    conn=sqlite3.connect(output)
    try:
        conn.execute('CREATE TABLE records ('+','.join(k+(' REAL' if k in NUMERIC else ' INTEGER' if k=='source_row' else ' TEXT') for k in FIELDS)+')')
        manifest={}
        for source,path in sources.items():
            if path and Path(path).exists():manifest[source]=import_file(conn,path,source)
        manifest['ECB']=import_file(conn,ecb,'ECB')
        conn.execute('CREATE INDEX account_idx ON records(source,account)')
        conn.execute('CREATE INDEX cat_idx ON records(source,category)')
        # Duplicate source IDs are excluded from all joins; never multiply account balances.
        conn.execute('CREATE TABLE duplicate_accounts AS SELECT source,account,currency,count(*) n FROM records GROUP BY source,account,currency HAVING count(*)>1')
        manifest['duplicates']=[dict(zip(('source','accounts'),r)) for r in conn.execute('SELECT source,count(*) FROM duplicate_accounts GROUP BY source')]
        conn.execute('CREATE TABLE unique_records AS SELECT r.* FROM records r WHERE NOT EXISTS (SELECT 1 FROM duplicate_accounts d WHERE d.source=r.source AND d.account=r.account AND d.currency IS r.currency)')
        conn.execute('CREATE UNIQUE INDEX unique_account_idx ON unique_records(source,account,currency)')
        enrichment={}
        for src in ('LOAN','DEPOSIT'):
            enrichment[src]=conn.execute("SELECT count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account AND (e.currency=m.currency OR e.currency IS NULL) WHERE e.source='ECB' AND m.source=?",(src,)).fetchone()[0]
        manifest['exact_account_joins']=enrichment
        conn.execute('CREATE TABLE metadata (key TEXT PRIMARY KEY,value TEXT)')
        conn.execute('INSERT INTO metadata VALUES (?,?)',('manifest',json.dumps(manifest)))
        conn.commit()
        return manifest
    finally:conn.close()

def load_manifest(database):
    with sqlite3.connect(database) as c:return json.loads(c.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()[0])
