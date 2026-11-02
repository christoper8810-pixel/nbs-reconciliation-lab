"""Windows patch package: install, repeat install, failure recovery, rollback, incompatible and locally changed installs.

Representative installations are rebuilt from Git history (initial application 3dcb6ef and the TB release
289c59b) with synthetic user data added. Skipped when Git history is not available (e.g. inside a release ZIP).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
REPO = APP.parent
PARTS = ('nbs_control', 'config', 'tests', 'samples', 'mapping_engine.py', 'requirements.txt', 'README.md', 'INSTALL.md',
         'Start_NBS_Rebuild.cmd', 'Start_NBS_Reports.cmd', 'source_inventory.json', 'source_manifest.json', 'source_findings.json',
         'report_sections.json', 'sample_clm_records.json', 'sample_non_clm_records.json')


def git_ok(commit):
    try:
        return subprocess.run(['git', 'cat-file', '-e', commit], cwd=REPO, capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def baseline(commit, dest):
    paths = [f'NBS_Mapping_Control/{p}' for p in PARTS]
    data = subprocess.run(['git', 'archive', '--format=tar', commit] + paths, cwd=REPO, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(dest, filter='data')
    app = dest / 'NBS_Mapping_Control'
    (app / 'data').mkdir(exist_ok=True)
    (app / 'data' / 'bank_20260930.sqlite').write_bytes(b'SQLite format 3\x00 synthetic user database')
    (app / 'exports' / 'old_run').mkdir(parents=True)
    (app / 'exports' / 'old_run' / 'previous_report.xlsx').write_bytes(b'previous report')
    (app / 'config' / 'balance_rules.json').write_text((app / 'config' / 'balance_rules.json').read_text() + '\n')   # user-edited config
    return app


def tree(app):
    out = {}
    for p in app.rglob('*'):
        rel = p.relative_to(app)
        if p.is_file() and rel.parts[0] not in ('patch_logs', 'patch_backups') and p.name != '.nbs_patch_state.json' and '__pycache__' not in rel.parts:
            out[rel.as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


@unittest.skipUnless(git_ok('3dcb6ef') and git_ok('289c59b'), 'Git history of the application not available')
class PatchPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='patch-'))
        sys.path.insert(0, str(APP / 'patching'))
        import build_patch
        cls.zip, cls.man = build_patch.build(cls.tmp / 'dist')
        cls.pkg = cls.tmp / 'pkg'
        with zipfile.ZipFile(cls.zip) as z:
            z.extractall(cls.pkg)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def engine(self, *args, env=None):
        e = {**os.environ, **(env or {})}
        e.pop('NBS_PATCH_FAIL_AFTER', None) if not env or 'NBS_PATCH_FAIL_AFTER' not in env else None
        r = subprocess.run([sys.executable, str(self.pkg / 'patch_engine.py')] + list(args), capture_output=True, text=True, env=e, timeout=1800)
        return r.returncode, r.stdout + r.stderr

    def test_zip_contents(self):
        names = set(zipfile.ZipFile(self.zip).namelist())
        for n in ('INSTALL_UPDATE.bat', 'patch_engine.py', 'manifest.json', 'ROLLBACK_UPDATE.bat', 'PATCH_NOTES.md', 'TEST_RESULTS.md'):
            self.assertIn(n, names)
        self.assertTrue(any(n.startswith('patch_files/nbs_control/studio/') for n in names))
        self.assertFalse([n for n in names if n.startswith(('patch_files/data/', 'patch_files/exports/', 'patch_files/inputs/'))])
        self.assertIn(b'\r\n', zipfile.ZipFile(self.zip).read('INSTALL_UPDATE.bat'))

    def test_install_repeat_rollback_on_initial_application(self):
        app = baseline('3dcb6ef', self.tmp / 'a')
        before = tree(app)
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch')
        self.assertEqual(rc, 0, out)
        self.assertIn('SUCCESS', out)
        self.assertIn('Regression tests (Studio + TB)', out)
        after = tree(app)
        for keep in ('data/bank_20260930.sqlite', 'exports/old_run/previous_report.xlsx', 'config/balance_rules.json'):
            self.assertEqual(before[keep], after[keep], keep)                         # user data and edited config untouched
        self.assertIn('nbs_control/studio/run.py', after)
        self.assertNotEqual(before['nbs_control/web.py'], after['nbs_control/web.py'])
        self.assertTrue((app / 'config' / 'studio.json').exists())
        state = json.loads((app / '.nbs_patch_state.json').read_text())
        self.assertEqual(state['current'], self.man['version'])
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch', '--skip-tests')
        self.assertEqual(rc, 0, out)
        self.assertIn('Already up to date', out)                                       # repeat installation is a no-op
        self.assertEqual(tree(app), after)
        rc, out = self.engine('rollback', '--app-dir', str(app), '--yes')
        self.assertEqual(rc, 0, out)
        self.assertEqual(tree(app), before)                                            # exact original restored

    def test_failure_mid_install_rolls_back(self):
        app = baseline('3dcb6ef', self.tmp / 'b')
        before = tree(app)
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch', '--skip-tests', env={'NBS_PATCH_FAIL_AFTER': '7'})
        self.assertEqual(rc, 2, out)
        self.assertIn('rolled back', out)
        self.assertEqual(tree(app), before)

    def test_tb_release_installation(self):
        app = baseline('289c59b', self.tmp / 'c')
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch', '--skip-tests')
        self.assertEqual(rc, 0, out)
        self.assertIn('REPLACE_KNOWN_VERSION', out)

    def test_locally_modified_files_get_anchored_insertions_only(self):
        app = baseline('3dcb6ef', self.tmp / 'd')
        for rel in ('nbs_control/web.py', 'nbs_control/cli.py'):
            p = app / rel
            p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n') + b'# local site change\r\n')   # CRLF + local edit
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch', '--skip-tests')
        self.assertEqual(rc, 0, out)
        self.assertIn('ANCHORED_INSERTIONS_ON_LOCAL_VERSION', out)
        web = (app / 'nbs_control' / 'web.py').read_bytes()
        self.assertIn(b'# local site change', web)
        self.assertIn(b'register_studio_routes', web)
        self.assertIn(b'\r\n', web)                                                    # line endings kept
        r = subprocess.run([sys.executable, '-m', 'nbs_control', 'studio-synthetic', '--dir', str(self.tmp / 'd_syn')], cwd=app,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_crlf_copy_of_known_version_is_recognised(self):
        app = baseline('3dcb6ef', self.tmp / 'e')
        p = app / 'nbs_control' / 'base.py'
        for rel in ('nbs_control/web.py', 'nbs_control/templates/base.html'):
            q = app / rel
            q.write_bytes(q.read_bytes().replace(b'\n', b'\r\n'))
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch', '--skip-tests', '--dry-run')
        self.assertEqual(rc, 0, out)
        self.assertIn('REPLACE_KNOWN_VERSION                  nbs_control/web.py', out)
        self.assertFalse(p.exists())

    def test_incompatible_installations_are_refused_without_change(self):
        empty = self.tmp / 'f'
        empty.mkdir()
        rc, out = self.engine('install', '--app-dir', str(empty), '--yes', '--no-launch')
        self.assertEqual(rc, 2)
        self.assertIn('No NBS Mapping Control installation found', out)
        app = baseline('3dcb6ef', self.tmp / 'g')
        cli = app / 'nbs_control' / 'cli.py'
        cli.write_text(cli.read_text().replace('    args = parser.parse_args(argv)\n', '    args = parser.parse_args(argv or None)\n'))
        before = tree(app)
        rc, out = self.engine('install', '--app-dir', str(app), '--yes', '--no-launch')
        self.assertEqual(rc, 2, out)
        self.assertIn('Nothing was changed', out)
        self.assertEqual(tree(app), before)
        self.assertFalse((app / 'patch_backups').exists())


if __name__ == '__main__':
    unittest.main()
