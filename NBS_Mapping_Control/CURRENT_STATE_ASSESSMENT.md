# Current state assessment (baseline before this change)

Observed on 2 November 2026 from `christoper8810-pixel/nbs-reconciliation-lab`, branch base commit `3dcb6ef` ("Initial NBS reconciliation application"), in a cloud container with Python 3.13 and synthetic data only.

## 1. Release / version status

The repository does not establish a release version:

- Git holds one squashed commit. There are no tags, no version string in the package (`nbs_control/__init__.py`) and no changelog. `PROGRESS.md` did not exist before this change.
- What carries numbers is configuration, not the application: `config/mapping_versions/target_mappings-v00001…v00017.json`, the stakeholder specification `NBS_Mapping_Specification_v17_…json` and dated review folders under `exports/` (17–25 October 2026).
- `.claude/launch.json` says `0.0.1`, but that is a launcher file, not an application version.

The application is therefore described here by what it does, not by a V2/V3/V4 label. The new reconciliation component carries its own version string, `tbrecon-1.0.0`.

## 2. What the application is

`NBS_Mapping_Control` is a local Flask + SQLite tool for the **QCB NBS regulatory report** mapping from Ethix to Temenos Transact/T24. It is **not** the earlier Ethix–Temenos HTML reconciliation tool. Its main parts:

| Area | Modules | Observed status |
|---|---|---|
| Owner-review catalogue: import of the two mapping workbooks, business IDs, decisions, rollback | `importer.py`, `catalog.py`, `service.py`, `store.py`, `web.py`, `cli.py` | Works. Tested with the supplied inventory (`refresh --from-supplied-inventory`). |
| Loan component engine (19 base balances, CLM / CLS link) | `mapping_engine.py`, `ecb_adapter.py`, `report_calc.py` | Works. Starter acceptance tests pass. |
| NBS rebuild from ECB balances + category entries, BO / live comparison | `rebuild_*.py`, `bank_data.py`, `categ_data.py`, `generation.py`, `qcb_validations.py`, `builder_web.py`, `nbs_web.py` | Code and synthetic tests pass. Needs the bank database `data/bank_20260930.sqlite` and source workbooks, which are not in Git. |
| GL mapping workbook adapter (GL Report DKBGL lines, CATEGORY, SEGMENT, Ethix GL → Transact GL) | `gl_mapping.py`, `gl_evidence.py`, `source_explorer.py` | Partially defective (see §5). |
| Temenos original-logic review | `temenos_review.py`, `mapping_export.py`, `logic_text.py` | Works on synthetic tests. |
| Legacy balance-sheet SQL reference model | `legacy_gl.py` | Code present. Its test inputs are excluded by `.gitignore` (see §4). |

## 3. Three-stream TB reconciliation: what existed

The requested whole-TB migration reconciliation was **not implemented**. The building blocks that existed:

- **Engine A (PRODUCT_S3 / asset type):** `bank_data.py` reads the ECB "asset type wise" export. It keeps each `*_BAL_QAR` column separately in a JSON `components` field and correctly avoids a blanket sum. CONSOL_KEY segments were decoded at **hard-coded positions** (currency 3, category 4, sector 6, residence 8, industry 9, company −1), with no verification and no PRODUCT or department segment. No unpivot to atomic balance type → GL rule → target GL existed. There was no expected-versus-actual TB comparison.
- **Engine B (INTERNAL_CUS_ACC):** absent. No one-to-one internal-account mapping engine and no customer-account (Nostro / Vostro) resolution. `exports/internal_account_review_20261022/` holds one-off analysis scripts about legacy GL segment 6, outside the application.
- **Engine C (PL):** `categ_data.py` has a separate, validated PL CONSOL.KEY layout (14 tokens; PL category, currency, product category, officer and company verified against explicit columns). That is a correct basis, but it fed only NBS Tables 400/500. No PL → target GL mapping or reconciliation existed.
- **Whole-TB reconstruction, roll-forward, benchmark, root-cause worklist:** absent. `TrialBalance_withConsolKey.csv` is not in the repository and nothing referenced it.

## 4. Tests and launch (baseline)

