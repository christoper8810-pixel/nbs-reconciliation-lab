# NBS Mapping Studio update (studio-1.0.0)

## Install (no GitHub, no administrator rights, no internet)

1. Close NBS Mapping Control if it is running (its black window).
2. Download `NBS_Mapping_Studio_Update.zip`. Right-click → Properties → tick **Unblock** if shown → OK.
3. Extract it, ideally next to or inside your `NBS_Mapping_Control` folder.
4. Double-click **`INSTALL_UPDATE.bat`**. Confirm the application folder it found, or pick it in the folder dialog. The folder is the one that contains `nbs_control\` and `config\`.
5. The installer checks compatibility, backs up, installs, validates the updated application (including its regression tests), and then starts **Mapping Studio** at `http://127.0.0.1:8765/studio`.

If anything fails, the installer restores the backup automatically and tells you that the application is unchanged. To undo a successful update later, double-click **`ROLLBACK_UPDATE.bat`**.

Command-line options, for example to give the folder explicitly:

```bash
python patch_engine.py install --app-dir "C:\NBS_Mapping_Control"
```

The other options are `--dry-run` (show what would change), `--skip-tests` (faster validation) and `--no-launch`. Status and rollback:

```bash
python patch_engine.py status --app-dir "C:\NBS_Mapping_Control"
```

```bash
python patch_engine.py rollback --app-dir "C:\NBS_Mapping_Control"
```

## What the installer guarantees

- **Never written:** `data\`, `exports\`, `inputs\`, your existing `config\*.json`, databases, mapping records, previous reports and decisions. A snapshot of `data\`, `inputs\` and `config\` is compared before and after installation.
- **Compatibility check:** every file the update changes must be a known version of NBS Mapping Control; line endings are ignored. A locally changed `web.py`, `cli.py` or `base.html` receives only small anchored insertions (route registration, menu links, commands). If an insertion point is missing, the update refuses and changes nothing. Optional fixes (`gl_mapping.py`, `bank_data.py`, `tests/test_rebuild.py`, `README.md`) are skipped with a warning on locally changed copies.
- **Backup first:** every file to be replaced is copied to `patch_backups\<update>_<time>\` and verified by SHA-256 before the first change.
- **No partial updates:** files are written to a temporary name and moved into place. Any error restores the backup.
- **Validation:** imports, the Studio and TB web pages, and the Studio and TB regression tests run in a separate process. Failure triggers automatic rollback.
- **Database migration:** none is needed. Mapping Studio keeps its own new store `data\studio\studio.sqlite`, created with additive `CREATE TABLE IF NOT EXISTS` on first use. Existing databases are never opened by the installer.
- **Running application:** an application window still open (ports 8765 / 8767) or a locked file stops the installer before any change.
- **Logs:** every run is logged in `patch_logs\`. `.nbs_patch_state.json` records the installed version and its backup.
- **Offline dependencies:** Flask and openpyxl are installed for the current user from the bundled `wheels\` only if they are missing.

## What is new

**Mapping Studio** (menu: *Mapping Studio*), the Excel-driven mapping validation, BO reconciliation and correction workflow:

1. Upload the mapping workbook, the BO-generated report and the supporting source records (file upload or local path).
2. **Rule compiler.** The workbook's own conditions are executed, with the exact cell of every condition kept:
   - GL Report lines (H / D / T) and criteria rows, continuation rows and `^` inheritance;
   - named ranges, workbook defined names and CATEGORY range groups;
   - cross-sheet formula references, including formulas saved without a calculated value;
   - lists separated by comma, space or new line, inclusive ranges, `>= / <=` comparisons, wildcards, and exclusions (`NOT`, `!`, `<>`, `EXCL`);
   - explicit blank and ANY semantics.

   Anything uninterpretable is flagged with its cell, never ignored or guessed.
3. **Validation** across GL Report, GL Mapping, CATEGORY, SEGMENT, COA, BRANCH, DAO, PRODUCT, COMPANY, CURRENCY and BALANCE TYPE sheets:
   - unknown codes, reversed ranges, overlapping and contradictory conditions;
   - unallocated lines, total-line hierarchy;
   - GL Mapping line, category and GL consistency;
   - PRODUCT / SECTOR column misalignment;
   - unallocated, double-allocated and undecided source records.
4. **Expected BO allocation** from the source records, and **reconciliation** with the BO report. The grain is the report line plus every dimension both files carry, such as currency or branch. BO internal totals are also checked.
5. **Automatic investigation.** Candidate single-cell corrections are verified by re-executing the workbook. Each proposal carries the worksheet, cell, existing and proposed value, reason, evidence, affected records, financial impact and a HIGH / MEDIUM / LOW confidence. Differences caused by the BO report (sign, unit, duplicate rows, lines not in the workbook) or by the source data are classified separately and are not "fixed" in the mapping. Where the BO report is too summarised to prove a cause, the specific evidence needed is requested.
6. **Approval:** one click for all HIGH proposals, individual decisions otherwise, with name and reason, and an audit trail.
7. **Corrected copy.** `CORRECTED_MAPPING_PREVIEW.xlsx` contains the approved edits only. It is verified cell by cell against the original: values, formulas, formats, comments and merged cells. The original file is never changed.
8. **Rerun** on the corrected copy, with a before-and-after summary.
9. **Reports:**
   - `BO_RECONCILIATION.xlsx`
   - `PROPOSED_MAPPING_PATCH.xlsx`
   - `CORRECTED_MAPPING_PREVIEW.xlsx`
   - `FINANCE_DECISION_WORKLIST.xlsx`
   - `MAPPING_VALIDATION_REPORT.xlsx`
   - `PATCH_AUDIT_LOG.xlsx`
   - `EXECUTIVE_SUMMARY.html`

Also included:
- The whole-TB reconciliation, kept as a separate tool in the menu.
- Fixes to the existing GL Report adapter: inline ranges such as `1000-1999, 6001` and listed balance types are now read correctly.
- Configurable ECB CONSOL_KEY positions, with the same defaults.

## Limits (see TEST_RESULTS.md)

All validation used SYNTHETIC files. The real mapping workbook and BO report were not available, so the column recognition and the BO column names must be confirmed on the first real run:
- The **Compiled workbook conditions** page shows every recognised sheet and column, and marks positional fall-backs.
- A BO report needs a line column (`LINE` / `DKBGL` / `REPORT_LINE` / `QCB_ITEM_CODE`) and an amount column (`AMOUNT` / `BALANCE` / `VALUE`).

Formulas other than direct references, saved without a calculated value, are reported as not executable. Open and save the workbook in Excel once so the values are calculated. The Excel library does not carry charts, images or pivot tables into the corrected copy; these are listed in `PATCH_AUDIT_LOG.xlsx` when present.
