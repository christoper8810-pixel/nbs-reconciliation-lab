# TEST_RESULTS: NBS Mapping Studio update studio-1.0.0

Actual results of runs on 2 November 2026 in a Linux cloud container (Python 3.13, openpyxl 3.1.5, Flask 3.1.3), with **SYNTHETIC data only**. The bank's real mapping workbook, BO report and Windows installation were not available here.

## 1. Full application test suite

Command:

```bash
python -m unittest discover -s tests -t .
```

Result: **Ran 263 tests in 55.812s; OK (skipped=20)**. 0 failures, 0 errors.

| Suite | Tests |
|---|---|
| Existing application (owner review, rebuild, generation, ECB adapter, selectors, QCB, Temenos review) | 192 |
| TB reconciliation, the separate tool (`tests/test_tbrecon.py`) | 45 |
| Mapping Studio (`tests/test_studio.py`) | 19 |
| Windows patch package (`tests/test_patch_package.py`) | 7 |

The 20 skipped tests need bank inputs that are not in Git. The skip reasons reported were: QCB files not present; generated bank workbook not available; legacy balance-sheet SQL CASE extract (excluded *.csv) not on this machine; no real run yet; original workbooks not on this machine; real category source not available; real store not built; starter review workbook not present; template missing.

## 2. Mapping Studio tests

- **Condition grammar:**
  - alternatives separated by comma, space, semicolon or new line;
  - inclusive ranges, comparisons, wildcards and exclusions;
  - named ranges and explicit blank / ANY;
  - malformed or undefined input rejected;
  - overlap test.
- **Workbook reading:**
  - sheet roles found;
  - columns found by header text, with any positional fall-back disclosed;
  - a cross-sheet formula reference and a workbook defined name;
  - a formula without a calculated value is resolved, or flagged as not executable (never read as blank).
- **Line structure:** continuation rows and `^` inheritance; members of total lines inferred and disclosed.
- **Clean scenario:** the expected allocation equals the independently generated truth; 19 of 19 BO keys match; no proposals.
- **Defect scenario:** each of the 8 injected workbook defects yields exactly the expected worksheet, cell, existing value, proposed value and confidence. The 4 injected BO-side and source-side defects are classified as BO_REPORT, SOURCE_DATA or MAPPING_OR_BO, not as mapping changes.
- **Edge cases:**
  - both overlap policies;
  - a BO report with no source records yields evidence requests and no invented corrections;
  - BO amount-scale detection.
- **Approval and corrected copy:**
  - every decision needs a name and a reason, and UNRESOLVED items cannot be approved;
  - only approved edits go into the corrected copy: 8 edits, every other cell unchanged, the original file's SHA-256 unchanged;
  - a formula, a comment and merged cells are preserved;
  - a cell that no longer holds the expected value is refused;
  - the Finance worklist leaves out approved HIGH items;
  - the rerun improves from 5 of 23 to 16 of 21 matched keys.
- **Interfaces:**
  - CLI exit codes;
  - the full web workflow: file upload, background job, dashboard, drill-down, proposals, validation, compiled rules, approval, export, download, and path traversal refused.
- **Scale:** 40,000 records analysed within the test's time limit. Measured separately: 200,000 records (9,043 signatures) in 9.1 s.

## 3. Windows patch tests (`patch_engine.py`)

The test installations are copies of the application rebuilt from Git history. Synthetic user data was added: a database file, a previous report and an edited configuration file.

| Test | Result |
|---|---|
| ZIP contents | INSTALL_UPDATE.bat, patch_engine.py, patch_files/, manifest.json, ROLLBACK_UPDATE.bat, PATCH_NOTES.md and TEST_RESULTS.md are present. Nothing from data/, exports/ or inputs/. Batch files use CRLF. |
| Install on the initial application (commit 3dcb6ef) | Success. The backup was verified. The database, previous report and edited configuration are byte-identical afterwards. The import check, the web smoke test (/studio and /tb return 200) and the Studio and TB regression tests all passed inside the installed copy. |
| Repeat installation | "Already up to date"; no file changed. |
| Rollback | Every file restored; the application tree is byte-identical to the original. |
| Simulated failure after 7 files | Automatic rollback; the tree is byte-identical to the original. |
| Install on the TB release (commit 289c59b) | Success; the known file versions were replaced. |
| Locally modified web.py and cli.py (CRLF line endings plus an extra line) | Only the anchored insertions were applied. The local line and the CRLF line endings were kept, and the updated command line works. |
| CRLF copy of a known version | Recognised as that known version. |
| Folder without the application | Refused. |
| cli.py without the required insertion point | Refused. Nothing was written and no backup folder was created. |

Not tested here: running the `.bat` files and launching the browser on a real Windows desktop, because the container runs Linux. The `.bat` files only find Python (`python`, or `py -3`) and call `patch_engine.py`, which is what was tested. On the first Windows install you can preview the changes without applying them:

```bash
INSTALL_UPDATE.bat --dry-run
```
