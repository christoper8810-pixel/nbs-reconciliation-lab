from pathlib import Path
from pdf2image import convert_from_path
from pypdf import PdfReader
import json
base=Path(__file__).resolve().parent/'tracked_christopher_joseph'
poppler=r'C:\Users\Test\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin'
report=[]
for pdf in (base/'pdf').glob('*.pdf'):
    reader=PdfReader(pdf);folder=base/'pages'/pdf.stem;folder.mkdir(parents=True,exist_ok=True)
    paths=convert_from_path(pdf,dpi=144,output_folder=str(folder),fmt='png',paths_only=True,
                            output_file='render',poppler_path=poppler,thread_count=2)
    assert len(paths)==len(reader.pages)
    images=[]
    for i,path in enumerate(paths,1):
        final=folder/('page-%02d.png'%i);Path(path).replace(final);images.append(str(final))
    text='\n\n'.join(p.extract_text() for p in reader.pages)
    (folder/'rendered_text.txt').write_text(text,encoding='utf-8')
    report.append({'document':pdf.stem+'.docx','pages':len(images),'images':images})
    print(pdf.name,len(images),'pages',flush=True)
(base/'render_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
