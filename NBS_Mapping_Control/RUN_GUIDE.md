# NBS mapping control: run guide

A local review application for owning the NBS report mapping. It re-imports the two original workbooks as evidence, proposes mappings against your rules, records your decisions with history, and exports differences, open items and the approved configuration. It never connects to the bank, never runs workbook text, and never certifies a report.

## 1. Set up (once)

Python 3.10 or newer. From this folder:

```bash
python -m pip install -r requirements.txt
```

## 2. Import the evidence

```bash
python -m nbs_control refresh
```

By default this reads `C:\Users\Test\Downloads\NBS MAPPING - 6 Oct 2026.xlsx` and `NBS01 Mapping (Ehab).xlsx`. For other files use `--t24 <path> --ethix <path>`. If the originals are not on the machine, `--from-supplied-inventory` rebuilds the catalog from the read-only `source_inventory.json` instead.

Each refresh records file hashes and cell addresses and keeps every catalog version. Decisions whose evidence changed are marked **STALE** and stop being effective until you review them again.

To confirm a fresh import matches the supplied inventory exactly (4,013 rows, same source IDs and values):

```bash
python -m nbs_control parity
```

## 3. Review in the browser

```bash
python -m nbs_control serve
```

Open http://127.0.0.1:8765. The pages are:

| Page | Purpose |
| --- | --- |
| Dashboard | Coverage, source hashes, mapping states, open configuration inputs |
| Proposed | 187 drafted proposals (never effective on their own) |
| Owner decisions | Current decision for each subject, its validity (CURRENT/STALE) and the change history |
| Effective | Mappings that pass every check |
| Unresolved | Blocking reasons, sections, finding items and missing inputs |
| Findings queue | 136 cell-level items from `source_findings.json`, classified as proven defect, policy mismatch, missing definition and so on |
| Sections | Ethix-to-NBS section joins. Choose the block for Table 6, ASSET-100 and Tables 26/28/37/42; decide on missing Table 38 |
| Configuration | Edit the versioned rules, selectors and policy. Each save is validated and history is kept, so you can restore |
| ECB review run | Upload an ECB JSON export to review component totals and exceptions |
| Exports | Generate the outputs, import an edited workbook, and see the remaining bank inputs |

On a mapping page, choose the action, then enter your name, a reason, the approval date and the approval evidence (minute, email or ticket). `APPROVE_PROPOSAL` takes the draft as it stands. `APPROVE_OVERRIDE` takes your own structured spec: a metric expression from the configured metrics, a JSON selector on configured T24 fields, an amount basis, an optional exclusive group and effective dates, plus the target NBS rows for an Ethix row. Every decision is appended to the history, and rollback adds a new entry rather than rewriting the old one.

**A mapping becomes effective only when all of these hold:**
- Your current, non-stale approval is recorded.
- Every metric it uses is defined. LOAN_FEES is not yet, so the Ethix carrying amount stays unavailable.
- The amount basis and the ECB adapter are approved.
- Every selector field is approved and the lending population is approved.
- Any section or block join is approved.
- The findings on its cells are decided.
- If its selector can reach category 3713, CREDIT's group is approved and the virtual-balance composition has been supplied.

## 4. Exports

```bash
python -m nbs_control export
```

This writes to `exports/`:

- `source_vs_proposed.csv`: legacy rule text, identifiers, and the owner codes missing or extra, alongside the proposed metric, draft selector and cell-level formula corrections.
- `unresolved_exceptions.csv`: open configuration inputs, sections, finding items and blocked mappings.
- `approved_mapping_config.json`: effective mappings only, with config hashes and decision provenance.
- `NBS_Owner_Review.xlsx`: an editable owner workbook. Edit only the amber columns, then run:

```bash
python -m nbs_control import-decisions exports/NBS_Owner_Review.xlsx
```

Imported rows are validated the same way as decisions entered in the UI. A row whose evidence changed since the export is refused as STALE.

## 5. Changing rules

Rules are versioned JSON in `config/`, edited through the Configuration page or directly:

- `balance_rules.json`: the 19 base balances, the CLM linked components and the approval state of CREDIT. Also the local AC.BALANCE.TYPE catalogue (`valid_balance_types`) and the virtual composition (`virtual_balances`).
- `report_selectors.json`: T24 selector fields (set `status: APPROVED` with `approved_by`/`approved_on`), the Ethix crosswalk, recorded contradictions and the lending population.
- `calculation_policy.json`: metrics (LOAN_FEES and SUSPENSE_SP are UNDEFINED), amount bases, ECB adapter fields and mode, the sparse-zero convention, maturity buckets and credit-quality totals.
- `finding_classification.json`: the classification of each finding.

To approve CREDIT's group, set `owner_approved: true`, `approved_by` and `approved_on` on its entry in `balance_rules.json`. After changing rules, run `refresh` so proposals are rebuilt.

## 6. ECB review run

```bash
python samples/make_samples.py
python -m nbs_control run-ecb --input samples/ecb_sample_clm.json --output exports/ecb_sample_review.json
```

The input is a JSON object with `reporting_date`, `ecb_records` and `links`. Each record has `record_id, company, source_system, contract_id, currency, snapshot_as_of, date_basis, category` and aligned multivalue arrays named in `calculation_policy.ecb_adapter.fields`. Each link has `link_id, company, source_system, as_of, currency, parent_contract_id, parent_category, child_contract_id, child_category, child_product, verified, evidence`.

Exit code 0 means complete for the supplied records, 2 means unresolved items remain, and 1 means an input or configuration error. The sample deliberately returns 2: CREDIT is pending and the virtual composition has not been supplied.

## 7. Tests

```bash
python -m unittest discover -s tests -t .
```

There are 96 tests. The originals-parity tests run only when the original workbooks are present.

## Remaining bank inputs

These are listed field by field on the Exports page and in the workbook's *Bank inputs* sheet:

1. AC.BALANCE.TYPE definitions and the virtual composition.
2. The ECB field schema, signs and date basis.
3. The CLM indicator field and values.
4. The authoritative 3713-to-6050 CLS relationship.
5. CREDIT's group.
6. The LOAN_FEES source, identifiers, sign and overlap.
7. Definitions for SP suspense, PDO*, DUEPRINCIPALPFT and NABPRINCIPALPFT.
8. The T24 selector fields.
9. The Ethix SIC/RIM/SYN/IST/IJR/personal-status/GL/residency crosswalk, including the RIM2398, SYN-overlap and GL1300050001 decisions.
10. The lending population.
11. Maturity fields and conventions.
12. The risk feed.
13. FX and local-currency handling.
14. The P&L adapter fields.
15. Section and block choices.
16. Reconciled representative contracts and control totals.
