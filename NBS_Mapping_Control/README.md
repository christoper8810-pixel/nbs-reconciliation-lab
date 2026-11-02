# NBS mapping control

ECB Excel report generation is now available at `http://127.0.0.1:8767/reports`. Double-click `Start_NBS_Reports.cmd` if the application is stopped. See **[NBS_REPORT_RUN_GUIDE.md](NBS_REPORT_RUN_GUIDE.md)** for uploading ECB, reviewing differences and changing row mappings or RCM / CLM calculation policies.

The local import, owner-review and component-mapping application is built. To use it, see **[RUN_GUIDE.md](RUN_GUIDE.md)**. The original starter notes follow; the engine and its rules are unchanged in meaning.

## Application layout

- `nbs_control/`: the application package.
  - `importer.py`: read-only re-import.
  - `catalog.py`: business IDs, proposals, findings queue, sections.
  - `service.py`: decisions and the effective/unresolved views.
  - `store.py`: SQLite history and rollback.
  - `ecb_adapter.py`: the ECB multivalue adapter and CLM links.
  - `report_calc.py`: maturity, credit-quality totals, metrics and exclusivity.
  - `exports.py`, `web.py`, `cli.py`.
- `config/`: versioned rules, selectors, calculation policy and finding classification, with saved history.
- `tests/`: 96 tests, including the 35 starter tests.
- `samples/`: synthetic ECB sample generator.
- `data/`: application state (catalog versions and the decision database).
- `exports/`: generated outputs.

## What is included

- `CLAUDE_CODE_PROMPT.md`: implementation brief based on both workbooks and the owner's clarifications.
- `config/balance_rules.json` (formerly `rules.json`): 19 exact base loan components and two conditional linked CLS components.
- `mapping_engine.py`: deterministic classifier and signed closing-balance review calculator, using only Python's standard library.
- `tests/test_mapping_engine.py`: acceptance and regression tests.
- `source_inventory.json`: original cell values, formulas, notes and locations for every populated source row.
- `mapping_register.csv`: editable row review register; source formulas are escaped as inert text.
- `source_manifest.json`: original file names and SHA-256 hashes.
- `report_sections.json`: candidate Ethix-to-NBS report-section matches, awaiting row/dimension approval.
- `source_findings.json`: 20 specific findings, original evidence and later owner updates.
- `sample_non_clm_records.json` / `sample_clm_records.json`: clearly synthetic input examples, never bank balances.

The separate Excel review workbook contains the rule dictionary, findings and editable owner-decision fields for 4,013 populated rows: 2,149 NBS rows and 1,864 Ethix rows. Heading and formula rows are included for coverage. A recorded spreadsheet decision does not activate engine rules or certify a report. Local-validation selections in the workbook do not automatically populate the engine's bank catalogue.

## Loan logic

The owner's base group counts are OUTSTANDING=12, AMORTIZED_EARNED=5 and UNEARNED_PROFIT=2. Identifiers are exact after trimming and uppercasing. PDO and SP variants receive no implied aliases.

For the category3713 Murabaha/CLM case, the owner supplied linked CLS category6050 balances CREDIT and ACCDEPOSITPFT. ACCDEPOSITPFT is assigned to AMORTIZED_EARNED from the owner's accrued-profit instruction. CREDIT to OUTSTANDING is a proposed implementation interpretation. It starts with `owner_approved=false`, so CLM totals remain unavailable pending that group decision. If the owner chooses a different group, edit the explicit rule rather than changing code. Record approval with `owner_approved`, `approved_by` and ISO `approved_on`; approval of a group does not validate its source/link or monetary basis.

Neither category alone nor a balance-type name proves CLM. The engine requires explicit `is_clm` and, for linked components, verified parent/child metadata. The starter accepts one paired CLS child per parent/reporting date. More complex link structures require an explicit coverage/allocation policy before extension.

Ehab's legacy loan carrying amount contains OUTSTANDING + AMORTIZED_EARNED + LOAN_FEES. The T24 loan-fee mapping remains unspecified. The engine does not calculate that carrying amount, an amortized-cost valuation, or a full NBS report. It never invents a fee zero or a deduction for UNEARNED_PROFIT.

## Run the starter

