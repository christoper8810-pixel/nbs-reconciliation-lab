# NBS source review for the rebuild

Reviewed on 17 October 2026 for the owner of the NBS mapping control application.

The new files materially improve the evidence for rebuilding NBS. They do not yet support a fully reconciled report by simply adding category entries to ECB. The correct next step is to rebuild the target around the BO item codes, keep balances separate from accounting events, apply the owner-confirmed September reporting basis, and correct the current calculation defects before relying on regenerated results.

**Owner clarification on 17 October 2026:** the category entries dated 1 October represent **30 September balances**. The earlier unresolved-date warning is superseded. Use this exact extract for September closing, retaining its original dates and recording a separate effective reporting date. The remaining findings about repeated records, accounting purpose, completeness and calculation defects still apply.

This is an inspection and a coding handoff. The existing application, effective mapping configuration and generated workbooks were not changed. No supplied SQL was executed. Document contents, workbook notes and existing prompts were treated as evidence rather than instructions from the user.

## What each new file supplies

| File | Verified contents | Appropriate use |
| --- | --- | --- |
| Mock3_UAT3 Categ Entry Extract (1).xlsx | 81,722 populated data rows, 237 PL categories, 11 companies. Raw booking and processing dates are 20261001; owner-confirmed effective reporting date is 2026-09-30. | September closing reconstruction and accounting-event investigation. P&L classification still requires its grain, completeness and signs to be established. |
| BO_QCB_NBS_Report.xlsx | 50 worksheets: Tables 001–045 and 100/200/300/400/500. There are 1,648 standard QCB item rows plus one special Table-020 record. | Target item and measure catalogue, and a separately versioned Ethix comparison reference. It contains reported aggregates, not account-level mapping definitions. |
| bs.docx | SQL reading Bo..Tbl_GL_Daily_Bo with a Crystal DBdate parameter. It has 37 ordered classification branches, a fallback group, and 37 final output lines. | Evidence for legacy GL classification and sign conventions. It is a financial balance-sheet query, not a complete NBS implementation. |

The category extract without “(1)” is byte-for-byte identical to the selected file. Loading both would duplicate the entire population. Hashes are recorded in audit_manifest.json and category_profile.json.

## September reporting basis is confirmed by the owner

All 1,648 standard BO item rows report 30 September 2026. The special Table-020 record also reports that date. All 81,722 category records have booking and processing dates of 1 October 2026. Their value dates are very different: 78,735 are on or before 30 September, 652 are 1 October, and 2,335 are blank. The earliest nonblank value date is 17 November 2011.

The owner has confirmed that this exact October-dated extract represents 30 September balances. Record that business basis as an enabled, source-hash-scoped policy: raw booking/processing date 2026-10-01, effective reporting date 2026-09-30. Do not overwrite the original dates, filter records out merely because their booking/value date is October, or request the same confirmation again. The policy must be visible in run manifests and editable with history. It does not automatically apply to other files dated in October, establish full YTD activity completeness, or resolve how balances and events overlap. The source-specific confirmation is retained in reporting_basis_owner_confirmation.json.

The original T24 mapping evidence in source_inventory.json also calls for CONSOLIDATE.PRFT.LOSS and describes BALANCE + DEBIT.MOVEMENT + CREDIT.MOVEMENT + BALANCE.YTD in Income!C5 and Expense!C5. That wording is not proof that these fields are independent. A data dictionary is needed before combining closing balances, movements and YTD measures. The category file does not contain those four consolidated fields.

## Repeated IDs and event meaning are material

The extract has 1,711 distinct IDs across 81,722 rows. There are 1,440 IDs with different exported row values. ID alone is not a unique row key. Across all populated exported columns, 24,515 occurrences repeat another row's values exactly. Their signed incremental amount is approximately minus 60,216,695.11 LCY. This is a duplicate-treatment sensitivity, not a confirmed overstatement: identical exported values can still represent separate accounting subentries when the source sequence has been omitted.

Preserve every source row. Do not use DISTINCT, deduplicate on ID, or delete identical observations automatically. Obtain the underlying record/subentry or multivalue sequence if available. category_repeated_export_groups.csv records the matching value fingerprints and source row numbers for investigation.

| Event population | Rows | Signed AMOUNT.LCY, rounded to cents |
| --- | ---: | ---: |
| CHARGE-MAKE.DUE-DUE / SDB-CHARGE | 290 | 190,000.00 |
| INTEREST-CHARGEOFF-DUE / DEBIT-INTEREST | 42,000 | -65,682,769.59 |
| ACCOUNT-CHARGEOFF-DUE / LOAN-ACCOUNT | 37,094 | -168,064,830.41 |
| ACCOUNT-CHARGEOFF-PAY-OS / LOAN-ACCOUNT | 3 | -7,253,114.04 |
| DC records without the soft accounting details | 2,335 | 8,868,772,428.08 |

