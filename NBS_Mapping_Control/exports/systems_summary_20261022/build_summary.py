from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

P=Path(__file__).resolve().parent
audit=json.loads((P.parent/'cell_audit_20261021/audit.json').read_text(encoding='utf-8'))
findings=audit['findings']
items=[
 ('Wrong category codes',
  'Some categories differ from the GLs in Ehab\'s mapping. Examples: government sukuk income uses 65037 instead of 65073; investment property uses 11320 instead of 13337.',
  'Confirm the intended NBS treatment and correct the category codes. Also review bond expense, where the selected GLs map to 66560-66562 rather than 60031-60034.',
  'Income B21/C21; Table 15 B10; Expense B22/C22', ['NBS-0085','NBS-0129','NBS-0093']),
 ('Finance company investments',
  'The finance-company line includes 11908 but leaves out 11903-11907 from the GLs selected by Ehab.',
  'Check each investment and put it in the correct company group. Confirm 11902-11907 for this line and explain whether 11908 belongs elsewhere.',
  'Table 14 C28; Ehab K938', ['NBS-0128']),
 ('Intangible assets',
  'The Other line leaves out 11301 and 11570 and includes 11550 compared with Ehab\'s selected GLs.',
  'Confirm which assets belong in each line and which accumulated amortisation belongs with them. Correct the gross and amortisation categories together.',
  'Table 18 B16/C16; Ehab K1042', ['NBS-0135']),
 ('Bank profit expense',
  'The bank-profit expense line includes product category 15154 and omits PL categories 66586-66588 found under the selected GLs.',
  'Use the correct profit-and-loss categories for this expense. Keep the product category separate and confirm the missing categories with Finance.',
  'Expense B30/C30/D30/F30/G30; Ehab K256', ['NBS-0094']),
 ('Loan balance components',
  'The financing schedules do not consistently use the same principal and profit components. Some definitions leave out overdue or prepaid components.',
  'Agree what each line should include: principal, earned profit, deferred profit and any fees. Document each component and apply the agreed definition consistently.',
  'Assets and Tables 8, 10, 12 and 44', []),
 ('Local and foreign currency rules',
  'Some local-currency and foreign-currency columns use different categories or sectors without an explanation.',
  'Use the same business selection for both columns unless a difference is intentional. Keep the currency filter and document any valid exception.',
  'Income C28:D37 and C80:D80; Expense C57:D58', ['NBS-0142','NBS-0143','NBS-0144','NBS-0145','NBS-0146','NBS-0147','NBS-0148']),
 ('Balance codes and field names',
  'Some names do not match the supplied data. Examples include CONTDRBL, CREDIIT and ACCOUNT.CUTOMER. Other requested balance components are missing from the extract.',
  'Correct spelling against the actual Temenos fields. Confirm each balance code and obtain missing inputs. Show missing data as incomplete; do not silently return zero or substitute a similar name.',
  'Table 35; Table 22 B13; Table 19; repeated customer rules', []),
 ('Profit on both accounting sides',
  'ACCDEFERREDPFT is selected in accrued-income assets and deferred-income liabilities for overlapping categories. This creates a risk of counting the same component twice.',
  'Finance and Systems should agree where this component belongs and how it is presented. Correct both schedules together and demonstrate that the balance is counted as intended.',
  'Table 19 C10 and related cells; Table 30 B7/E7', ['NBS-1451']),
 ('Customer sector classification',
  'Table 11 includes sector 2006 under non-bank financial institutions, while the supplied GL dictionary calls 2006 Salary Cards.',
  'Confirm the sector dictionary used by the live report. Agree the bank-to-QCB classification with Finance and use it consistently across the affected tables.',
  'Table 11 B7 and repeated cells; GL SEGMENT C30', ['NBS-1452']),
 ('Credit quality calculations',
  'Some Table 11 totals mix direct and indirect exposures or count performing balances again. The source has 75 formula defects and 90 saved Excel errors.',
  'Rebuild the totals from their labelled columns. Test with nonzero examples so each exposure appears once in the correct performing or non-performing total.',
  'Table 11 F/G/N/O/P/Q columns', []),
 ('Maturity calculations',
  'Some rules subtract maturity from the reporting date, giving negative days for future contracts. Table 10 also misses eight exact boundaries and treats Without Maturity as a one-day band.',
  'Calculate days from 30 September 2026 to maturity. Give every boundary one clear home. Handle overdue balances, missing dates and open-ended contracts separately.',
  'Table 10 D6:N6; Table 24 E9:J9', []),
 ('Totals using the wrong columns',
  'Twenty-five written totals point to the wrong columns. For example, the inside-Qatar total in Assets E61 says B+C although its amount columns are C and D.',
  'Correct the references against the headings. Check local currency, foreign currency, inside Qatar, outside Qatar and grand totals using an independent example.',
  'Assets rows 61-62; Table 9 row 6; Table 26 rows 5/26', ['NBS-1171']),
 ('Repeated treasury-share GL',
  'Ehab uses GL 3200000001 for both treasury-share nominal value and premium or discount. The GL mapping places it under category 18008.',
  'Investigate whether the second line needs another GL or a documented split. Agree this with the bank\'s GL owner before removing or changing either entry.',
  'Ehab K109/K111; Liabilities C56/C58', ['NBS-1450']),
 ('Mapping versions',
  'The clearing-account rule matches the September GL version, but the current GL adds category 18062. Later changes can therefore look like original errors.',
  'Confirm which mapping is deployed and its effective date. Record the old and new rules and update the NBS where the change is applicable.',
  'Table 2 B12/E12; Ehab L380', ['NBS-0107']),
 ('Missing schedules and source rules',
  'Tables 20 and 38 have no worksheet in the supplied Systems mapping. Some treasury and other externally sourced lines also lack a complete category bridge.',
  'Provide the missing specifications and source definitions. For each line, show the source, selection, balance components, sign, calculation and reporting split.',
  'Tables 20/38; source-dependent lines in the detailed register', ['NBS-1473','NBS-1474'])
]
known={f['id'] for f in findings}
assert all(i in known for item in items for i in item[4])
(P/'summary_items.json').write_text(json.dumps([dict(number=i+1,topic=t,issue=a,fix=b,reference=r,evidence=ids) for i,(t,a,b,r,ids) in enumerate(items)],ensure_ascii=False,indent=2),encoding='utf-8')
intro=('Please review the points below against the NBS mapping dated 6 October 2026 and confirm the changes needed in the configured report. '
       'The comparison uses Ehab\'s mapping and the September and current GL versions. Category differences need confirmation before activation; formula and spelling defects can be corrected against the source definitions.')
