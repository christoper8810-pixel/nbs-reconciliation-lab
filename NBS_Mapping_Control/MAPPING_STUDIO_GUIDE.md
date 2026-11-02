# Mapping Studio guide

Start: double-click `Start_Mapping_Studio.cmd` and open `http://127.0.0.1:8765/studio`. Work through the steps on the page.

| Step | What you do | What the Studio does |
|---|---|---|
| 1 | Upload the Excel mapping workbook (.xlsx / .xlsm) | Reads every sheet. Finds GL Report, GL Mapping, CATEGORY, COA, SEGMENT, BRANCH, DAO, PRODUCT, COMPANY, CURRENCY and BALANCE TYPE sheets by name, and their columns by header text. |
| 2 | Upload the BO-generated report | Needs a line column (LINE, DKBGL, REPORT_LINE, QCB_ITEM_CODE, …) and an amount column (AMOUNT, BALANCE, VALUE …). Optional dimension columns (CURRENCY, BRANCH, COMPANY, CATEGORY, …) refine the comparison. |
| 3 | Upload the supporting source records | Account-level balances with CATEGORY, SECTOR, BALANCE_TYPE, CURRENCY, PRODUCT, BRANCH, DAO … (or LEGACY_GL for GL Mapping rows), or the ECB wide layout with `<TYPE>_BAL_QAR` columns and CONSOL_KEY. |
| 4 | – | Compiles every condition, keeping its cell and original text (page *Compiled workbook conditions*). |
| 5 | – | Validates the mapping across sheets (page *Mapping validation*). |
| 6 | – | Executes the conditions on the source records: the expected BO allocation. |
| 7 | – | Compares it with the BO report (*Discrepancy dashboard*). Click a key to drill down to its rules, cells and source records. |
| 8 | – | Investigates every difference and groups systemic root causes. |
| 9 | Review *Proposed corrections* | HIGH = verified deterministic edit; MEDIUM / LOW need Finance confirmation; unresolved items list the evidence needed. |
| 10 | Approve (one click for all HIGH), then *Write CORRECTED_MAPPING_PREVIEW.xlsx* | Applies approved edits to a copy and verifies every other cell is unchanged. |
| 11 | *Rerun* | Reconciles again with the corrected copy and shows before and after. |

## Condition grammar (one cell)

| In the cell | Meaning |
|---|---|
| blank | no restriction |
| `*` / `ANY` / `ALL` | no restriction, stated explicitly |
| `<BLANK>` | the source value must be empty |
| `3701, 3702` (or one per line, `;`, spaces) | alternatives |
| `1000-1999` | inclusive range |
| `>=5000`, `<6000` | comparisons |
| `37*`, `3?13` | wildcards |
| `NOT USD`, `!3713`, `<>3713`, `EXCL 3713` | exclusions |
| `*NAME` | named range (GL Report range table, workbook defined name, CATEGORY group) |
| `=CATEGORY!B6` | cross-sheet reference (value used, reference shown) |
| `^` | same as the previous criteria row of the line |

Columns of one criteria row are combined with AND. A row with an empty LINE cell adds another criteria row (OR) to the line above.

## Settings

Defaults are in `config/studio.json` and can be changed on the upload page per run:
- tolerance;
- BO amount unit (for example 1000 when BO shows thousands);
- BO sign;
- overlap policy: count a doubly matched record in each line and flag it, or use the most specific line only.

## Command line

```bash
python -m nbs_control studio-analyse --workbook "C:\maps\GL mapping.xlsx" --bo "C:\maps\BO report.xlsx" --sources "C:\maps\balances.xlsx"
```
```bash
python -m nbs_control studio-decide <run_id> --all-high --actor "Your Name" --reason "verified"
```
```bash
python -m nbs_control studio-export <run_id> --actor "Your Name"
```
```bash
python -m nbs_control studio-rerun <run_id>
```

Outputs are written to `exports\studio\<run_id>\`. The Studio's own store is `data\studio\studio.sqlite`. Both stay on this computer.