PL category 51008 accounts for 79,097 rows and a signed amount of approximately minus 241,000,714.04 LCY. The event descriptions identify charge-off activity. Those amounts must not be relabelled as ordinary earned profit, loan fees or additional drawn balances without an accounting rule and overlap check.

Every CURRENCY value is QAR. AMOUNT.LCY is the supplied local-currency measure; no source-currency amount or FX rate is supplied. Preserve this distinction and verify the company base currency. The file alone cannot supply a general foreign-currency split for the bank.

## Account links are useful but are not one-to-one postings

79,387 category rows have OUR.REFERENCE matching an ECB account with the same QAR currency. They relate to only 1,611 distinct accounts. The remaining 2,335 DC rows have blank references and customer IDs. The owner-confirmed September basis allows these sources to be reconciled at the same effective date. It does not make stock balances and category events additive or establish one-to-one joins.

An account-to-entry join is one-to-many. Joining raw category rows to ECB and summing the repeated ECB balance would multiply balances. Calculate stock balances and event totals at their respective grains, then combine only through a documented rule. DC records require their own classification route and cannot be silently discarded for lacking customer/account metadata.

The header row ends at T, SOFT.ACCTNG.DTLS, but 79,387 rows also have populated U cells containing DEBIT-INTEREST, LOAN-ACCOUNT or SDB-CHARGE. That field is unheaded. Preserve it under a neutral technical name and seek its definition. The PL CONSOL.KEY has 14 tokens in every row. Its PL category, currency, product category, officer and company tokens agree with the corresponding explicit fields. Other token meanings should remain unconfirmed until defined. Do not reuse the ECB CONSOL.KEY positions for this PL key.

## The BO workbook provides a better target identity

The standard records have unique table/item/date keys. Preserve Table Code as text, including leading zeroes. Use table + full Qcb Item Code + measure + reporting date + reference version as the reference-cell key. Keep the code's hierarchy and the source sheet/cell address.

The workbook contains no formula cells and no embedded external connections, query tables or VBA components. It supplies reported values and labels; it does not reveal the source-account selectors, stored-procedure logic or adjustments that produced them.

Schema differences are real:

- Table-020 uses Acquistion No, Provision Amount and Net Value rather than a Qcb Item Code. Its one supplied record contains zeros. It needs its own schema, not rejection by a universal item-row importer.
- Table-022 uses Rep Date instead of Report Date.
- Tables 031–033 use Qcb Item Desc instead of Qcb Item Description.
- Table-009 has Uae Fc at M4 and Uae Lc at N4, in the opposite currency order from other tables. Map measures by validated names, not fixed column positions.
- Maturity, risk, amount-band counts, depreciation rates, collateral and securities dimensions have different units and aggregation rules. A global monetary divisor or generic subtotal is insufficient.

The current layout has 49 sections and 1,641 mapped rows. The BO has 50 sheets and 1,649 records when Table-020 is included. The counts include different headings and layouts, so the differences are not a simple missing-row count. Table-044 alone has 205 BO item records versus 152 currently mapped rows. Reconcile each target code and measure rather than carrying forward row offsets.

The diagnostic crosswalk found 1,037 unique normalized full-hierarchy candidates and 611 unresolved BO item rows. All candidates remain unreviewed. None was activated. bo_to_current_mapping_candidates.csv preserves this distinction. A matching description or candidate is not a certified account mapping.

## Reference differences must remain visible

The BO headers do not explicitly state a monetary unit. Cash values of 417,680 LC and 76,581 FC match the corresponding earlier live report values, whose reporting basis was QAR thousands. This supports that interpretation, but the import contract must explicitly record it. Counts and rates remain separate. The following arithmetic is stated in raw BO display units.

For intangibles, Table-100!E50 reports 896,109. Table-018 top-level gross costs also sum to 896,109. Its signed amortization is minus 603,699, giving net 292,410. The earlier live asset report shows 292,410. This is a gross-versus-net difference that can explain a large variance; blindly forcing the two reference versions to agree would conceal the issue. Table-018's Others parent already contains its detailed children, so summing both would double-count it.

The four primary geographical/currency columns of Table-100's root sum to 128,899,398. The corresponding Table-200 root sums to 123,151,838. The difference is 5,747,560 in display units. This is a source control difference requiring investigation of scope, adjustments and presentation. It is not a balancing adjustment to feed into the rebuilt output. Source cells are Table-100!E5:H5 and Table-200!E5:H5.

There are 97 changed primary amount cells in the base Assets/Liabilities rows for which an exact normalized hierarchy comparison with the earlier reference was possible. This is a diagnostic subset, not a full-workbook difference count. The detailed CSV records both source cells and versions. Small parent-versus-child discrepancies also occur because the BO stores rounded amounts; use an explicit rounding policy rather than assuming exact equality of displayed sums.