closing=('Please return a corrected mapping workbook, a response against each item, and a rerun for 30 September 2026 showing the changes in the report. '
         'Identify any point requiring a Finance decision. Keep a record of each change and its effective date.')
doc=Document();section=doc.sections[0]
section.page_width=Inches(8.5);section.page_height=Inches(11)
section.top_margin=Inches(.65);section.bottom_margin=Inches(.65);section.left_margin=Inches(.65);section.right_margin=Inches(.65)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
 st.font.size=Pt(11)
doc.styles['Normal'].paragraph_format.space_after=Pt(5)
doc.styles['Normal'].paragraph_format.line_spacing=1.03
doc.styles['Title'].font.size=Pt(19);doc.styles['Title'].paragraph_format.space_after=Pt(5)
doc.add_paragraph('NBS mapping issues for Systems Limited',style='Title')
p=doc.add_paragraph('22 October 2026');p.paragraph_format.space_after=Pt(8)
doc.add_paragraph(intro)
p=doc.add_paragraph('Issue and action summary');p.runs[0].bold=True;p.paragraph_format.space_before=Pt(3)
table=doc.add_table(rows=1,cols=3);table.autofit=False
widths=[1.3,2.7,3.2]
for c,w in zip(table.columns,widths):c.width=Inches(w)
for c,txt,w in zip(table.rows[0].cells,['Issue','What we found','Action requested'],widths):
 c.width=Inches(w);c.text=txt
 tcPr=c._tc.get_or_add_tcPr();shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'D9D9D9');tcPr.append(shade)
 for r in c.paragraphs[0].runs:r.bold=True;r.font.color.rgb=RGBColor(0,0,0)
table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
for i,(topic,issue,fix,ref,ids) in enumerate(items,1):
 row=table.add_row();row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
 for c,w in zip(row.cells,widths):c.width=Inches(w)
 c=row.cells[0];c.text=f'{i}  {topic}'
 for r in c.paragraphs[0].runs:r.bold=True
 p=c.add_paragraph(ref);p.paragraph_format.space_before=Pt(4)
 for r in p.runs:r.font.size=Pt(9);r.font.color.rgb=RGBColor(70,70,70)
 row.cells[1].text=issue;row.cells[2].text=fix
for row in table.rows:
 for cell in row.cells:
  props=cell._tc.get_or_add_tcPr();margins=OxmlElement('w:tcMar')
  for side in ['top','bottom','left','right']:
   el=OxmlElement('w:'+side);el.set(qn('w:w'),'90');el.set(qn('w:type'),'dxa');margins.append(el)
  props.append(margins)
  for p in cell.paragraphs:
   p.paragraph_format.space_after=Pt(3)
   p.paragraph_format.keep_with_next=False
   p.paragraph_format.widow_control=True
   for r in p.runs:
    r.font.name='Arial'
    if r.font.size is None:r.font.size=Pt(10.5)
pr=table._tbl.tblPr
borders=OxmlElement('w:tblBorders')
for side in ['top','bottom','left','right','insideH','insideV']:
 el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'C9C9C9');borders.append(el)
pr.append(borders)
p=doc.add_paragraph(closing);p.paragraph_format.space_before=Pt(8)
p=doc.add_paragraph('Supporting evidence: NBS_Ehab_Systems_GL_Cell_Audit_21Oct2026.xlsx and the detailed numbered findings register.')
for r in p.runs:r.font.size=Pt(9)
footer=section.footer.paragraphs[0];footer.alignment=2
r=footer.add_run('Systems Limited review  |  ');r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
doc.core_properties.title='NBS mapping issues for Systems Limited'
doc.core_properties.subject='Issue and action summary for the 6 October 2026 NBS mapping'
doc.core_properties.author=''
doc.core_properties.keywords='NBS, mapping review, Systems Limited'
out=P/'NBS_Systems_Limited_Issues_and_Fixes_22Oct2026.docx';doc.save(out)
md=['# NBS mapping issues for Systems Limited','','22 October 2026','',intro,'','| No. | Issue | Action requested |','|---|---|---|']
for i,(topic,a,b,ref,ids) in enumerate(items,1):md.append(f'| {i}. {topic} | {a} | {b} |')
md+=['',closing,'','Detailed references are in the supporting audit workbook.']
(P/'NBS_Systems_Limited_Issues_and_Fixes_22Oct2026.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'document':out.name,'issues':len(items),'words':len(' '.join([intro,closing]+[x for t,a,b,r,ids in items for x in [t,a,b,r]]).split())}))
