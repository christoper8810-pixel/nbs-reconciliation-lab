# Generate NBS reports from ECB

Open `http://127.0.0.1:8767/reports`. If the application is not running, double-click `Start_NBS_Reports.cmd` in this folder.

1. Select the ECB asset-type-wise Excel workbook. The September supporting loan, deposit, trial balance and live NBS files are already loaded.
2. Select **Generate reports**. Leave the file fields blank to rerun September using the saved mappings.
3. Choose a report section. Each row shows the calculated amount, the Ethix reference, the difference, its source and its remaining issues.
4. Click a report row to edit its population filter, source, measure, presentation sign or exact balance types. Save with your name and a change note, then generate again.
5. Use **Edit RCM / CLM calculation rules** to inspect or change the separate product-specific report measures. The prior policy is retained in the change history.
6. Download the complete CSV comparison or detailed results. Select **Create Excel workbook for this run** for the Excel report, then download it when the export completes. Its Comparison tab links to Generated NBS and Ethix reference. Regenerate reports after changing mappings.

The first full import and Excel export can each take several minutes. The progress page refreshes automatically. An identical ECB upload can reuse the verified source cache, while changed mappings are still recalculated.

## Reading the amounts

Amounts are QAR thousands; count columns remain counts. An unavailable cell is blank in the application and `n.a.` in the workbook. A genuine zero remains numeric zero. **PARTIAL** identifies an available portion of an incomplete measure or total. **PROVISIONAL** means a calculated amount under the visible mapping, not a certified regulatory balance.

The live Ethix report is a comparison input and is never copied into an unavailable generated value. `TB` rows use the separately supplied Ethix trial balance. They have aggregate currency totals but no invented inside/outside split. ECB loan carrying amounts include the separately supplied, dated Ethix loan-fee field because a T24 fee crosswalk is still absent.

## Loan measures

`carrying` retains the original owner component groups plus Ethix fees. `ethix_carrying` applies the documented RCM / CLM report policies and uses the original measure for other products. The original `config/balance_rules.json` is preserved.

- RCM: principal ACCOUNT balances plus `-RECDEFERREDPFT-ACCDEFERREDPFT` as earned profit, plus the supplied fees. September testing matches 1,614 of 1,623 accounts within QAR 1. Nine accounts still differ.
- CLM: verified category 3713 parent plus the signed category 6050 child CREDIT, with the linked child's distinct `ACCCRPROFIT` considered in the report earned measure. September testing matches 160 of 161 verified pairs within QAR 1. `ACCCRPROFIT` is never declared an alias of `ACCDEPOSITPFT`. Seven missing or unverified links are excluded from monetary totals and remain exceptions.

These are evidence-based September report policies, visible in `config/report_product_policies.json`. They do not establish the bank's official balance-type definitions. Change or disable them on the product-policy page and regenerate to inspect the effect.

## Remaining limitations

- The ECB headers omit `NABACCOUNT`, `NABDEFERREDPFT`, `RECPRINCIPALPFT` and `DEFERREDPFT`. Their absence is not silently treated as a complete zero. CO, CUST and BL variants are distinct.
- 34 loan accounts and one deposit account have no ECB account match in the supplied September files.
- Missing CLM links, commitment-only accounts and product-specific account differences remain in the exception exports.
- Collateral, treasury instrument details, indirect credit-risk grades, some customer subdivisions and some report dimensions are absent. A report section can therefore have calculated rows alongside unavailable rows.
- Maturity uses the reporting date, not today's date. Days 0–7 enter the first bucket; later buckets exclude their previous boundary. Overdue and missing maturities are separate exceptions. Deposit demand products are separated from time-deposit maturity buckets.
- The supplied source dates must match 30 September 2026. The application refuses to silently combine another month's ECB workflow with stale loan/deposit detail. A changed live report template also requires its row mappings to be rebuilt and checked.

## Local files and recovery

The original attached files are untouched. Extracted supporting workbooks are in `data/bank_sources`. The normalized September account database is `data/bank_20260930.sqlite`. Row mappings are in `config/generation_rules.json`; calculation policies are in `config/report_product_policies.json`. Versioned edits are in `config/generation_history`. Each upload run has its own state, source files, output folder and error status.

Back up `config` and `data` together. The earlier owner-decision system remains available separately. A provisional generation rule does not fabricate an owner approval in that register.

To generate from the command line, run `python -m nbs_control generate-reports`. To start the local application, run `python -m nbs_control serve --port 8767`.