| Step | Result |
|---|---|
| `python -m unittest discover -s tests -t .` without dependencies | 180 run, 7 errors (Flask / Werkzeug not installed), 13 skipped |
| After installing `requirements.txt` | **187 run, 2 errors, 13 skipped** |
| The 2 errors | `T13LegacyGL` and `T8T16T17T18EndToEnd` read `exports/rebuild_review_20261017/balance_sheet_case_rules.csv`, which `.gitignore` (`*.csv`) excludes. Missing runtime evidence, not a code defect. |
| 13 skips | Tests that need original workbooks, the real bank store, QCB files or a real run. They skip as designed. |
| `python -m nbs_control serve` | Starts. `/nbs` returns 200. |

### Runtime inputs absent from Git (not defects)

- `data/bank_20260930.sqlite` (account database) and other `*.sqlite` stores.
- Original workbooks in `inputs/` (NBS mapping, Ethix mapping, ECB, All Loan, All Deposit, Historical TB, GL mapping, category entries, BO, QCB rules).
- `exports/rebuild_review_20261017/balance_sheet_case_rules.csv` and `balance_sheet_output_lines.csv`.
- `TrialBalance_withConsolKey.csv`, the legacy cut-off TB, the Temenos pre-COB TB, internal-account mappings and PL balances.

Synthetic fixtures now stand in for all of these (`nbs_control/tbrecon/synthetic.py`).

## 5. Defects found in existing code

| # | Defect | Effect |
|---|---|---|
| 1 | `gl_mapping._token_filter` kept inline ranges such as `1000-1999, 6001, 7001` as the literal text `1000-1999` | Category ranges written in a GL Report cell never matched. Balances silently dropped out of GL-line parts. |
| 2 | `gl_mapping._balance_types` treated `CURACCOUNT, DUEACCOUNT` as one balance-type name | Grouped balance types written inline matched nothing. |
| 3 | `bank_data.py` decoded CONSOL_KEY at fixed, unverified positions, with no PRODUCT segment and no misalignment diagnostic | A PRODUCT / SECTOR column problem cannot be detected or corrected through configuration. |
| 4 | Two tests depend on a `.gitignore`-excluded CSV and error instead of skipping | The suite reports errors on any clean checkout. |
| 5 | `Start_NBS_Rebuild.cmd` installs from `%~dp0wheels`, but the wheels are tracked under `exports/transfer/wheels` | Offline install fails from a Git checkout unless the folder is copied. The release ZIP now places the wheels at `wheels/`. |
| 6 | Repository hygiene: 9 tracked copies of test temporary folders (`data/test_temp/nbs-template-*`), 2 duplicate code / data copies (`.verification/`, `exports/temenos_review_20261020/update/payload`), process logs `p.out` / `p2.out` | Size (about 600 MB checkout) and ambiguity about which copy is current. Not removed in this change (see REMAINING_ISSUES.md). |

## 6. Security observation: possibly sensitive material in Git

Per the security boundary, these paths were **not opened or processed** beyond their names, sizes and the repository's own description of them. Their names or the README indicate real bank or confidential content. They are excluded from the release ZIP. Removing them from Git history is an owner decision.

- `source_inventory.json` and its 9 copies under `data/test_temp/*/supplied/` (README: "original cell values, formulas, notes … for every populated source row" of the bank mapping workbooks).
- `data/catalogs/catalog-0001.json` and its copies (`.verification/`, `exports/temenos_review_20261020/update/payload/`, `data/test_temp/*`).
- `exports/**/*.xlsx.inspect.ndjson` (cell dumps of generated NBS workbooks, up to 70 MB each).
- `exports/cell_audit_20261021/`, `exports/internal_account_review_20261022/internal_review.json`, `exports/temenos_review_20261020/` (review JSON, GL snapshot, presentation, screenshots).
- `exports/rebuild_review_20261017/` (BO rows and profiles, extracted SQL), `exports/mapping_specification/`.
- `exports/andrei_documents_review_20261022/originals/*.docx` and derived text (personal names in paths), `exports/andrei_returned_review_20261025/`, `exports/systems_summary_20261022/`.
- `data/bank_*.json`, `data/difference_investigation.json`, `data/rebuild/gl_line_amounts.json`, `data/rebuild/gl_evidence.json`, `data/report_template_values.json`, `data/generation_jobs/*.json`, `p.out`, `p2.out`.

A name search of code, scripts, docs and `config/` for passwords, API keys, connection strings, JDBC / ODBC data sources and private keys found only the Flask session key. It is generated randomly at start-up (`web.py`), plus a test placeholder. No production endpoint is referenced.
