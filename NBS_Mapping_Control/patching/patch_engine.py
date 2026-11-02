"""NBS Mapping Studio Windows patch engine (Python standard library only).

    python patch_engine.py install  [--app-dir DIR] [--yes] [--no-launch] [--skip-tests] [--dry-run]
    python patch_engine.py rollback [--app-dir DIR] [--yes] [--backup DIR]
    python patch_engine.py status   [--app-dir DIR]

Safety model
* Compatibility: the folder must contain the NBS Mapping Control package. Every file the patch changes must be a
  known version (compared with line endings normalised); a locally changed file only receives small anchored
  insertions, never a whole-file overwrite. If a required insertion point is missing the patch refuses.
* Preflight renders every new file in memory and compiles every Python file before anything is written.
* A backup of every file to be changed is written and verified (SHA-256) before the first change.
* Each file is written to a temporary name and moved into place. Any error restores the backup automatically.
* Databases, data/, exports/, inputs/ and existing configuration files are never written. New configuration files
  are only added when missing. New Studio tables are created by the application on first use (additive).
* After installation the update is validated in a separate Python process; failure triggers automatic rollback.
* Every step is logged in <app>/patch_logs/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = '.nbs_patch_state.json'
PROTECTED = ('data', 'exports', 'inputs', 'patch_backups', 'patch_logs')
PORTS = (8765, 8767)


class PatchError(Exception):
    pass


def nhash(data: bytes) -> str:
    """SHA-256 with CRLF normalised to LF (a Windows copy of a file matches its repository version)."""
    return hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()


def fhash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Log:
    def __init__(self, app=None):
        self.lines, self.path = [], None
        if app:
            d = app / 'patch_logs'
            d.mkdir(exist_ok=True)
            self.path = d / f'{dt.datetime.now():%Y%m%d-%H%M%S}_{os.getpid()}.log'

    def __call__(self, msg):
        line = f'{dt.datetime.now():%H:%M:%S} {msg}'
        print(line, flush=True)
        self.lines.append(line)
        if self.path:
            with self.path.open('a', encoding='utf-8') as f:
                f.write(line + '\n')


def manifest():
    return json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))


# ------------------------------------------------------------------ locating and checking the application
def is_app(p: Path):
    return (p / 'nbs_control' / '__init__.py').exists() and (p / 'nbs_control' / 'web.py').exists() and (p / 'config').is_dir()


def resolve_app(arg, interactive):
    cands = []
    if arg:
        cands.append(Path(arg))
    else:
        cands += [HERE.parent, HERE.parent / 'NBS_Mapping_Control', HERE.parent.parent, HERE.parent.parent / 'NBS_Mapping_Control',
                  Path.home() / 'NBS_Mapping_Control', Path('C:/NBS_Mapping_Control'), Path.cwd()]
    for c in cands:
        for p in (c, c / 'NBS_Mapping_Control'):
            if is_app(p):
                if arg or not interactive or _confirm(f'Install the update into {p.resolve()}?'):
                    return p.resolve()
    if interactive:
        chosen = _choose_folder()
        if chosen:
            for p in (Path(chosen), Path(chosen) / 'NBS_Mapping_Control'):
                if is_app(p):
                    return p.resolve()
    raise PatchError('No NBS Mapping Control installation found. Run INSTALL_UPDATE.bat --app-dir "C:\\path\\to\\NBS_Mapping_Control" '
                     'or choose the folder that contains nbs_control\\ and config\\.')


def _confirm(q):
    try:
        return input(q + ' [Y/n] ').strip().lower() in ('', 'y', 'yes')
    except EOFError:
        return False


def _choose_folder():
    try:
        import tkinter
        from tkinter import filedialog
        root = tkinter.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        d = filedialog.askdirectory(title='Select the NBS_Mapping_Control application folder')
        root.destroy()
        return d or None
    except Exception:  # noqa: BLE001 - no GUI available
        try:
            return input('Path of the NBS_Mapping_Control folder: ').strip().strip('"') or None
        except EOFError:
            return None


def app_running():
    busy = []
    for port in PORTS:
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                busy.append(port)
    return busy


def locked(paths):
    out = []
    for p in paths:
        if p.exists():
            try:
                with p.open('r+b'):
                    pass
            except OSError:
                out.append(str(p))
    return out


# ------------------------------------------------------------------ planning
def _apply_ops(text, ops, path):
    """Anchored insertions for a locally modified file. Returns new text or raises PatchError."""
    nl = '\r\n' if '\r\n' in text else '\n'
    t = text.replace('\r\n', '\n')
    for op in ops:
        if op['marker'] in t:
            continue
        anchor = op['anchor']
        if t.count(anchor) != 1:
            raise PatchError(f'{path}: insertion point not found exactly once ({anchor.strip()[:60]!r}); the file differs too much '
                             'from any known version')
        if op['op'] == 'insert_before':
            t = t.replace(anchor, op['text'] + anchor, 1)
        elif op['op'] == 'insert_after':
            t = t.replace(anchor, anchor + op['text'], 1)
        else:
            raise PatchError(f'unknown op {op["op"]}')
    return t.replace('\n', nl)


def plan(app: Path, man, log):
    steps, problems, warnings = [], [], []
    for f in man['files']:
        target = app / f['path']
        if Path(f['path']).parts[0] in PROTECTED:
            raise PatchError(f'manifest tries to write protected path {f["path"]}')
        new = (HERE / 'patch_files' / f['path']).read_bytes() if f['action'] != 'ops_only' else None
        exists = target.exists()
        cur = target.read_bytes() if exists else None
        if f['action'] == 'config_add_if_missing':
            steps.append({'path': f['path'], 'do': 'KEEP_EXISTING_CONFIG' if exists else 'ADD', 'data': None if exists else new})
            continue
        if exists and nhash(cur) == f['new_sha256']:
            steps.append({'path': f['path'], 'do': 'ALREADY_UP_TO_DATE', 'data': None})
            continue
        if not exists:
            if f['action'] == 'modify':
                (problems if f.get('required') else warnings).append(f'{f["path"]} is missing from the installation')
                continue
            steps.append({'path': f['path'], 'do': 'ADD', 'data': new})
            continue
        if f['action'] == 'add':                       # a file this patch adds already exists
            if nhash(cur) in f.get('accepted_sha256', []):
                steps.append({'path': f['path'], 'do': 'REPLACE_KNOWN_VERSION', 'data': new})
            else:
                warnings.append(f'{f["path"]} exists with local changes; it is replaced (the original is kept in the backup)')
                steps.append({'path': f['path'], 'do': 'REPLACE_LOCAL_CHANGES_BACKED_UP', 'data': new})
            continue
        if nhash(cur) in f.get('accepted_sha256', []):
            steps.append({'path': f['path'], 'do': 'REPLACE_KNOWN_VERSION', 'data': new})
        elif f.get('ops'):
            try:
                data = _apply_ops(cur.decode('utf-8'), f['ops'], f['path']).encode('utf-8')
                steps.append({'path': f['path'], 'do': 'ANCHORED_INSERTIONS_ON_LOCAL_VERSION', 'data': data})
                warnings.append(f'{f["path"]} differs from the known versions; only the anchored insertions were applied')
            except PatchError as exc:
                (problems if f.get('required') else warnings).append(str(exc))
        else:
            msg = f'{f["path"]} differs from the known versions; {"cannot update safely" if f.get("required") else "optional fix not applied"}'
            (problems if f.get('required') else warnings).append(msg)
    for s in steps:
        if s['data'] is not None and s['path'].endswith('.py'):
            try:
                compile(s['data'].decode('utf-8'), s['path'], 'exec')
            except SyntaxError as exc:
                problems.append(f'{s["path"]}: rendered file does not compile: {exc}')
    return steps, problems, warnings


# ------------------------------------------------------------------ backup / apply / restore
def backup(app, steps, man, log):
    d = app / 'patch_backups' / f'{man["patch_id"]}_{dt.datetime.now():%Y%m%d-%H%M%S}'
    (d / 'files').mkdir(parents=True)
    entries = []
    for s in steps:
        if s['data'] is None:
            continue
        t = app / s['path']
        e = {'path': s['path'], 'existed': t.exists(), 'action': s['do']}
        if t.exists():
            b = d / 'files' / s['path']
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(t, b)
            e['sha256'] = fhash(t)
            if fhash(b) != e['sha256']:
                raise PatchError(f'backup verification failed for {s["path"]}')
        entries.append(e)
    (d / 'backup_manifest.json').write_text(json.dumps({'patch_id': man['patch_id'], 'version': man['version'], 'app': str(app),
                                                        'created': dt.datetime.now().isoformat(timespec='seconds'), 'files': entries}, indent=1))
    log(f'Backup written and verified: {d} ({sum(1 for e in entries if e["existed"])} files backed up, '
        f'{sum(1 for e in entries if not e["existed"])} new files recorded)')
    return d


def restore(app, bdir, log):
    bm = json.loads((bdir / 'backup_manifest.json').read_text(encoding='utf-8'))
    errors = []
    for e in reversed(bm['files']):
        t = app / e['path']
        try:
            if e['existed']:
                tmp = t.with_name(t.name + '.restore-tmp')
                shutil.copy2(bdir / 'files' / e['path'], tmp)
                os.replace(tmp, t)
                if fhash(t) != e['sha256']:
                    errors.append(f'{e["path"]}: restored file hash mismatch')
            elif t.exists():
                t.unlink()
        except OSError as exc:
            errors.append(f'{e["path"]}: {exc}')
    for e in bm['files']:                               # remove directories the patch created and left empty
        p = (app / e['path']).parent
        while p != app and p.exists() and not any(p.iterdir()):
            p.rmdir()
            p = p.parent
    if errors:
        raise PatchError('Restore incomplete: ' + '; '.join(errors) + f'. Copy the files manually from {bdir / "files"}')
    log(f'Restored {sum(1 for e in bm["files"] if e["existed"])} file(s) and removed {sum(1 for e in bm["files"] if not e["existed"])} '
        f'added file(s) from {bdir}')


def apply(app, steps, log):
    fail_after = int(os.environ.get('NBS_PATCH_FAIL_AFTER', '-1'))
    n = 0
    for s in steps:
        if s['data'] is None:
            continue
        if n == fail_after:
            raise PatchError('simulated failure (NBS_PATCH_FAIL_AFTER) during installation')
        t = app / s['path']
        t.parent.mkdir(parents=True, exist_ok=True)
        tmp = t.with_name(t.name + '.patch-tmp')
        tmp.write_bytes(s['data'])
        os.replace(tmp, t)
        n += 1
    log(f'{n} file(s) written')


def data_snapshot(app):
    snap = {}
    for sub in ('data', 'inputs'):
        d = app / sub
        if d.exists():
            for p in d.rglob('*'):
                if p.is_file():
                    st = p.stat()
                    snap[str(p.relative_to(app))] = (st.st_size, st.st_mtime_ns)
    for p in (app / 'config').glob('*.json'):
        snap[str(p.relative_to(app))] = fhash(p)
    return snap


def validate(app, man, skip_tests, log):
    py = sys.executable
    code = ('import sys; sys.path.insert(0, "."); import nbs_control.web, nbs_control.cli, nbs_control.studio.run, nbs_control.tbrecon.run; '
            'from nbs_control.studio import STUDIO_VERSION; assert STUDIO_VERSION == %r; print("import ok")' % man['version'])
    r = subprocess.run([py, '-c', code], cwd=app, capture_output=True, text=True, timeout=300)
    log('Import check: ' + (r.stdout.strip() or r.stderr.strip()[-400:]))
    if r.returncode != 0:
        return False
    smoke = ('import sys, tempfile, shutil, pathlib; sys.path.insert(0, ".");'
             'from nbs_control.service import ControlService; from nbs_control.web import create_app;'
             't = pathlib.Path(tempfile.mkdtemp()); shutil.copytree("config", t / "config", ignore=shutil.ignore_patterns("history", "mapping_versions", "policy_history"));'
             'app = create_app(ControlService(t / "config", t / "data", t / "supplied"), export_dir=t / "exports");'
             'c = app.test_client(); codes = [c.get(u).status_code for u in ("/studio", "/tb")]; shutil.rmtree(t, ignore_errors=True);'
             'print("pages", codes); assert codes == [200, 200]')
    r = subprocess.run([py, '-c', smoke], cwd=app, capture_output=True, text=True, timeout=300)
    log('Web smoke test: ' + (r.stdout.strip() or r.stderr.strip()[-400:]))
    if r.returncode != 0:
        return False
    if not skip_tests:
        r = subprocess.run([py, '-m', 'unittest', 'tests.test_studio', 'tests.test_tbrecon'], cwd=app, capture_output=True, text=True, timeout=1800)
        tail = (r.stderr or r.stdout).strip().splitlines()[-3:]
        log('Regression tests (Studio + TB): ' + ' | '.join(tail))
        if r.returncode != 0:
            return False
    return True


def ensure_dependencies(log):
    missing = []
    for mod in ('flask', 'openpyxl', 'werkzeug'):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if not missing:
        return
    wheels = HERE / 'wheels'
    log(f'Missing Python packages {missing}; installing for the current user from the bundled wheels (offline)')
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '--no-index', '--find-links', str(wheels), 'flask', 'openpyxl'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise PatchError('Required packages could not be installed offline: ' + r.stderr.strip()[-300:])


# ------------------------------------------------------------------ commands
def install(args):
    man = manifest()
    pre = Log()
    pre(f'NBS Mapping Studio update {man["version"]} ({man["patch_id"]})')
    if sys.version_info < (3, 10):
        raise PatchError(f'Python 3.10 or newer is required (found {sys.version.split()[0]})')
    app = resolve_app(args.app_dir, not args.yes)
    log = Log(app)
    for line in pre.lines:
        log(line.split(' ', 1)[1])
    log(f'Application folder: {app}')
    busy = app_running()
    while busy:
        msg = f'The application is running (port {", ".join(map(str, busy))}). Close its window before updating.'
        if args.yes or not _confirm(msg + ' Closed it - try again?'):
            raise PatchError(msg)
        busy = app_running()
    ensure_dependencies(log)
    steps, problems, warnings = plan(app, man, log)
    for s in steps:
        log(f'  {s["do"]:38} {s["path"]}')
    for w in warnings:
        log('WARNING ' + w)
    if problems:
        for p in problems:
            log('REFUSED ' + p)
        raise PatchError('The installation is not compatible with this update. Nothing was changed.')
    todo = [s for s in steps if s['data'] is not None]
    lock = locked([app / s['path'] for s in todo])
    if lock:
        raise PatchError('Files are in use (close the application and any editor): ' + ', '.join(lock))
    if args.dry_run:
        log(f'Dry run: {len(todo)} file(s) would change. Nothing was changed.')
        return 0
    before = data_snapshot(app)
    if not todo:
        log('Already up to date: no file needs to change.')
        bdir = None
    else:
        bdir = backup(app, steps, man, log)
        try:
            apply(app, todo, log)
        except Exception as exc:  # noqa: BLE001
            log(f'ERROR during installation: {exc}. Restoring the backup ...')
            restore(app, bdir, log)
            raise PatchError('Update failed and was rolled back; the application is unchanged.') from exc
    ok = validate(app, man, args.skip_tests, log)
    after = data_snapshot(app)
    written = {s['path'] for s in todo}
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k) and k.replace(os.sep, '/') not in written)
    if changed:
        log('ERROR: data or configuration files changed during installation: ' + ', '.join(changed[:20]))
        ok = False
    if not ok:
        if bdir:
            log('Validation failed. Restoring the backup ...')
            restore(app, bdir, log)
            raise PatchError('Validation of the updated application failed; the update was rolled back and the application is unchanged.')
        raise PatchError('Validation failed on an installation that was already up to date; see the log.')
    state_p = app / STATE
    state = json.loads(state_p.read_text(encoding='utf-8')) if state_p.exists() else {'history': []}
    if bdir:
        state['history'].append({'patch_id': man['patch_id'], 'version': man['version'], 'installed': dt.datetime.now().isoformat(timespec='seconds'),
                                 'backup': str(bdir), 'log': str(log.path)})
    state['current'] = man['version']
    state_p.write_text(json.dumps(state, indent=1), encoding='utf-8')
    log(f'SUCCESS: NBS Mapping Studio {man["version"]} installed and validated. Log: {log.path}')
    if bdir:
        log(f'Rollback at any time: ROLLBACK_UPDATE.bat (backup {bdir})')
    if not args.no_launch:
        launcher = app / 'Start_Mapping_Studio.cmd'
        if os.name == 'nt' and launcher.exists():
            log('Starting the application ...')
            subprocess.Popen(['cmd', '/c', 'start', '', str(launcher)], cwd=app)
        else:
            log(f'Start the application with {launcher}')
    return 0


def rollback(args):
    app = resolve_app(args.app_dir, not args.yes)
    log = Log(app)
    if app_running():
        raise PatchError('Close the application before rolling back.')
    state_p = app / STATE
    state = json.loads(state_p.read_text(encoding='utf-8')) if state_p.exists() else {'history': []}
    if args.backup:
        bdir = Path(args.backup)
    elif state['history']:
        bdir = Path(state['history'][-1]['backup'])
    else:
        raise PatchError('No installed update recorded in this folder; nothing to roll back.')
    if not (bdir / 'backup_manifest.json').exists():
        raise PatchError(f'Backup not found: {bdir}')
    if not args.yes and not _confirm(f'Restore the application from {bdir}?'):
        return 1
    before = data_snapshot(app)
    restore(app, bdir, log)
    if before != data_snapshot(app):
        log('WARNING: data/configuration snapshot changed during rollback')
    state['history'] = [h for h in state['history'] if h['backup'] != str(bdir)]
    state['current'] = state['history'][-1]['version'] if state['history'] else None
    state_p.write_text(json.dumps(state, indent=1), encoding='utf-8')
    log('SUCCESS: application restored to the version before the update.')
    return 0


def status(args):
    app = resolve_app(args.app_dir, False)
    man = manifest()
    steps, problems, warnings = plan(app, man, Log())
    state = json.loads((app / STATE).read_text(encoding='utf-8')) if (app / STATE).exists() else {}
    print(json.dumps({'app': str(app), 'installed': state.get('current'), 'patch': man['version'],
                      'pending_changes': sum(1 for s in steps if s['data'] is not None), 'problems': problems, 'warnings': warnings}, indent=1))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='NBS Mapping Studio update')
    ap.add_argument('command', choices=('install', 'rollback', 'status'))
    ap.add_argument('--app-dir')
    ap.add_argument('--yes', action='store_true', help='non-interactive')
    ap.add_argument('--no-launch', action='store_true')
    ap.add_argument('--skip-tests', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--backup')
    a = ap.parse_args(argv)
    try:
        return {'install': install, 'rollback': rollback, 'status': status}[a.command](a)
    except PatchError as exc:
        print(f'\nNOT COMPLETED: {exc}', flush=True)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
