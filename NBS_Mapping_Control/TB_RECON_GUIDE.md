# TB reconciliation: Windows installation, launch and input guide

The whole-TB migration reconciliation runs locally. It needs no administrator rights, no internet and no bank connection.

## 1. Install (once)

1. Install Python 3.10–3.14 for the current user from python.org. No administrator rights are needed; tick "Add python.exe to PATH".
2. Unzip the release (for example `NBS_Mapping_Control_tbrecon-1.0.0_<date>.zip`) to a folder you own, such as `C:\Users\<you>\NBS_Mapping_Control`. If Windows marks the ZIP as blocked: right-click → Properties → Unblock, before unzipping.
3. Double-click **`Start_TB_Reconciliation.cmd`**. On first start it installs Flask, openpyxl and lxml into your user profile from the bundled `wheels` folder (offline):

```bash
python -m pip install --user --no-index --find-links wheels -r requirements.txt
```

With a proxy or an internal mirror, the normal `pip install --user -r requirements.txt` with `--proxy` or `--index-url` also works.

4. The browser opens `http://127.0.0.1:8765/tb`. Keep the black window open while you work. The server listens on this computer only.

Check the installation:

```bash
python -m unittest discover -s tests -t .
```

## 2. Prepare an input folder

Put the files in one folder, as `.csv` or `.xlsx` (first sheet, first non-empty row = header). Missing files leave the affected analysis SOURCE_PENDING / INCOMPLETE; they never produce a false success.

| File | Required columns (aliases accepted) | Stream |
|---|---|---|
| `legacy_tb` | LEGACY_GL (OLD_GL, ETHIX_GL), CURRENCY (CCY), BALANCE (AMOUNT); optional CLASS = BS / PL / OBS | source of expected balances |
| `actual_tb` | TARGET_GL (DKB_GL, TRANSACT_GL), CURRENCY, BALANCE, BUSINESS_DATE; optional CLASS | Temenos pre-COB or dated actual |
| `gl_mapping` | LEGACY_GL, TARGET_GL (several GLs comma-separated allowed); optional CURRENCY | authorised legacy → target mapping |
| `asset_balances` | ACCOUNT_NO and / or ARRANGEMENT_ID, CONSOL_KEY, LEGACY_GL, `<TYPE>_BAL_QAR` columns; optional explicit STATUS / PRODUCT / … | Engine A |
| `gl_rules` | RULE_ID (LINE), TYPE (H / D / T), DESCRIPTION, TARGET_GL, BALANCE_TYPE, criteria columns CATEGORY, PRODUCT, SECTOR, DEPARTMENT, RESIDENCE, INDUSTRY, MATURITY, CURRENCY, COMPANY, STATUS; PRIORITY; TOTAL_OF; RANGE_NAME + RANGE_VALUES | Engine A |
| `internal_balances` | ACCOUNT_NO, CURRENCY, BALANCE, LEGACY_GL; optional CUSTOMER_ACCOUNT_REF | Engine B |
| `internal_mapping` | ACCOUNT_NO (SOURCE_ACCOUNT), TARGET_ACCOUNT and / or TARGET_GL | Engine B |
| `customer_account_mapping` | ACCOUNT_NO (LEGACY_ACCOUNT), TARGET_ACCOUNT, TARGET_GL | Engine B (Nostro / Vostro refs) |
| `target_accounts` (optional) | TARGET_ACCOUNT, TARGET_GL, BALANCE | Engine B account-level check |
| `pl_balances` | CONSOL_KEY (PL layout) and / or PL_CATEGORY, PRODUCT, DEPARTMENT, SECTOR, RESIDENCE, CURRENCY, COMPANY; BALANCE; LEGACY_GL | Engine C |
| `pl_rules` | RULE_ID, TARGET_GL, and any of the PL dimensions above | Engine C |
| `post_cob_movements` | TARGET_GL, CURRENCY, BALANCE (AMOUNT), BUSINESS_DATE; optional MOVEMENT_TYPE, VALIDATED (Y / N) | roll-forward |
| `TrialBalance_withConsolKey` | TARGET_GL, CURRENCY, BALANCE | independent benchmark only |

Optional `tb_recon.json` in the same folder overrides `config/tb_recon.json` for that run. Typical overrides are `cutover_date`, tolerance, aliases and contra types. A `manifest.json` (`{"legacy_tb": "my file.xlsx", …}`) can point at differently named files.

### Rule cell grammar

- `1000-1999, 6001, 7001`: inclusive range OR list. Newlines and semicolons also separate alternatives. `37*` is a prefix. `*NAME` refers to a named range.
- Blank means unrestricted. `*` / `ANY` means explicitly unrestricted. `<BLANK>` means the source value must be empty.
- A row with blank RULE_ID continues the line above (additional OR criteria). A cell of `^` inherits the previous criteria row's value.
- Several GLs in TARGET_GL never allocate by themselves; they report MULTI_TARGET_UNRESOLVED.
- Equally specific conflicting rules report AMBIGUOUS. Use PRIORITY (a higher integer wins) only as an approved decision.

## 3. Work through a run

1. **TB reconciliation → Run.** Enter the folder and an optional label. To try the tool first, click **Create synthetic dataset** (SYNTHETIC data only).
2. **Run page:** statistics, streams, 13 controls, the expected-versus-actual TB filtered by BS / PL / OBS, currency, status or GL, and the legacy-TB → stream table.
3. **Click a GL:** allocation grain (balance type × rule), mapped components, unresolved items that may belong to the GL, roll-forward and exceptions. **Click an account:** every balance-type component of that account or arrangement.
4. **Root causes & exceptions:** systemic issues with records, accounts, net and absolute amounts, action, confidence and open question.
5. **Correction worklist:** proposals with original value, proposed value, reason and evidence. Mapping files are never changed. Mode "Apply auto-applicable proposals" re-runs on a corrected copy.
6. **Compare** two runs (before and after).
7. **Downloads:** `reconciliation.xlsx`, `report.html`, `audit.json` and CSVs, in `exports\tb_recon\<run>\`.

The command-line equivalents follow, one command each:

```bash
python -m nbs_control tb-recon --inputs "C:\recon\2026-09-30" --label "Sep cut-over"
```
```bash
python -m nbs_control tb-recon --inputs "C:\recon\2026-09-30" --apply-proposals
```
```bash
python -m nbs_control tb-recon-compare <before_run_id> <after_run_id>
```
```bash
python -m nbs_control tb-recon-runs
```

Exit code 0 = fully reconciled with all inputs present; 2 = open items or missing inputs; 1 = input error.

## 4. Data handling

Run outputs (`exports\tb_recon\`) and the run index (`data\tbrecon\`) contain financial results. They are excluded from Git by `.gitignore` and from the release ZIP. Keep real input files outside the application folder, or in `inputs\`, which is also excluded from the release.
