from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import json, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).resolve().parent
OUT = BASE / 'revised'
OUT.mkdir(exist_ok=True)
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
NS = {'w': W}
def q(x): return '{'+W+'}'+x
def txt(p): return ''.join(p.itertext()) if False else ''.join(p.xpath('.//w:t/text()', namespaces=NS))
def settext(p, text):
    rp = p.find('.//'+q('rPr'))
    rp = deepcopy(rp) if rp is not None else None
    for ch in list(p):
        if ch.tag != q('pPr'): p.remove(ch)
    run = E.SubElement(p, q('r'))
    if rp is not None: run.append(rp)
    t = E.SubElement(run, q('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    t.text = text

GENERAL = ('All changes proposed in NBS01 must be correctly reflected in all three interconnected mappings: '
           'NBS01, NBS001 Additional Tables, and LCR & NSFR (Solo). Apply the same underlying balance components, '
           'linked offsets and category exclusions wherever that population is used, including referenced cells, '
           'direct CAL/ECB rules, supporting schedules and totals. Preserve each report\'s required dimensions, '
           'cash-flow timing and weights, and reconcile the differences.')
POLICY = [
    ('Confirmed mapping changes on 22 October 2026', True),
    ('PRINCIPALPFT: Report related balances with the associated loans, in the same product and customer classification. '
     'Cover ACCPRINCIPALPFT, RECPRINCIPALPFT, GRCPRINCIPALPFT, DUEPRINCIPALPFT, NABPRINCIPALPFT, '
     'DELPRINCIPALPFT, PREPRINCIPALPFT and other locally defined states. Preserve SP status and its loan treatment; '
     'do not rename SP as ordinary profit. Remove separate accrued-income/other-asset contributions for the same amounts.', False),
    ('Category 3713: Offset the loan balance with the linked category 6050 CREDIT balance. Where ACCCRPROFIT and '
     'ACCDEPOSITPFT are mapped together, offset the matched pair. Combine the verified signed components once at '
     'the linked loan/account level; do not net unrelated accounts or subtract an already negative credit twice.', False),
    ('Category 6050: Exclude it from all deposit reporting, including totals, breakdowns, deposit ratios, LCR deposit '
     'outflows and NSFR deposit funding. Trace linked offsets to the related loan. Flag missing or ambiguous links '
     'for investigation; do not put them back into deposits or force a balancing amount.', False),
    (GENERAL, False),
    ('The figures below are retained historical UAT observations. They are not recalculated impacts of these changes. '
     'Apply the confirmed treatment above wherever an earlier recommendation would conflict with it.', False),
]

NBS = {
 37: 'Split the shared category/type predicate into explicit branches. Restrict the accrued-income DEBIT branch to categories 13440-13459 after validating their definitions. Move loan-related PRINCIPALPFT to the associated loan lines (C1); preserve separately defined fee and other-income selectors. Apply the same changes to the configured ASSET - 100 expression and auxiliary rules.',
 42: 'Align the resident and non-resident selections. Exclude category 6050 from deposit/prepaid selections; apply the matched ACCCRPROFIT/ACCDEPOSITPFT offset in D3 wherever both are mapped together. Do not report the same linked profit separately as a prepaid asset or profit payable.',
 53: 'Use the owner-defined OUTSTANDING group: CURACCOUNT, PREACCOUNT, GRCACCOUNT, DELACCOUNT, NABACCOUNT, DUEACCOUNT, DELDEFERREDPFT, GRCDEFERREDPFT, NABDEFERREDPFT, DUEDEFERREDPFT, RECDEFERREDPFT, PREDEFERREDPFT. Add the associated PRINCIPALPFT components under C1 and apply D3 offsets. Remove duplicate RECDEFERREDPFT from accrued income where already in outstanding. Reconcile signed components by contract.',
 58: 'Use the 12-code OUTSTANDING group in B1 for outstanding loan stock, together with the associated PRINCIPALPFT in C1 and offsets in D3. Restore DELACCOUNT and PREACCOUNT. Define PDOACCOUNT separately; do not silently add it to the named group. Preserve separate overdraft, suspense and contingent measures, and exclude 6050 from deposits.',
 63: 'Add owner-confirmed 3713 to Murabaha and remove it from Others in the same change. Offset each 3713 loan with its linked 6050 CREDIT and apply the matched profit offset in D3. Do not require a separate CLM label to apply this confirmed category treatment. Validate 3709, 3715 and 3740 against the product dictionary before assigning them.',
 73: 'Use the B1 loan-stock components plus associated PRINCIPALPFT (C1) and linked offsets (D3). Preserve customer, industry, residence and currency dimensions; attribute the linked offset to the related loan. Keep other facility measures distinct. Reconcile the category population with Table 8 before comparing totals.',
 96: 'Loan-related PRINCIPALPFT balances are omitted or treated as separate accrued income instead of following the associated loans',
 97: 'Loan lines in Tables 8, 9, 10, 11, 12, 44 and ASSET - 100; Table 19 and its auxiliary rules',
 98: 'The earlier 808.7m ACC/DEL/PRE observation does not quantify the full correction. Inventory all PRINCIPALPFT states and reconcile their loan attribution.',
 99: 'Move all loan-related PRINCIPALPFT states with their loans; remove separate Table 19/other-asset contributions for the same amounts. AMORTIZED_EARNED has ACC, REC, GRC, DEL and PRE PRINCIPALPFT; its five-code definition must not omit DUE, NAB or other valid loan states from reporting. Preserve SP status with the associated loan treatment. Apply D3 offsets and propagate to NBS001 and liquidity mappings.',
 114: 'Rebuild M10 and P10 consistently with C1 and D3: remove loan-related PRINCIPALPFT and any separately repeated linked profit amounts from accrued income. Confirm whether these auxiliary columns feed configured processing. Keep fees and Ijara receivables in their separately defined measures; do not copy a duplicated predicate.',
 116: 'SP states are incomplete; loan-related PRINCIPALPFTSP must follow the associated loan treatment rather than a blanket suspended-income rule',
 117: 'Loan and credit-classification lines; Tables 29, 30, 11 and any separate income/suspense selections',
 119: 'Inventory missing SP types. Keep loan-related PRINCIPALPFTSP with its associated loan and preserve its suspended status; do not also add it to a separate income total. Define ACCLATEPAYMENTSP and DEFERREDPFTSP treatment separately. Check diagnostic/classification disclosures without duplicating the same economic amount in totals.',
 137: 'Matured deposits and payable profit need complete rules; 3713/6050 loan offsets and the exclusion of 6050 from all deposit reporting are not explicit',
 138: 'Category 3713 loan lines; category 6050 CREDIT; ACCCRPROFIT/ACCDEPOSITPFT; all deposit selections, Table 31 and Table 45',
 139: 'Earlier observations: PAYACCOUNT 340m, PAYDEPOSITPFT 509.5m and 6050 debit 571m. These are not the amount of the required CREDIT/profit offsets.',
 140: 'Offset each category 3713 loan with its linked 6050 CREDIT. Offset matched ACCCRPROFIT and ACCDEPOSITPFT wherever mapped together, using verified signs once. Exclude category 6050 from every deposit rule and total; investigate missing/ambiguous links without a deposit fallback. Retain PAYACCOUNT and PAYDEPOSITPFT corrections for other eligible deposits. Reconcile component reuse and loan attribution.',
 150: 'Reconcile liability parents to components using same-date sources. Exclude category 6050 from all deposit totals/breakdowns and remove any duplicate linked profit already offset under D3. Resolve 18001 overlap in subordinated debt/AT1; correct Table 21 E19 outside-Qatar residence. Validate Table 26 subtotals, signs and populations before quantifying impacts.',
 157: 'Implement the owner-confirmed 22 October treatment of PRINCIPALPFT, 3713/6050 CREDIT and paired ACCCRPROFIT/ACCDEPOSITPFT across all three mappings. Validate the account links, signs, source dictionaries and remaining product/presentation questions; the confirmed treatment is no longer a pending conditional proposal.',
 158: 'Maintain one cell-level change register across NBS01, NBS001 Additional Tables and LCR & NSFR (Solo): current rule, replacement, dependent references/direct rules, inclusion/exclusion changes and reconciliation status. Apply connected changes together and retain unresolved source/link exceptions explicitly.',
 159: 'Rerun all three mappings on the same company, population, reporting date and valuation basis. Reconcile Tables 100/200 and breakdowns, the loan components/offsets and zero category-6050 contribution to deposits. Bridge liquidity totals for cash-flow timing and weights. Investigate abnormal records before quarantine/removal. Retain the Table 10 maturity-boundary and Table 11 subtotal corrections.',
}
ADD = {
 13: 'About 95bn of financing principal (31 Aug) falls outside the rules; the loan component and product selections need rebuilding',
 34: 'Remove the duplicated ACCDEFERREDPFT asset contribution and keep the defined deferred-income treatment, consistent with NBS01 A1. This does not remove PRINCIPALPFT: report loan-related PRINCIPALPFT with the associated loan and reconcile signed components.',
 43: 'The same Ijara balance, including related PRINCIPALPFT, can be selected in both product lines',
 44: 'Make the loan/product populations mutually exclusive (B1-B3). Keep related PRINCIPALPFT with its assigned loan product and apply linked offsets once.',
 55: 'Align product categories with NBS01 Table 8, including 3713 in Murabaha. Fill Others with the remaining eligible population without overlap. Carry the related PRINCIPALPFT with each loan and apply the linked 3713/6050 CREDIT and paired profit offsets (B5).',
 57: 'The generic Loans line mixes product selection and profit components, overlapping the Islamic finance lines',
 59: 'Incomplete loan selection and possible duplication; loan-related PRINCIPALPFT itself belongs with the loan',
 60: 'Allocate loans to mutually exclusive NBS01-aligned product lines. Keep associated PRINCIPALPFT with each loan, including DUE/GRC/NAB and other valid states; remove its separate other-asset contribution. Resolve deferred profit under A1 and NBS01 B1. Do not delete all profit components or assume the loan line must be empty.',
 64: 'An unrestricted selection can include commitments, unrelated fees and duplicated components; required loan-related PRINCIPALPFT must be retained',
 65: 'Use the NBS01 loan-stock components, including its 12-code OUTSTANDING group, plus related PRINCIPALPFT and the linked offsets in B5. Define PDOACCOUNT separately. Preserve SP status, maturity and sector dimensions. Exclude unrelated fees/commitments and duplicate other-asset contributions; seven principal types alone are not the complete loan measure.',
 86: 'Use one sector definition across NBS001. Attribute linked 6050 offsets and related profit to the associated 3713 loan sector so the net loan is not split into a deposit sector.',
 115: 'Deposit selections omit matured balances and do not explicitly exclude category 6050',
 116: 'Tables 610/611, 625 and every deposit total/breakdown or dependent deposit selection',
 117: 'CURBALANCE is absent from the sampled CAL; PAYACCOUNT (about 340m at 31 Aug) is missed. Category 6050 would also be misreported if admitted as a deposit.',
 118: 'Exclude CATEGORY = 6050 before applying CREDIT, CURACCOUNT and PAYACCOUNT to other eligible deposits. Check CURBALANCE against the versioned dictionary before replacing it. Apply the exclusion to totals, maturity/sector splits and the Table 625 deposit denominator; no 6050 deposit fallback for unresolved links. Apply the matched profit offset wherever the pair is mapped together.',
 123: 'Build credit from Tables 608/609 with related PRINCIPALPFT and linked 3713/6050 and profit offsets. Build the deposit denominator from eligible deposits excluding all 6050. Trace each component once; do not deduct the same offset again when deriving the ratio.',
 140: 'Tables 613, 614, 615 and parts of the combined sheet list seven principal types, including DEL and PRE. This is useful coverage but not a complete loan measure: align the component definitions with NBS01 and include related PRINCIPALPFT and linked offsets wherever the same loan stock is measured.',
 144: 'SL to correct Tables 604/605 and rebuild 608/609, applying the confirmed PRINCIPALPFT and linked-offset rules in the same release. Propagate them to all relevant asset lines, then complete A1 and E1-E3. Exclude category 6050 throughout the deposit selections.',
 145: 'Rerun NBS001 and reconcile loan components, offsets, deposits and claims on banks to NBS01 and same-date sources. Test every deposit total/breakdown for zero 6050 contribution. Apply the connected changes to LCR & NSFR and reconcile timing/weight differences. Track unmatched links as exceptions.',
}
LIQ = {
 42: 'Use scheduled installments within the next 30 days. Apply the confirmed loan components and linked offsets to the eligible cash flows, including the PRINCIPALPFT due with each loan payment. Do not substitute the full accounting loan stock for scheduled receipts; validate the payment-schedule source.',
 53: 'Filter on SECTOR = 1000-1999, 4000-4004, 6000/6001, 7000/7001, with CATEGORY <> 6050 applied to both clauses and all deposit subgroups. Keep the same exclusion in NSFR deposit funding.',
 106: 'Keep one controlling definition per line and align its NBS reference and direct CAL/ECB alternative with the same NBS01 components, linked offsets and category exclusions. Update dependent schedules together with NBS001. Preserve each liquidity metric\'s cash-flow timing and weights; do not add both alternatives.',
 111: 'Reconcile the corrected NBS01 asset basis and the NSFR residual. Move related PRINCIPALPFT into the associated loan stock and remove it from separate other assets. Apply the linked offsets once; bridge NSFR classifications and weights to the trial balance.',
 113: 'Deposit rules miss matured balances and do not explicitly exclude category 6050',
 114: 'LCR_00 C50-C58; NSFR_00 C13-C21, all related deposit lines, totals and supporting schedules',
 115: 'CURBALANCE is absent from the sampled CAL; PAYACCOUNT (about 340m at 31 Aug) is missed. Admitting 6050 would also misstate deposit outflows/funding.',
 116: 'Apply CATEGORY <> 6050 before selecting CREDIT, CURACCOUNT and PAYACCOUNT for other eligible deposits. Check CURBALANCE against the versioned dictionary. Exclude 6050 from every deposit outflow, deposit funding/ASF selection and supporting total, including referenced NBS populations. Do not return unmatched 6050 balances to deposits.',
 124: 'Term deposits (6600-6999) are covered by the second ADD clause. Apply CATEGORY <> 6050 to all deposit clauses and their combined totals; retain the maturity correction in A1.',
 129: 'SL to correct A1, B1, C1, D1 and E3, together with E5/E6 and every dependent reference. Apply the confirmed loan/profit offsets and deposit exclusion consistently with the NBS01/NBS001 release.',
 130: 'Identify one controlling rule per line (E1). Reflect every NBS01 change in NBS001 Additional Tables and this liquidity mapping wherever the population is shared; check both NBS references and direct CAL/ECB definitions.',
 131: 'Rerun LCR and NSFR on the same reporting date. Reconcile HQLA, underlying loan stock and eligible deposit funding to corrected NBS01/NBS001 and the trial balance. Bridge scheduled cash flows and weights separately. Test zero 6050 contribution to deposit outflows/funding, each linked offset once, and unmatched-link exceptions.',
}

ADDITIONAL_ROWS = {
 'add': [('B5', 'Category 3713 requires linked 6050 CREDIT and paired profit offsets',
          'All 3713 loan-stock selections, Tables 608/609, 613-615 and 625; other asset/profit lines using the same population',
          'Gross loan/offset amounts or duplicated profit can distort loan totals and the credit/deposit ratio',
          'Offset each 3713 loan with its linked 6050 CREDIT. Offset ACCCRPROFIT against matched ACCDEPOSITPFT wherever mapped together. Use verified signed components once, retain the loan dimensions and flag unmatched links. Remove duplicated profit from other assets and exclude all 6050 from deposits.')],
 'liq': [
     ('E5', 'Loan-related PRINCIPALPFT must follow the associated loans',
      'LCR_00 C86/C87; NSFR loan-stock rules, NBS references and related supporting schedules',
      'Separate accrued/other-asset treatment can omit or duplicate loan components and place them in the wrong liquidity classification',
      'Use the corrected NBS01/NBS001 loan component basis for NSFR loan stock, retaining SP status and applicable weights. In LCR use only eligible scheduled receipts, including related PRINCIPALPFT due in the horizon. Remove the same amounts from separate accrued/other assets; do not treat the full stock as a 30-day inflow.'),
     ('E6', 'Linked 3713/6050 and paired profit offsets must flow through all liquidity rules',
      'Loan inflows/stock; LCR_00 C50-C58 and C86/C87; NSFR_00 C13-C21; all deposit and loan supporting schedules',
      'Gross exposures, double offsets or 6050 deposit treatment would be inconsistent with the corrected NBS mappings',
      'Apply the 3713 loan/linked 6050 CREDIT offset and matched ACCCRPROFIT/ACCDEPOSITPFT offset once in the shared balance basis. Use documented timing for the resulting eligible cash flows before weighting; do not net unrelated maturities/accounts. Exclude 6050 from all deposit outflows and deposit funding/ASF; flag unmatched links.')
 ]
}
FILES = [
 ('nbs', 'NBS_Mapping_Review_Clean_Corrections_1.docx', 'NBS01 Mapping Review Revised 22Oct2026.docx', NBS),
 ('add', 'NBS001 Additional Tables - Mapping Review.docx', 'NBS001 Additional Tables Review Revised 22Oct2026.docx', ADD),
 ('liq', 'LCR & NSFR (Solo) - Mapping Review.docx', 'LCR and NSFR Solo Review Revised 22Oct2026.docx', LIQ),
]

def newpara(template, text, bold=False):
    p = deepcopy(template)
    settext(p, text)
    p.set('{http://schemas.microsoft.com/office/word/2010/wordml}paraId',hashlib.sha256(text.encode()).hexdigest()[:8].upper())
    pp = p.find(q('pPr'))
    if pp is None: pp = E.Element(q('pPr')); p.insert(0,pp)
    for tag in ['pageBreakBefore','keepNext']:
        for el in pp.findall(q(tag)): pp.remove(el)
    for tag in ['numPr','pStyle']:
        for el in pp.findall(q(tag)): pp.remove(el)
    rp=p.find(q('r')).find(q('rPr'))
    if rp is None: rp=E.Element(q('rPr'));p.find(q('r')).insert(0,rp)
    for tag in ['b','bCs','i','iCs','sz','szCs']:
        for el in rp.findall(q(tag)):rp.remove(el)
    E.SubElement(rp,q('sz')).set(q('val'),'24' if bold else '22')
    E.SubElement(rp,q('szCs')).set(q('val'),'24' if bold else '22')
    if bold:
        E.SubElement(rp,q('b'))
        E.SubElement(pp,q('keepNext'))
    return p

def addrow(table, values):
    tr = deepcopy(table.findall(q('tr'))[-1])
    cells = tr.findall(q('tc'))
    assert len(cells)==len(values)
    for cell, value in zip(cells, values):
        ps=cell.findall(q('p'))
        settext(ps[0], value)
        for p in ps[1:]: cell.remove(p)
    table.append(tr)

def layout(root):
    # Keep the original landscape format, colours and typefaces. Rebalance
    # the existing columns so the expanded correction text remains readable.
    title=root.find('.//'+q('body')+'/'+q('p'))
    pp=title.find(q('pPr'))
    if pp is None: pp=E.Element(q('pPr'));title.insert(0,pp)
    style=pp.find(q('pStyle'))
    if style is None:style=E.SubElement(pp,q('pStyle'))
    style.set(q('val'),'Title')
    for r in title.findall(q('r')):
        rp=r.find(q('rPr'))
        if rp is None:rp=E.Element(q('rPr'));r.insert(0,rp)
        for tag in ['sz','szCs','color','u']:
            for e in rp.findall(q(tag)):rp.remove(e)
        E.SubElement(rp,q('sz')).set(q('val'),'40')
        E.SubElement(rp,q('szCs')).set(q('val'),'40')
        E.SubElement(rp,q('color')).set(q('val'),'000000')
    for table in root.findall('.//'+q('tbl')):
        rows=table.findall(q('tr'))
        cols=len(rows[0].findall(q('tc')))
        widths=[int(c.get(q('w'))) for c in table.find(q('tblGrid')).findall(q('gridCol'))]
        assert len(widths)==cols
        pr=table.find(q('tblPr'))
        if pr is None:pr=E.Element(q('tblPr'));table.insert(0,pr)
        for tag in ['tblW','tblLayout']:
            for e in pr.findall(q(tag)):pr.remove(e)
        tw=E.SubElement(pr,q('tblW'));tw.set(q('w'),str(sum(widths)));tw.set(q('type'),'dxa')
        grid=table.find(q('tblGrid'))
        if grid is None:grid=E.Element(q('tblGrid'));table.insert(1,grid)
        for e in list(grid):grid.remove(e)
        for width in widths:E.SubElement(grid,q('gridCol')).set(q('w'),str(width))
        for ri,row in enumerate(rows):
            trpr=row.find(q('trPr'))
            if trpr is None:trpr=E.Element(q('trPr'));row.insert(0,trpr)
            if trpr.find(q('cantSplit')) is None:E.SubElement(trpr,q('cantSplit'))
            if ri==0 and trpr.find(q('tblHeader')) is None:E.SubElement(trpr,q('tblHeader'))
            for cell,width in zip(row.findall(q('tc')),widths):
                cp=cell.find(q('tcPr'))
                if cp is None:cp=E.Element(q('tcPr'));cell.insert(0,cp)
                for e in cp.findall(q('tcW')):cp.remove(e)
                cw=E.SubElement(cp,q('tcW'));cw.set(q('w'),str(width));cw.set(q('type'),'dxa')
                if ri==0:
                    for p in cell.findall(q('p')):
                        pp=p.find(q('pPr'))
                        if pp is None:pp=E.Element(q('pPr'));p.insert(0,pp)
                        if pp.find(q('keepNext')) is None:E.SubElement(pp,q('keepNext'))
    for p in root.find(q('body')).findall(q('p')):
        text=txt(p)
        if text and (text[0].isdigit() or (len(text)>2 and text[1:3]=='. ')):
            pp=p.find(q('pPr'))
            if pp is None:pp=E.Element(q('pPr'));p.insert(0,pp)
            for e in pp.findall(q('pageBreakBefore')):pp.remove(e)
            if pp.find(q('keepNext')) is None:E.SubElement(pp,q('keepNext'))
    # Delete standalone manual page breaks; flow section headings with content.
    for p in root.find(q('body')).findall(q('p')):
        if not txt(p).strip():
            for b in p.xpath('.//w:br[@w:type="page"]',namespaces=NS):b.getparent().remove(b)
    orders={
      'tblPr':'tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription tblPrChange',
      'tcPr':'cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark headers cellIns cellDel cellMerge tcPrChange',
      'trPr':'cnfStyle divId gridBefore gridAfter wBefore wAfter cantSplit trHeight tblHeader tblCellSpacing jc hidden ins del trPrChange',
      'pPr':'pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange',
    }
    for tag,names in orders.items():
        ranking={q(n):i for i,n in enumerate(names.split())}
        for pr in root.findall('.//'+q(tag)):
            pr[:]=sorted(pr,key=lambda e:ranking.get(e.tag,999))

def addcomment(parts, root, anchor):
    commentroot=E.Element(q('comments'), nsmap={'w':W})
    c=E.SubElement(commentroot,q('comment'))
    for k,v in {'id':'0','author':'Mapping Review','initials':'MR','date':'2026-10-22T09:00:00Z'}.items(): c.set(q(k),v)
    p=E.SubElement(c,q('p')); rr=E.SubElement(p,q('r')); E.SubElement(rr,q('t')).text=GENERAL
    parts['word/comments.xml']=E.tostring(commentroot,xml_declaration=True,encoding='UTF-8',standalone=True)
    start=E.Element(q('commentRangeStart')); start.set(q('id'),'0')
    end=E.Element(q('commentRangeEnd')); end.set(q('id'),'0')
    run=E.Element(q('r')); ref=E.SubElement(run,q('commentReference')); ref.set(q('id'),'0')
    anchor.insert(1 if anchor.find(q('pPr')) is not None else 0,start)
    anchor.append(end); anchor.append(run)
    rels=E.fromstring(parts['word/_rels/document.xml.rels'])
    assert not any('comments' in x.get('Type','') for x in rels)
    ids={x.get('Id') for x in rels}; ix=1
    while 'rId'+str(ix) in ids: ix+=1
    rel=E.SubElement(rels,'{'+R+'}Relationship',Id='rId'+str(ix),Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments',Target='comments.xml')
    parts['word/_rels/document.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    ct=E.fromstring(parts['[Content_Types].xml'])
    E.SubElement(ct,'{'+CT+'}Override',PartName='/word/comments.xml',ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml')
    parts['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)

log=[]
for key,filename,outname,replacements in FILES:
    src=BASE/'originals'/filename
    with ZipFile(src) as z: parts={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(parts['word/document.xml'])
    pars=[p for p in root.findall('.//'+q('body')+'//'+q('p')) if txt(p).strip()]
    inspection=json.loads((BASE/(filename+'.json')).read_text(encoding='utf-8'))
    assert len(pars)==len(inspection['paragraphs'])
    for i,p in enumerate(pars): assert txt(p)==inspection['paragraphs'][i]['text'], (filename,i)
    changes=[]
    for i,new in replacements.items():
        before=txt(pars[i]); settext(pars[i],new)
        changes.append({'paragraph':i,'before':before,'after':new})
    # Keep source preparation dates; identify the revision separately.
    subtitle=pars[1]
    settext(subtitle,txt(subtitle).rstrip()+' Revised 22 October 2026.')
    pivot=pars[8 if key=='nbs' else 7]
    parent=pivot.getparent(); at=parent.index(pivot)
    template=pars[7 if key=='nbs' else 6]
    general_anchor=None
    for text,bold in POLICY:
        p=newpara(template,text,bold)
        parent.insert(at,p); at+=1
        if text==GENERAL: general_anchor=p
    tables=root.findall('.//'+q('tbl'))
    if key=='nbs':
        addrow(tables[0],['4','Loan-related PRINCIPALPFT and linked 3713/6050 offsets (C1, D3)','Keep related profit with loans, apply matched offsets once and exclude 6050 from every deposit population'])
    elif key=='add':
        addrow(tables[0],['5','Loan component and linked-offset alignment with NBS01 (B2, B3, B5, E1)','Include related PRINCIPALPFT; net linked 3713/6050 and paired profit; exclude 6050 from deposits'])
        for row in ADDITIONAL_ROWS[key]: addrow(tables[2],row)
    else:
        addrow(tables[0],['6','Loan components, linked offsets and 6050 deposit exclusion (E3, E5, E6)','Carry the corrected NBS loan population into liquidity rules with the proper cash-flow timing and weights'])
        for row in ADDITIONAL_ROWS[key]: addrow(tables[-1],row)
    body=root.find(q('body'))
    tail=body.find(q('sectPr'))
    checks=[
        ('6. Implementation checks',True),
        ('Trace every valid loan-related PRINCIPALPFT state to its loan line and SP status. Confirm that the same amount is not also added to accrued income or other assets.',False),
        ('Reconcile each 3713 loan to its linked 6050 CREDIT and each jointly mapped ACCCRPROFIT/ACCDEPOSITPFT pair. Verify source signs, unique component use and all unmatched or ambiguous links; do not remove repeated source entries without investigating their identities.',False),
        ('Demonstrate zero category-6050 contribution to every deposit total, breakdown and ratio, and to LCR deposit outflows and NSFR deposit funding. Include direct rules, referenced cells and supporting schedules.',False),
        ('Reconcile the shared components across all three mappings on the same reporting basis. Explain differences caused by report dimensions, scheduled cash flows and regulatory weights. Record the changed cells, old/new rules and test evidence before release.',False),
    ]
    for text,bold in checks:
        p=newpara(template,text,bold)
        if tail is not None: body.insert(body.index(tail),p)
        else: body.append(p)
    layout(root)
    addcomment(parts,root,general_anchor)
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    target=OUT/outname
    with ZipFile(target,'w',ZIP_DEFLATED) as z:
        for n,b in parts.items(): z.writestr(n,b)
    log.append({'original':filename,'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
                'revised':outname,'revised_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                'changes':changes,'added_policy_paragraphs':len(POLICY),'general_comments':1,
                'added_issue_rows':len(ADDITIONAL_ROWS.get(key,[]))})
    print(outname, len(changes),'paragraph corrections')
(BASE/'change_register.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'source_manifest.json').write_text(json.dumps({'zip':'C:/Users/Test/Downloads/OneDrive_1_10-22-2026.zip',
 'zip_sha256':hashlib.sha256(Path('C:/Users/Test/Downloads/OneDrive_1_10-22-2026.zip').read_bytes()).hexdigest(),
 'documents':[{'filename':x['original'],'sha256':x['original_sha256']} for x in log]},indent=2),encoding='utf-8')
