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
