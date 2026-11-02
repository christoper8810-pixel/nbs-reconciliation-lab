# Remaining issues and open questions

## 1. Needs bank evidence (cannot be resolved in a cloud environment with synthetic data)

| # | Item | Why it matters | What is needed |
|---|---|---|---|
| R1 | **AC CONSOL_KEY layout is unverified.** Positions come from the historical example and the earlier loader. PRODUCT (5) and department (7) are candidates only. | The PRODUCT / SECTOR misalignment diagnostic tests data against the configured positions. If the positions are wrong, findings point the wrong way. Control C12 stays WARN. | The bank's `CONSOLIDATE.COND` record for the AC application, and a sample of keys with explicit CATEGORY / PRODUCT / SECTOR columns. Then set `verified: true` and the evidence in `config/tb_recon.json`. |
| R2 | **No production run has been made.** All results are synthetic. | No claim is made about the bank's TB, the real PRODUCT / SECTOR issue, or real differences. | Run `tb-recon` locally on Windows with the legacy cut-off TB, the actual pre-COB TB, PRODUCT_S3, the GL rules, internal-account and customer-account mappings, PL balances and post-COB movements. |
| R3 | **Contra / BL accounting treatment.** BL types are only identified by the configured list and prefix (`BL`). They allocate only through explicit rules. | Netting versus separate contra GL is an accounting policy decision. | Owner confirmation per BL type, and the AC.BALANCE.TYPE definitions. |
| R4 | **Sign convention per extract.** All multipliers are 1 (debit-positive assumed). | A sign reversal is detected (C08 / SIGN_CONVENTION_MISMATCH) but never auto-corrected. | Evidence of each extract's sign convention. |
| R5 | **Multi-target legacy GLs without an account-level population** stay unallocated (C06). | Expected balances for their candidate GLs are incomplete. | An allocation rule (balance type / status / category) or an account-level extract for those GLs. |
| R6 | **PL key tokens 5–12** are unnamed. PL sector and residence come only from explicit columns. | PL rules on those dimensions report DIMENSION_NOT_AVAILABLE. | The complete PL CONSOL.KEY dictionary, already requested in the earlier rebuild brief. |
| R7 | **Cutover date and TB date conventions** must be set per run (`cutover_date`). | Without them, post-COB movements cannot be placed (C09 INCOMPLETE). | The confirmed migration cutover date and the actual TB business date. |
| R8 | **Customer-account reference field.** Engine B reads `CUSTOMER_ACCOUNT_REF` (aliases `CUSTOMER_ACCOUNT`, `CUS_ACC_REF`). | The real INTERNAL_CUS_ACC extract may name the field differently. | The extract header; add an alias in `tables.ALIASES` if needed. |

## 2. Engineering follow-ups

| # | Item |
|---|---|
| E1 | **Repository hygiene.** The possibly sensitive files listed in CURRENT_STATE_ASSESSMENT.md §6 are still tracked, and remain in history. Removing them needs an owner decision and a history rewrite (e.g. `git filter-repo`), which this change deliberately did not do. 9 tracked `data/test_temp/nbs-template-*` folders, `.verification/`, `exports/temenos_review_20261020/update/payload/` and `p.out` / `p2.out` duplicate other files. |
| E2 | `Start_NBS_Rebuild.cmd` expects `wheels/` next to it. In Git the wheels are in `exports/transfer/wheels`. The release ZIP fixes this by copying them to `wheels/`; the Git layout is unchanged. |
| E3 | The bundled wheels cover Windows x64 and CPython 3.10–3.14 only (lxml and MarkupSafe are binary). Other platforms need internet or a mirror. `tbrecon` itself needs only openpyxl (pure Python) plus Flask for the UI. |
| E4 | GL-level root-cause attribution is heuristic where several defects overlap on one GL (confidence LOW, with the explained and residual amounts shown). Exact attribution needs account-level drill-down, which the GL page provides. |
| E5 | Memory: components are held in memory during a run. With caching this is fine for hundreds of thousands of rows. For tens of millions of rows, stream through SQLite instead (the indexed `run.sqlite` structure already exists for the output side). Reproducibility re-runs are skipped above 300,000 input rows (C10 then reports NOT_TESTED on the first run and compares with the previous identical run later). |
| E6 | The existing NBS rebuild uses `gl_mapping.line_parts`, which now benefits from fix A1 / A2. NBS lines generated earlier with literal ranges should be regenerated and compared once the bank database is available. |
| E7 | The two legacy-SQL test classes now skip when their excluded CSV is absent. Supplying those CSVs locally re-enables them. |
| E8 | The rule-file layout is the tool's own convention (RULE_ID, TYPE, TARGET_GL, BALANCE_TYPE, CATEGORY, PRODUCT, SECTOR, …). Loading the bank's GL Report sheet directly into Engine A, rather than through `gl_mapping.py` into the NBS rebuild, still needs a small column-mapping adapter once the sheet's exact columns are confirmed. |

## 3. Mapping Studio (studio-1.0.0)

| # | Item |
|---|---|
| S1 | **Real workbook not seen.** Sheets are recognised by name and columns by header text, using the existing adapter's letters as a disclosed fall-back. Confirm the column map on the first real run. Headers the Studio does not recognise are listed and are not used as conditions. |
| S2 | **Real BO report not seen.** It needs a line column and an amount column. Confirm the unit (thousands?), the sign convention and whether total lines are included. A global scale or sign pattern is detected and reported, but never applied automatically. |
| S3 | **Overlapping lines.** Whether BO counts a record that two lines match in both lines or in one is not known. The setting `overlap_policy` (ALL, the default and flagged, or MOST_SPECIFIC) must be confirmed. |
| S4 | **Formulas.** Formula cells that are not direct references and were saved without a calculated value are marked not executable. Fix: open and save the workbook in Excel once. |
| S5 | **Corrected copy limits.** The Excel library does not carry charts, images, pivot tables or external links into the corrected copy. When the workbook contains them, PATCH_AUDIT_LOG.xlsx lists them. Copying the approved cell values into the original by hand is then the alternative. |
| S6 | **Scope of proposals.** Each proposal changes one condition cell, one GL Mapping line cell, or moves a value between two columns of one row. Structural redesign (new lines, new allocation rules) is reported for Finance and never generated. |
| S7 | **Windows tests.** The `.bat` wrappers were not run on Windows in this environment; the patch engine they call was tested on Linux. Use `INSTALL_UPDATE.bat --dry-run` first. |
