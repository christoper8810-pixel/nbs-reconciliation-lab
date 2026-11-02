"""Apply the Temenos-source review update with backups and automatic rollback."""
import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


def apply(target, package):
    target=Path(target).expanduser().resolve()
    package=Path(package).resolve()
    if not (target/'nbs_control/rebuild_engine.py').is_file():
        raise ValueError('Choose the existing NBS tool folder containing nbs_control and config.')
    manifest=json.loads((package/'payload_manifest.json').read_text(encoding='utf-8'))
    backup=target/'backups'/('temenos_review_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    changed=[]
    for rel,sha in manifest.items():
        p=(package/'payload'/rel).resolve()
        if not p.is_relative_to((package/'payload').resolve()) or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
            raise ValueError('Update file failed integrity check: '+rel)
        if rel.endswith('.py'):
            compile(p.read_text(encoding='utf-8-sig'),rel,'exec')
    backup.mkdir(parents=True)
    try:
        for rel in manifest:
            dest=(target/rel).resolve()
            if not dest.is_relative_to(target):
                raise ValueError('Unsafe update destination')
            # Never replace an installation's catalogue with the presentation snapshot.
            if rel.startswith('data/catalogs/') and dest.exists():
                continue
            existed=dest.exists()
            if existed:
                saved=backup/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,saved)
            changed.append((rel,existed))
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(package/'payload'/rel,dest)
        cfg=target/'config/hierarchy_predicates.json'
        if cfg.exists():
            saved=backup/'config/hierarchy_predicates.json';saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(cfg,saved)
            changed.append(('config/hierarchy_predicates.json',True))
            doc=json.loads(cfg.read_text(encoding='utf-8-sig'))
            for name in ('overdraft','loans and advances'):
                entry=doc.get('labels',{}).get(name,{})
                if entry.get('FORCE') and 'NONE_CONVENTIONAL_PRODUCT' in json.dumps(entry) and not entry.get('owner_confirmed'):
                    entry['enabled']=False
                    entry['disabled_reason']='20 October review: preserve original Temenos selection instead of forcing an empty population.'
            cfg.write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8')
        (backup/'restore_manifest.json').write_text(json.dumps(changed,indent=2),encoding='utf-8')
    except Exception:
        for rel,existed in reversed(changed):
            dest=target/rel
            if existed:
                shutil.copy2(backup/rel,dest)
            elif dest.exists():
                dest.unlink()
        raise
    print('UPDATED. Your mappings, source-file selections and bank database are preserved.')
    print('Backup:',backup)
    print('Start the NBS tool and choose Original Temenos logic. Generate a new run to apply the corrected balance labels.')
    return backup


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--target');args=ap.parse_args()
    package=Path(__file__).resolve().parent
    target=args.target or (str(package.parent) if (package.parent/'nbs_control').is_dir() else input('Existing NBS tool folder: ').strip().strip('"'))
    try:
        apply(target,package)
    except Exception as e:
        print('NOT UPDATED:',e)
        raise SystemExit(1)
