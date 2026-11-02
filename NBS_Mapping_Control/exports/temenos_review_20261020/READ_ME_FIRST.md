# NBS mapping for the meeting on 21 October 2026

Open **NBS_Temenos_Presentation.html** in your browser. It works offline and needs no installation.
Use Meeting brief first, then Full NBS mapping. Select any of the 50 tables or search a category, sector or balance type.

Use **NBS_Temenos_Mapping_for_21Oct2026.xlsx** as the stakeholder mapping file. Filter NBS mapping by table; the first columns show
the original Temenos selection. Current engine selections and differences appear alongside. Record decisions in the two yellow columns.
Original cells contains 5,444 unique source cells, with exact worksheet and cell addresses. No customer account identifiers are included.

The review covers 1,649 NBS items. There are 1,548 links to original Temenos rows and 101 items without a unique original row.
These are mapping-coverage counts, not balance-reconciliation percentages.

## Findings to explain

- Table 10 defines NBFI using **SECTOR = 2004**, while the current loan draft uses SIC 441* and excludes 44108.
- Some engine rows had been labelled as original T24 rows even though their row numbers belonged to Ehab's layout. Labels are corrected.
- Original performance bonds use **CONTCR + CONTDRBL**. CONTDRBL is absent from ECB. The proposed typo correction to CONTDBBL
  produces a signed source total of QAR 17,333,718,623.85; that is a proposal, not proof of the QCB reporting basis.
- Original acceptances use **ACPTCONTRABL**, which gives QAR 100,083,149.61 across categories 23000â€“23999.
  The latest GL review uses **DEFPAY/DEFPAYBL** (DEFPAY raw total QAR -4,710,403,386.76) and deliberately excludes
  **ACPTBANK** as the same exposure. Do not add these exposure families together.
- The forced-empty overdraft / loan rules have been disabled. Missing required balance columns now produce PARTIAL or unavailable results.
- Loan fees from Ethix and the RCM/CLM product adjustments are identified as additions to the original Temenos wording.
- Balance examples preserve raw signs. Presentation signs and QCB classifications require explicit mapping decisions.

## Evidence and result

The 6 October Temenos workbook and Ehab workbook hashes were verified against the catalogue. The GL tool was read without modification:
completed run 54, mapping version 6, engine 1.7.0, prepared 20 October 2026. Detailed GL findings were checked against the newer
19 October Andrei review and the 20 October release notes 1.9.3.

Rebuilt NBS run: **20261020-55a063da**. All 17,014 workbook cells passed export verification.
The run identifies **2,253 partial cells**, **895 draft-preview cells**, and **13,866 unavailable cells**. It is not a complete reconciled NBS.
304 of 2,009 nonzero BO reference cells are within tolerance. Presenting this as a 100% match would conceal unresolved data and mapping decisions.

Tests: 192 tests completed, 2 data-dependent checks skipped; no failures. Five new tests verify original-cell links, literal type loading,
refusal to invent missing definitions, withdrawal of forced-zero rules and partial-balance labelling.

The local tool has a new **Original Temenos logic** menu item and **Load original Temenos cells** in the logic builder.
Loading those cells creates an unsaved draft; it preserves the raw accounting sign and refuses unsupported complex expressions.
