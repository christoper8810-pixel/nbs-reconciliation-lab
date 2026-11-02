from pathlib import Path
from pdf2image import convert_from_path
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
import json
base=Path(__file__).resolve().parent
poppler=r'C:\Users\Test\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin'
allpages=[]; report=[]
for f in (base/'pdf').glob('*.pdf'):
    reader=PdfReader(f)
    target=base/'pages'/f.stem
    target.mkdir(parents=True,exist_ok=True)
    paths=convert_from_path(f,dpi=144,output_folder=str(target),fmt='png',paths_only=True,
                            output_file='page',poppler_path=poppler,thread_count=2)
    texts=[p.extract_text() for p in reader.pages]
    assert len(paths)==len(texts)
    for page,text in enumerate(texts):
        assert text.strip(),(f.name,page,'empty page')
        # Store the rendered text to check that cell content made it into PDF.
    (target/'rendered_text.txt').write_text('\n\n'.join(texts),encoding='utf-8')
    pagepaths=[]
    for i,path in enumerate(paths,1):
        final=target/('page-%02d.png'%i)
        Path(path).replace(final);pagepaths.append(str(final));allpages.append((f.stem,i,final))
    report.append({'document':f.stem+'.docx','pages':len(paths),'images':pagepaths})
    print(f.name,len(paths),'pages',flush=True)
width=600;height=455
sheet=Image.new('RGB',(width*3,height*((len(allpages)+2)//3)),'#cccccc')
draw=ImageDraw.Draw(sheet)
for idx,(name,i,path) in enumerate(allpages):
    im=Image.open(path);im.thumbnail((width-12,height-35))
    x=(idx%3)*width;y=(idx//3)*height
    sheet.paste(im,(x+(width-im.width)//2,y+28))
    draw.text((x+8,y+5),name.split(' Review')[0]+' page '+str(i),fill='black')
sheet.save(base/'contact_sheet.png')
(base/'render_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
