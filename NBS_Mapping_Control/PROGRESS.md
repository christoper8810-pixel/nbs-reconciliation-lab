# Progress

No `PROGRESS.md` existed before this change. This file starts the record. Earlier history is visible only through the dated review folders in `exports/` (17–25 October 2026) and the configuration versions in `config/mapping_versions/`.

## 2026-11-02: whole-TB migration reconciliation (`tbrecon-1.0.0`)

Done:
- Forensic baseline: CURRENT_STATE_ASSESSMENT.md (baseline 187 tests, 2 errors, 13 skipped; no TB reconciliation engine existed; 6 defects identified; possibly sensitive tracked files listed without being processed).
- Fixed the GL Report adapter's inline ranges and balance-type lists, made the ECB CONSOL_KEY positions configurable, and made the two tests depending on an excluded CSV skip.
- New `nbs_control/tbrecon`: Engine A (PRODUCT_S3 atomic balance types), Engine B (INTERNAL_CUS_ACC one-to-one), Engine C (PL own layout), DIRECT stream, whole-TB aggregation, GL Report H / D / T, pre / post-COB roll-forward, benchmark, root-cause classification, systemic issues, correction worklist, 13 controls, persistent runs and rule versions, Excel / CSV / HTML / audit-JSON exports, web pages and CLI commands.
- POSSIBLE_MAPPING_COLUMN_MISALIGNMENT diagnostic with evidence and a proposed correction.
- Synthetic generator (clean and 19-defect scenarios) with independent truth. 45 new tests. Full suite: 237 tests OK, 20 skipped.
- Windows launcher `Start_TB_Reconciliation.cmd`, guide TB_RECON_GUIDE.md, `build_release.py`.

Next (see REMAINING_ISSUES.md):
1. Obtain CONSOLIDATE.COND and verify the AC layout (R1), then run on the real files locally (R2).
2. Owner decisions on worklist items: contra treatment, ambiguous rules, multi-target allocation design, sign convention.
3. Repository clean-up of sensitive and duplicate files (E1), an owner decision.

## 2026-11-02: NBS Mapping Studio (`studio-1.0.0`) and Windows patch

Done:
- **Baseline:** the GL mapping workbook was read only at fixed column letters. Its conditions were never executed, there was no reconciliation against a BO report, and no corrections were proposed. The TB reconciliation is kept as a separate tool.
- **New `nbs_control/studio`:**
  - a workbook condition compiler that keeps the exact cell of every condition;
  - cross-sheet validation;
  - the expected BO allocation built from the source records, and reconciliation against the BO report;
  - automatic investigation by verified what-if re-execution, with HIGH / MEDIUM / LOW / UNRESOLVED confidence;
  - responsibility classification (MAPPING / BO_REPORT / SOURCE_DATA / TIMING);
  - approvals with an audit trail;
  - a corrected copy, verified cell by cell against the original;
  - a rerun, reports A–G, an 11-step web workflow and CLI commands.
- **Fixes found while testing:**
  - a blank column value was being treated as an unknown dimension;
  - edits that created a double allocation were being accepted as improvements;
  - a formula cell saved without a calculated value was read as blank. Direct references are now resolved, and other such formulas are flagged as not executable.
- **Windows patch** (`patching/`): `NBS_Mapping_Studio_Update.zip` with compatibility check, verified backup, atomic installation, validation, automatic rollback and `ROLLBACK_UPDATE.bat`.
- **Tests:** 263 run, OK, 20 skipped. Details in MAPPING_STUDIO_VALIDATION.md and patching/TEST_RESULTS.md.

Next:
1. First real run: upload the real mapping workbook, BO report and source extract. Check the column recognition on the "Compiled workbook conditions" page, and confirm the BO amount unit, sign and overlap policy.
2. Finance decisions on MEDIUM / LOW proposals and on the evidence requests in FINANCE_DECISION_WORKLIST.xlsx.
