"""Original Temenos cell evidence and current NBS logic, kept separately and linked by item code.

This review never changes original workbook cells or silently activates proposed mappings.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from . import logic_text as lt, target_mappings as tm

REVIEW_DIR = 'exports/temenos_review_20261020'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def hash_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def original_rows(target, rules, by_id):
    """Resolve only the recorded catalogue links; never join on row positions or invented descriptions."""
    rid = target.get('legacy_rule_id') or target.get('suggested_legacy_rule_id')
    if not rid:
        rid = (target.get('structural_link') or {}).get('rule_id')
    evidence = by_id.get(rid, {})
    ids = [x['business_id'] for x in evidence.get('nbs_row_candidates', [])]
    direct = rules.get(rid, {}).get('target_id')
    if direct and direct not in ids:
        ids.append(direct)
    return [by_id[x] for x in ids if x in by_id and by_id[x]['source_system'] == 'T24']


def context_cells(row, block):
    """Row, hierarchy ancestors and header/context cells in its own block; exact source wording and cell references."""
    out = []
    for m in block:
        own = m['business_id'] == row['business_id']
        ancestor = bool(m.get('path_key') and row.get('path_key', '').startswith(m['path_key'] + ' > '))
        context = m['source_row'] <= row['source_row'] and m.get('kind') in ('TITLE', 'HEADER', 'CONTEXT')
        if not (own or ancestor or context):
            continue
        for cell in m['cells']:
            if cell['column'] == m.get('description_column') or cell.get('value') is None:
                continue
            val = str(cell['value'])
            if not val.strip():
                continue
            out.append({'sheet': m['sheet'], 'cell': cell['coord'], 'text': val,
                        'role': 'LINE' if own else 'PARENT' if ancestor else 'HEADER',
                        'type': cell.get('type'), 'source_row': m['source_row']})
    return out


def extract_fields(cells):
    """Extract *wording*, not runnable expressions. Unsupported words remain available in Original cells."""
    fields = defaultdict(list)
    for c in cells:
        text = c['text']
        for label, pat in {
            'category': r'\b(?:PL\.?\s*)?CATEGORY\s*(?:=|<>|NOT\s+EQUAL\s+TO|EQUAL\s+TO)\s*[^\n&]*',
            'sector': r'\b(?:PL\.?\s*)?SECTOR\s*(?:=|<>|NOT\s+EQUAL\s+TO|EQUAL\s+TO)\s*[^\n&]*',
            'industry': r'\bINDUSTR(?:Y|IES)\s*(?:=|<>|NOT\s+EQUAL\s+TO|EQUAL\s+TO)\s*[^\n&]*',
            'balance_types': r'\bASSET\s*TYPE\s*=\s*[\s\S]*?(?=\b(?:CATEGORY|SECTOR|INDUSTRY|CURRENCY|RESIDENCE)\b|$)',
            'residence': r'\bRESIDEN(?:CE|CY)\s*(?:=|<>|NOT\s+EQUAL\s+TO|EQUAL\s+TO)\s*[^\n&]*',
            'currency': r'\bCURRENCY\s*(?:=|<>|NOT\s+EQUAL\s+TO|EQUAL\s+TO)\s*[^\n&]*',
        }.items():
            for match in re.finditer(pat, text, re.I):
                wording = match.group().strip()
                entry = f'{c["sheet"]}!{c["cell"]}: {wording}'
                if entry not in fields[label]:
                    fields[label].append(entry)
    return {k: '\n'.join(v) for k, v in fields.items()}


def original_parts(root, target):
    """Compile only the original workbook's narrow, explicit criterion grammar into builder parts.
    Any unrepresented field, formula, customer lookup or missing balance definition blocks the import.
    Raw accounting sign is retained; the owner can set the presentation sign in the builder.
    """
    root=Path(root)
    catalog=read_json(root/'data/catalogs/catalog-0001.json')
    by_id={m['business_id']:m for m in catalog['mappings']}
    rules=read_json(root/'config/generation_rules.json')['rules']
    matches=original_rows(target,rules,by_id)
    if len(matches)!=1:
        raise ValueError('This item has no unique original Temenos row. Review the source-cell page.')
    row=matches[0]
    evidence=context_cells(row,[m for m in catalog['mappings'] if m['block_key']==row['block_key']])
    marker=re.compile(r'\b(CATEGORY|SECTOR|INDUSTRY|ASSET\s*TYPE|CURRENCY|RESIDENCE)\s*(NOT\s+EQUAL\s+TO|EQUAL\s+TO|<>|=)\s*',re.I)
    selections=[]
    for col in ('B','C','E','F'):
        filt=[];types=[];used=[]
        for c in evidence:
            if re.sub(r'\d','',c['cell'])!=col:
                continue
            text=c['text'].strip()
            if c['type']=='f':
                raise ValueError(f'{c["sheet"]}!{c["cell"]}: formula requires an explicit mapping decision')
            if not re.search(r'CATEGORY|SECTOR|INDUSTRY|ASSET\s*TYPE|CURRENCY|RESIDENCE|CUSTOMER|CRM',text,re.I):
                if c['role']=='LINE' and re.search(r'[A-Za-z]',text):
                    raise ValueError(f'{c["sheet"]}!{c["cell"]}: unsupported wording retained in the original-cell review')
                continue
            marks=list(marker.finditer(text))
            prefix=text[:marks[0].start()].strip() if marks else text
            if not marks or prefix not in ('','CONSOLIDATE.ASST.LIAB >'):
                raise ValueError(f'{c["sheet"]}!{c["cell"]}: customer lookup or complex wording needs a field definition')
            for i,m in enumerate(marks):
                field=re.sub(r'\s+','',m.group(1).upper());op=m.group(2).upper()
                val=text[m.end():marks[i+1].start() if i+1<len(marks) else len(text)].strip(' &\r\n')
                if field=='ASSETTYPE':
                    if not re.fullmatch(r'[A-Z0-9_,&\s]+',val):
                        raise ValueError(f'{c["cell"]}: unsupported balance expression')
                    types=[t for t in re.split(r'[\s,&]+',val) if t]
                else:
                    name={'CATEGORY':'category','SECTOR':'sector','INDUSTRY':'industry','CURRENCY':'currency','RESIDENCE':'country'}[field]
                    if field in ('CURRENCY','RESIDENCE'):
                        if not re.fullmatch(r'[A-Z]{2,3}',val):
                            raise ValueError(f'{c["cell"]}: unsupported currency/residence expression')
                        node={'field':name,'op':'eq','values':[val]}
                    else:
                        if not re.fullmatch(r'[0-9,\s&-]+',val):
                            raise ValueError(f'{c["cell"]}: unsupported numeric selection')
                        atoms=[]
                        for lo,hi,single in re.findall(r'(\d+)\s*-\s*(\d+)|(\d+)',val):
                            atoms.append({'field':name,'op':'range','values':[int(lo),int(hi)]} if lo else {'field':name,'op':'eq','values':[single]})
                        node=atoms[0] if len(atoms)==1 else {'any':atoms}
                    if op in ('<>','NOT EQUAL TO'):
                        node={'not':node}
                    filt.append(node)
            used.append(f'{c["sheet"]}!{c["cell"]}')
        if types:
            if not filt:
                raise ValueError('Original types have no explicit account population')
            selections.append((tuple(types),{'all':filt} if len(filt)>1 else filt[0],used))
    if not selections:
        raise ValueError('Original Temenos row does not specify exact balance types; no formula has been invented.')
    grouped={}
    for types,node,refs in selections:
        group=grouped.setdefault(types,{'nodes':[],'refs':[]})
        if node not in group['nodes']:
            group['nodes'].append(node)
        group['refs']+=refs
    return [{'kind':'STOCK','source':'ECB','measure':'components','components':list(types),
             'filter':g['nodes'][0] if len(g['nodes'])==1 else {'any':g['nodes']},'factor':1,'enabled':True,
             'label':'Original Temenos cells: '+', '.join(dict.fromkeys(g['refs']))+' (raw sign; review presentation sign)'}
            for types,g in grouped.items()]


def gl_snapshot(gl_root, out):
    """Read-only, stable SQLite snapshot of the GL tool's latest complete non-preview run.
    immutable=1 is used only when no WAL exists; that guarantees the committed database is self-contained.
    """
    p = Path(gl_root) / 'data/recon.db'
    if Path(str(p) + '-wal').exists() and Path(str(p) + '-wal').stat().st_size:
        raise ValueError('GL database has a live WAL. Use a completed database backup for the presentation snapshot.')
    c = sqlite3.connect(p.as_uri() + '?mode=ro&immutable=1', uri=True)
    c.row_factory = sqlite3.Row
    try:
        run = dict(c.execute("SELECT id,version_id,ecb_file_id,pl_file_id,tb_file_id,engine_version,created_at,status FROM run WHERE status='complete' AND is_preview=0 ORDER BY id DESC LIMIT 1").fetchone())
        version = dict(c.execute('SELECT id,file_id,name,created_at FROM mapping_version WHERE id=?', (run['version_id'],)).fetchone())
        files = [dict(r) for r in c.execute('SELECT id,role,filename,sha256,uploaded_at FROM input_file WHERE id IN (?,?,?,?)',
                                          (version['file_id'],run['ecb_file_id'],run['pl_file_id'],run['tb_file_id']))]
        totals = {}
        for row in c.execute('SELECT src,bal_type,gl_line,status,net,n_items FROM alloc WHERE run_id=?', (run['id'],)):
            key = (row['src'], row['bal_type'] or '', row['gl_line'] or '(no destination)', row['status'])
            a = totals.setdefault(key, [Decimal(0), 0, 0])
            a[0] += Decimal(row['net'] or '0')
            a[1] += row['n_items'] or 0
            a[2] += 1
        rows = [{'source': k[0], 'balance_type': k[1], 'gl_line': k[2], 'outcome': k[3],
                 'signed_qar': str(v[0]), 'source_records': v[1], 'groups': v[2]} for k, v in sorted(totals.items())]
        meta = {'database': str(p), 'database_bytes': p.stat().st_size, 'snapshot_mode': 'immutable read of committed database; no WAL',
                'run': run, 'mapping_version': version, 'files': files, 'read_at': datetime.now().isoformat(timespec='seconds')}
        (out / 'gl_snapshot.json').write_text(json.dumps({'metadata': meta, 'balances': rows}, indent=2), encoding='utf-8')
        return meta, rows
    finally:
        c.close()


DECISIONS = [
    ('01', 'Acceptances', 'Table 35!B48:F48', 'CATEGORY 23000–23999; ASSET TYPE ACPTCONTRABL',
     'DEFPAY / DEFPAYBL are acceptance legs; ACPTBANK is deliberately excluded as the same exposure. Ten ACPTCONTRA pairs remain disputed.',
     'Propose one acceptance exposure family; show DEFPAY/DEFPAYBL and ACPTCONTRA disputes separately. Do not add ACPTBANK on top.',
     'Temenos trade owner', 'GL docs/REVIEW_NBS_COMPARISON_19OCT.md D4; mapping v6 and run 54'),
    ('02', 'NBFI and customer sectors', 'Table 10!B7; Table 35 sector rows', 'SECTOR = 2004 for NBFI; some Table 35 bank rows say SECTOR = 3001',
     'DKB segment dictionary: 2004 Banks & FI; 2005 Government. Current NBS loan draft uses SIC 441* and excludes 44108.',
     'Keep the original T24 SECTOR selection visible; separate QCB institution class from industry and obtain the bank-to-QCB sector crosswalk.',
     'Temenos customer data / Regulatory reporting', 'Original NBS cells; GL SEGMENT and mapping evidence'),
    ('03', 'Forced zero financing lines', 'Tables 8 / 9 / 10', 'Original overdraft lines specify CATEGORY 1000–1004 and ASSET TYPE DEBIT',
     'Recent draft forced empty populations because BO was zero and the bank is Islamic.',
     'Withdraw the forced empty selection. Calculate the original criteria; missing product definitions remain open.',
     'Correction applied to engine on 20 October', 'config/policy_history/hierarchy_review_20261020.json'),
    ('04', 'Loan carrying value', 'Tables 8 / 9 / 10 / 12 / 44', 'Original cells do not uniformly define the owner component dictionary or a fee feed',
     'Current draft substitutes RCM/CLM empirical policies and adds Ethix Loan_Fees_QAR.',
     'Show principal, earned profit and fees as separate components. Keep hybrid calculations identified; no fee amount without a source.',
     'Temenos lending / Regulatory reporting', 'balance_rules.json; report_product_policies.json; original NBS cells'),
    ('05', 'Accrued / deferred profit', 'Table 19 / Table 30 / ASSET-100', 'ACCDEFERREDPFT appears on both accrued/deferred sides in the old NBS evidence',
     'GL review puts ACCDEFERREDPFT on deferred income 2610; RECDEFERREDPFT on financing, apart from defined 3730/3750 exceptions.',
     'Apply category-specific classifications; prevent the same profit balance from appearing in two asset/liability lines.',
     'Finance / Temenos lending', 'GL docs/REVIEW_NBS_COMPARISON_19OCT.md A1/B1'),
    ('06', 'Guarantee balance type spelling', 'Table 35!B16:F16 and sibling lines', 'CONTCR & CONTDRBL',
     'CONTDRBL is absent from ECB. CONTDB and CONTDBBL exist and are opposite legs.',
     'Retain the original spelling as evidence; flag CONTDRBL→CONTDBBL as a proposed correction and select one reporting leg.',
     'Temenos trade', 'Original Table 35; component_corrections.json; ECB headers'),
    ('07', 'Customer status', 'Table 23!B43:F47', 'CUSTOMER.STATUS = 81 corporate; CUSTOMER.STATUS = 80 personal',
     'The engine uses loan/deposit Personal/NonPersonal rather than a direct CUSTOMER.STATUS field.',
     'Show this as an attribute crosswalk requiring validation, not an original T24 field supplied in ECB.',
     'Customer data owner', 'Original Table 23; loan/deposit fields'),
    ('08', 'WIA deposits', 'Tables 23 / 24 / 25 / 45', 'PAYACCOUNT/PAYDEPOSITPFT and product/category references vary by row',
     '6513 CREDIT belongs on deposit lines; GL Report lacks several lines while GL Mapping already allocates it.',
     'Carry 6513 CREDIT once in the appropriate deposit population; validate QCB current/saving/time class independently.',
     'Deposits / Regulatory reporting', 'GL review D3/6513; CATEGORY dictionary'),
    ('09', 'PL category entries', 'Income / Expense; Tables 400 / 500', 'CONSOLIDATE.PRFT.LOSS and BALANCE / MOVEMENT / YTD expressions',
     'GL PL matching uses Migration PL J before L, product K before N, plus company and department.',
     'Use original PL categories with the validated field precedence; establish September/YTD completeness before treating events as reported income.',
     'Finance PL / Temenos accounting', 'GL docs/REVIEW.md section 1; owner September basis policy'),
    ('10', 'Late-payment balances', 'Table 19 receivables', 'Old NBS uses LATEPAYMENTFEE names',
     'ACCLATEPAYMENT is present; GL mapping places 466 balances in receivables 1910. CUST variants can have a different destination.',
     'Propose the actual type by category and account class; keep CUST/SP types separate.',
     'Finance / Lending', 'GL review C2; ECB header inventory'),
    ('11', 'Maturity', 'Tables 3 / 7 / 10 / 22 / 24 / 28 / 38', 'Original table headers define remaining maturity bands',
     'CALENDAR_EOM reproduces the 31 December loans; revolving loans still differ. Original tenor is absent.',
     'Keep boundary convention provisional and show the date field; do not substitute remaining term for original tenor.',
     'Regulatory reporting / Temenos lending', 'GL review 1.9.0; NBS maturity sensitivity'),
    ('12', 'Missing balance columns', 'All relevant tables', 'NABACCOUNT, NABDEFERREDPFT, RECPRINCIPALPFT and other requested types',
     'Absent ECB columns were omitted from numeric sums; current display could look complete.',
     'Partial when some required types are absent; unavailable when no requested type exists. Owner 19-code groups are preserved.',
     'Correction applied to engine on 20 October', 'ECB headers and balance_rules.json'),
    ('13', 'Duplicates / signs', 'Category extract and all balances', 'Raw dates, repeated fields and accounting signs',
     'Whole-file duplicate uploads deduplicate by hash; all 81,722 raw event rows are retained. GL comparisons may ignore signs by GL.',
     'NBS keeps signed balances; do not copy GL absolute-value matching, 5-QAR closure or first-match choices into NBS cells.',
     'Finance / Regulatory reporting', 'GL RELEASE_NOTES_1.9.3; NBS reporting-basis and duplicate policies'),
    ('14', 'Collateral / risk / country detail', 'Tables 11 / 13 and country/GCC measures', 'CR.ASSET.CLASS, collateral and country breakdowns',
     'Source attributes are incomplete; a GL line or BO amount cannot provide these missing dimensions.',
     'List exact missing fields per item; present NBS logic with missing-input status rather than a balancing zero.',
     'Risk / Treasury / Customer data', 'Original Temenos cells; NBS coverage register'),
]


def build(root, gl_root=None):
    root = Path(root)
    out = root / REVIEW_DIR
    out.mkdir(parents=True, exist_ok=True)
    catalog = read_json(root / 'data/catalogs/catalog-0001.json')
    by_id = {m['business_id']: m for m in catalog['mappings']}
    blocks = defaultdict(list)
    for m in catalog['mappings']:
        if m['source_system'] == 'T24':
            blocks[m['block_key']].append(m)
    ctx = lt.Context(root)
    mappings = tm.load(root / 'config')
    raw, records = [], []
    for t in sorted(mappings['targets'].values(), key=lambda t: (t['table'], t['item_code'])):
        original = original_rows(t, ctx.rules, by_id)
        cells = [c for m in original for c in context_cells(m, blocks[m['block_key']])]
        fields = extract_fields(cells)
        d = lt.describe(t, ctx)
        source_ref = '; '.join(f'{m["sheet"]}!row {m["source_row"]}' for m in original)
        flags = []
        if len(original) != 1:
            flags.append('No unique original Temenos row' if not original else 'Multiple original Temenos rows')
        if d['inherited']:
            flags.append('Engine adds corrections / inherited conditions: ' + d['inherited'])
        if t['method'] in ('QCB_COMPOSITION', 'QCB_POPULATION', 'SUBTOTAL_OF_CHILDREN'):
            flags.append('Derived from QCB / hierarchy, not an original account rule')
        rid = t.get('legacy_rule_id')
        spec = ctx.rules.get(rid, {})
        if spec.get('measure') == 'ethix_carrying':
            flags.append('Hybrid fees and empirical RCM/CLM policies; not stated in original Temenos cells')
        original_types = set()
        for c in cells:
            for match in re.finditer(r'ASSET\s*TYPE\s*=\s*([\s\S]*?)(?=\b(?:CATEGORY|SECTOR|INDUSTRY|CURRENCY|RESIDENCE)\b|$)', c['text'], re.I):
                original_types.update(re.findall(r'\b[A-Z][A-Z0-9_]+\b', match.group(1).upper()))
        original_types -= {'AND','CATEGORY','ASSET','TYPE','SECTOR'}
        missing = sorted(original_types - ctx.available)
        if missing:
            flags.append('Original types absent in September ECB: ' + ', '.join(missing))
        if fields.get('sector') and spec.get('source') in ('ECB_LOAN','ECB_DEPOSIT'):
            flags.append('Original T24 sector conditions must be reconciled with current loan/deposit attribute selections')
        direct_rule = '\n'.join(f'{c["sheet"]}!{c["cell"]}: {c["text"]}' for c in cells if c['role']=='LINE')
        parent_rule = '\n'.join(f'{c["sheet"]}!{c["cell"]}: {c["text"]}' for c in cells if c['role']=='PARENT')
        header_rule = '\n'.join(f'{c["sheet"]}!{c["cell"]}: {c["text"]}' for c in cells if c['role']=='HEADER')
        record = {'target_id': t['target_id'], 'table': t['table'], 'item_code': t['item_code'], 'description': t['description'],
                  'temenos_reference': source_ref, 'original_line': direct_rule, 'original_parents': parent_rule,
                  'original_headers': header_rule, 'category': fields.get('category',''), 'sector': fields.get('sector',''),
                  'industry': fields.get('industry',''), 'residence': fields.get('residence',''), 'currency': fields.get('currency',''),
                  'original_types': fields.get('balance_types',''), 'current_source': d['source'], 'current_selection': d['accounts'],
                  'current_types': lt.types_text(d['types']), 'current_method': t['method'], 'current_status': t['status'],
                  'current_evidence': d['how'], 'split': d['split'], 'review': '\n'.join(flags),
                  'proposed_logic': 'Preserve exact original line + parent + column conditions. Amend only the evidenced defect with a recorded decision.' if original else
                                    'No unique original row located. Retain QCB item and current evidence; resolve account selection and balance types explicitly.',
                  'stakeholder_decision': '', 'owner': ''}
        records.append(record)
        raw.extend({'target_id':t['target_id'], **c} for c in cells)
    gl_meta, gl_rows = gl_snapshot(gl_root, out) if gl_root else ({}, [])
    manifest = {'prepared_date':'2026-10-20', 'presentation_date':'2026-10-21', 'reporting_date':'2026-09-30',
                'mapping_version': mappings['version'], 'items': len(records), 'tables': len({r['table'] for r in records}),
                'original_linked_items': sum(bool(r['temenos_reference']) for r in records),
                'raw_cell_evidence_records': len(raw), 'catalog_sources':catalog['sources'], 'gl_snapshot': gl_meta,
                'status':'Presentation review; exact original wording and proposed corrections kept separate from active engine rules',
                'control':'Counts and balances across NBS tables overlap; do not sum them as a balance-sheet total.'}
    files = {'catalog':root/'data/catalogs/catalog-0001.json','generation_rules':root/'config/generation_rules.json',
             'target_mappings':root/'config/target_mappings.json','hierarchy':root/'config/hierarchy_predicates.json',
             'balance_groups':root/'config/balance_rules.json'}
    manifest['input_hashes'] = {k:hash_file(p) for k,p in files.items()}
    decisions = [dict(zip(('id','topic','original_reference','original_logic','gl_finding','proposal','owner','evidence'),r)) for r in DECISIONS]
    examples = balance_examples(root)
    payload = {'manifest':manifest,'mapping':records,'original_cells':raw,'decisions':decisions,'gl_balances':gl_rows,'examples':examples}
    (out/'NBS_Temenos_Mapping_Review.json').write_text(json.dumps(payload,indent=1,ensure_ascii=False),encoding='utf-8')
    for name, rows in [('NBS_Temenos_Mapping', records), ('Original_Cells', raw), ('Decisions', decisions), ('GL_Current_Balances',gl_rows), ('Balance_Examples',examples)]:
        if rows:
            with (out/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('catalog_sources','input_hashes','gl_snapshot')},indent=2))
    return payload


def balance_examples(root):
    """Small independently reproducible ECB totals. No sign inversion, fee addition or GL absolute-value netting."""
    c=sqlite3.connect((Path(root).resolve()/'data/bank_20260930.sqlite').as_uri()+'?mode=ro',uri=True)
    specs=[('Cash','CATEGORY 10000–10025',['DEBIT'],10000,10025,'Original Table 1; report sign -1 is a separate presentation choice'),
           ('Performance bonds: original','CATEGORY 28002',['CONTCR','CONTDRBL'],28002,28002,'Original Table 35; missing CONTDRBL makes the result incomplete'),
           ('Performance bonds: typo proposal','CATEGORY 28002',['CONTCR','CONTDBBL'],28002,28002,'Proposed spelling correction; do not add CONTDB and CONTDBBL together'),
           ('Acceptances: original','CATEGORY 23000–23999',['ACPTCONTRABL'],23000,23999,'Original Table 35 scope'),
           ('Acceptances: DEFPAY candidate','CATEGORY 23000–23999',['DEFPAY'],23000,23999,'GL review acceptance asset family; sign and QCB classification require decision'),
           ('Acceptances: ACPTBANK excluded','CATEGORY 23000–23999',['ACPTBANK'],23000,23999,'Same exposure as DEFPAY per GL review; displayed only to explain exclusion'),
           ('Deferred income component','All ECB categories',['ACCDEFERREDPFT'],None,None,'Component inventory; GL mapping assigns 2610 with category/account conditions'),
           ('Late payment component','All ECB categories',['ACCLATEPAYMENT'],None,None,'Component inventory; GL mapping assigns receivables 1910 with category/account conditions')]
    try:
        from .bank_data import load_manifest
        cols=set(load_manifest(Path(root)/'data/bank_20260930.sqlite')['ECB']['component_columns'])
        out=[]
        for label,criteria,types,lo,hi,note in specs:
            where="source='ECB'";params=[]
            if lo is not None:
                where+=' AND CAST(category AS INTEGER) BETWEEN ? AND ?';params=[lo,hi]
            n=0;nonzero=0;total=Decimal(0)
            for (comp,) in c.execute('SELECT components FROM unique_records WHERE '+where,params):
                n+=1;d=json.loads(comp or '{}');amt=sum((Decimal(str(d.get(t) or 0)) for t in types if t in cols),Decimal(0))
                nonzero+=bool(amt);total+=amt
            missing=[t for t in types if t not in cols]
            out.append({'example':label,'criteria':criteria,'balance_types':' + '.join(types),'account_rows':n,'nonzero_rows':nonzero,
                        'raw_qar':str(total),'raw_qar_thousands':str(total/1000),'status':'PARTIAL' if missing else 'SOURCE TOTAL',
                        'missing_types':', '.join(missing),'explanation':note})
        return out
    finally:
        c.close()


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--gl-root')
    args=p.parse_args();build(args.root,args.gl_root)
