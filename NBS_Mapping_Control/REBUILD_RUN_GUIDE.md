# NBS rebuild: run guide (17 October 2026)

The rebuild keys every NBS target by **BO table + QCB item code** and every measure by its validated BO header. The BO workbook and the earlier live NBS01 report are comparison references only; generated amounts never read them.

## Run it

```bash
python -m nbs_control rebuild-setup
```
Imports the category extract (the identical copy is recognised by hash and loaded once), the BO reference and the earlier live report into `data/rebuild/rebuild_store.sqlite`. Other files: `--categ <path>` (repeatable) and `--bo <path>`.

```bash
python -m nbs_control rebuild-run --label "my note"
```
About 5 minutes. Writes a new folder under `data/rebuild/runs/<run id>/`; earlier runs are never changed.

Owner interface: `python -m nbs_control serve`, then open **NBS rebuild** (http://127.0.0.1:8765/rebuild). From there: select/upload files, generate a run, open a table, click a cell to see contributing accounts/rows, edit a mapping (structured fields, preview old vs new, save with a reason), and edit the reporting-basis and duplicate policies.

## What a run contains

| File | Content |
| --- | --- |
| `manifest.json` | Report date, period, units, source hashes, category reporting basis (policy ID/version, raw and effective dates), mapping/policy versions, cell statuses, materiality |
| `NBS_Rebuild_2026-09-30.xlsx` | One sheet per BO table with the BO's own headers, corrected legacy Table 10 layout, comparisons, controls, data requests. Re-read and validated after saving |
| `comparison_bo.csv`, `comparison_live.csv` | Generated vs each named reference, with difference category |
| `coverage_register.csv` | Every BO code × measure (and Table-020) with mapping and cell status |
| `review_queue.csv` | 611 unresolved items + 1,037 unreviewed draft candidates |
| `controls.json` | Source controls, duplicates, account links, whole-source reconciliation, stock population, partition overlap/gaps, BO reference controls, legacy GL model, maturity-convention sensitivity |
| `data_requests.csv` | Evidence still needed from the bank |
| `run.sqlite` | Pre-round cell values and per-record contributions (drilldown) |

## Statuses

`DRAFT_CANDIDATE_PREVIEW` – value from an unreviewed exact-path candidate mapping; never certified. `PROVISIONAL` / `CALCULATED_SUPPORTED` – after you set the mapping to PROVISIONAL / APPROVED. `PARTIAL`, `UNRESOLVED_DUPLICATE_BASIS`, `UNAVAILABLE` (blank / `n.a.`, never zero), `MANUAL_OVERRIDE` (deliberate value, including a deliberate 0) and `MANUAL_OVERRIDE_EMPTY`.

## Policies (config/)

- `reporting_basis_policies.json` – owner-confirmed: category extract `a9dc0021…` (raw booking/processing 2026-10-01) has effective reporting date 2026-09-30. Scoped to that hash only; another October file is rejected for September.
- `duplicate_policy.json` – default `UNRESOLVED_RETAIN_ALL`: every row counts and the 24,515 repeated observations are reported as an unresolved −60,216,695.11 LCY sensitivity. Decisions are per value fingerprint (not row position); `COUNT_ONCE` excludes the excess with a visible reason.
- `target_mappings.json` (+ `mapping_versions/`) – one record per BO target; every save is a new version with history.
- `bo_measure_catalogue.json` – semantic meaning, kind (money/count/rate/notional/fair value), unit, additivity and primary/subset flag per table header.
- `rebuild_settings.json` – maturity convention (`CALENDAR_EOM`, provisional; evidence recorded in the file) and evidenced open-ended products (none yet).

## Tests

```bash
python -m unittest discover -s tests -t .
```
179 tests. `tests/test_rebuild.py` covers the 18 acceptance tests in the brief; `tests/test_rebuild_qcb.py` covers the QCB rules, crosswalk, inheritance, distinctness, QCB-derived mappings, GL evidence and the export.

## QCB validation rules, crosswalk and stakeholder export (18 October 2026)

```bash
python -m nbs_control rebuild-setup
python -m nbs_control rebuild-enhance
python -m nbs_control rebuild-run
python -m nbs_control rebuild-gl-evidence
python -m nbs_control rebuild-export-mapping
```
- `data/qcb_validations/` holds the five QCB validation-rule workbooks (2,664 unique rules after de-duplication, 0 parse errors). Every run checks them against BO and generated values (`qcb_validation_results.csv`).
- `rebuild-enhance` drafts mappings from three sources: the QCB code structure, QCB identities and reference-additive subtotals. It withholds drafts whose selectors cannot separate items and never changes owner-edited mappings.
- `config/hierarchy_predicates.json` controls parent-level dimension inheritance, the SECTOR-code correction, the provisional Islamic-bank product rule and customer-level size bands. `config/component_corrections.json` lists balance-type typo corrections. `config/rebuild_settings.json` sets the maturity convention (CALENDAR_EOM, provisional).
- `exports/mapping_specification/NBS_Mapping_Specification_v<version>_<date>.xlsx` (plus JSON/CSV) is the stakeholder file; the same file is available on the NBS rebuild page under "Stakeholder mapping specification".

## Sources, Explore and Logic builder (19 October 2026)

- **Sources** (`/rebuild/sources`): choose each input file on the computer you use (ECB, All Loan, All Deposit, trial balance, GL mapping workbook, category entries, BO, live NBS, QCB rules). Files are copied into `inputs/` and recorded with their SHA-256 in `config/source_files.json`; nothing refers to another computer's folders. Buttons build the account database (the previous one is kept as `.bak`), import the reference files and compute the GL Report lines from ECB.
- **GL mapping workbook** (`gl_mapping.py`): GL Report DKBGL lines with their T24 criteria (category ranges, sectors, balance-type groups such as *PRINCIPAL2), the CATEGORY and SEGMENT dictionaries and the Ethix GL -> Transact/DKBGL mapping. The workbook is marked as a migration reference and is labelled as such.
- **Explore** (`/rebuild/explore`): totals of every source by any dimension with descriptions; GL Report lines show the ECB-computed amount next to the trial balance mapped to the same line.
- **Logic builder** (`/rebuild/builder/<item>`): the item's current logic as readable parts; add parts from ECB balances, ECB with loan/deposit attributes, trial-balance GL, a GL Report line (expanded to its criteria) or category entries; preview per measure against BO, per part, with a double-count warning; save as a `SOURCE_RULE` mapping version.
