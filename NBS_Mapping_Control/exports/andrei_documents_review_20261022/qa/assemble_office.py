from pathlib import Path
import json, shutil
base=Path(__file__).resolve().parent
files=json.loads((base/'msi_files.json').read_text(encoding='utf-8-sig'))
components={x['id']:x['directory'] for x in json.loads((base/'msi_components.json').read_text(encoding='utf-8-sig'))}
dirs={x['id']:x for x in json.loads((base/'msi_directories.json').read_text(encoding='utf-8-sig'))}
root=base/'portable_office'
root.mkdir(exist_ok=True)
def directory(id):
    if id=='INSTALLLOCATION': return root
    d=dirs[id]
    if not d['parent']: raise ValueError(id)
    name=d['name'].split(':')[0].split('|')[-1]
    return directory(d['parent'])/('' if name=='.' else name)
count=0
for f in files:
    src=base/'office_files'/f['id']
    if not src.exists(): continue
    try: target=directory(components[f['component']])/f['name'].split('|')[-1]
    except ValueError: continue
    assert target.resolve().is_relative_to(root.resolve()), target
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists(): shutil.copyfile(src,target)
    count+=1
print('Portable converter files prepared:',count)
print('Native converter:',root/'program'/'soffice.exe')