Use Python 3.10 or newer from the extracted folder. No external package installation is needed for the supplied engine.

```powershell
python -m unittest discover -s tests -t .
python mapping_engine.py classify --rules config/balance_rules.json --balance-type RECDEFERREDPFT --is-clm false
python mapping_engine.py classify --rules config/balance_rules.json --balance-type ACCDEPOSITPFT --is-clm true --category 6050 --parent-category 3713 --component-origin CLS --verified-link true
python mapping_engine.py aggregate --rules config/balance_rules.json --input sample_non_clm_records.json --output exports/non_clm_review.json
python mapping_engine.py aggregate --rules config/balance_rules.json --input sample_clm_records.json --output exports/clm_review.json
```

Exit 0 means the supplied component check passed; exit 2 means unresolved review inputs; exit 1 means a file/configuration error. The synthetic CLM example intentionally returns exit 2 while CREDIT's group approval is pending. Every output has `production_ready=false`.

## Balance input contract

JSON can be a record array or an object containing `records`. CSV is also accepted with distinct headers and quoted multiline fields. Every input row requires:

| Field | Meaning |
| --- | --- |
| company | Accounting company identifier, text |
| source_system | T24 or TRANSACT; ETHIX requires an explicit approved crosswalk |
| contract_id | Original loan or CLS account identifier, text |
| currency | Currency of the supplied amount |
| as_of | Reporting date, YYYY-MM-DD |
| category | Category3713 for a true CLM parent; category6050 for its linked components |
| balance_type | Exact source balance identifier |
| signed_closing_balance | Decimal text or integer; retain original sign |
| is_clm | Explicit true, false or unknown |
| record_id | Unique source record identifier within source/company |

Linked CLS component rows additionally require `parent_contract_id`, `parent_category="3713"`, `component_origin="CLS"` and `verified_link=true`. Preserve the specific CLS account as `contract_id`. The engine reports linked balances under the parent while retaining source account IDs. Both supplemental components must belong to the same verified child in this starter policy. Links must match company, source, currency and reporting date. A child reused across conflicting parents at the same reporting date is rejected.

The engine requires all 19 base balance records, plus both linked component records for true CLM, even where the amount is an explicit zero. This is a conservative input contract. It does not assert every balance exists for every bank product. For a sparse bank extract, implement and approve a documented zero/coverage convention in the adapter; do not silently zero-fill missing types in this engine.

Duplicate record identities, duplicate parent/type grain, missing amounts, unknown codes, mixed CLM states, ambiguous links and incomplete coverage prevent contract totals. Partition totals remain unavailable if any input contract is incomplete. Company, source, date and currency stay separate. The engine accepts closing amounts only; it does not reconstruct ECB opening/movement arrays, convert FX, determine debit/credit signs, or validate regulatory reporting basis.

Optional `valid_balance_types` supplies the local bank dictionary. Leave null while unavailable; an empty list is invalid. Optional `ethix_crosswalk` has `approved_by`, `approved_on`, and `mappings` from exact source codes to configured target codes. This is a balance-code crosswalk, not the report/product/selector crosswalk Claude still must build. Neither optional setting proves valuation equivalence.

## Inputs still needed for the complete report

The source workbooks provide mapping specifications, not reconciled transaction/balance extracts. Claude must expose these missing inputs individually:

1. Local AC.BALANCE.TYPE definitions and any virtual/aggregate balance composition.
2. Actual CLM indicator and authoritative Murabaha3713-to-CLS6050 account relationship.
3. Owner decision on CREDIT's destination group and approved sign/valuation basis.
4. T24 LOAN_FEES source, balance identifiers, signs and overlap treatment.
5. Ethix-to-T24 product, sector, SIC/RIM, residency and risk feed crosswalks.
6. Report dates, FX/local-currency conventions, mature/overdue treatment and maturity boundaries.
7. Explicit row/dimension/block joins, including repeated NBS Table6 and missing Table38/report303.
8. Reconciled example contracts and full population/control totals.

Public Temenos documentation describes balance types as institution-defined and requires local balance definitions. It supports the implementation framework but does not verify this bank's exact group memberships:

- https://developer.temenos.com/events/financial-accounting/contract-balances-updated
- https://developer.temenos.com/article/accounting-events-lifecycle-guide