GCC and country breakdowns are additional views or subsets. They must not be added to the four primary inside/outside and LC/FC amounts when calculating a grand total.

## What the Word SQL establishes

The supplied query selects Asset, Liability and Capital rows from Bo..Tbl_GL_Daily_Bo at A.bdate = {?DBdate}. It uses cur_bal_Begin and Equiv_cur_bal_Begin, divides by 1,000 and casts to Decimal(21,6). The field names raise an opening-versus-closing timing question; the actual table definition is needed to settle it.

Its CASE is ordered. Specific GL and full-account exceptions precede broader prefixes. Preserve those exceptions and the first-match order. The listed sign flips apply to particular prefixes and exact ledger numbers, not universally to every liability or every contra asset. Keep these Ethix display rules separate from T24 source signs.

The final SQL returns 16 literal-zero lines, including TOTAL ASSETS, TOTAL LIABILITIES, TOTAL OWNERS EQUITY and Total Deposits. The supplied SQL itself does not calculate those totals. Crystal formulas or other report logic may exist, but they have not been supplied. Do not treat those zeros as real totals or silently reproduce them in the new application.

Classification group 17, Investment - Land, and fallback group 38 are not consumed by any final output group sum. Nonzero balances assigned there could disappear from the final SQL output. The new engine should expose such omissions and unclassified balances.

The SQL does not reference QCB item codes or implement the NBS maturity, residency, economic-sector, quality, collateral and contingent schedules. It is supporting balance-sheet evidence. Its provenance as the exact embedded query of New BalanceSheet.rpt has not been independently verified.

The extracted source is retained verbatim in bs_source_extracted.sql, with Word tabs preserved. balance_sheet_case_rules.csv and balance_sheet_output_lines.csv provide reviewable classifications and output dependencies. None was executed.

## Confirmed defect in the current prototype

In nbs_control/generation.py, the maturity_loan branch uses eight fixed future buckets, writes them from column B, and writes the total in J. The actual existing Table 10 header at row 769 has Without Maturity in B, the week bucket in C, further buckets through L, and Total Amount in M.

For example, the saved generated row 770 writes 2,110,791.70457 into J770 as a total, while J769 labels that column as the 5-to-10-year bucket. It supplies no M770 total. This is a confirmed column-alignment defect. Correct it before using the current maturity output. A passing workbook export or consistency check cannot detect this by comparing only the exported values with the same flawed generated JSON.

The current file importer supports ECB, LOAN, DEPOSIT and TB, not the new category and BO formats. The existing row specifications rely on a legacy template hash and row identities. Dedicated adapters and a code-keyed target model are therefore necessary. The owner dictionary and empirical RCM/CLM report policies remain separate; the new files do not automatically establish missing loan-fee or balance-component definitions.

## Recommended implementation sequence

1. Preserve immutable raw files and source hashes. Implement and validate the category and BO adapters, including the special schemas and source row lineage.
2. Establish a reporting-date contract. Apply the owner-confirmed September effective date for this exact category extract while preserving its original October dates. Keep the policy scoped to its source version and recorded in every run.
3. Build the full BO code-and-measure target catalogue. Maintain both BO and earlier live references as named versions. Reconcile ambiguous rows explicitly.
4. Correct table-specific maturity and other measure calculations. Separate stock, events, P&L, provisions and regulatory dimensions. Prevent one-to-many joins and repeated parent/child summation.
5. Make mappings editable with old/new values, reason, effective period, source evidence, preview and history. Allow continued coding and provisional results while unresolved business meanings remain clearly marked.
6. Reconcile from source controls to account components to target cells. Test the actual accounting rules and headers with an independent oracle, then exercise upload, mapping edit, regeneration and download.

The companion Claude brief provides the concrete module changes, data model, acceptance tests, data requests and delivery requirements. The audit evidence supports investigation; it is not an approval to label all mappings accurate or all NBS schedules complete.

## Evidence locations

Thirty-one inspection, arithmetic and owner-policy checks passed, including independent workbook spot checks of dates, schema variations, the gross/net calculation, root totals and the current maturity-column defect. The additional policy check verifies the owner-confirmed September effective date is scoped to the exact category source and preserves the raw October dates. Source hashes were checked again after the review. These checks validate the review evidence; they do not certify a corrected NBS generator, which is the next implementation task.

All audit files are beside this review. Main evidence is category_profile.json, category_totals.csv, category_repeated_export_groups.csv, bo_profile.json, bo_reference_cells.csv, bo_relationship_findings.json, bo_vs_earlier_reference_base_differences.csv, bo_to_current_mapping_candidates.csv and the three SQL extraction files. The main coding brief is CLAUDE_NBS_REBUILD_BRIEF_20261017.md in the project root.

Original new sources remain at C:\Users\Test\Downloads. The earlier reference remains data/bank_sources/NBS01 Sep 2026 English.xlsx. The existing normalized bank database was opened read-only for account matching. No bank connection was used.
