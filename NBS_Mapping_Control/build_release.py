"""Build the versioned release ZIP of NBS Mapping Control (allow-list; no confidential data or runtime databases).

    python build_release.py [--out DIR]

Included: application code, tests, configuration, synthetic samples, launchers, user documentation and the
offline wheels (copied to wheels/). Excluded by construction: data/, exports/ (except the wheels), inputs/,
.verification/, the bank-workbook evidence files (source_inventory.json, source_findings.json,
source_manifest.json, report_sections.json, VALIDATION.json), review briefs quoting bank figures, process
logs, *.sqlite and any run output. A manifest with SHA-256 of every packed file is added.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import zipfile
from pathlib import Path

from nbs_control.tbrecon import ENGINE_VERSION

ROOT = Path(__file__).resolve().parent
INCLUDE_DIRS = ('nbs_control', 'tests', 'config', 'samples')
INCLUDE_FILES = ('mapping_engine.py', 'requirements.txt', 'build_release.py', 'Start_NBS_Rebuild.cmd', 'Start_NBS_Reports.cmd',
                 'Start_TB_Reconciliation.cmd', 'README.md', 'INSTALL.md', 'RUN_GUIDE.md', 'REBUILD_RUN_GUIDE.md',
                 'NBS_REPORT_RUN_GUIDE.md', 'TB_RECON_GUIDE.md', 'CURRENT_STATE_ASSESSMENT.md', 'FIXES_IMPLEMENTED.md',
                 'RECONCILIATION_VALIDATION.md', 'REMAINING_ISSUES.md', 'PROGRESS.md', 'sample_clm_records.json',
                 'sample_non_clm_records.json')
WHEELS = ROOT / 'exports' / 'transfer' / 'wheels'
SKIP_PARTS = {'__pycache__', '.pytest_cache', 'history', 'generation_history'}
SKIP_SUFFIX = ('.pyc', '.sqlite', '.sqlite3', '.db', '.xlsx', '.xls', '.xlsm', '.csv', '.zip', '.log')


def files():
    for d in INCLUDE_DIRS:
        for p in sorted((ROOT / d).rglob('*')):
            if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_PARTS) and not p.name.endswith(SKIP_SUFFIX):
                yield p, p.relative_to(ROOT).as_posix()
    for f in INCLUDE_FILES:
        if (ROOT / f).exists():
            yield ROOT / f, f
    if WHEELS.exists():
        for p in sorted(WHEELS.glob('*.whl')):
            yield p, 'wheels/' + p.name


def build(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.date.today().isoformat()
    name = f'NBS_Mapping_Control_{ENGINE_VERSION}_{stamp}'
    path = out_dir / f'{name}.zip'
    manifest = []
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for src, arc in files():
            data = src.read_bytes()
            manifest.append(f'{hashlib.sha256(data).hexdigest()}  {arc}')
            z.writestr(f'{name}/{arc}', data)
        notes = (f'{name}\n\nComponent version {ENGINE_VERSION}. Built {stamp}.\n'
                 'Contains no bank data, mapping-workbook evidence, runtime databases or run outputs.\n'
                 'The owner-review catalogue needs the supplied evidence files (source_inventory.json, source_manifest.json,\n'
                 'source_findings.json, report_sections.json) from your controlled location; tests that need them fail until\n'
                 'they are copied in. The TB reconciliation tests run standalone: python -m unittest tests.test_tbrecon\n'
                 'Start: double-click Start_TB_Reconciliation.cmd. See TB_RECON_GUIDE.md.\n')
        z.writestr(f'{name}/RELEASE_NOTES.txt', notes)
        z.writestr(f'{name}/MANIFEST.sha256', '\n'.join(manifest) + '\n')
    return path, len(manifest)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(ROOT / 'dist'))
    p, n = build(ap.parse_args().out)
    print(f'{p} ({n} files)')
