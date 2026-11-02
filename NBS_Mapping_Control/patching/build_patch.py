"""Build NBS_Mapping_Studio_Update.zip from this source tree.

    python patching/build_patch.py --out DIR [--test-results FILE]

Known versions of modified files are read from Git (the initial application commit and the TB-reconciliation
commit) when Git is available; their line-ending-normalised SHA-256 lets the installer recognise them on Windows.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from nbs_control.studio import STUDIO_VERSION  # noqa: E402

KNOWN_COMMITS = ('3dcb6ef', '289c59b')            # initial application; TB reconciliation release
NEW_TREES = ('nbs_control/studio', 'nbs_control/tbrecon')
NEW_FILES = ('nbs_control/studio_app.py', 'tests/test_studio.py', 'tests/test_tbrecon.py', 'Start_Mapping_Studio.cmd', 'Start_TB_Reconciliation.cmd', 'build_release.py',
             'MAPPING_STUDIO_GUIDE.md', 'TB_RECON_GUIDE.md', 'CURRENT_STATE_ASSESSMENT.md', 'FIXES_IMPLEMENTED.md', 'RECONCILIATION_VALIDATION.md',
             'REMAINING_ISSUES.md', 'PROGRESS.md', 'MAPPING_STUDIO_VALIDATION.md')
CONFIGS = ('config/studio.json', 'config/tb_recon.json')
# Studio runs through nbs_control/studio_app.py, so no existing file has to change for it to work: these edits only
# add the Studio to the existing 'serve' command, menu and command line, and are skipped (with a warning) if impossible.
REQUIRED_MODIFY = ()
INTEGRATION_MODIFY = ('nbs_control/web.py', 'nbs_control/cli.py', 'nbs_control/templates/base.html')
OPTIONAL_MODIFY = ('nbs_control/gl_mapping.py', 'nbs_control/bank_data.py', 'tests/test_rebuild.py', 'README.md')


def nhash(b):
    return hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()


def git_show(commit, rel):
    try:
        r = subprocess.run(['git', 'show', f'{commit}:NBS_Mapping_Control/{rel}'], cwd=APP, capture_output=True, check=True)
        return r.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def between(text, start, end, include_start=True):
    a = text.index(start)
    b = text.index(end, a + len(start))
    return text[a if include_start else a + len(start):b]


def ops_for(rel):
    cur = (APP / rel).read_text(encoding='utf-8')
    if rel == 'nbs_control/web.py':
        anchor = '    register_rebuild_routes(app,service.config_dir.parent)\n'
        alt = [{'op': 'insert_after', 'anchor': anchor}, {'op': 'insert_before', 'anchor': '\n    return app\n'}]
        return [{'marker': 'register_studio_routes', 'alternatives': alt,
                 'text': '    from .studio.web import register_studio_routes\n    register_studio_routes(app, service.config_dir.parent)\n'},
                {'marker': 'register_tb_routes', 'alternatives': alt,
                 'text': '    from .tbrecon.web import register_tb_routes\n    register_tb_routes(app, service.config_dir.parent)\n'}]
    if rel == 'nbs_control/templates/base.html':
        studio = '''  {% if config.get('STUDIO_ENABLED') %}<a href="{{ url_for('studio_home') }}"><b>Mapping Studio</b></a>{% endif %}\n'''
        tb = '''  {% if config.get('TB_RECON_ENABLED') %}<a href="{{ url_for('tb_home') }}">TB reconciliation (separate tool)</a>{% endif %}\n'''
        return [{'marker': "url_for('studio_home')", 'text': studio,
                 'alternatives': [{'op': 'insert_before', 'anchor': '''  <a href="{{ url_for('nbs_home') }}">Home</a>'''},
                                  {'op': 'insert_before', 'anchor': '</header>'}]},
                {'marker': "url_for('tb_home')", 'text': tb,
                 'alternatives': [{'op': 'insert_after', 'anchor': '''  <a href="{{ url_for('nbs_downloads') }}">4 Downloads</a>\n'''},
                                  {'op': 'insert_before', 'anchor': '</header>'}]}]
    if rel == 'nbs_control/cli.py':
        parse = '    args = parser.parse_args(argv)\n'
        tb_sub = between(cur, "    p = sub.add_parser('tb-recon', ", "    p = sub.add_parser('studio-analyse'")
        st_sub = between(cur, "    p = sub.add_parser('studio-analyse'", parse)
        st_fn = between(cur, 'def _studio(args) -> int:', 'def _tb_recon(args) -> int:')
        tb_fn = between(cur, 'def _tb_recon(args) -> int:', 'if __name__ == "__main__":')
        return [{'op': 'insert_before', 'anchor': parse, 'marker': "add_parser('tb-recon'", 'text': tb_sub},
                {'op': 'insert_before', 'anchor': parse, 'marker': "add_parser('studio-analyse'", 'text': st_sub},
                {'op': 'insert_after', 'anchor': parse + '    try:\n', 'marker': "args.command.startswith('tb-recon')",
                 'text': "        if args.command.startswith('tb-recon'):\n            return _tb_recon(args)\n"},
                {'op': 'insert_after', 'anchor': parse + '    try:\n', 'marker': "args.command.startswith('studio-')",
                 'text': "        if args.command.startswith('studio-'):\n            return _studio(args)\n"},
                {'op': 'insert_before', 'anchor': 'if __name__ == "__main__":', 'marker': 'def _tb_recon(args)', 'text': tb_fn},
                {'op': 'insert_before', 'anchor': 'if __name__ == "__main__":', 'marker': 'def _studio(args)', 'text': st_fn}]
    return []


def file_list():
    out = []
    for tree in NEW_TREES:
        for p in sorted((APP / tree).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                out.append((p.relative_to(APP).as_posix(), 'add'))
    for p in sorted((APP / 'nbs_control' / 'templates').glob('*.html')):
        if p.name.startswith(('studio_', 'tb_')):
            out.append((p.relative_to(APP).as_posix(), 'add'))
    out += [(f, 'add') for f in NEW_FILES if (APP / f).exists()]
    out += [(f, 'config_add_if_missing') for f in CONFIGS]
    out += [(f, 'modify') for f in REQUIRED_MODIFY + INTEGRATION_MODIFY + OPTIONAL_MODIFY]
    return out


def build(out_dir, test_results=None):
    out_dir = Path(out_dir)
    stage = out_dir / 'NBS_Mapping_Studio_Update'
    if stage.exists():
        shutil.rmtree(stage)
    (stage / 'patch_files').mkdir(parents=True)
    files = []
    for rel, action in file_list():
        src = APP / rel
        data = src.read_bytes()
        dst = stage / 'patch_files' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        known = sorted({nhash(b) for b in (git_show(c, rel) for c in KNOWN_COMMITS) if b is not None} | {nhash(data)})
        entry = {'path': rel, 'action': action, 'new_sha256': nhash(data), 'accepted_sha256': known}
        if action == 'modify':
            entry['required'] = rel in REQUIRED_MODIFY
            entry['ops'] = ops_for(rel)
            for op in entry['ops']:
                op.setdefault('alternatives', [{'op': op.pop('op'), 'anchor': op.pop('anchor')}] if 'op' in op else [])
                assert op['marker'] in data.decode('utf-8'), (rel, op['marker'])
        files.append(entry)
    man = {'patch_id': f'NBS_MAPPING_STUDIO_{STUDIO_VERSION}', 'version': STUDIO_VERSION,
           'built': dt.datetime.now().isoformat(timespec='seconds'), 'requires': {'python': '>=3.10', 'packages': ['flask', 'openpyxl']},
           'compatible_with': 'NBS Mapping Control installations containing nbs_control/web.py with register_rebuild_routes '
                              f'(initial application {KNOWN_COMMITS[0]} and later)',
           'never_written': ['data/', 'exports/', 'inputs/', 'existing config/*.json'], 'files': files}
    (stage / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    shutil.copy2(APP / 'patching' / 'patch_engine.py', stage / 'patch_engine.py')
    wheels = APP / 'exports' / 'transfer' / 'wheels'
    if wheels.exists():
        (stage / 'wheels').mkdir()
        for w in wheels.glob('*.whl'):
            shutil.copy2(w, stage / 'wheels' / w.name)
    for name in ('INSTALL_UPDATE.bat', 'ROLLBACK_UPDATE.bat', 'PATCH_NOTES.md'):
        shutil.copy2(APP / 'patching' / name, stage / name)
    tr = Path(test_results) if test_results else APP / 'patching' / 'TEST_RESULTS.md'
    shutil.copy2(tr, stage / 'TEST_RESULTS.md')
    zpath = out_dir / 'NBS_Mapping_Studio_Update.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(stage).as_posix())
    return zpath, man


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--test-results')
    a = ap.parse_args()
    z, m = build(a.out, a.test_results)
    print(f'{z} ({len(m["files"])} managed files)')
