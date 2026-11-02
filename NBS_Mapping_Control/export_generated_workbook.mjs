import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const resultPath=process.argv[2]||'exports/NBS_generated_review.json';
const result=JSON.parse(await fs.readFile(resultPath,'utf8'));
const template=JSON.parse(await fs.readFile(process.argv[3]||'data/report_template_values.json','utf8'));
const mappings=result.mapping_snapshot?{rules:result.mapping_snapshot}:JSON.parse(await fs.readFile('config/generation_rules.json','utf8'));
const outputDir=path.dirname(resultPath);
const wb=Workbook.create();
const overview=wb.worksheets.add('Overview');
const generated=wb.worksheets.add('Generated NBS');
const reference=wb.worksheets.add('Ethix reference');
const comparison=wb.worksheets.add('Comparison');
const mapping=wb.worksheets.add('Mapping notes');
const format='#,##0.000;(#,##0.000);0.000';
function style(sh,rows,cols){
 sh.showGridLines=false;
 sh.getRangeByIndexes(0,0,rows,cols).format.font={name:'Arial',size:10,color:'#263347'};
 sh.getRangeByIndexes(0,0,rows,cols).format.rowHeight=20;
 sh.getRangeByIndexes(0,0,rows,cols).format.verticalAlignment='center';
}
function header(sh,row,last){
 const r=sh.getRangeByIndexes(row-1,0,1,last);
 r.format.fill='#233A56';r.format.font={bold:true,color:'#FFFFFF'};r.format.rowHeight=26;
}
const rowmap=new Map(result.rows.map(r=>[r.row,r]));
const lastRow=Math.max(...Object.keys(template).map(Number));
const gm=[],rm=[];
for(let i=1;i<=lastRow;i++){
 const src=template[i]||{};const r=rowmap.get(i);const a=Array(24).fill(null);const b=Array(21).fill(null);
 for(let j=0;j<21;j++){
   const col=String.fromCharCode(65+j);const value=src[col];
   b[j]=r&&r.reference[col]!==undefined?r.reference[col]:(value??null);
   if(j===0 || (typeof value==='string' && !/^[\d,\s.()+-]+$/.test(value))){a[j]=value??null;}
   else if(r && r.values[col]!==undefined && r.values[col]!==null){a[j]=r.values[col];}
   else if(value!==undefined && value!==null){a[j]='n.a.';}
 }
 if(r){for(const [col,v] of Object.entries(r.values)){if(col.length===1 && col<='U')a[col.charCodeAt(0)-65]=v??'n.a.';}a[21]=r.status;a[22]=r.source||'Unavailable';a[23]=[...new Set(r.issues)].join('. ');}
 gm.push(a);rm.push(b);
}
generated.getRange(`A1:X${lastRow}`).values=gm;reference.getRange(`A1:U${lastRow}`).values=rm;
for(const sh of [generated,reference]){
 style(sh,lastRow,sh===generated?24:21);sh.getRange(`A1:A${lastRow}`).format.columnWidth=60;
 sh.getRange(`B1:U${lastRow}`).format.columnWidth=16;sh.getRange(`B1:U${lastRow}`).setNumberFormat(format);
 sh.getRange(`B1:U${lastRow}`).format.horizontalAlignment='right';
 sh.freezePanes.freezeColumns(1);sh.tabColor=sh===generated?'#233A56':'#CAB898';
 for(let i=1;i<=lastRow;i++){
   const label=template[i]?.A;
   if(typeof label==='string' && /^(Table\s*\(|Assets As|Liabilities As|Contra Items As|Income As|Expenses As)/i.test(label)){
      sh.getRange(`A${i}`).format.font={bold:true,size:12};sh.getRange(`A${i}:J${i}`).format.fill='#E7EDF4';
   }
   if(label==='Description'||label==='Sector / Subdivision')header(sh,i,Math.min(21,21));
 }
}
generated.getRange(`V1:W${lastRow}`).format.columnWidth=23;generated.getRange(`X1:X${lastRow}`).format.columnWidth=90;
generated.getRange(`X1:X${lastRow}`).format.wrapText=false;
const flat=[];
for(const r of result.rows){for(const col of [...new Set([...Object.keys(r.reference),...Object.keys(r.values)])].sort()){
 flat.push([r.id,r.row,col,r.description,r.values[col]??'n.a.',r.reference[col]??'n.a.',null,r.status,r.source||'Unavailable']);
}}
comparison.getRange('A1:I1').values=[['Mapping ID','Report row','Column','Description','Generated','Ethix','Difference','Status','Source']];
comparison.getRange(`A2:I${flat.length+1}`).values=flat;
const sourceLinks=[],differenceFormulas=[];
for(let i=0;i<flat.length;i++){
 const n=i+2;const [id,row,col]=flat[i];
 const g=rowmap.get(row).values[col];const e=rowmap.get(row).reference[col];
 // Batch formula writes avoid recalculating a growing comparison after every cell.
 sourceLinks.push([g!==undefined&&g!==null?`='Generated NBS'!${col}${row}`:'="n.a."',e!==undefined&&e!==null?`='Ethix reference'!${col}${row}`:'="n.a."']);
 differenceFormulas.push([`=IF(AND(ISNUMBER(E${n}),ISNUMBER(F${n})),E${n}-F${n},"n.a.")`]);
}
comparison.getRange(`E2:F${flat.length+1}`).formulas=sourceLinks;
comparison.getRange(`G2:G${flat.length+1}`).formulas=differenceFormulas;
style(comparison,flat.length+1,9);header(comparison,1,9);comparison.freezePanes.freezeRows(1);
comparison.getRange(`A1:A${flat.length+1}`).format.columnWidth=22;comparison.getRange(`B1:C${flat.length+1}`).format.columnWidth=12;
comparison.getRange(`D1:D${flat.length+1}`).format.columnWidth=60;comparison.getRange(`E1:G${flat.length+1}`).format.columnWidth=18;
comparison.getRange(`E2:G${flat.length+1}`).setNumberFormat(format);comparison.getRange(`H1:I${flat.length+1}`).format.columnWidth=23;
comparison.tables.add(`A1:I${flat.length+1}`,true,'ComparisonTable');
comparison.getRange(`A2:I${flat.length+1}`).format.fill='#FFFFFF';
comparison.getRange(`E2:G${flat.length+1}`).format.horizontalAlignment='right';
header(comparison,1,9);
comparison.getRange(`G2:G${flat.length+1}`).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:1,format:{fill:'#FBE6E4'}});
comparison.getRange(`G2:G${flat.length+1}`).conditionalFormats.add('cellIs',{operator:'lessThan',formula:-1,format:{fill:'#FBE6E4'}});
const specs=result.rows.map(r=>{const s=mappings.rules[r.id];return [r.id,r.row,r.description,s.source||'Unavailable',s.measure||'',s.factor,JSON.stringify(s.filter),s.components.join(', '),r.status,[...new Set(r.issues)].join('. ')];});
mapping.getRange('A1:J1').values=[['Mapping ID','Report row','Description','Source','Measure','Multiplier','Population filter','Balance types','Result status','Notes']];
mapping.getRange(`A2:J${specs.length+1}`).values=specs;style(mapping,specs.length+1,10);header(mapping,1,10);mapping.freezePanes.freezeRows(1);
mapping.getRange(`A1:A${specs.length+1}`).format.columnWidth=22;mapping.getRange(`B1:B${specs.length+1}`).format.columnWidth=12;mapping.getRange(`C1:C${specs.length+1}`).format.columnWidth=60;
mapping.getRange(`D1:F${specs.length+1}`).format.columnWidth=22;mapping.getRange(`G1:H${specs.length+1}`).format.columnWidth=70;
mapping.getRange(`I1:I${specs.length+1}`).format.columnWidth=20;mapping.getRange(`J1:J${specs.length+1}`).format.columnWidth=110;
mapping.tables.add(`A1:J${specs.length+1}`,true,'MappingNotesTable');
mapping.getRange(`A2:J${specs.length+1}`).format.fill='#FFFFFF';header(mapping,1,10);
overview.getRange('A2').values=[['September NBS generation']];overview.getRange('A2').format.font={name:'Arial',size:16,bold:true};
const s=result.summary,c=result.checks;
const summary=[['Reporting date',s.as_of],['Units','QAR thousands. Counts remain counts.'],['Report sections',s.report_sections],['Rows with available calculations',s.rows_with_amounts],['Rows reviewed',s.rows],['Compared cells',s.comparable_cells],['Comparisons within QAR 1,000',s.within_one_thousand],['Full reconciliation','Not achieved'],['Matched loan accounts',c.joined_loans],['Matched deposit accounts',c.joined_deposits],['Verified CLM links',c.clm_linked],['Missing CLM links',c.unresolved_clm_links],['Overdue loan maturities',c.maturity_overdue_loans],['Missing owner components',Object.values(c.missing_balance_columns).flat().join(', ')]];
overview.getRange(`A5:B${summary.length+4}`).values=summary;
overview.getRange('A21').values=[['Use the app to edit row mappings and regenerate. This workbook is a saved report run.']];
overview.getRange('A22').values=[['Generated amounts can be partial. n.a. is unavailable. Ethix values are comparison inputs.']];
overview.getRange('A23').values=[['Fees use the dated Ethix loan extract. Trial balance rows are supplementary, with geography unavailable.']];
overview.getRange('A24').values=[['No missing NAB, REC or deferred component was silently replaced by CO, CUST or BL balances.']];
let row=27;overview.getRange(`A${row}:D${row}`).values=[['Source','File','Rows','SHA-256']];header(overview,row,4);row++;
for(const [kind,m] of Object.entries(result.manifest)){if(!m||!m.path)continue;overview.getRange(`A${row}:D${row}`).values=[[kind,path.basename(m.path),m.rows,m.sha256]];row++;}
overview.getRange(`A${row}:D${row}`).values=[['ETHIX REPORT',path.basename(result.template),'',result.template_sha256]];
style(overview,row,4);overview.getRange('A1:A40').format.columnWidth=44;overview.getRange('B1:B40').format.columnWidth=66;overview.getRange('C1:C40').format.columnWidth=14;overview.getRange('D1:D40').format.columnWidth=72;overview.tabColor='#233A56';
overview.getRange('A2').format.font={name:'Arial',size:16,bold:true};
overview.getRange('B18').format.font={color:'#B42318'};
wb.recalculate();
await fs.mkdir(outputDir,{recursive:true});
console.log((await wb.inspect({kind:'table',range:'Overview!A5:B18',include:'values',tableMaxRows:14,tableMaxCols:2})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20}})).ndjson);
for(const [sh,range] of [['Overview','A1:C24'],['Generated NBS','A1:L18'],['Ethix reference','A1:L18'],['Comparison','A1:I12'],['Mapping notes','A1:F12']]){
 const blob=await wb.render({sheetName:sh,range,scale:1.2,format:'png'});
 await fs.writeFile(path.join(outputDir,sh.replaceAll(' ','_')+'_preview.png'),new Uint8Array(await blob.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(outputDir,'NBS_Generated_September_2026.xlsx'));
console.log('Saved report workbook');
process.exit(0);
