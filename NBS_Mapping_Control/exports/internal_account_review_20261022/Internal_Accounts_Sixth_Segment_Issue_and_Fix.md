# Internal accounts and the sixth GL segment

Priority request for Systems Limited

Please demonstrate that the NBS preserves the internal-account population selected in Ehab's mapping. The sixth segment is the ten-digit ledger reference, not a complete Transact account or a complete NBS rule. Retain Ehab's exact ledgers, prefixes, exclusions and signed deductions.

## What the focused check establishes

- 74 Ehab rule cells select current INTERNAL mapping rows.
- 115 of 120 distinct explicit ledger codes in those rules are present in the supplied COA and have current INTERNAL mapping rows. This validates identifier coverage, not every NBS classification.
- 5 codes require clarification. They are listed below and have not been removed.
- 897 rows in Other T24 Account are INTERNAL and have no corresponding Ethix GL. They need a separate NBS decision; an old-ledger-only review cannot establish their treatment.
- The review uses the frozen supplied GL v6 mapping and 9 September source versions recorded in the detailed audit. It does not establish what is currently deployed in the bank.

## Specific issues and requested handling

| Issue | Evidence | Action requested |
|---|---|---|
| Reserve accounts in hidden retained rows | Assets rows 57-108 are hidden. Their C64/D64/F64/G64 say 5003/5004. The visible Assets B8 links to Table 2, whose B10 correctly specifies 18060/18061. | Confirm which retained specification is deployed. This is a hidden specification conflict, not a confirmed error in the visible reserve selection. |
| Cash population | Ehab's 100 prefix, excluding 1003, also selects internal petty cash and cash-in-transit categories 12903-12907. Table 1 cash specifies 10000-10025. | Confirm the intended NBS line for each additional cash category. Do not lose these accounts or automatically move them into Cash on hand without confirming the reporting classification. |
| Clearing routes | Current foreign-currency INTERNAL rows for ledger 1003000020 use 18062. Its QAR CUSTOMER ACCOUNT row uses 5002. | Keep both routes distinct. Do not classify the customer-account row as an internal account or apply one broad category change to both. |
| Investment properties | Ehab ledger 1700000001 maps to internal account QAR-13337-1149-1900, category 13337. Table 15 B10 says 11320. | Confirm the correct NBS property classification and correct the category/account selection. |
| Intangible amortisation | Ehab ledger 2801000001 maps to 11570. Category 11550 maps to ledger 2802000001, accumulated depreciation of the main building. | Review Table 18 C16 and keep building depreciation separate from intangible amortisation unless Finance documents a different reporting requirement. |
| Department changes during migration | In 3,081 INTERNAL rows, column M differs from the department encoded in the actual target account in E. Example: row 2 has M=1201 but E=AED-10011-9999-1001. | Use the actual recorded target account. Do not construct it by assuming the old/mapping department is the target department. These differences are not automatically mapping errors. |
| Repeated target cash accounts | Five company/account keys have two mapping rows each. Both old GLs have sixth segment 1000000010 but different departments, 3601 and 5260, and converge on department 9999 in the target account. | Preserve both old-to-new links. Confirm the consolidation and ensure the same target balance is counted once when the NBS is calculated. |
| New internal accounts | The Other T24 Account sheet contains INTERNAL rows explicitly labelled No corresponding Ethix GL. | Define their NBS treatment separately; do not exclude them just because Ehab has no sixth-segment reference. |
| Internal account reporting split | An internal account may have no customer-residency attribute. | Use the approved entity/account basis for inside/outside Qatar. Do not drop it or invent customer residency. Keep the currency, source balance type and reporting sign explicit. |

## Five ledger codes requiring clarification

| Sixth segment | Ehab cells | Current supplied evidence | Requested clarification |
|---|---|---|---|
| 1500000000 | K566 | Not found in the supplied COA or GL Mapping | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |
| 1603010002 | K578, L27 | No INTERNAL row; classifications: NOT TO BE MAPPED | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |
| 1900010055 | K1056 | No INTERNAL row; classifications: CLOSED, CLOSED COMPANY, CLOSED DAO, LOAN | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |
| 1904030002 | K1054 | No INTERNAL row; classifications: NOT TO BE MAPPED | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |
| 2801000002 | K49 | Not found in the supplied COA or GL Mapping | Confirm whether it was replaced, closed, excluded or belongs to a different source route. |

## Evidence to return

For every internal-account NBS line, provide Ehab cell and ledger rule, full old GL, exact Transact account, company, currency, source balance type, reporting sign and NBS line. Show exclusions, unmapped records and new internal accounts separately. Compare the old-ledger selection with the account selection at one reporting date and explain missing or additional balances.

No source rows or mapping entries were removed. This focused review refines the earlier all-class category comparison, particularly for clearing: 5002 and 18062 belong to different account routes.