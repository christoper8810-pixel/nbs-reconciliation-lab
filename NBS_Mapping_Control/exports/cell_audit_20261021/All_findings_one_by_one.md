# NBS Ehab / Systems / GL cell audit

1520 finding occurrences. Copied occurrences are separate; one cell can have several findings. Status distinguishes confirmed defects from differences, ambiguity, input gaps and review topics.

10,979 populated NBS cells and 1,663,670 total source cells captured across 81 worksheets.

## NBS-0001 — REVIEW — No numeric category bridge: ...01 Cash and Precious metals

Systems: ASSET - 100!A6 · Ehab: K5 · GL: 

Ehab K5: All Gl's  Start by 100  Except  1003. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0002 — DIFFERENCE — Ehab GL-to-category selection differs: ...01 Cash and Precious metals

Systems: ASSET - 100!C62, D62 · Ehab: K5 · GL: Current v6: GL Mapping!A2, L2 = 10011; Current v6: GL Mapping!A3, L3 = 10011; Current v6: GL Mapping!A298, L298 = 10011; Current v6: GL Mapping!A317, L317 = 10011; Current v6: GL Mapping!A352, L352 = 10001; 9 September: GL Mapping!A2, L2 = 10011; 9 September: GL Mapping!A3, L3 = 10011; 9 September: GL Mapping!A298, L298 = 10011; 9 September: GL Mapping!A317, L317 = 10011; 9 September: GL Mapping!A320, L320 = 10011

Ehab K5 selects GL sixth segments whose current categories are 10001, 10009, 10011, 10024–10025, 12903–12907. Systems criteria select 10000–10025, 12900–12919.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0003 — DIFFERENCE — Ehab GL-to-category selection differs: .....01 Required Reserve

Systems: ASSET - 100!C64, D64, F64, G64 · Ehab: K7 · GL: Current v6: GL Mapping!A2569, L2569 = 18060; Current v6: GL Mapping!A2573, L2573 = 18061; 9 September: GL Mapping!A2569, L2569 = 18060; 9 September: GL Mapping!A2573, L2573 = 18061

Ehab K7 selects GL sixth segments whose current categories are 18060–18061. Systems criteria select 5003–5004.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0004 — REVIEW — No numeric category bridge: .....02 Others

Systems: ASSET - 100!A9 · Ehab: K8 · GL: 

Ehab K8: 1003000020. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0005 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Others

Systems: ASSET - 100!C65, D65, F65, G65 · Ehab: K8 · GL: Current v6: GL Mapping!A2581, L2581 = 18062; Current v6: GL Mapping!A2586, L2586 = 5002; 9 September: GL Mapping!A2586, L2586 = 5002

Ehab K8 selects GL sixth segments whose current categories are 5002, 18062. Systems criteria select 5002.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0006 — REVIEW — No numeric category bridge: .......01 Demand and Call

Systems: ASSET - 100!A12 · Ehab: K11 · GL: 

Ehab K11: All Gl's  Start by 11 . Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0007 — REVIEW — No numeric category bridge: .......02 Placements

Systems: ASSET - 100!A13 · Ehab: K12 · GL: 

Ehab K12: 1200000010, 1302000010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0008 — REVIEW — No numeric category bridge: .......02 Placements

Systems: ASSET - 100!A69 · Ehab: K12 · GL: 

Ehab K12: 1200000010, 1302000010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0009 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A19 · Ehab: K18 · GL: 

Ehab K18: 1502010005. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0010 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A75 · Ehab: K18 · GL: 

Ehab K18: 1502010005. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0011 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A24 · Ehab: K23 · GL: 

Ehab K23: inside 1500000010, 1502000010, 1502010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0012 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A80 · Ehab: K23 · GL: 

Ehab K23: inside 1500000010, 1502000010, 1502010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0013 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A24 · Ehab: L23 · GL: 

Ehab L23: outside 1602000010, 1600000010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0014 — REVIEW — No numeric category bridge: .......01 Issued by Governments

Systems: ASSET - 100!A80 · Ehab: L23 · GL: 

Ehab L23: outside 1602000010, 1600000010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0015 — REVIEW — No numeric category bridge: .......03 Issued by Banks

Systems: ASSET - 100!A26 · Ehab: K25 · GL: 

Ehab K25: inside 1502000011, 1500000011. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0016 — REVIEW — No numeric category bridge: .......03 Issued by Banks

Systems: ASSET - 100!A82 · Ehab: K25 · GL: 

Ehab K25: inside 1502000011, 1500000011. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0017 — REVIEW — No numeric category bridge: .......03 Issued by Banks

Systems: ASSET - 100!A26 · Ehab: L25 · GL: 

Ehab L25: outside 1602000011, 1600000011. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0018 — REVIEW — No numeric category bridge: .......03 Issued by Banks

Systems: ASSET - 100!A82 · Ehab: L25 · GL: 

Ehab L25: outside 1602000011, 1600000011. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0019 — REVIEW — No numeric category bridge: .......04 Issued by Others

Systems: ASSET - 100!A27 · Ehab: K26 · GL: 

Ehab K26: inside 1502000012, 1500000012. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0020 — REVIEW — No numeric category bridge: .......04 Issued by Others

Systems: ASSET - 100!A83 · Ehab: K26 · GL: 

Ehab K26: inside 1502000012, 1500000012. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0021 — REVIEW — No numeric category bridge: .......04 Issued by Others

Systems: ASSET - 100!A27 · Ehab: L26 · GL: 

Ehab L26: outside 1600000012, 1602000012, 1602010010, 1600010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0022 — REVIEW — No numeric category bridge: .......04 Issued by Others

Systems: ASSET - 100!A83 · Ehab: L26 · GL: 

Ehab L26: outside 1600000012, 1602000012, 1602010010, 1600010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0023 — REVIEW — No numeric category bridge: .....03 Equity Participation

Systems: ASSET - 100!A28 · Ehab: K27 · GL: 

Ehab K27: inside 1500000001, 1501000001, 1501010001, 1501020001. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0024 — REVIEW — No numeric category bridge: .....03 Equity Participation

Systems: ASSET - 100!A84 · Ehab: K27 · GL: 

Ehab K27: inside 1500000001, 1501000001, 1501010001, 1501020001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0025 — REVIEW — No numeric category bridge: .....03 Equity Participation

Systems: ASSET - 100!A28 · Ehab: L27 · GL: 

Ehab L27: outside 1600000001, 1600000002, 1600000015, 1601000011, 1601010001, 1603010002. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0026 — REVIEW — No numeric category bridge: .....03 Equity Participation

Systems: ASSET - 100!A84 · Ehab: L27 · GL: 

Ehab L27: outside 1600000001, 1600000002, 1600000015, 1601000011, 1601010001, 1603010002. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0027 — REVIEW — No numeric category bridge: .....04 Mutual funds and Others

Systems: ASSET - 100!A29 · Ehab: L28 · GL: 

Ehab L28: outside 1600000003, 1601010005. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0028 — DIFFERENCE — Ehab GL-to-category selection differs: .....04 Mutual funds and Others

Systems: ASSET - 100!C85, D85, F85, G85 · Ehab: L28 · GL: Current v6: GL Mapping!A8799, L8799 = 13272; Current v6: GL Mapping!A8838, L8838 = 13292; 9 September: GL Mapping!A8799, L8799 = 13272; 9 September: GL Mapping!A8838, L8838 = 13292

Ehab L28 selects GL sixth segments whose current categories are 13272, 13292. Systems criteria select 13204, 13223, 13229, 13232, 13278, 13287.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0029 — REVIEW — No numeric category bridge: ...05 Credit Facilities

Systems: ASSET - 100!A30 · Ehab: K29 · GL: 

Ehab K29: (All Gl's  Start by 13  Except  1302000010 + Gl's  under 190002 + Gl's  under 190005 + Gl's  under 1904 Except  190401, 1904030002) minus GL's under 2302. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0030 — REVIEW — No numeric category bridge: ...05 Credit Facilities

Systems: ASSET - 100!A86 · Ehab: K29 · GL: 

Ehab K29: (All Gl's  Start by 13  Except  1302000010 + Gl's  under 190002 + Gl's  under 190005 + Gl's  under 1904 Except  190401, 1904030002) minus GL's under 2302. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0031 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A34 · Ehab: K33 · GL: 

Ehab K33: from all loan file NonPersonal all sic code start by 441 Except  44108 (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0032 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A90 · Ehab: K33 · GL: 

Ehab K33: from all loan file NonPersonal all sic code start by 441 Except  44108 (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0033 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A34 · Ehab: L33 · GL: 

Ehab L33: outside from all loan file NonPersonal all sic code start by 441 Except  44108 nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0034 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A90 · Ehab: L33 · GL: 

Ehab L33: outside from all loan file NonPersonal all sic code start by 441 Except  44108 nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0035 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A38 · Ehab: K37 · GL: 

Ehab K37: from all loan file NonPersonal all sic code start by 1,2,3  Except  Rim 2398 (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0036 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A94 · Ehab: K37 · GL: 

Ehab K37: from all loan file NonPersonal all sic code start by 1,2,3  Except  Rim 2398 (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0037 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A38 · Ehab: L37 · GL: 

Ehab L37: outside from all loan file NonPersonal all sic code start by 1,2,3  nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0038 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A94 · Ehab: L37 · GL: 

Ehab L37: outside from all loan file NonPersonal all sic code start by 1,2,3  nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0039 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A42 · Ehab: K41 · GL: 

Ehab K41: from all loan personal + NonPersonal all sic code start by 4 Except  441 + GL  1300050001. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0040 — DIFFERENCE — Ehab GL-to-category selection differs: .......03 Islamic Finance

Systems: ASSET - 100!C98, D98, F98, G98 · Ehab: K41 · GL: Current v6: GL Mapping!A3325, L3325 = 13101; 9 September: GL Mapping!A3325, L3325 = 13101

Ehab K41 selects GL sixth segments whose current categories are 13101. Systems criteria select 3000–3001, 3100–3112, 3148–3149, 3301–3305, 3314, 3501–3504, 3591, 3601, 3609, 3701–3718, 3720, 3730, 3740, 3791.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Some selected GL rows have no executable numeric category; see unresolved GL rows. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0041 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A42 · Ehab: L41 · GL: 

Ehab L41: outside from all loan personal + NonPersonal all sic code start by 4 Except  441 nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0042 — REVIEW — No numeric category bridge: .......03 Islamic Finance

Systems: ASSET - 100!A98 · Ehab: L41 · GL: 

Ehab L41: outside from all loan personal + NonPersonal all sic code start by 4 Except  441 nonresident (Outstanding_QAR+ Amortized_Earned_QAR + Loan_Fees_QAR). Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0043 — REVIEW — No numeric category bridge: .....01 Subsidiaries

Systems: ASSET - 100!A44 · Ehab: K43 · GL: 

Ehab K43: 1503000001, 1503000002, 1503000003, 1503000004, 1503000005, 1503000006, 1503000007. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0044 — DIFFERENCE — Ehab GL-to-category selection differs: .....01 Subsidiaries

Systems: ASSET - 100!C100, D100, F100, G100 · Ehab: K43 · GL: Current v6: GL Mapping!A8749, L8749 = 11901; Current v6: GL Mapping!A8752, L8752 = 11902; Current v6: GL Mapping!A8755, L8755 = 11903; Current v6: GL Mapping!A8758, L8758 = 11904; Current v6: GL Mapping!A8761, L8761 = 11905; 9 September: GL Mapping!A8749, L8749 = 11901; 9 September: GL Mapping!A8752, L8752 = 11902; 9 September: GL Mapping!A8755, L8755 = 11903; 9 September: GL Mapping!A8758, L8758 = 11904; 9 September: GL Mapping!A8761, L8761 = 11905

Ehab K43 selects GL sixth segments whose current categories are 11901–11907. Systems criteria select 8020, 8022.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0045 — REVIEW — No numeric category bridge: .....02 Associates

Systems: ASSET - 100!A45 · Ehab: K44 · GL: 

Ehab K44: 1503010011. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0046 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Associates

Systems: ASSET - 100!C101, D101, F101, G101 · Ehab: K44 · GL: Current v6: GL Mapping!A8774, L8774 = 11983; 9 September: GL Mapping!A8774, L8774 = 11983

Ehab K44 selects GL sixth segments whose current categories are 11983. Systems criteria select 8021, 8023.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0047 — REVIEW — No numeric category bridge: ...07 Investment in Real Estates

Systems: ASSET - 100!A46 · Ehab: K45 · GL: 

Ehab K45: 1700000001. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0048 — REVIEW — No numeric category bridge: ...07 Investment in Real Estates

Systems: ASSET - 100!A102 · Ehab: K45 · GL: 

Ehab K45: 1700000001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0049 — DIFFERENCE — Ehab GL-to-category selection differs: ...08 Net Fixed Assets

Systems: ASSET - 100!A47 · Ehab: K46 · GL: Current v6: GL Mapping!A8889, L8889 = 11001; Current v6: GL Mapping!A9004, L9004 = 11311; Current v6: GL Mapping!A9005, L9005 = 11311; Current v6: GL Mapping!A9006, L9006 = 11311; Current v6: GL Mapping!A9007, L9007 = 11311; 9 September: GL Mapping!A8889, L8889 = 11001; 9 September: GL Mapping!A9004, L9004 = 11311; 9 September: GL Mapping!A9005, L9005 = 11311; 9 September: GL Mapping!A9006, L9006 = 11311; 9 September: GL Mapping!A9007, L9007 = 11311

Ehab K46 selects GL sixth segments whose current categories are 11001, 11201, 11210, 11221, 11231, 11241, 11300, 11311–11312, 11510–11514, 11520, 11550–11551. Systems criteria select 11201, 11210, 11221–11231, 11241, 11300, 11510–11514, 11520.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0050 — DIFFERENCE — Ehab GL-to-category selection differs: ...08 Net Fixed Assets

Systems: ASSET - 100!C103, D103, F103, G103 · Ehab: K46 · GL: Current v6: GL Mapping!A8892, L8892 = 11201; Current v6: GL Mapping!A8893, L8893 = 11210; Current v6: GL Mapping!A8897, L8897 = 11210; Current v6: GL Mapping!A8910, L8910 = 11210; Current v6: GL Mapping!A8913, L8913 = 11210; 9 September: GL Mapping!A8892, L8892 = 11201; 9 September: GL Mapping!A8893, L8893 = 11210; 9 September: GL Mapping!A8897, L8897 = 11210; 9 September: GL Mapping!A8910, L8910 = 11210; 9 September: GL Mapping!A8913, L8913 = 11210

Ehab K46 selects GL sixth segments whose current categories are 11001, 11201, 11210, 11221, 11231, 11241, 11300, 11311–11312, 11510–11514, 11520, 11550–11551. Systems criteria select 11001, 11005.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0051 — REVIEW — No numeric category bridge: .....01 Positive F.V. of Derivatives

Systems: ASSET - 100!A49 · Ehab: K48 · GL: 

Ehab K48: 1909500000, 1909500001, 1909501001, 1909502001 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0052 — REVIEW — No numeric category bridge: .....01 Positive F.V. of Derivatives

Systems: ASSET - 100!A105 · Ehab: K48 · GL: 

Ehab K48: 1909500000, 1909500001, 1909501001, 1909502001 . Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0053 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Intangible Assets

Systems: ASSET - 100!A50 · Ehab: K49 · GL: Current v6: GL Mapping!A8979, L8979 = 11301; Current v6: GL Mapping!A8981, L8981 = 11303; Current v6: GL Mapping!A8982, L8982 = 11304; Current v6: GL Mapping!A8983, L8983 = 11305; Current v6: GL Mapping!A29768, L29768 = 11570; 9 September: GL Mapping!A8979, L8979 = 11301; 9 September: GL Mapping!A8981, L8981 = 11303; 9 September: GL Mapping!A8982, L8982 = 11304; 9 September: GL Mapping!A8983, L8983 = 11305; 9 September: GL Mapping!A29763, L29763 = 11570

Ehab K49 selects GL sixth segments whose current categories are 11301–11305, 11570–11573. Systems criteria select 11302.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0054 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Intangible Assets

Systems: ASSET - 100!C106, D106 · Ehab: K49 · GL: Current v6: GL Mapping!A29768, L29768 = 11570; Current v6: GL Mapping!A29769, L29769 = 11571; Current v6: GL Mapping!A29770, L29770 = 11572; Current v6: GL Mapping!A29771, L29771 = 11573; Current v6: GL Mapping!A8979, L8979 = 11301; 9 September: GL Mapping!A29763, L29763 = 11570; 9 September: GL Mapping!A29764, L29764 = 11571; 9 September: GL Mapping!A29765, L29765 = 11572; 9 September: GL Mapping!A29766, L29766 = 11573; 9 September: GL Mapping!A8979, L8979 = 11301

Ehab K49 selects GL sixth segments whose current categories are 11301–11305, 11570–11573. Systems criteria select 11301–11305.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0055 — DIFFERENCE — Ehab GL-to-category selection differs: .....03 Others

Systems: ASSET - 100!A51 · Ehab: K50 · GL: Current v6: GL Mapping!A9906, L9906 = 12199; Current v6: GL Mapping!A10288, L10288 = 13440; Current v6: GL Mapping!A10290, L10290 = 13440; Current v6: GL Mapping!A10295, L10295 = 13441; Current v6: GL Mapping!A10296, L10296 = 13446; 9 September: GL Mapping!A9906, L9906 = 12199; 9 September: GL Mapping!A10288, L10288 = 13440; 9 September: GL Mapping!A10290, L10290 = 13440; 9 September: GL Mapping!A10295, L10295 = 13441; 9 September: GL Mapping!A10296, L10296 = 13446

Ehab K50 selects GL sixth segments whose current categories are 3000–3899, 6640–6642, 12010–12012, 12030, 12033, 12101–12103, 12105, 12110–12111, 12121–12123, 12129–12149, 12170–12172, 12179–12199, 12500, 12505, 12511, 12515, 12651–12669, 12920–12921, 12930, 13151–13168, 13170–13171, 13400–13402, 13430, 13440–13446, 13450–13451, 13470, 13475–13476, 13480–13481, 13485–13487, 13490–13494, 13500, 13521–13527, 14002–14003, 14006–14007, 14009, 14011, 14021, 14061–14065, 14068, 16600–16610, 16650–16652, 16661, 16671–16674. Systems criteria select 3000–3999, 6000–6999, 12000–12099, 12101–12198, 12500–12599, 12650–12699, 12800–12809, 12920–12921, 13150–13179, 13400–13430, 13490–13499, 13510–13529, 14000–14069, 14150–14159, 14460–14999, 16600–16619, 16650–16699.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0056 — DIFFERENCE — Ehab GL-to-category selection differs: .....03 Others

Systems: ASSET - 100!C107, D107, F107, G107 · Ehab: K50 · GL: Current v6: GL Mapping!A9034, L9034 = 12010; Current v6: GL Mapping!A9036, L9036 = 12011; Current v6: GL Mapping!A9037, L9037 = 12011; Current v6: GL Mapping!A9039, L9039 = 12012; Current v6: GL Mapping!A9040, L9040 = 12012; 9 September: GL Mapping!A9034, L9034 = 12010; 9 September: GL Mapping!A9036, L9036 = 12011; 9 September: GL Mapping!A9037, L9037 = 12011; 9 September: GL Mapping!A9039, L9039 = 12012; 9 September: GL Mapping!A9040, L9040 = 12012

Ehab K50 selects GL sixth segments whose current categories are 3000–3899, 6640–6642, 12010–12012, 12030, 12033, 12101–12103, 12105, 12110–12111, 12121–12123, 12129–12149, 12170–12172, 12179–12199, 12500, 12505, 12511, 12515, 12651–12669, 12920–12921, 12930, 13151–13168, 13170–13171, 13400–13402, 13430, 13440–13446, 13450–13451, 13470, 13475–13476, 13480–13481, 13485–13487, 13490–13494, 13500, 13521–13527, 14002–14003, 14006–14007, 14009, 14011, 14021, 14061–14065, 14068, 16600–16610, 16650–16652, 16661, 16671–16674. Systems criteria select 1000–1999, 3000–3999, 6640–6649, 8025, 12101–12198, 12500–12599, 12650–12699, 12800–12809, 12920–12921, 13150–13169, 13400–13429, 13440–13459, 13470, 13489–13500, 13510–13529, 14000–14069, 14460–14999, 16600–16619, 134030.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0057 — REVIEW — No numeric category bridge: .....02 REPO

Systems: Liabilities!A12 · Ehab: K65 · GL: 

Ehab K65: 2200000020. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0058 — REVIEW — No numeric category bridge: .......01 Demand and Call

Systems: Liabilities!A16 · Ehab: K69 · GL: 

Ehab K69: inside 2100010013, 2100010015, 2100010016, 2100010021, 2100010022. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0059 — REVIEW — No numeric category bridge: .......01 Demand and Call

Systems: Liabilities!A16 · Ehab: L69 · GL: 

Ehab L69: outside 2100010006, 2100010008, 2100010009, 2100010010, 2100010011, 2100010012, 2100010014,2100010019, 2100010020. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0060 — REVIEW — No numeric category bridge: .......02 Placements

Systems: Liabilities!A17 · Ehab: K70 · GL: 

Ehab K70: inside 2200000001, 2305902001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0061 — REVIEW — No numeric category bridge: .......02 Placements

Systems: Liabilities!A17 · Ehab: L70 · GL: 

Ehab L70: outside  2305901002, 2306001001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0062 — REVIEW — No numeric category bridge: .......03 Borrowings / Finance

Systems: Liabilities!A18 · Ehab: L71 · GL: 

Ehab L71: 2306001010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0063 — REVIEW — No numeric category bridge: .......04 REPO

Systems: Liabilities!A19 · Ehab: L72 · GL: 

Ehab L72: 2306000001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0064 — REVIEW — No numeric category bridge: .......01 Current and Call

Systems: Liabilities!A23 · Ehab: K76 · GL: 

Ehab K76: from all Deposits file NonPersonal all sic code start by 441 account type (CAL, CUR, SAL, WMI). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0065 — REVIEW — No numeric category bridge: .......02 Saving and Time

Systems: Liabilities!A24 · Ehab: K77 · GL: 

Ehab K77: from all Deposits file NonPersonal all sic code start by 441 account type (DHW, MSP, MSS, NTD, PIA, PSV,SAV, SSV, YSV). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0066 — REVIEW — No numeric category bridge: .......01 Current and Call

Systems: Liabilities!A26 · Ehab: K79 · GL: 

Ehab K79: from all Deposits file NonPersonal all sic code start by 1,2,3 account type (CAL, CUR, SAL, WMI). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0067 — REVIEW — No numeric category bridge: .......02 Saving and Time

Systems: Liabilities!A27 · Ehab: K80 · GL: 

Ehab K80: from all Deposits file NonPersonal all sic code start by 1,2,3 account type (DHW, MSP, MSS, NTD, PIA, PSV,SAV, SSV, YSV). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0068 — REVIEW — No numeric category bridge: .......01 Current and Call

Systems: Liabilities!A29 · Ehab: K82 · GL: 

Ehab K82: from all Deposits file NonPersonal all sic code start by 4 Except 441 + all personal deposits account type (CAL, CUR, SAL, WMI). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0069 — REVIEW — No numeric category bridge: .......02 Saving and Time

Systems: Liabilities!A30 · Ehab: K83 · GL: 

Ehab K83: from all Deposits file NonPersonal all sic code start by 4 Except 441 + all personal deposits account type (DHW, MSP, MSS, NTD, PIA, PSV,SAV, SSV, YSV). Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0070 — DIFFERENCE — Ehab GL-to-category selection differs: ...06 Cash Margin

Systems: Liabilities!A39 · Ehab: K92 · GL: Current v6: GL Mapping!A30350, L30350 = 6502; Current v6: GL Mapping!A30353, L30353 = 6502; Current v6: GL Mapping!A30355, L30355 = 6502; Current v6: GL Mapping!A30357, L30357 = 6502; Current v6: GL Mapping!A30358, L30358 = 6502, 6500; 9 September: GL Mapping!A30345, L30345 = 6502; 9 September: GL Mapping!A30348, L30348 = 6502; 9 September: GL Mapping!A30350, L30350 = 6502; 9 September: GL Mapping!A30352, L30352 = 6502; 9 September: GL Mapping!A30355, L30355 = 6502

Ehab K92 selects GL sixth segments whose current categories are 6500–6503. Systems criteria select 4000–4001, 4999, 13402, 16500, 16599, 17566.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0071 — REVIEW — No numeric category bridge: .....01 Specific Loans / Finance

Systems: Liabilities!A41 · Ehab: K94 · GL: 

Ehab K94: GL's Start by 23050, 23090. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0072 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Specific Contingent liabilities

Systems: Liabilities!A42 · Ehab: K95 · GL: Current v6: GL Mapping!A29597, L29597 = 15110; Current v6: GL Mapping!A29598, L29598 = 15111; Current v6: GL Mapping!A29599, L29599 = 15111; Current v6: GL Mapping!A29600, L29600 = 15111; Current v6: GL Mapping!A29601, L29601 = 15112; 9 September: GL Mapping!A29592, L29592 = 15110; 9 September: GL Mapping!A29593, L29593 = 15111; 9 September: GL Mapping!A29594, L29594 = 15111; 9 September: GL Mapping!A29595, L29595 = 15111; 9 September: GL Mapping!A29596, L29596 = 15112

Ehab K95 selects GL sixth segments whose current categories are 15110–15115. Systems criteria select 15110–15115, 15120–15125.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0073 — REVIEW — No numeric category bridge: .....07 Interest / Income in Suspense

Systems: Liabilities!A47 · Ehab: K100 · GL: 

Ehab K100: GL's Start by 2301. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0074 — REVIEW — No numeric category bridge: .....08 Expected Credit Loss

Systems: Liabilities!A48 · Ehab: K101 · GL: 

Ehab K101: GL's Start by 23055, 23080, 23085. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0075 — REVIEW — No numeric category bridge: .....01 Deffered Interest / Income

Systems: Liabilities!A50 · Ehab: K103 · GL: 

Ehab K103: GL's Start by 2300 Except  2300020010, 2300070010. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0076 — REVIEW — No numeric category bridge: .....02 Negative F.V. of Derivatives

Systems: Liabilities!A51 · Ehab: K104 · GL: 

Ehab K104: GL's Start by 29095. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0077 — REVIEW — No numeric category bridge: .....03 Net Profit for The Period

Systems: Liabilities!A52 · Ehab: K105 · GL: 

Ehab K105: 3800000001. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0078 — DIFFERENCE — Ehab GL-to-category selection differs: .....04 Others

Systems: Liabilities!A53 · Ehab: K106 · GL: Current v6: GL Mapping!A29461, L29461 = 13804; Current v6: GL Mapping!A29463, L29463 = 13804; Current v6: GL Mapping!A51997, L51997 = 13804; Current v6: GL Mapping!A51998, L51998 = 3000-3740; Current v6: GL Mapping!A29465, L29465 = 13803; 9 September: GL Mapping!A29456, L29456 = 13804; 9 September: GL Mapping!A29458, L29458 = 13804; 9 September: GL Mapping!A51951, L51951 = 13804; 9 September: GL Mapping!A51952, L51952 = 3000-3740; 9 September: GL Mapping!A29460, L29460 = 13803

Ehab K106 selects GL sixth segments whose current categories are 3000–3740, 5001, 6001, 6003, 6006, 6010–6011, 6013, 6015, 6020–6021, 6031, 6033, 6041, 6051, 6102–6106, 6111, 6113, 6121, 6123, 6601–6611, 6621–6630, 6641–6643, 6701, 6714, 6716, 6721, 6741, 8013, 13461, 13800–13804, 14032–14035, 14046, 14058, 14065–14067, 15050–15055, 15301, 15311–15313, 15315, 15321, 15325–15326, 15330–15332, 15335–15336, 15338–15340, 15342, 15344–15346, 15349, 15353, 15355, 15358–15360, 15362–15369, 15380–15390, 15400–15401, 15405–15412, 15420–15423, 16530, 16700–16705, 16720, 16725, 16800–16803, 16810–16813, 16821–16822, 16825, 16830–16831, 17215, 17255–17256, 17401–17403, 17405–17413, 17415–17419, 17504–17505, 17515–17517, 17550–17552, 17560–17561, 17565–17566, 17601–17605, 17620–17621, 17630–17631, 17660, 17670, 17920–17921, 17930–17934, 17940–17943. Systems criteria select 15311–15399, 16800–16831, 17670–17699.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0079 — DIFFERENCE — Ehab GL-to-category selection differs: .....04 Treasury Shares - Prem. / Disc.

Systems: Liabilities!C58, D58 · Ehab: K111 · GL: Current v6: GL Mapping!A34388, L34388 = 18008; 9 September: GL Mapping!A34382, L34382 = 18008

Ehab K111 selects GL sixth segments whose current categories are 18008. Systems criteria select 18006.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0080 — DIFFERENCE — Ehab GL-to-category selection differs: .....09 Retained Earnings

Systems: Liabilities!C63, D63 · Ehab: K116 · GL: Current v6: GL Mapping!A36776, L36776 = 18051; Current v6: GL Mapping!A35587, L35587 = 18040; Current v6: GL Mapping!A36778, L36778 = 18002; 9 September: GL Mapping!A36770, L36770 = 18051; 9 September: GL Mapping!A35581, L35581 = 18040; 9 September: GL Mapping!A36772, L36772 = 18002

Ehab K116 selects GL sixth segments whose current categories are 18002, 18040, 18051. Systems criteria select 18002, 18040, 18045–18048, 18050.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0081 — REVIEW — No numeric category bridge: .....01 Letters of Guarantee

Systems: CONTRA ITEMS!A9 · Ehab: K129 · GL: 

Ehab K129: 8001000001. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0082 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Letters of Credit

Systems: CONTRA ITEMS!A10 · Ehab: K130 · GL: Current v6: GL Mapping!A48314, L48314 = 23005-23024, 23051-23074; Current v6: GL Mapping!A48320, L48320 = 23005-23024; 9 September: GL Mapping!A48303, L48303 = 23005-23024; 9 September: GL Mapping!A48305, L48305 = 23005-23024

Ehab K130 selects GL sixth segments whose current categories are 23005–23024, 23051–23074. Systems criteria select 23000–23999.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0083 — DIFFERENCE — Ehab GL-to-category selection differs: ...03 Derivative Contracts

Systems: CONTRA ITEMS!C16, F16 · Ehab: K136 · GL: Current v6: GL Mapping!A48450, L48450 = 19601; Current v6: GL Mapping!A50338, L50338 = 19840; Current v6: GL Mapping!A50339, L50339 = 19841; Current v6: GL Mapping!A50350, L50350 = 19851; Current v6: GL Mapping!A50353, L50353 = 19852; 9 September: GL Mapping!A48424, L48424 = 19601; 9 September: GL Mapping!A50292, L50292 = 19840; 9 September: GL Mapping!A50293, L50293 = 19841; 9 September: GL Mapping!A50304, L50304 = 19851; 9 September: GL Mapping!A50307, L50307 = 19852

Ehab K136 selects GL sixth segments whose current categories are 19601, 19840–19841, 19851–19852. Systems criteria select 19701–19706.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0084 — DIFFERENCE — Ehab GL-to-category selection differs: ...04 Assets Under Management

Systems: CONTRA ITEMS!A17 · Ehab: K137 · GL: Current v6: GL Mapping!A49213, L49213 = 19801; Current v6: GL Mapping!A49214, L49214 = 19805; Current v6: GL Mapping!A49215, L49215 = 19810; Current v6: GL Mapping!A49219, L49219 = 19811; Current v6: GL Mapping!A49223, L49223 = 19812; 9 September: GL Mapping!A49167, L49167 = 19801; 9 September: GL Mapping!A49168, L49168 = 19805; 9 September: GL Mapping!A49169, L49169 = 19810; 9 September: GL Mapping!A49173, L49173 = 19811; 9 September: GL Mapping!A49177, L49177 = 19812

Ehab K137 selects GL sixth segments whose current categories are 19801, 19805, 19810–19821. Systems criteria select 19901–19929.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0085 — DIFFERENCE — Ehab GL-to-category selection differs: .........01 Issued by Governments

Systems: Income!B21, C21, D21, F21, G21 · Ehab: K162 · GL: Current v6: GL Mapping!A38424, J38424 = 65073; Current v6: GL Mapping!A38426, J38426 = 65073; 9 September: GL Mapping!A38418, J38418 = 65073; 9 September: GL Mapping!A38420, J38420 = 65073

Ehab K162 selects GL sixth segments whose current categories are 65073. Systems criteria select 65037.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0086 — REVIEW — No numeric category bridge: .....04 From Credit Facilities

Systems: Income!A25 · Ehab: K166 · GL: 

Ehab K166: starts with 4001 Except  400102, 400107. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0087 — REVIEW — No numeric category bridge: .......03 Equity Participation

Systems: Income!A48 · Ehab: K189 · GL: 

Ehab K189: 4003010003. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0088 — REVIEW — No numeric category bridge: .....02 Net Profit ( Loss ) From Sale

Systems: Income!A63 · Ehab: K204 · GL: 

Ehab K204: 4500090010. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0089 — DIFFERENCE — Ehab GL-to-category selection differs: .....01 Credit Facilities

Systems: Income!B70, C70, D70, F70, G70 · Ehab: K211 · GL: Current v6: GL Mapping!A41799, J41799 = 52652; Current v6: GL Mapping!A41808, J41808 = 52652; Current v6: GL Mapping!A41817, J41817 = 52652; Current v6: GL Mapping!A38447, J38447 = 52260; Current v6: GL Mapping!A38450, J38450 = 52260; 9 September: GL Mapping!A41793, J41793 = 52652; 9 September: GL Mapping!A41802, J41802 = 52652; 9 September: GL Mapping!A41811, J41811 = 52652; 9 September: GL Mapping!A38441, J38441 = 52260; 9 September: GL Mapping!A38444, J38444 = 52260

Ehab K211 selects GL sixth segments whose current categories are 52260, 52651–52653, 52664–52665. Systems criteria select 52260, 52651, 52653, 52664–52665.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0090 — DIFFERENCE — Ehab GL-to-category selection differs: .....02 Contingent liabilities

Systems: Income!B71, C71, D71, F71, G71 · Ehab: K212 · GL: Current v6: GL Mapping!A40189, J40189 = 52300; Current v6: GL Mapping!A40207, J40207 = 52301; Current v6: GL Mapping!A40217, J40217 = 52308; Current v6: GL Mapping!A40229, J40229 = 52368; Current v6: GL Mapping!A40240, J40240 = 52370; 9 September: GL Mapping!A40183, J40183 = 52300; 9 September: GL Mapping!A40201, J40201 = 52301; 9 September: GL Mapping!A40211, J40211 = 52308; 9 September: GL Mapping!A40223, J40223 = 52368; 9 September: GL Mapping!A40234, J40234 = 52370

Ehab K212 selects GL sixth segments whose current categories are 52300–52301, 52308, 52368, 52370, 52372, 52398. Systems criteria select 52300–52399.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0091 — DIFFERENCE — Ehab GL-to-category selection differs: .....05 Other Banking Services

Systems: Income!B74, C74, D74, F74, G74 · Ehab: K215 · GL: Current v6: GL Mapping!A39045, L39045 = 65150; Current v6: GL Mapping!A39048, L39048 = 65151; Current v6: GL Mapping!A40126, J40126 = 65153; Current v6: GL Mapping!A40182, J40182 = 65139; Current v6: GL Mapping!A40183, J40183 = 65139; 9 September: GL Mapping!A39039, L39039 = 65150; 9 September: GL Mapping!A39042, L39042 = 65151; 9 September: GL Mapping!A40120, J40120 = 65153; 9 September: GL Mapping!A40176, J40176 = 65139; 9 September: GL Mapping!A40177, J40177 = 65139

Ehab K215 selects GL sixth segments whose current categories are 52005–52006, 52010–52012, 52016–52017, 52040, 52070–52071, 52112–52113, 52161, 52258, 52270, 65100–65103, 65105–65106, 65109, 65111–65139, 65150–65151, 65153–65154, 65160, 65162, 65164–65166, 65168–65180, 65182–65194, 65196. Systems criteria select 52000–52100, 52102–52113, 52125, 52130–52131, 52257–52258, 52270–52272, 65100–65103, 65105–65106, 65109, 65111–65138, 65160, 65162, 65164–65166, 65168–65180, 65182–65194.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0092 — DIFFERENCE — Ehab GL-to-category selection differs: .....03 Others

Systems: Income!B80, D80, F80, G80 · Ehab: K221 · GL: Current v6: GL Mapping!A41795, J41795 = 52743; Current v6: GL Mapping!A42303, J42303 = 66020; Current v6: GL Mapping!A42309, J42309 = 66020; Current v6: GL Mapping!A42310, J42310 = 66020; Current v6: GL Mapping!A42311, J42311 = 66020; 9 September: GL Mapping!A41789, J41789 = 52743; 9 September: GL Mapping!A42297, J42297 = 66020; 9 September: GL Mapping!A42303, J42303 = 66020; 9 September: GL Mapping!A42304, J42304 = 66020; 9 September: GL Mapping!A42305, J42305 = 66020

Ehab K221 selects GL sixth segments whose current categories are 52743, 54600, 54700, 65220–65221, 65227–65228, 66020, 66043–66044. Systems criteria select 54600, 54700, 65220–65221, 65227–65228, 66022, 66043–66044.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0093 — DIFFERENCE — Ehab GL-to-category selection differs: .........02 Bonds

Systems: Expense!B22, C22, D22, F22, G22 · Ehab: K248 · GL: Current v6: GL Mapping!A48195, J48195 = 66560; Current v6: GL Mapping!A48197, J48197 = 66561; Current v6: GL Mapping!A48201, J48201 = 66562; 9 September: GL Mapping!A48188, J48188 = 66560; 9 September: GL Mapping!A48190, J48190 = 66561; 9 September: GL Mapping!A48194, J48194 = 66562

Ehab K248 selects GL sixth segments whose current categories are 66560–66562. Systems criteria select 60031–60034.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0094 — DIFFERENCE — Ehab GL-to-category selection differs: .......02 Banks

Systems: Expense!B30, C30, D30, F30, G30 · Ehab: K256 · GL: Current v6: GL Mapping!A48224, J48224 = 66586; Current v6: GL Mapping!A51900, L51900 = 66587; Current v6: GL Mapping!A51906, L51906 = 66588; Current v6: GL Mapping!A46531, J46531 = 66502; Current v6: GL Mapping!A46542, J46542 = 66505; 9 September: GL Mapping!A48217, J48217 = 66586; 9 September: GL Mapping!A51854, L51854 = 66587; 9 September: GL Mapping!A51860, L51860 = 66588; 9 September: GL Mapping!A46524, J46524 = 66502; 9 September: GL Mapping!A46535, J46535 = 66505

Ehab K256 selects GL sixth segments whose current categories are 66502, 66505, 66580–66588. Systems criteria select 15154, 66502, 66505, 66580–66585.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0095 — DIFFERENCE — Ehab GL-to-category selection differs: .........04 Corporates

Systems: Expense!B35, C35, D35, F35, G35 · Ehab: K261 · GL: Current v6: GL Mapping!A46573, L46573 = 50000, 50001, 50500, 50510; Current v6: GL Mapping!A46456, J46456 = 50000; Current v6: GL Mapping!A46467, J46467 = 50000; Current v6: GL Mapping!A46476, J46476 = 50000; Current v6: GL Mapping!A46488, J46488 = 50000; 9 September: GL Mapping!A46566, L46566 = 50000, 50001, 50500, 50510; 9 September: GL Mapping!A46449, J46449 = 50000; 9 September: GL Mapping!A46460, J46460 = 50000; 9 September: GL Mapping!A46469, J46469 = 50000; 9 September: GL Mapping!A46481, J46481 = 50000

Ehab K261 selects GL sixth segments whose current categories are 50000–50001, 50500, 50510. Systems criteria select 50000–50001.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0096 — DIFFERENCE — Ehab GL-to-category selection differs: .........05 Personal

Systems: Expense!B36 · Ehab: K262 · GL: Current v6: GL Mapping!A45612, J45612 = 50000; Current v6: GL Mapping!A45619, J45619 = 50000; Current v6: GL Mapping!A45623, J45623 = 50000; Current v6: GL Mapping!A45821, J45821 = 50000; Current v6: GL Mapping!A45828, J45828 = 50000; 9 September: GL Mapping!A45605, J45605 = 50000; 9 September: GL Mapping!A45612, J45612 = 50000; 9 September: GL Mapping!A45616, J45616 = 50000; 9 September: GL Mapping!A45814, J45814 = 50000; 9 September: GL Mapping!A45821, J45821 = 50000

Ehab K262 selects GL sixth segments whose current categories are 50000–50001, 50632–50633. Systems criteria select 50000–50001, 50632–50633, 51000.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0097 — REVIEW — No numeric category bridge: .....07 Expected Credit Loss

Systems: Expense!A78 · Ehab: K304 · GL: 

Ehab K304: starts with 5500006, 5500007. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0098 — REVIEW — No numeric category bridge: .....01 Fixed Assets

Systems: Expense!A97 · Ehab: K323 · GL: 

Ehab K323: starts with 52000 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0099 — DIFFERENCE — Ehab GL-to-category selection differs: .......02 The right to use leased assets

Systems: Expense!B101, C101, D101, F101, G101 · Ehab: K327 · GL: Current v6: GL Mapping!A45579, J45579 = 64650; Current v6: GL Mapping!A45580, J45580 = 64650; Current v6: GL Mapping!A45582, J45582 = 64650; Current v6: GL Mapping!A45583, J45583 = 64650; Current v6: GL Mapping!A45584, J45584 = 64651; 9 September: GL Mapping!A45572, J45572 = 64650; 9 September: GL Mapping!A45573, J45573 = 64650; 9 September: GL Mapping!A45575, J45575 = 64650; 9 September: GL Mapping!A45576, J45576 = 64650; 9 September: GL Mapping!A45577, J45577 = 64651

Ehab K327 selects GL sixth segments whose current categories are 64650–64655. Systems criteria select 64651–64655.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0100 — REVIEW — No numeric category bridge: .....01 Wages and salaries

Systems: Expense!A104 · Ehab: K330 · GL: 

Ehab K330: starts with 50000 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0101 — REVIEW — No numeric category bridge: .....04 Other staff costs

Systems: Expense!A107 · Ehab: K333 · GL: 

Ehab K333: starts with 50050,50080,50090 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0102 — REVIEW — No numeric category bridge: .....02 Legal and professional fees

Systems: Expense!A110 · Ehab: K336 · GL: 

Ehab K336: starts with 5100030 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0103 — REVIEW — No numeric category bridge: .....04 Communications , utilities and insurance

Systems: Expense!A112 · Ehab: K338 · GL: 

Ehab K338: starts with 5100002,5100003 . Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0104 — DIFFERENCE — Ehab GL-to-category selection differs: .....05 Publications and stationery

Systems: Expense!B113, C113, D113, F113, G113 · Ehab: K339 · GL: Current v6: GL Mapping!A44901, J44901 = 61131; Current v6: GL Mapping!A44902, J44902 = 61131; Current v6: GL Mapping!A44903, J44903 = 61131; Current v6: GL Mapping!A44904, J44904 = 61131; Current v6: GL Mapping!A44905, J44905 = 61131; 9 September: GL Mapping!A44894, J44894 = 61131; 9 September: GL Mapping!A44895, J44895 = 61131; 9 September: GL Mapping!A44896, J44896 = 61131; 9 September: GL Mapping!A44897, J44897 = 61131; 9 September: GL Mapping!A44898, J44898 = 61131

Ehab K339 selects GL sixth segments whose current categories are 61115–61116, 61130–61131. Systems criteria select 61115–61116, 61130.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0105 — DIFFERENCE — Ehab GL-to-category selection differs: .....09 Others

Systems: Expense!B117, C117, D117, F117, G117 · Ehab: K343 · GL: Current v6: GL Mapping!A44392, J44392 = 61065; Current v6: GL Mapping!A44398, J44398 = 61065; Current v6: GL Mapping!A44399, J44399 = 61065; Current v6: GL Mapping!A44400, J44400 = 61065; Current v6: GL Mapping!A44401, J44401 = 61065; 9 September: GL Mapping!A44385, J44385 = 61065; 9 September: GL Mapping!A44391, J44391 = 61065; 9 September: GL Mapping!A44392, J44392 = 61065; 9 September: GL Mapping!A44393, J44393 = 61065; 9 September: GL Mapping!A44394, J44394 = 61065

Ehab K343 selects GL sixth segments whose current categories are 51200, 61010–61012, 61045, 61050–61056, 61060, 61065, 61070–61073, 61080, 61100–61102, 61110, 61140–61142, 61190–61195, 61205, 61221–61225, 61230–61235, 66520–66531, 66590, 66595, 66606. Systems criteria select 51200, 61010–61012, 61045, 61050–61056, 61060, 61070–61102, 61110, 61140–61142, 61190–61195, 61205, 61221–61225, 61230–61235, 61605, 66520–66525, 66531, 66590, 66595, 66606.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0106 — DIFFERENCE — Ehab GL-to-category selection differs: 01 Cash on hand

Systems: Table 1!B9, C9 · Ehab: K358 · GL: Current v6: GL Mapping!A2596, L2596 = 12905; Current v6: GL Mapping!A2599, L2599 = 12905; Current v6: GL Mapping!A2600, L2600 = 12905; Current v6: GL Mapping!A2601, L2601 = 12905; Current v6: GL Mapping!A2602, L2602 = 12903; 9 September: GL Mapping!A2596, L2596 = 12905; 9 September: GL Mapping!A2599, L2599 = 12905; 9 September: GL Mapping!A2600, L2600 = 12905; 9 September: GL Mapping!A2601, L2601 = 12905; 9 September: GL Mapping!A2602, L2602 = 12903

Ehab K358 selects GL sixth segments whose current categories are 10001, 10009, 10011, 10024–10025, 12903–12907. Systems criteria select 10000–10025.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0107 — DIFFERENCE — Ehab GL-to-category selection differs: .......01 Clearing Account

Systems: Table 2!B12, E12 · Ehab: L380 · GL: Current v6: GL Mapping!A2581, L2581 = 18062; Current v6: GL Mapping!A2586, L2586 = 5002; 9 September: GL Mapping!A2586, L2586 = 5002

Ehab L380 selects GL sixth segments whose current categories are 5002, 18062. Systems criteria select 5002.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0108 — REVIEW — No numeric category bridge: .........01 Commercial / Conventional

Systems: Table 2!A19 · Ehab: L387 · GL: 

Ehab L387: All Gl's  Start by 11 Except 1101000004. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0109 — REVIEW — No numeric category bridge: .........02 Islamic

Systems: Table 2!A20 · Ehab: L388 · GL: 

Ehab L388: 1101000004. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0110 — DIFFERENCE — Ehab GL-to-category selection differs: ......02 Sukuk

Systems: Table 6!C11, D11, E11, G11, H11 · Ehab: K566 · GL: Current v6: GL Mapping!A8695, L8695 = 13207; Current v6: GL Mapping!A8697, L8697 = 13207; Current v6: GL Mapping!A8803, L8803 = 13273; Current v6: GL Mapping!A8804, L8804 = 13273; Current v6: GL Mapping!A8805, L8805 = 13274; 9 September: GL Mapping!A8695, L8695 = 13207; 9 September: GL Mapping!A8697, L8697 = 13207; 9 September: GL Mapping!A8803, L8803 = 13273; 9 September: GL Mapping!A8804, L8804 = 13273; 9 September: GL Mapping!A8805, L8805 = 13274

Ehab K566 selects GL sixth segments whose current categories are 13207, 13273–13275, 13281. Systems criteria select 13206–13207, 13273–13275, 13281.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0111 — REVIEW — No numeric category bridge: ......02 Sukuk

Systems: Table 6!B45 · Ehab: K566 · GL: 

Ehab K566: 1500000012, 1500000000, 1600000010, 1600000011, 1600000012, 1600010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0112 — REVIEW — No numeric category bridge: ......03 Shares

Systems: Table 6!B46 · Ehab: K567 · GL: 

Ehab K567: 1500000001, 1600000001, 1600000015. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0113 — REVIEW — No numeric category bridge: ........03 Shares

Systems: Table 6!B52 · Ehab: K573 · GL: 

Ehab K573: 1600000002. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0114 — REVIEW — No numeric category bridge: ........04 Mutual funds and Others

Systems: Table 6!B53 · Ehab: K574 · GL: 

Ehab K574: 1500000003, 1600000003. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0115 — DIFFERENCE — Ehab GL-to-category selection differs: ........03 Shares

Systems: Table 6!C23, D23, E23, G23, H23 · Ehab: K578 · GL: Current v6: GL Mapping!A8769, L8769 = 11908; Current v6: GL Mapping!A8704, L8704 = 13221; Current v6: GL Mapping!A8705, L8705 = 13221; Current v6: GL Mapping!A8713, L8713 = 13231; Current v6: GL Mapping!A8714, L8714 = 13231; 9 September: GL Mapping!A8769, L8769 = 11908; 9 September: GL Mapping!A8704, L8704 = 13221; 9 September: GL Mapping!A8705, L8705 = 13221; 9 September: GL Mapping!A8713, L8713 = 13231; 9 September: GL Mapping!A8714, L8714 = 13231

Ehab K578 selects GL sixth segments whose current categories are 11908, 13221, 13230–13231, 13286, 13289, 13291. Systems criteria select 8020, 8023, 13221, 13230–13231, 13286, 13289, 13291.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0116 — REVIEW — No numeric category bridge: ........03 Shares

Systems: Table 6!B57 · Ehab: K578 · GL: 

Ehab K578: 1501010001, 1503000008, 1501000001, 1501020001, 1601000001, 1601000011, 1603010002, 1601010001. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0117 — DIFFERENCE — Ehab GL-to-category selection differs: ........04 Mutual funds and Others **

Systems: Table 6!C24, G24, H24 · Ehab: K579 · GL: Current v6: GL Mapping!A8838, L8838 = 13292; 9 September: GL Mapping!A8838, L8838 = 13292

Ehab K579 selects GL sixth segments whose current categories are 13292. Systems criteria select 13287, 13292.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0118 — REVIEW — No numeric category bridge: ........04 Mutual funds and Others **

Systems: Table 6!B58 · Ehab: K579 · GL: 

Ehab K579: 1601010005. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0119 — REVIEW — No numeric category bridge: ....01 Debt Securities ( Amortized Cost )

Systems: Table 6!B60 · Ehab: K581 · GL: 

Ehab K581: 1502010005. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0120 — DIFFERENCE — Ehab GL-to-category selection differs: ....02 Sukuk

Systems: Table 6!C27, D27, E27, G27, H27 · Ehab: K582 · GL: Current v6: GL Mapping!A8734, L8734 = 13250; Current v6: GL Mapping!A8736, L8736 = 13251; Current v6: GL Mapping!A8738, L8738 = 13252; Current v6: GL Mapping!A8856, L8856 = 13310; Current v6: GL Mapping!A8860, L8860 = 13311; 9 September: GL Mapping!A8734, L8734 = 13250; 9 September: GL Mapping!A8736, L8736 = 13251; 9 September: GL Mapping!A8738, L8738 = 13252; 9 September: GL Mapping!A8856, L8856 = 13310; 9 September: GL Mapping!A8860, L8860 = 13311

Ehab K582 selects GL sixth segments whose current categories are 13250–13252, 13310–13312, 13315. Systems criteria select 13250–13252, 13257–13259, 13310–13312, 13315–13317.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0121 — REVIEW — No numeric category bridge: ....02 Sukuk

Systems: Table 6!B61 · Ehab: K582 · GL: 

Ehab K582: 1502000010, 1502000011, 1502000012, 1602000010, 1602000011, 1602000012, 1602010010. Systems linked row has treasury/outbound logic.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Systems uses treasury/outbound data; GL equivalence is not established.

## NBS-0122 — DIFFERENCE — Ehab GL-to-category selection differs: ...........01 Credit Cards

Systems: Table 8!B60 · Ehab: L682 · GL: Current v6: GL Mapping!A3325, L3325 = 13101; 9 September: GL Mapping!A3325, L3325 = 13101

Ehab L682 selects GL sixth segments whose current categories are 13101. Systems criteria select 13101, 13103, 13105.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0123 — REVIEW — No numeric category bridge: ......01 Governments

Systems: Table 9!A51 · Ehab: L735 · GL: 

Ehab L735: sic start by 1 Except rim 2398. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0124 — REVIEW — No numeric category bridge: ......03 Government Inst.

Systems: Table 9!A53 · Ehab: L737 · GL: 

Ehab L737: sic start by 2. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0125 — REVIEW — No numeric category bridge: ......04 Semi Government Inst.

Systems: Table 9!A54 · Ehab: L738 · GL: 

Ehab L738: sic start by 3. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0126 — REVIEW — No numeric category bridge: ........02 Other Corporates

Systems: Table 9!A67 · Ehab: L751 · GL: 

Ehab L751: Sic start by 4 type SYN. Systems linked row has no safely traceable explicit category selection.

Handling: Obtain the source-specific bridge or complete the original category/balance definition.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Ehab mixes loan/customer logic with GL references; GL-only portion is incomplete.

## NBS-0127 — DIFFERENCE — Ehab GL-to-category selection differs: ...........01 Investment Companies

Systems: TABLE 14 !C27 · Ehab: K937 · GL: Current v6: GL Mapping!A8749, L8749 = 11901; 9 September: GL Mapping!A8749, L8749 = 11901

Ehab K937 selects GL sixth segments whose current categories are 11901. Systems criteria select 11901, 11903.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0128 — DIFFERENCE — Ehab GL-to-category selection differs: ...........02 Finance Companies

Systems: TABLE 14 !C28 · Ehab: K938 · GL: Current v6: GL Mapping!A8755, L8755 = 11903; Current v6: GL Mapping!A8758, L8758 = 11904; Current v6: GL Mapping!A8761, L8761 = 11905; Current v6: GL Mapping!A8764, L8764 = 11906; Current v6: GL Mapping!A8767, L8767 = 11907; 9 September: GL Mapping!A8755, L8755 = 11903; 9 September: GL Mapping!A8758, L8758 = 11904; 9 September: GL Mapping!A8761, L8761 = 11905; 9 September: GL Mapping!A8764, L8764 = 11906; 9 September: GL Mapping!A8767, L8767 = 11907

Ehab K938 selects GL sixth segments whose current categories are 11902–11907. Systems criteria select 11902, 11908.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0129 — DIFFERENCE — Ehab GL-to-category selection differs: .......01 Lands

Systems: Table 15!B10 · Ehab: K976 · GL: Current v6: GL Mapping!A8888, L8888 = 13337; 9 September: GL Mapping!A8888, L8888 = 13337

Ehab K976 selects GL sixth segments whose current categories are 13337. Systems criteria select 11320.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0130 — DIFFERENCE — Ehab GL-to-category selection differs: .......01 Lands

Systems: Table 16!B8 · Ehab: N993 · GL: Current v6: GL Mapping!A8888, L8888 = 13337; 9 September: GL Mapping!A8888, L8888 = 13337

Ehab N993 selects GL sixth segments whose current categories are 13337. Systems criteria select 11320.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0131 — DIFFERENCE — Ehab GL-to-category selection differs: 01 Lands and Buildings

Systems: Table 17 !B8, D8 · Ehab: L1011 · GL: Current v6: GL Mapping!A8889, L8889 = 11001; Current v6: GL Mapping!A8890, L8890 = 11005; Current v6: GL Mapping!A29657, L29657 = 11500; 9 September: GL Mapping!A8889, L8889 = 11001; 9 September: GL Mapping!A8890, L8890 = 11005; 9 September: GL Mapping!A29652, L29652 = 11500

Ehab L1011 selects GL sixth segments whose current categories are 11001, 11005, 11500. Systems criteria select 11001, 11005, 11500, 11515.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0132 — DIFFERENCE — Ehab GL-to-category selection differs: 03 Furniture and Equipments

Systems: Table 17 !B10, D10 · Ehab: L1013 · GL: Current v6: GL Mapping!A8924, L8924 = 11221; Current v6: GL Mapping!A8937, L8937 = 11221; Current v6: GL Mapping!A8940, L8940 = 11221; Current v6: GL Mapping!A8943, L8943 = 11221; Current v6: GL Mapping!A8944, L8944 = 11221; 9 September: GL Mapping!A8924, L8924 = 11221; 9 September: GL Mapping!A8937, L8937 = 11221; 9 September: GL Mapping!A8940, L8940 = 11221; 9 September: GL Mapping!A8943, L8943 = 11221; 9 September: GL Mapping!A8944, L8944 = 11221

Ehab L1013 selects GL sixth segments whose current categories are 11221, 11231, 11512–11513. Systems criteria select 11221–11231, 11512–11513.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0133 — DIFFERENCE — Ehab GL-to-category selection differs: .........01 Lands and Buildings

Systems: Table 17 !B14, D14, B16, D16 · Ehab: L1019 · GL: Current v6: GL Mapping!A9008, L9008 = 11312; Current v6: GL Mapping!A9016, L9016 = 11312; Current v6: GL Mapping!A8984, L8984 = 11300; Current v6: GL Mapping!A8998, L8998 = 11300; Current v6: GL Mapping!A9001, L9001 = 11300; 9 September: GL Mapping!A9008, L9008 = 11312; 9 September: GL Mapping!A9016, L9016 = 11312; 9 September: GL Mapping!A8984, L8984 = 11300; 9 September: GL Mapping!A8998, L8998 = 11300; 9 September: GL Mapping!A9001, L9001 = 11300

Ehab L1019 selects GL sixth segments whose current categories are 11300, 11311–11312, 11520, 11550–11551. Systems criteria select 11300, 11311, 11314, 11520, 11550–11551, 11553, 13112.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0134 — DIFFERENCE — Ehab GL-to-category selection differs: .........04 Customers Relations

Systems: TABLE 18!B15, C15 · Ehab: K1041 · GL: Current v6: GL Mapping!A8981, L8981 = 11303; Current v6: GL Mapping!A29769, L29769 = 11571; 9 September: GL Mapping!A8981, L8981 = 11303; 9 September: GL Mapping!A29764, L29764 = 11571

Ehab K1041 selects GL sixth segments whose current categories are 11303, 11571. Systems criteria select 11301, 11303, 11571.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0135 — DIFFERENCE — Ehab GL-to-category selection differs: .........05 Other

Systems: TABLE 18!B16, C16 · Ehab: K1042 · GL: Current v6: GL Mapping!A8979, L8979 = 11301; Current v6: GL Mapping!A29768, L29768 = 11570; Current v6: GL Mapping!A8982, L8982 = 11304; Current v6: GL Mapping!A8983, L8983 = 11305; Current v6: GL Mapping!A29770, L29770 = 11572; 9 September: GL Mapping!A8979, L8979 = 11301; 9 September: GL Mapping!A29763, L29763 = 11570; 9 September: GL Mapping!A8982, L8982 = 11304; 9 September: GL Mapping!A8983, L8983 = 11305; 9 September: GL Mapping!A29765, L29765 = 11572

Ehab K1042 selects GL sixth segments whose current categories are 11301, 11304–11305, 11570, 11572–11573. Systems criteria select 11304–11305, 11550, 11572–11573.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0136 — DIFFERENCE — Ehab GL-to-category selection differs: 01 Accrued Income

Systems: TABLE 19!C10, D10, F10, G10 · Ehab: K1054 · GL: Current v6: GL Mapping!A10288, L10288 = 13440; Current v6: GL Mapping!A10290, L10290 = 13440; Current v6: GL Mapping!A10300, L10300 = 13442; Current v6: GL Mapping!A10307, L10307 = 13443; Current v6: GL Mapping!A10309, L10309 = 13444; 9 September: GL Mapping!A10288, L10288 = 13440; 9 September: GL Mapping!A10290, L10290 = 13440; 9 September: GL Mapping!A10300, L10300 = 13442; 9 September: GL Mapping!A10307, L10307 = 13443; 9 September: GL Mapping!A10309, L10309 = 13444

Ehab K1054 selects GL sixth segments whose current categories are 13440, 13442–13444. Systems criteria select 1000–1999, 3000–3999, 13440–13459.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0137 — DIFFERENCE — Ehab GL-to-category selection differs: 02 Prepaid Expenses

Systems: TABLE 19!C11, F11 · Ehab: K1055 · GL: Current v6: GL Mapping!A9459, L9459 = 12101; Current v6: GL Mapping!A9472, L9472 = 12101; Current v6: GL Mapping!A9475, L9475 = 12101; Current v6: GL Mapping!A9478, L9478 = 12101; Current v6: GL Mapping!A9480, L9480 = 12101; 9 September: GL Mapping!A9459, L9459 = 12101; 9 September: GL Mapping!A9472, L9472 = 12101; 9 September: GL Mapping!A9475, L9475 = 12101; 9 September: GL Mapping!A9478, L9478 = 12101; 9 September: GL Mapping!A9480, L9480 = 12101

Ehab K1055 selects GL sixth segments whose current categories are 6640–6642, 12101–12103, 12105, 12110–12111, 12121–12123, 12129–12149, 12170–12172, 12179. Systems criteria select 6000–6999, 12101–12179.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0138 — DIFFERENCE — Ehab GL-to-category selection differs: 03 Amounts Receivables

Systems: TABLE 19!C12, F12 · Ehab: K1056 · GL: Current v6: GL Mapping!A9436, L9436 = 13430; Current v6: GL Mapping!A9447, L9447 = 13430; Current v6: GL Mapping!A9450, L9450 = 13430; Current v6: GL Mapping!A9452, L9452 = 13430; Current v6: GL Mapping!A9454, L9454 = 13430; 9 September: GL Mapping!A9436, L9436 = 13430; 9 September: GL Mapping!A9447, L9447 = 13430; 9 September: GL Mapping!A9450, L9450 = 13430; 9 September: GL Mapping!A9452, L9452 = 13430; 9 September: GL Mapping!A9454, L9454 = 13430

Ehab K1056 selects GL sixth segments whose current categories are 3000–3899, 12010–12012, 12030, 12033, 12500, 12505, 12511, 12515, 13401–13402, 13430. Systems criteria select 3000–3999, 12000–12099, 13400–13429.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0139 — DIFFERENCE — Ehab GL-to-category selection differs: .........03 For Fixed assets

Systems: TABLE 19!C18 · Ehab: K1062 · GL: Current v6: GL Mapping!A9906, L9906 = 12199; Current v6: GL Mapping!A9830, L9830 = 12180; Current v6: GL Mapping!A9832, L9832 = 12181; Current v6: GL Mapping!A9833, L9833 = 12182; Current v6: GL Mapping!A9834, L9834 = 12183; 9 September: GL Mapping!A9906, L9906 = 12199; 9 September: GL Mapping!A9830, L9830 = 12180; 9 September: GL Mapping!A9832, L9832 = 12181; 9 September: GL Mapping!A9833, L9833 = 12182; 9 September: GL Mapping!A9834, L9834 = 12183

Ehab K1062 selects GL sixth segments whose current categories are 12180–12199. Systems criteria select 12180–12198.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation.

## NBS-0140 — DIFFERENCE — Ehab GL-to-category selection differs: 07 Suspense Account

Systems: TABLE 19!C20, D20 · Ehab: K1064 · GL: Current v6: GL Mapping!A18005, L18005 = 12930; Current v6: GL Mapping!A18053, L18053 = 13500; Current v6: GL Mapping!A17900, L17900 = 12651; Current v6: GL Mapping!A17902, L17902 = 12652; Current v6: GL Mapping!A17903, L17903 = 12652; 9 September: GL Mapping!A18005, L18005 = 12930; 9 September: GL Mapping!A18053, L18053 = 13500; 9 September: GL Mapping!A17900, L17900 = 12651; 9 September: GL Mapping!A17902, L17902 = 12652; 9 September: GL Mapping!A17903, L17903 = 12652

Ehab K1064 selects GL sixth segments whose current categories are 12651–12669, 12930, 13151–13168, 13170–13171, 13490–13494, 13500, 13521–13527, 14002–14003, 14006–14007, 14009, 14011, 14021, 14061–14065, 14068. Systems criteria select 12650–12699, 13150–13179, 13490–13499, 13520–13529, 14000–14069, 14150–14159, 14460–14999.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0141 — DIFFERENCE — Ehab GL-to-category selection differs: 08 Others

Systems: TABLE 19!C21, D21 · Ehab: K1065 · GL: Current v6: GL Mapping!A10343, L10343 = 13470; Current v6: GL Mapping!A10350, L10350 = 13475; Current v6: GL Mapping!A10351, L10351 = 13480; Current v6: GL Mapping!A10352, L10352 = 13480; Current v6: GL Mapping!A10355, L10355 = 13485; 9 September: GL Mapping!A10343, L10343 = 13470; 9 September: GL Mapping!A10350, L10350 = 13475; 9 September: GL Mapping!A10351, L10351 = 13480; 9 September: GL Mapping!A10352, L10352 = 13480; 9 September: GL Mapping!A10355, L10355 = 13485

Ehab K1065 selects GL sixth segments whose current categories are 12920–12921, 13470, 13475–13476, 13480–13481, 13485–13487, 16600–16610, 16650–16652, 16661, 16671–16674. Systems criteria select 12180–12198, 12500–12599, 12800–12809, 12920–12921, 13430, 13510–13519, 14016–14018, 16600–16619, 16650–16699.

Handling: Reconcile each missing/extra category with the retained GL conditions. Do not replace the NBS category list with the GL union automatically.
Limits: Category sets only. GL conditions and balance types are retained in GL trace; agreement is not full mapping validation. Some selected GL rows have no executable numeric category; see unresolved GL rows.

## NBS-0142 — DIFFERENCE — LC/FC CATEGORY criteria differ: .........02 Islamic Finance

Systems: Income!C28, D28 · Ehab:  · GL: 

Inside Qatar / LC: 51000–51010, 51500–51510. Inside Qatar / FC: 51000–51010.

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0143 — DIFFERENCE — LC/FC CATEGORY criteria differ: .........02 Islamic Finance

Systems: Income!C31, D31 · Ehab:  · GL: 

Inside Qatar / LC: 51000–51010, 51500–51510. Inside Qatar / FC: 51000–51010.

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0144 — DIFFERENCE — LC/FC CATEGORY criteria differ: .........02 Islamic Finance

Systems: Income!C34, D34 · Ehab:  · GL: 

Inside Qatar / LC: 51000–51010, 51500–51510. Inside Qatar / FC: 51000–51010.

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0145 — DIFFERENCE — LC/FC CATEGORY criteria differ: .........02 Islamic Finance

Systems: Income!C37, D37 · Ehab:  · GL: 

Inside Qatar / LC: 51000–51010, 51500–51510. Inside Qatar / FC: 51000–51010.

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0146 — DIFFERENCE — LC/FC CATEGORY criteria differ: .....03 Others

Systems: Income!C80, D80 · Ehab:  · GL: 

Inside Qatar / LC: (not specified in this cell). Inside Qatar / FC: 54600, 54700, 65220–65221, 65227–65228, 66022, 66043–66044.

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0147 — DIFFERENCE — LC/FC SECTOR criteria differ: .........05 Personal Against Salary

Systems: Expense!C57, D57 · Ehab:  · GL: 

Inside Qatar / LC: 1000–1999, 4000–4004. Inside Qatar / FC: (not specified in this cell).

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0148 — DIFFERENCE — LC/FC SECTOR criteria differ: .........06 Other Personal

Systems: Expense!C58, D58 · Ehab:  · GL: 

Inside Qatar / LC: 1000–1999, 4000–4004. Inside Qatar / FC: (not specified in this cell).

Handling: Confirm whether this population difference is intentional. Otherwise synchronize both currency columns and retain their currency conditions.
Limits: A currency-specific product can justify different categories; this is a specification inconsistency to resolve, not a proven numerical misstatement.

## NBS-0149 — CONFIRMED — Malformed field or operator: EQUA;

Systems: ASSET - 100!D84 · Ehab:  · GL: 

1.OUTBOUND TABLE: CRSEQUITYT 
2.SUM(MV_QAR)
3.[LISTED] = Not Listed
COUNTRY = QA
CURRENCY IS NOT EQUA; TO = QAR

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0150 — CONFIRMED — Malformed field or operator: EQUA;

Systems: ASSET - 100!F84 · Ehab:  · GL: 

1.OUTBOUND TABLE: CRSEQUITYT 
2.SUM(MV_QAR)
3.[LISTED] = Not Listed
COUNTRY IS NOT EQUA; TO = QA
CURRENCY = QAR

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0151 — CONFIRMED — Malformed field or operator: EQUA;, NOT EUAL

Systems: ASSET - 100!G84 · Ehab:  · GL: 

1.OUTBOUND TABLE: CRSEQUITYT 
2.SUM(MV_QAR)
3.[LISTED] = Not Listed
COUNTRY IS NOT EUAL TO = QA
CURRENCY IS NOT EQUA; TO = QAR

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0152 — CONFIRMED — Malformed field or operator: ASSTE TYPE, CATEGRY

Systems: ASSET - 100!C107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0153 — CONFIRMED — Malformed field or operator: ASSTE TYPE, CATEGRY

Systems: ASSET - 100!D107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0154 — CONFIRMED — Malformed field or operator: ASSTE TYPE, CATEGRY

Systems: ASSET - 100!F107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0155 — CONFIRMED — Malformed field or operator: ASSTE TYPE, CATEGRY

Systems: ASSET - 100!G107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0156 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0157 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0158 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0159 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0160 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0161 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0162 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0163 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0164 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0165 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0166 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0167 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0168 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0169 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0170 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0171 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0172 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0173 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0174 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T12 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0175 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0176 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0177 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0178 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0179 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0180 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0181 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0182 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0183 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0184 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0185 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0186 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0187 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0188 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0189 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0190 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0191 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0192 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0193 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T13 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0194 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0195 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0196 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0197 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0198 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0199 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0200 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0201 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0202 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0203 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0204 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0205 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0206 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0207 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0208 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0209 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0210 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0211 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0212 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T14 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0213 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0214 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0215 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0216 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0217 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0218 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0219 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0220 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0221 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0222 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0223 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0224 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0225 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0226 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0227 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0228 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0229 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0230 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0231 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T15 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0232 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0233 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0234 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0235 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0236 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0237 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0238 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0239 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0240 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0241 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0242 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0243 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0244 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0245 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0246 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0247 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0248 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0249 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0250 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T16 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0251 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0252 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0253 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0254 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0255 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0256 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0257 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0258 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0259 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0260 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0261 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0262 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0263 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0264 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0265 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0266 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0267 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0268 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0269 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T17 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0270 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0271 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0272 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0273 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0274 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0275 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0276 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0277 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0278 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0279 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0280 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0281 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0282 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0283 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0284 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0285 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0286 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0287 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0288 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T19 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0289 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0290 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0291 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0292 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0293 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0294 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0295 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0296 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0297 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0298 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0299 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0300 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0301 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0302 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0303 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0304 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0305 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0306 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0307 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T29 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0308 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!B32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0309 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!C32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0310 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!D32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0311 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!E32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0312 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!F32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0313 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!G32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0314 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!H32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0315 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!I32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0316 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!J32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0317 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!K32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0318 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!L32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0319 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!M32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0320 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!N32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0321 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!O32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0322 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!P32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0323 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!Q32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0324 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!R32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0325 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!S32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0326 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 12!T32 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0327 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M7 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0328 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M8 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0329 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M9 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0330 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M10 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0331 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M11 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0332 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M12 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0333 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M14 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0334 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M23 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81 & Sector = 1005

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0335 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M24 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81 & Sector <> 1005

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0336 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 13!M27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0337 — CONFIRMED — Malformed field or operator: ASSTE TYPE

Systems: TABLE 19!C10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0338 — CONFIRMED — Malformed field or operator: ASSTE TYPE

Systems: TABLE 19!D10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0339 — CONFIRMED — Malformed field or operator: ASSTE TYPE

Systems: TABLE 19!F10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0340 — CONFIRMED — Malformed field or operator: ASSTE TYPE

Systems: TABLE 19!G10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0341 — CONFIRMED — Malformed field or operator: ASSTE TYPE

Systems: TABLE 19!M10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0342 — CONFIRMED — Malformed field or operator: ASSTE TYPE, CATEGRY, DEBITANDCATEGORY

Systems: TABLE 19!P10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFTANDCATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCEANDCATEGORY = 12180-12198
ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT ANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0343 — AMBIGUOUS — Disjoint repeated CATEGORY conditions joined by &

Systems: TABLE 19!P10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFTANDCATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCEANDCATEGORY = 12180-12198
ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT ANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0344 — AMBIGUOUS — Disjoint repeated CATEGORY conditions joined by &

Systems: TABLE 19!C11 · Ehab:  · GL: 

CATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFT

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0345 — AMBIGUOUS — Disjoint repeated CATEGORY conditions joined by &

Systems: TABLE 19!M11 · Ehab:  · GL: 

CATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFT

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0346 — CONFIRMED — Malformed field or operator: CATEGRY

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0347 — CONFIRMED — Malformed field or operator: CATEGRY

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0348 — CONFIRMED — Malformed field or operator: DEBITANDCATEGORY

Systems: TABLE 19!M20 · Ehab:  · GL: 

CATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBIT

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0349 — CONFIRMED — Malformed field or operator: CATEGRY

Systems: TABLE 19!C21 · Ehab:  · GL: 

CATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0350 — CONFIRMED — Malformed field or operator: CATEGRY

Systems: TABLE 19!D21 · Ehab:  · GL: 

CATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0351 — CONFIRMED — Malformed field or operator: CATEGRY

Systems: TABLE 19!M21 · Ehab:  · GL: 

CATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT ANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0352 — CONFIRMED — Malformed field or operator: CREDIIT

Systems: Table 22!B13 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CREDIIT & CATEGORY
  =   5002 & 2001

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0353 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0354 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0355 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0356 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0357 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0358 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0359 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0360 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0361 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0362 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0363 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0364 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0365 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0366 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0367 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0368 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0369 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0370 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0371 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0372 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0373 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0374 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0375 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0376 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0377 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0378 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0379 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0380 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0381 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B20 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0382 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C20 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0383 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E20 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0384 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F20 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0385 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B21 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0386 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C21 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0387 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E21 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0388 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F21 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0389 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B22 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0390 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C22 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0391 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E22 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0392 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F22 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0393 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B23 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0394 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C23 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0395 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E23 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0396 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F23 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0397 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B24 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0398 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C24 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0399 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E24 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0400 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F24 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0401 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B25 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0402 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C25 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0403 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E25 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0404 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F25 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0405 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B27 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0406 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C27 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0407 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E27 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0408 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F27 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0409 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B43 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0410 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C43 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0411 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E43 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0412 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F43 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0413 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B44 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0414 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C44 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0415 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E44 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0416 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F44 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0417 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B46 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0418 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C46 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0419 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E46 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0420 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F46 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0421 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!B47 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0422 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!C47 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0423 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!E47 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0424 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 23!F47 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0425 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0426 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0427 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0428 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0429 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0430 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0431 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0432 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0433 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J11 · Ehab:  · GL: 

INDUSTRY = 44103 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0434 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0435 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0436 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0437 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0438 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0439 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0440 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0441 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0442 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J12 · Ehab:  · GL: 

INDUSTRY = 44105 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0443 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0444 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0445 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0446 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0447 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0448 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0449 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0450 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0451 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J13 · Ehab:  · GL: 

INDUSTRY = 44104 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0452 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0453 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0454 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0455 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0456 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0457 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0458 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0459 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0460 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J14 · Ehab:  · GL: 

INDUSTRY = 44102 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0461 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0462 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0463 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0464 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0465 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0466 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0467 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0468 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0469 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J15 · Ehab:  · GL: 

INDUSTRY = 44107 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0470 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0471 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0472 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0473 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0474 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0475 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0476 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0477 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0478 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J16 · Ehab:  · GL: 

INDUSTRY = 44101 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0479 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0480 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0481 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0482 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0483 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0484 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0485 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0486 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0487 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J18 · Ehab:  · GL: 

INDUSTRY =  44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0488 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0489 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0490 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0491 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0492 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0493 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0494 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0495 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0496 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J26 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0497 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!B27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0498 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!C27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0499 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!D27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0500 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!E27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0501 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!F27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0502 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!G27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0503 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!H27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0504 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!I27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0505 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 24!J27 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0506 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!B25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0507 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!C25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0508 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!D25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0509 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!E25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0510 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!F25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0511 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!G25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0512 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!H25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0513 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!I25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0514 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!J25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0515 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!K25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0516 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!L25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0517 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!M25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0518 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!N25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0519 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!O25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0520 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!P25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0521 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!Q25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0522 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!R25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0523 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!S25 · Ehab:  · GL: 

ALL INDUSTRIES EXCEPT INDUSTRY <> 44103, 44105, 44104, 44102, 44107, 44101, 44106, 44108, 44109, 44110 & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 81

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0524 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!B26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0525 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!C26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0526 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!D26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0527 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!E26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0528 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!F26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0529 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!G26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0530 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!H26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0531 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!I26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0532 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!J26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0533 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!K26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0534 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!L26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0535 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!M26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0536 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!N26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0537 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!O26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0538 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!P26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0539 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!Q26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0540 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!R26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0541 — CONFIRMED — Malformed field or operator: ACCOUNT.CUTOMER

Systems: Table 25!S26 · Ehab:  · GL: 

ALL INDUSTRIES & ACCOUNT.CUTOMER = RECID.CUSTOMER > CUSTOMER.STATUS = 80

Handling: Correct the specification spelling after preserving the original cell. Confirm the actual source field name.
Limits: 

## NBS-0542 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B15 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0543 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C15 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0544 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E15 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0545 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F15 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0546 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B18 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0547 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C18 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0548 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E18 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0549 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F18 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0550 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B22 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0551 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C22 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0552 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E22 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0553 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F22 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0554 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B30 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0555 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C30 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0556 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E30 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0557 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F30 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0558 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B42 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0559 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C42 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0560 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E42 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0561 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F42 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0562 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B46 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0563 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C46 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0564 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E46 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0565 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F46 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0566 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!B51 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0567 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!C51 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0568 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!E51 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0569 — AMBIGUOUS — Disjoint repeated SECTOR conditions joined by &

Systems: Table 35!F51 · Ehab:  · GL: 

SECTOR =  2000 - 2003 & SECTOR = 4000-4004, 1000-1999

Handling: State OR / separate additive components explicitly. Literal AND yields an empty selection.
Limits: The workbook uses & for both lists and conjunction. The intended operator cannot be proved from the cell alone.

## NBS-0570 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: ASSET - 100!C107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0571 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: ASSET - 100!C107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0572 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: ASSET - 100!D107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0573 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: ASSET - 100!D107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0574 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: ASSET - 100!F107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0575 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: ASSET - 100!F107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0576 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: ASSET - 100!G107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0577 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: ASSET - 100!G107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0578 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B20 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0579 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B20 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0580 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E20 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0581 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E20 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0582 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B23 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0583 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B23 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0584 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E23 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0585 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E23 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0586 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!L25 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
NABACCOUNT&CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
NABACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0587 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B27 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0588 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B27 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0589 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E27 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0590 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E27 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0591 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B37 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0592 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B37 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0593 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E37 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > &  SECTOR = 2004 ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0594 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E37 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > &  SECTOR = 2004 ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0595 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B40 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0596 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B40 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0597 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E40 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0598 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E40 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0599 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B44 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0600 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B44 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0601 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E44 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0602 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E44 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0603 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B54 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0604 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B54 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0605 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E54 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0606 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E54 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0607 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B57 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0608 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B57 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0609 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E57 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0610 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E57 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0611 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!B61 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0612 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!B61 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0613 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 8!E61 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0614 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 8!E61 · Ehab:  · GL: 

CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0615 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B14 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0616 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B14 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0617 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B17 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0618 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B17 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0619 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B19 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0620 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B19 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0621 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B27 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0622 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B27 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0623 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B30 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0624 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B30 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0625 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B32 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0626 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B32 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0627 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B40 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0628 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B40 · Ehab:  · GL: 

CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0629 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B43 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0630 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B43 · Ehab:  · GL: 

CATEGORY = 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0631 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 10!B45 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0632 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 10!B45 · Ehab:  · GL: 

CATEGORY = 13101, 13103, 13105 &  
CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717, 3704, 3702, 3706 &  ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0633 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0634 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0635 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0636 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0637 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0638 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0639 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0640 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0641 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0642 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 11!B25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0643 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0644 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0645 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0646 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0647 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0648 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0649 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0650 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0651 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0652 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 11!D25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0653 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0654 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0655 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0656 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0657 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0658 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0659 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0660 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0661 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0662 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 11!H25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0663 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0664 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0665 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0666 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0667 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0668 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0669 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0670 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0671 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0672 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 11!J25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0673 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0674 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0675 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0676 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0677 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0678 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0679 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0680 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0681 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0682 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 11!L25 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0683 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFT

Systems: Table 11!B26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0684 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFT

Systems: Table 11!B26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0685 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFT

Systems: Table 11!D26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0686 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFT

Systems: Table 11!D26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0687 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFT

Systems: Table 11!H26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0688 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFT

Systems: Table 11!H26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0689 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFT

Systems: Table 11!J26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0690 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFT

Systems: Table 11!J26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0691 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFT

Systems: Table 11!L26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0692 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFT

Systems: Table 11!L26 · Ehab:  · GL: 

AA.ARRANGEMENT > LINKED APPL ID > ECB SUM(OPEN + DEBIT+ CREDIT) WHERE ASSET TYPE = ACCDEFERREDPFT
DUEDEFERREDPFT
GRCDEFERREDPFT
PDODEFERREDPFT
NABDEFERREDPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0693 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 12!B8 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0694 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 12!B8 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0695 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!C10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0696 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!C10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0697 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!D10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0698 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!D10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0699 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!F10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0700 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!F10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0701 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!G10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0702 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!G10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0703 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!M10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0704 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!M10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0705 — INPUT GAP — Original balance type absent from supplied ECB: DRINTEREST

Systems: TABLE 19!P10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFTANDCATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCEANDCATEGORY = 12180-12198
ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT ANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0706 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFT

Systems: TABLE 19!P10 · Ehab:  · GL: 

CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST, ANDCATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFTANDCATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCEANDCATEGORY = 12180-12198
ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 12650-12699 , 13150-13169 , 14060-14069 , 13490-13499 , 14000-14059 , 14460-14999 , 13520-13529 , 14150-14159 , 13170-13179 & ASSET TYPE = DEBITANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT ANDCATEGORY = 13430, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, 16650-16699 & ASSET = DEBIT , 
CATEGRY = 12180-12198  ASSET TYPE = DEBIT 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0707 — INPUT GAP — Original balance type absent from supplied ECB: INVDEPOSITPFT

Systems: TABLE 19!C11 · Ehab:  · GL: 

CATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0708 — INPUT GAP — Original balance type absent from supplied ECB: INVDEPOSITPFT

Systems: TABLE 19!F11 · Ehab:  · GL: 



CATEGORY = 6000-6999 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0709 — INPUT GAP — Original balance type absent from supplied ECB: INVDEPOSITPFT

Systems: TABLE 19!M11 · Ehab:  · GL: 

CATEGORY = 12101 - 12179  ASSET TYPE = DEBIT &

CATEGORY = 6640 - 6649 & Asset Type = ACCDEPOSITPFT, INVDEPOSITPFT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0710 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0711 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0712 — INPUT GAP — Original balance type absent from supplied ECB: ACCLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0713 — INPUT GAP — Original balance type absent from supplied ECB: DELADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0714 — INPUT GAP — Original balance type absent from supplied ECB: DELLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0715 — INPUT GAP — Original balance type absent from supplied ECB: DUEADHOCFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0716 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0717 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0718 — INPUT GAP — Original balance type absent from supplied ECB: DUECREDITBUREAUFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0719 — INPUT GAP — Original balance type absent from supplied ECB: DUELATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0720 — INPUT GAP — Original balance type absent from supplied ECB: DUEPOSTPONEMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0721 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEEAMORT

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0722 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0723 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0724 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0725 — INPUT GAP — Original balance type absent from supplied ECB: GRCLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0726 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0727 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0728 — INPUT GAP — Original balance type absent from supplied ECB: NABLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0729 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALBALANCE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0730 — INPUT GAP — Original balance type absent from supplied ECB: NABRENTALRECEIVABLE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0731 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0732 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEES

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0733 — INPUT GAP — Original balance type absent from supplied ECB: PDOLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0734 — INPUT GAP — Original balance type absent from supplied ECB: RECLATEPAYMENTFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0735 — INPUT GAP — Original balance type absent from supplied ECB: RESCHEDULEFEE

Systems: TABLE 19!C12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0736 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0737 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0738 — INPUT GAP — Original balance type absent from supplied ECB: ACCLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0739 — INPUT GAP — Original balance type absent from supplied ECB: DELADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0740 — INPUT GAP — Original balance type absent from supplied ECB: DELLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0741 — INPUT GAP — Original balance type absent from supplied ECB: DUEADHOCFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0742 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0743 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0744 — INPUT GAP — Original balance type absent from supplied ECB: DUECREDITBUREAUFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0745 — INPUT GAP — Original balance type absent from supplied ECB: DUELATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0746 — INPUT GAP — Original balance type absent from supplied ECB: DUEPOSTPONEMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0747 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEEAMORT

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0748 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0749 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0750 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0751 — INPUT GAP — Original balance type absent from supplied ECB: GRCLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0752 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0753 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0754 — INPUT GAP — Original balance type absent from supplied ECB: NABLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0755 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALBALANCE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0756 — INPUT GAP — Original balance type absent from supplied ECB: NABRENTALRECEIVABLE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0757 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0758 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEES

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0759 — INPUT GAP — Original balance type absent from supplied ECB: PDOLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0760 — INPUT GAP — Original balance type absent from supplied ECB: RECLATEPAYMENTFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0761 — INPUT GAP — Original balance type absent from supplied ECB: RESCHEDULEFEE

Systems: TABLE 19!F12 · Ehab:  · GL: 

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0762 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0763 — INPUT GAP — Original balance type absent from supplied ECB: ACCADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0764 — INPUT GAP — Original balance type absent from supplied ECB: ACCLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0765 — INPUT GAP — Original balance type absent from supplied ECB: DELADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0766 — INPUT GAP — Original balance type absent from supplied ECB: DELLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0767 — INPUT GAP — Original balance type absent from supplied ECB: DUEADHOCFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0768 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0769 — INPUT GAP — Original balance type absent from supplied ECB: DUEADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0770 — INPUT GAP — Original balance type absent from supplied ECB: DUECREDITBUREAUFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0771 — INPUT GAP — Original balance type absent from supplied ECB: DUELATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0772 — INPUT GAP — Original balance type absent from supplied ECB: DUEPOSTPONEMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0773 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEEAMORT

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0774 — INPUT GAP — Original balance type absent from supplied ECB: DUETAKAFULFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0775 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0776 — INPUT GAP — Original balance type absent from supplied ECB: GRCADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0777 — INPUT GAP — Original balance type absent from supplied ECB: GRCLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0778 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0779 — INPUT GAP — Original balance type absent from supplied ECB: NABADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0780 — INPUT GAP — Original balance type absent from supplied ECB: NABLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0781 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALBALANCE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0782 — INPUT GAP — Original balance type absent from supplied ECB: NABRENTALRECEIVABLE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0783 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0784 — INPUT GAP — Original balance type absent from supplied ECB: PDOADMINFEES

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0785 — INPUT GAP — Original balance type absent from supplied ECB: PDOLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0786 — INPUT GAP — Original balance type absent from supplied ECB: RECLATEPAYMENTFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0787 — INPUT GAP — Original balance type absent from supplied ECB: RESCHEDULEFEE

Systems: TABLE 19!M12 · Ehab:  · GL: 

CATEGRY = 12000-12099, 13400-13429 & Asset type = DEBIT

CATEGORY = 3000-3999
Asset type = ACCLATEPAYMENTFEE, DUELATEPAYMENTFEE, DELLATEPAYMENTFEE, GRCLATEPAYMENTFEE, PDOLATEPAYMENTFEE, NABLATEPAYMENTFEE, RECLATEPAYMENTFEE, ACCADMINFEE, DUEADMINFEE, GRCADMINFEE, PDOADMINFEE, NABADMINFEE, ACCADMINFEES, DUEADMINFEES, GRCADMINFEES, PDOADMINFEES, DELADMINFEES, NABADMINFEES, DUEPOSTPONEMENTFEE, DUETAKAFULFEES, DUECREDITBUREAUFEE, RESCHEDULEFEE, DUETAKAFULFEEAMORT, DUEADHOCFEE, RENTALRECEIVABLE, PRINCIPALBALANCE, NABRENTALRECEIVABLE, NABPRINCIPALBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0788 — INPUT GAP — Original balance type absent from supplied ECB: CREDIIT

Systems: Table 22!B13 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CREDIIT & CATEGORY
  =   5002 & 2001

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0789 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!C10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0790 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!C10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0791 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!D10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0792 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!D10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0793 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!E10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0794 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!E10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0795 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!F10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0796 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!F10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0797 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!G10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0798 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!G10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0799 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!H10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0800 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!H10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0801 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!I10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0802 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!I10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0803 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!J10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0804 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!J10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0805 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!K10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0806 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!K10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0807 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 44!L10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0808 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 44!L10 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
GRCACCOUNT
DUEACCOUNT
PDOACCOUNT
NABACCOUNT
DELACCOUNT
PREACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0809 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!B19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0810 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!B19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0811 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!C19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0812 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!C19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0813 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!E19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0814 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!E19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0815 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!F19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0816 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!F19 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0817 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!B35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0818 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!B35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0819 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!C35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0820 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!C35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0821 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!E35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0822 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!E35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0823 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!F35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0824 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!F35 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0825 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!B45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0826 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!B45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0827 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!C45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0828 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!C45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0829 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!E45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0830 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!E45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0831 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 23!F45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0832 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 23!F45 · Ehab:  · GL: 

CATEGORY = 6000-6999
ASSET TYPE = CREDIT, CURBALANCE, PAYACCOUNT & CURACCOUNT


Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0833 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 24!D7 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT, PAYACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0834 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 24!D7 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT, PAYACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0835 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 25!B7 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
CREDIT
CURBALANCE
PAYACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0836 — INPUT GAP — Original balance type absent from supplied ECB: PAYACCOUNT

Systems: Table 25!B7 · Ehab:  · GL: 

ASSET TYPE = CURACCOUNT
CREDIT
CURBALANCE
PAYACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0837 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0838 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0839 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0840 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0841 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0842 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0843 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0844 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0845 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0846 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 29!B56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0847 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0848 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0849 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0850 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0851 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0852 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0853 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0854 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0855 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0856 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 29!C56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0857 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0858 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0859 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0860 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0861 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0862 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0863 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0864 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0865 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0866 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 29!E56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0867 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0868 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0869 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0870 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0871 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0872 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0873 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0874 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0875 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0876 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 29!F56 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0877 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0878 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0879 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0880 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0881 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0882 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0883 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0884 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0885 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0886 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 30!C7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0887 — INPUT GAP — Original balance type absent from supplied ECB: ACCDEFERREDPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0888 — INPUT GAP — Original balance type absent from supplied ECB: ACCPRINCIPALPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0889 — INPUT GAP — Original balance type absent from supplied ECB: DUEDEFERREDPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0890 — INPUT GAP — Original balance type absent from supplied ECB: DUEPRINCIPALPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0891 — INPUT GAP — Original balance type absent from supplied ECB: GRCDEFERREDPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0892 — INPUT GAP — Original balance type absent from supplied ECB: GRCPRINCIPALPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0893 — INPUT GAP — Original balance type absent from supplied ECB: NABDEFERREDPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0894 — INPUT GAP — Original balance type absent from supplied ECB: NABPRINCIPALPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0895 — INPUT GAP — Original balance type absent from supplied ECB: PDODEFERREDPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0896 — INPUT GAP — Original balance type absent from supplied ECB: PDOPRINCIPALPFTSP

Systems: Table 30!F7 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = ACCDEFERREDPFTSP
DUEDEFERREDPFTSP
GRCDEFERREDPFTSP
PDODEFERREDPFTSP
NABDEFERREDPFTSP
ACCPRINCIPALPFTSP
DUEPRINCIPALPFTSP
GRCPRINCIPALPFTSP
PDOPRINCIPALPFTSP
NABPRINCIPALPFTSP

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0897 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!B10 · Ehab:  · GL: 

CATEGORY = 28005
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0898 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!C10 · Ehab:  · GL: 

CATEGORY = 28005
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0899 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!E10 · Ehab:  · GL: 

CATEGORY = 28005
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0900 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!F10 · Ehab:  · GL: 

CATEGORY = 28005
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0901 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!B16 · Ehab:  · GL: 

CATEGORY = 28002
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0902 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!C16 · Ehab:  · GL: 

CATEGORY = 28002
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0903 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!E16 · Ehab:  · GL: 

CATEGORY = 28002
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0904 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!F16 · Ehab:  · GL: 

CATEGORY = 28002
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0905 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!B20 · Ehab:  · GL: 

CATEGORY = 28003
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0906 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!C20 · Ehab:  · GL: 

CATEGORY = 28003
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0907 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!E20 · Ehab:  · GL: 

CATEGORY = 28003
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0908 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!F20 · Ehab:  · GL: 

CATEGORY = 28003
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0909 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!B28 · Ehab:  · GL: 

CATEGORY = 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0910 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!C28 · Ehab:  · GL: 

CATEGORY = 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0911 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!E28 · Ehab:  · GL: 

CATEGORY = 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0912 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!F28 · Ehab:  · GL: 

CATEGORY = 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0913 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!B37 · Ehab:  · GL: 

CATEGORY = 28000 - 28999 BUT <>28002, 28003, 28005 & 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0914 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!C37 · Ehab:  · GL: 

CATEGORY = 28000 - 28999 BUT <>28002, 28003, 28005 & 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0915 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!E37 · Ehab:  · GL: 

CATEGORY = 28000 - 28999 BUT <>28002, 28003, 28005 & 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0916 — INPUT GAP — Original balance type absent from supplied ECB: CONTDRBL

Systems: Table 35!F37 · Ehab:  · GL: 

CATEGORY = 28000 - 28999 BUT <>28002, 28003, 28005 & 28020
ASSET TYPE = CONTCR &  CONTDRBL

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0917 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 36!C11 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0918 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 36!D11 · Ehab:  · GL: 

CATEGORY = 3000-3999 ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0919 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 36!F11 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0920 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 36!G11 · Ehab:  · GL: 

CATEGORY = 3000-3999
ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0921 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 37!B7 · Ehab:  · GL: 

ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0922 — INPUT GAP — Original balance type absent from supplied ECB: AVLACCOUNT

Systems: Table 37!B44 · Ehab:  · GL: 

ASSET TYPE = AVLACCOUNT

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0923 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D14 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0924 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D14 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0925 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B23 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0926 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D23 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0927 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D23 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0928 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B24 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0929 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D24 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0930 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D24 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0931 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B25 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0932 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D25 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0933 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D25 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0934 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B26 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0935 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D26 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0936 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D26 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0937 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B27 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0938 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D27 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0939 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D27 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0940 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B38 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0941 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D38 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0942 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D38 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0943 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B47 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER & SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0944 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D47 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER & SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0945 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D47 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER & SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0946 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B48 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0947 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D48 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0948 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D48 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0949 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B49 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0950 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D49 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0951 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D49 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0952 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B50 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0953 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D50 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0954 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D50 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0955 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 40!B51 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0956 — INPUT GAP — Original balance type absent from supplied ECB: NABACCOUNT

Systems: Table 40!D51 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0957 — INPUT GAP — Original balance type absent from supplied ECB: PDOACCOUNT

Systems: Table 40!D51 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 3000 - 3999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURACCOUNT, DUEACCOUNT, GRCACCOUNT, NABACCOUNT & PDOACCOUNT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0958 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B13 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0959 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B22 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0960 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B23 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0961 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B24 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0962 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B25 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0963 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B26 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8020 & 8022.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0964 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B37 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR <> 2004 

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0965 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B46 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER & SECTOR = 2004 & INDUSTRY = 14103, 24103, 34103, 44103

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0966 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B47 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14105, 24105, 34105, 44105

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0967 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B48 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14102, 24102, 34102, 44102

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0968 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B49 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14107, 24107, 34107, 44107

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0969 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 41!B50 · Ehab:  · GL: 

1. Account > PICK CUSTOMER where Category=  8021 & 8023.
2.SEARCH THE IDENTIFIED CUSTOMER IN ACCOUNT WHERE CATEGORY = 6000 - 6999 
3. Pick the ID of account and go to  EB.CONTRACT.BALANCES   SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) & ASSET TYPE = CURBALANCE, CURACCOUNT & CREDIT & CUSTOMER SECTOR = 2004 & INDUSTRY = 14101, 24101, 34101, 44101

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0970 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!B10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0971 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!C10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0972 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!D10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0973 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!E10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0974 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!F10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0975 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!G10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0976 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!H10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0977 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!I10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0978 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!J10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0979 — INPUT GAP — Original balance type absent from supplied ECB: CURBALANCE

Systems: Table 45!K10 · Ehab:  · GL: 

ASSET TYPE = CREDIT, CURACCOUNT & CURBALANCE

Handling: Confirm the exact Temenos balance code and source availability. Do not substitute a similar code silently.
Limits: Absent from this supplied ECB header/population does not prove the code cannot exist in Temenos.

## NBS-0980 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F5 · Ehab:  · GL: 

SYSTEMS Table 11!F5: saved error #VALUE!; formula SUM(B5+D5).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0981 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G5 · Ehab:  · GL: 

SYSTEMS Table 11!G5: saved error #VALUE!; formula SUM(B6+D6).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0982 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N5 · Ehab:  · GL: 

SYSTEMS Table 11!N5: saved error #VALUE!; formula SUM(D5 + F5 + H5 +J5 + L5).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0983 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O5 · Ehab:  · GL: 

SYSTEMS Table 11!O5: saved error #VALUE!; formula SUM(C5 + E5 + H5 + J5 +L5 + N5).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0984 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P5 · Ehab:  · GL: 

SYSTEMS Table 11!P5: saved error #VALUE!; formula SUM(B5 + D5 + F5 + H5 +J5 + L5).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0985 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q5 · Ehab:  · GL: 

SYSTEMS Table 11!Q5: saved error #VALUE!; formula SUM(E5 + H5 + J5 +L5 + N5).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0986 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F7 · Ehab:  · GL: 

SYSTEMS Table 11!F7: saved error #VALUE!; formula SUM(B7+D7).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0987 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G7 · Ehab:  · GL: 

SYSTEMS Table 11!G7: saved error #VALUE!; formula SUM(B8+D8).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0988 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N7 · Ehab:  · GL: 

SYSTEMS Table 11!N7: saved error #VALUE!; formula SUM(D7 + F7 + H7 +J7 + L7).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0989 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O7 · Ehab:  · GL: 

SYSTEMS Table 11!O7: saved error #VALUE!; formula SUM(C7 + E7 + H7 + J7 +L7 + N7).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0990 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P7 · Ehab:  · GL: 

SYSTEMS Table 11!P7: saved error #VALUE!; formula SUM(B7 + D7 + F7 + H7 +J7 + L7).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0991 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q7 · Ehab:  · GL: 

SYSTEMS Table 11!Q7: saved error #VALUE!; formula SUM(E7 + H7 + J7 +L7 + N7).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0992 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F8 · Ehab:  · GL: 

SYSTEMS Table 11!F8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0993 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G8 · Ehab:  · GL: 

SYSTEMS Table 11!G8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0994 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N8 · Ehab:  · GL: 

SYSTEMS Table 11!N8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0995 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O8 · Ehab:  · GL: 

SYSTEMS Table 11!O8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0996 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P8 · Ehab:  · GL: 

SYSTEMS Table 11!P8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0997 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q8 · Ehab:  · GL: 

SYSTEMS Table 11!Q8: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0998 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F9 · Ehab:  · GL: 

SYSTEMS Table 11!F9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-0999 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G9 · Ehab:  · GL: 

SYSTEMS Table 11!G9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1000 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N9 · Ehab:  · GL: 

SYSTEMS Table 11!N9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1001 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O9 · Ehab:  · GL: 

SYSTEMS Table 11!O9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1002 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P9 · Ehab:  · GL: 

SYSTEMS Table 11!P9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1003 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q9 · Ehab:  · GL: 

SYSTEMS Table 11!Q9: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1004 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F10 · Ehab:  · GL: 

SYSTEMS Table 11!F10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1005 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G10 · Ehab:  · GL: 

SYSTEMS Table 11!G10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1006 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N10 · Ehab:  · GL: 

SYSTEMS Table 11!N10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1007 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O10 · Ehab:  · GL: 

SYSTEMS Table 11!O10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1008 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P10 · Ehab:  · GL: 

SYSTEMS Table 11!P10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1009 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q10 · Ehab:  · GL: 

SYSTEMS Table 11!Q10: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1010 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F11 · Ehab:  · GL: 

SYSTEMS Table 11!F11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1011 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G11 · Ehab:  · GL: 

SYSTEMS Table 11!G11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1012 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N11 · Ehab:  · GL: 

SYSTEMS Table 11!N11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1013 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O11 · Ehab:  · GL: 

SYSTEMS Table 11!O11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1014 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P11 · Ehab:  · GL: 

SYSTEMS Table 11!P11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1015 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q11 · Ehab:  · GL: 

SYSTEMS Table 11!Q11: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1016 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F12 · Ehab:  · GL: 

SYSTEMS Table 11!F12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1017 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G12 · Ehab:  · GL: 

SYSTEMS Table 11!G12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1018 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N12 · Ehab:  · GL: 

SYSTEMS Table 11!N12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1019 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O12 · Ehab:  · GL: 

SYSTEMS Table 11!O12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1020 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P12 · Ehab:  · GL: 

SYSTEMS Table 11!P12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1021 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q12 · Ehab:  · GL: 

SYSTEMS Table 11!Q12: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1022 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F13 · Ehab:  · GL: 

SYSTEMS Table 11!F13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1023 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G13 · Ehab:  · GL: 

SYSTEMS Table 11!G13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1024 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N13 · Ehab:  · GL: 

SYSTEMS Table 11!N13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1025 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O13 · Ehab:  · GL: 

SYSTEMS Table 11!O13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1026 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P13 · Ehab:  · GL: 

SYSTEMS Table 11!P13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1027 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q13 · Ehab:  · GL: 

SYSTEMS Table 11!Q13: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1028 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F14 · Ehab:  · GL: 

SYSTEMS Table 11!F14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1029 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G14 · Ehab:  · GL: 

SYSTEMS Table 11!G14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1030 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N14 · Ehab:  · GL: 

SYSTEMS Table 11!N14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1031 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O14 · Ehab:  · GL: 

SYSTEMS Table 11!O14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1032 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P14 · Ehab:  · GL: 

SYSTEMS Table 11!P14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1033 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q14 · Ehab:  · GL: 

SYSTEMS Table 11!Q14: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1034 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F16 · Ehab:  · GL: 

SYSTEMS Table 11!F16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1035 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G16 · Ehab:  · GL: 

SYSTEMS Table 11!G16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1036 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N16 · Ehab:  · GL: 

SYSTEMS Table 11!N16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1037 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O16 · Ehab:  · GL: 

SYSTEMS Table 11!O16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1038 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P16 · Ehab:  · GL: 

SYSTEMS Table 11!P16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1039 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q16 · Ehab:  · GL: 

SYSTEMS Table 11!Q16: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1040 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F17 · Ehab:  · GL: 

SYSTEMS Table 11!F17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1041 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G17 · Ehab:  · GL: 

SYSTEMS Table 11!G17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1042 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N17 · Ehab:  · GL: 

SYSTEMS Table 11!N17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1043 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O17 · Ehab:  · GL: 

SYSTEMS Table 11!O17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1044 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P17 · Ehab:  · GL: 

SYSTEMS Table 11!P17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1045 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q17 · Ehab:  · GL: 

SYSTEMS Table 11!Q17: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1046 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F18 · Ehab:  · GL: 

SYSTEMS Table 11!F18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1047 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G18 · Ehab:  · GL: 

SYSTEMS Table 11!G18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1048 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N18 · Ehab:  · GL: 

SYSTEMS Table 11!N18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1049 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O18 · Ehab:  · GL: 

SYSTEMS Table 11!O18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1050 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P18 · Ehab:  · GL: 

SYSTEMS Table 11!P18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1051 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q18 · Ehab:  · GL: 

SYSTEMS Table 11!Q18: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1052 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F19 · Ehab:  · GL: 

SYSTEMS Table 11!F19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1053 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G19 · Ehab:  · GL: 

SYSTEMS Table 11!G19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1054 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N19 · Ehab:  · GL: 

SYSTEMS Table 11!N19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1055 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O19 · Ehab:  · GL: 

SYSTEMS Table 11!O19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1056 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P19 · Ehab:  · GL: 

SYSTEMS Table 11!P19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1057 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q19 · Ehab:  · GL: 

SYSTEMS Table 11!Q19: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1058 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F20 · Ehab:  · GL: 

SYSTEMS Table 11!F20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1059 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G20 · Ehab:  · GL: 

SYSTEMS Table 11!G20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1060 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N20 · Ehab:  · GL: 

SYSTEMS Table 11!N20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1061 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O20 · Ehab:  · GL: 

SYSTEMS Table 11!O20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1062 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P20 · Ehab:  · GL: 

SYSTEMS Table 11!P20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1063 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q20 · Ehab:  · GL: 

SYSTEMS Table 11!Q20: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1064 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!F21 · Ehab:  · GL: 

SYSTEMS Table 11!F21: saved error #VALUE!; formula SUM(B21+D21).

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1065 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!G21 · Ehab:  · GL: 

SYSTEMS Table 11!G21: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1066 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!N21 · Ehab:  · GL: 

SYSTEMS Table 11!N21: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1067 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!O21 · Ehab:  · GL: 

SYSTEMS Table 11!O21: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1068 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!P21 · Ehab:  · GL: 

SYSTEMS Table 11!P21: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1069 — CONFIRMED — Original cached Excel error: #VALUE!

Systems: Table 11!Q21 · Ehab:  · GL: 

SYSTEMS Table 11!Q21: saved error #VALUE!; formula shared formula / formula precedent.

Handling: Repair the specification formula and its text/numeric precedents. Recalculate a working copy after the definition is agreed.
Limits: This is the saved source error. Source formulas were not executed during the audit.

## NBS-1070 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G5 · Ehab:  · GL: 

Original =SUM(B6+D6). The source headings require C5+E5.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1071 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N5 · Ehab:  · GL: 

Original =SUM(D5 + F5 + H5 +J5 + L5). The source headings require H5+J5+L5.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1072 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O5 · Ehab:  · GL: 

Original =SUM(C5 + E5 + H5 + J5 +L5 + N5). The source headings require I5+K5+M5.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1073 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P5 · Ehab:  · GL: 

Original =SUM(B5 + D5 + F5 + H5 +J5 + L5). The source headings require F5+N5.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1074 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q5 · Ehab:  · GL: 

Original =SUM(E5 + H5 + J5 +L5 + N5). The source headings require G5+O5.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1075 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G7 · Ehab:  · GL: 

Original =SUM(B8+D8). The source headings require C7+E7.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1076 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N7 · Ehab:  · GL: 

Original =SUM(D7 + F7 + H7 +J7 + L7). The source headings require H7+J7+L7.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1077 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O7 · Ehab:  · GL: 

Original =SUM(C7 + E7 + H7 + J7 +L7 + N7). The source headings require I7+K7+M7.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1078 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P7 · Ehab:  · GL: 

Original =SUM(B7 + D7 + F7 + H7 +J7 + L7). The source headings require F7+N7.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1079 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q7 · Ehab:  · GL: 

Original =SUM(E7 + H7 + J7 +L7 + N7). The source headings require G7+O7.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1080 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G8 · Ehab:  · GL: 

Original =SUM(B9+D9). The source headings require C8+E8.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1081 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N8 · Ehab:  · GL: 

Original =SUM(D8 + F8 + H8 +J8 + L8). The source headings require H8+J8+L8.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1082 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O8 · Ehab:  · GL: 

Original =SUM(C8 + E8 + H8 + J8 +L8 + N8). The source headings require I8+K8+M8.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1083 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P8 · Ehab:  · GL: 

Original =SUM(B8 + D8 + F8 + H8 +J8 + L8). The source headings require F8+N8.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1084 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q8 · Ehab:  · GL: 

Original =SUM(E8 + H8 + J8 +L8 + N8). The source headings require G8+O8.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1085 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G9 · Ehab:  · GL: 

Original =SUM(B10+D10). The source headings require C9+E9.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1086 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N9 · Ehab:  · GL: 

Original =SUM(D9 + F9 + H9 +J9 + L9). The source headings require H9+J9+L9.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1087 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O9 · Ehab:  · GL: 

Original =SUM(C9 + E9 + H9 + J9 +L9 + N9). The source headings require I9+K9+M9.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1088 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P9 · Ehab:  · GL: 

Original =SUM(B9 + D9 + F9 + H9 +J9 + L9). The source headings require F9+N9.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1089 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q9 · Ehab:  · GL: 

Original =SUM(E9 + H9 + J9 +L9 + N9). The source headings require G9+O9.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1090 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G10 · Ehab:  · GL: 

Original =SUM(B11+D11). The source headings require C10+E10.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1091 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N10 · Ehab:  · GL: 

Original =SUM(D10 + F10 + H10 +J10 + L10). The source headings require H10+J10+L10.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1092 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O10 · Ehab:  · GL: 

Original =SUM(C10 + E10 + H10 + J10 +L10 + N10). The source headings require I10+K10+M10.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1093 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P10 · Ehab:  · GL: 

Original =SUM(B10 + D10 + F10 + H10 +J10 + L10). The source headings require F10+N10.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1094 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q10 · Ehab:  · GL: 

Original =SUM(E10 + H10 + J10 +L10 + N10). The source headings require G10+O10.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1095 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G11 · Ehab:  · GL: 

Original =SUM(B12+D12). The source headings require C11+E11.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1096 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N11 · Ehab:  · GL: 

Original =SUM(D11 + F11 + H11 +J11 + L11). The source headings require H11+J11+L11.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1097 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O11 · Ehab:  · GL: 

Original =SUM(C11 + E11 + H11 + J11 +L11 + N11). The source headings require I11+K11+M11.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1098 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P11 · Ehab:  · GL: 

Original =SUM(B11 + D11 + F11 + H11 +J11 + L11). The source headings require F11+N11.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1099 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q11 · Ehab:  · GL: 

Original =SUM(E11 + H11 + J11 +L11 + N11). The source headings require G11+O11.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1100 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G12 · Ehab:  · GL: 

Original =SUM(B13+D13). The source headings require C12+E12.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1101 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N12 · Ehab:  · GL: 

Original =SUM(D12 + F12 + H12 +J12 + L12). The source headings require H12+J12+L12.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1102 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O12 · Ehab:  · GL: 

Original =SUM(C12 + E12 + H12 + J12 +L12 + N12). The source headings require I12+K12+M12.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1103 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P12 · Ehab:  · GL: 

Original =SUM(B12 + D12 + F12 + H12 +J12 + L12). The source headings require F12+N12.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1104 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q12 · Ehab:  · GL: 

Original =SUM(E12 + H12 + J12 +L12 + N12). The source headings require G12+O12.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1105 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G13 · Ehab:  · GL: 

Original =SUM(B14+D14). The source headings require C13+E13.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1106 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N13 · Ehab:  · GL: 

Original =SUM(D13 + F13 + H13 +J13 + L13). The source headings require H13+J13+L13.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1107 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O13 · Ehab:  · GL: 

Original =SUM(C13 + E13 + H13 + J13 +L13 + N13). The source headings require I13+K13+M13.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1108 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P13 · Ehab:  · GL: 

Original =SUM(B13 + D13 + F13 + H13 +J13 + L13). The source headings require F13+N13.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1109 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q13 · Ehab:  · GL: 

Original =SUM(E13 + H13 + J13 +L13 + N13). The source headings require G13+O13.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1110 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G14 · Ehab:  · GL: 

Original =SUM(B15+D15). The source headings require C14+E14.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1111 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N14 · Ehab:  · GL: 

Original =SUM(D14 + F14 + H14 +J14 + L14). The source headings require H14+J14+L14.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1112 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O14 · Ehab:  · GL: 

Original =SUM(C14 + E14 + H14 + J14 +L14 + N14). The source headings require I14+K14+M14.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1113 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P14 · Ehab:  · GL: 

Original =SUM(B14 + D14 + F14 + H14 +J14 + L14). The source headings require F14+N14.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1114 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q14 · Ehab:  · GL: 

Original =SUM(E14 + H14 + J14 +L14 + N14). The source headings require G14+O14.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1115 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G16 · Ehab:  · GL: 

Original =SUM(B17+D17). The source headings require C16+E16.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1116 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N16 · Ehab:  · GL: 

Original =SUM(D16 + F16 + H16 +J16 + L16). The source headings require H16+J16+L16.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1117 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O16 · Ehab:  · GL: 

Original =SUM(C16 + E16 + H16 + J16 +L16 + N16). The source headings require I16+K16+M16.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1118 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P16 · Ehab:  · GL: 

Original =SUM(B16 + D16 + F16 + H16 +J16 + L16). The source headings require F16+N16.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1119 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q16 · Ehab:  · GL: 

Original =SUM(E16 + H16 + J16 +L16 + N16). The source headings require G16+O16.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1120 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G17 · Ehab:  · GL: 

Original =SUM(B18+D18). The source headings require C17+E17.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1121 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N17 · Ehab:  · GL: 

Original =SUM(D17 + F17 + H17 +J17 + L17). The source headings require H17+J17+L17.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1122 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O17 · Ehab:  · GL: 

Original =SUM(C17 + E17 + H17 + J17 +L17 + N17). The source headings require I17+K17+M17.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1123 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P17 · Ehab:  · GL: 

Original =SUM(B17 + D17 + F17 + H17 +J17 + L17). The source headings require F17+N17.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1124 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q17 · Ehab:  · GL: 

Original =SUM(E17 + H17 + J17 +L17 + N17). The source headings require G17+O17.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1125 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G18 · Ehab:  · GL: 

Original =SUM(B19+D19). The source headings require C18+E18.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1126 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N18 · Ehab:  · GL: 

Original =SUM(D18 + F18 + H18 +J18 + L18). The source headings require H18+J18+L18.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1127 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O18 · Ehab:  · GL: 

Original =SUM(C18 + E18 + H18 + J18 +L18 + N18). The source headings require I18+K18+M18.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1128 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P18 · Ehab:  · GL: 

Original =SUM(B18 + D18 + F18 + H18 +J18 + L18). The source headings require F18+N18.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1129 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q18 · Ehab:  · GL: 

Original =SUM(E18 + H18 + J18 +L18 + N18). The source headings require G18+O18.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1130 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G19 · Ehab:  · GL: 

Original =SUM(B20+D20). The source headings require C19+E19.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1131 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N19 · Ehab:  · GL: 

Original =SUM(D19 + F19 + H19 +J19 + L19). The source headings require H19+J19+L19.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1132 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O19 · Ehab:  · GL: 

Original =SUM(C19 + E19 + H19 + J19 +L19 + N19). The source headings require I19+K19+M19.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1133 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P19 · Ehab:  · GL: 

Original =SUM(B19 + D19 + F19 + H19 +J19 + L19). The source headings require F19+N19.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1134 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q19 · Ehab:  · GL: 

Original =SUM(E19 + H19 + J19 +L19 + N19). The source headings require G19+O19.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1135 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G20 · Ehab:  · GL: 

Original =SUM(B21+D21). The source headings require C20+E20.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1136 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N20 · Ehab:  · GL: 

Original =SUM(D20 + F20 + H20 +J20 + L20). The source headings require H20+J20+L20.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1137 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O20 · Ehab:  · GL: 

Original =SUM(C20 + E20 + H20 + J20 +L20 + N20). The source headings require I20+K20+M20.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1138 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P20 · Ehab:  · GL: 

Original =SUM(B20 + D20 + F20 + H20 +J20 + L20). The source headings require F20+N20.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1139 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q20 · Ehab:  · GL: 

Original =SUM(E20 + H20 + J20 +L20 + N20). The source headings require G20+O20.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1140 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!G21 · Ehab:  · GL: 

Original =SUM(B22+D22). The source headings require C21+E21.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1141 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!N21 · Ehab:  · GL: 

Original =SUM(D21 + F21 + H21 +J21 + L21). The source headings require H21+J21+L21.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1142 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!O21 · Ehab:  · GL: 

Original =SUM(C21 + E21 + H21 + J21 +L21 + N21). The source headings require I21+K21+M21.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1143 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!P21 · Ehab:  · GL: 

Original =SUM(B21 + D21 + F21 + H21 +J21 + L21). The source headings require F21+N21.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1144 — CONFIRMED — Credit-quality total uses wrong buckets or direct/indirect columns

Systems: Table 11!Q21 · Ehab:  · GL: 

Original =SUM(E21 + H21 + J21 +L21 + N21). The source headings require G21+O21.

Handling: Correct the formula against the Direct/Indirect and Performing/Non-performing headers. Use a nonzero independent fixture to exclude double counting.
Limits: 

## NBS-1145 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!D6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is Equal to or less than 1 Days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) 

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1146 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!E6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is Equal to or less than  7 Days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) 

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1147 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!F6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 7 and less than 30 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) 

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1148 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!G6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 30 and less than 90 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1149 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!H6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 90 and less than 180 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1150 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!I6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 180 and less than 365 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1151 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!J6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 365 and less than 730 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) 

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1152 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!K6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 730 and less than 1825 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1153 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!L6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 1825 and less than 3650 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1154 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!M6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 3650 and less than 7300 days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1155 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 10!N6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 7300
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT)

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1156 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!E9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 7 and less than and equal to 30 days.

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1157 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!F9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 30 and less than and equal to 90 days.

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1158 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!G9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 90 and less than and equal to 180 days.

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1159 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!H9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 180 and less than and equal to 360 days.

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1160 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!I9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 360 and less than and equal to 720 days.

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1161 — CONFIRMED — Remaining maturity subtraction runs backwards

Systems: Table 24!J9 · Ehab:  · GL: 

Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is greater than 720 DAYS

Handling: For future maturity bands use MATURITY.DATE minus the effective reporting date. Handle overdue and missing dates separately.
Limits: Confirmed arithmetic direction under the future-maturity labels. Calendar-day/month/year conventions remain a separate decision.

## NBS-1162 — CONFIRMED — Without Maturity is defined as a one-day date band

Systems: Table 10!D6 · Ehab:  · GL: 

1.Take the Account ID and go to AA.ACCOUNT.DETAILS where(System Date - MATURITY.DATE) is Equal to or less than 1 Days.
2. Take the Account ID and go to EB.CONTRACT.BALANCES and SUM(OPEN.BALANCE + CREDIT.MVMT + DEBIT.MVMT) 

Handling: Select missing/open-ended maturity according to the approved source definition. Do not treat a near-term or overdue date as a missing date.
Limits: 

## NBS-1163 — CONFIRMED — Exact maturity boundary 30 days is omitted

Systems: Table 10!F6, G6 · Ehab:  · GL: 

F6 ends at less than 30; G6 starts at greater than 30. A balance at exactly 30 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1164 — CONFIRMED — Exact maturity boundary 90 days is omitted

Systems: Table 10!G6, H6 · Ehab:  · GL: 

G6 ends at less than 90; H6 starts at greater than 90. A balance at exactly 90 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1165 — CONFIRMED — Exact maturity boundary 180 days is omitted

Systems: Table 10!H6, I6 · Ehab:  · GL: 

H6 ends at less than 180; I6 starts at greater than 180. A balance at exactly 180 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1166 — CONFIRMED — Exact maturity boundary 365 days is omitted

Systems: Table 10!I6, J6 · Ehab:  · GL: 

I6 ends at less than 365; J6 starts at greater than 365. A balance at exactly 365 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1167 — CONFIRMED — Exact maturity boundary 730 days is omitted

Systems: Table 10!J6, K6 · Ehab:  · GL: 

J6 ends at less than 730; K6 starts at greater than 730. A balance at exactly 730 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1168 — CONFIRMED — Exact maturity boundary 1825 days is omitted

Systems: Table 10!K6, L6 · Ehab:  · GL: 

K6 ends at less than 1825; L6 starts at greater than 1825. A balance at exactly 1825 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1169 — CONFIRMED — Exact maturity boundary 3650 days is omitted

Systems: Table 10!L6, M6 · Ehab:  · GL: 

L6 ends at less than 3650; M6 starts at greater than 3650. A balance at exactly 3650 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1170 — CONFIRMED — Exact maturity boundary 7300 days is omitted

Systems: Table 10!M6, N6 · Ehab:  · GL: 

M6 ends at less than 7300; N6 starts at greater than 7300. A balance at exactly 7300 days reaches neither band.

Handling: Use mutually exclusive bands with one inclusive side at each shared boundary.
Limits: 

## NBS-1171 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!E61 · Ehab:  · GL: 

Inside Qatar / Total contains B+C. Valid labelled components: C+D.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1172 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!H61 · Ehab:  · GL: 

Outside Qatar / Total contains E+F. Valid labelled components: F+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1173 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!I61 · Ehab:  · GL: 

Grand Total / LC contains B+E. Valid labelled components: C+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1174 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!J61 · Ehab:  · GL: 

Grand Total / FC contains C+F. Valid labelled components: D+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1175 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!K61 · Ehab:  · GL: 

Grand Total / Total contains H+J. Valid labelled components: I+J or E+H.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1176 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!E62 · Ehab:  · GL: 

Inside Qatar / Total contains B+C. Valid labelled components: C+D.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1177 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!H62 · Ehab:  · GL: 

Outside Qatar / Total contains E+F. Valid labelled components: F+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1178 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!I62 · Ehab:  · GL: 

Grand Total / LC contains B+E. Valid labelled components: C+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1179 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!J62 · Ehab:  · GL: 

Grand Total / FC contains C+F. Valid labelled components: D+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1180 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: ASSET - 100!K62 · Ehab:  · GL: 

Grand Total / Total contains H+J. Valid labelled components: I+J or E+H.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1181 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 9!D6 · Ehab:  · GL: 

Inside Qatar / Total contains C+D. Valid labelled components: B+C.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1182 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 9!G6 · Ehab:  · GL: 

Outside Qatar / Total contains F+G. Valid labelled components: E+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1183 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 9!H6 · Ehab:  · GL: 

Grand Total / LC contains C+F. Valid labelled components: B+E.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1184 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 9!I6 · Ehab:  · GL: 

Grand Total / FC contains D+G. Valid labelled components: C+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1185 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 9!J6 · Ehab:  · GL: 

Grand Total / Total contains I+J. Valid labelled components: H+I or D+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1186 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!D5 · Ehab:  · GL: 

Inside Qatar / Total contains C+D. Valid labelled components: B+C.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1187 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!G5 · Ehab:  · GL: 

Outside Qatar / Total contains F+G. Valid labelled components: E+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1188 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!H5 · Ehab:  · GL: 

Grand Total / LC contains C+F. Valid labelled components: B+E.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1189 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!I5 · Ehab:  · GL: 

Grand Total / FC contains D+G. Valid labelled components: C+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1190 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!J5 · Ehab:  · GL: 

Grand Total / Total contains I+J. Valid labelled components: H+I or D+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1191 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!D26 · Ehab:  · GL: 

Inside Qatar / Total contains C+D. Valid labelled components: B+C.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1192 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!G26 · Ehab:  · GL: 

Outside Qatar / Total contains F+G. Valid labelled components: E+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1193 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!H26 · Ehab:  · GL: 

Grand Total / LC contains C+F. Valid labelled components: B+E.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1194 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!I26 · Ehab:  · GL: 

Grand Total / FC contains D+G. Valid labelled components: C+F.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1195 — CONFIRMED — Total expression uses the wrong labelled columns

Systems: Table 26!J26 · Ehab:  · GL: 

Grand Total / Total contains I+J. Valid labelled components: H+I or D+G.

Handling: Correct the written total expression to the labelled source columns.
Limits: 

## NBS-1196 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 65037

Systems: Income!B21 · Ehab:  · GL: 

CATEGORY = 65037 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1197 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 65037

Systems: Income!C21 · Ehab:  · GL: 

CATEGORY = 65037 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1198 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 65037

Systems: Income!D21 · Ehab:  · GL: 

CATEGORY = 65037 , 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1199 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 65037

Systems: Income!F21 · Ehab:  · GL: 

CATEGORY = 65037 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1200 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 65037

Systems: Income!G21 · Ehab:  · GL: 

CATEGORY = 65037 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1201 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 66022

Systems: Income!B80 · Ehab:  · GL: 

CATEGORY = 65220 ,54600 ,65220 ,65221 ,54700 ,65227 ,65228, 66022, 66043, 66044

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1202 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 66022

Systems: Income!D80 · Ehab:  · GL: 

CATEGORY = 65220 ,54600 ,65220 ,65221 ,54700 ,65227 ,65228, 66022, 66043, 66044

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1203 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 66022

Systems: Income!F80 · Ehab:  · GL: 

CATEGORY = 65220 ,54600 ,65220 ,65221 ,54700 ,65227 ,65228, 66022, 66043, 66044

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1204 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 66022

Systems: Income!G80 · Ehab:  · GL: 

CATEGORY = 65220 ,54600 ,65220 ,65221 ,54700 ,65227 ,65228, 66022, 66043, 66044

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1205 — DIFFERENCE — Product category placed in a consolidated P&L selector: 15154

Systems: Expense!B30 · Ehab:  · GL: Current v6 CATEGORY!D824:F824

Cell: Category = 66502, 66505, 15154 ,66580 ,66581 ,66582 ,66583 ,66584 ,66585. CATEGORY!D824: None; CATEGORY!F824: ECL Financing Private Banking.

Handling: Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.
Limits: 

## NBS-1206 — DIFFERENCE — Product category placed in a consolidated P&L selector: 15154

Systems: Expense!C30 · Ehab:  · GL: Current v6 CATEGORY!D824:F824

Cell: CATEGORY = 66502, 66505, 15154 ,66580 ,66581 ,66582 ,66583 ,66584 ,66585 > SECTOR = 3001. CATEGORY!D824: None; CATEGORY!F824: ECL Financing Private Banking.

Handling: Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.
Limits: 

## NBS-1207 — DIFFERENCE — Product category placed in a consolidated P&L selector: 15154

Systems: Expense!D30 · Ehab:  · GL: Current v6 CATEGORY!D824:F824

Cell: CATEGORY = 66502, 66505, 15154 ,66580 ,66581 ,66582 ,66583 ,66584 ,66585 > SECTOR = 3001. CATEGORY!D824: None; CATEGORY!F824: ECL Financing Private Banking.

Handling: Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.
Limits: 

## NBS-1208 — DIFFERENCE — Product category placed in a consolidated P&L selector: 15154

Systems: Expense!F30 · Ehab:  · GL: Current v6 CATEGORY!D824:F824

Cell: CATEGORY = 66502, 66505, 15154 ,66580 ,66581 ,66582 ,66583 ,66584 ,66585 > SECTOR = 3001. CATEGORY!D824: None; CATEGORY!F824: ECL Financing Private Banking.

Handling: Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.
Limits: 

## NBS-1209 — DIFFERENCE — Product category placed in a consolidated P&L selector: 15154

Systems: Expense!G30 · Ehab:  · GL: Current v6 CATEGORY!D824:F824

Cell: CATEGORY = 66502, 66505, 15154 ,66580 ,66581 ,66582 ,66583 ,66584 ,66585 > SECTOR = 3001. CATEGORY!D824: None; CATEGORY!F824: ECL Financing Private Banking.

Handling: Establish the corresponding PL category using Migration PL and the documented source. Keep product category separate.
Limits: 

## NBS-1210 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 61605

Systems: Expense!B117 · Ehab:  · GL: 

Category = 61010, 61011, 61012, 61050 ,61051 ,61052 ,61053 ,61054 ,61055 ,61056, 61070 ,61071 ,61072 ,61073-61100 ,61101 ,61102, 61140 ,61141 ,61142, 61190 ,61191 ,61192 ,61193 ,61194 ,61195, 61221 ,61222 ,61223 ,61224 ,61225, 61230 ,61231 ,61232 ,61233 ,61234 ,61235, 66590, 66520 ,66521 ,66531 ,66522 ,66523 ,66524 ,66525, 61110, 61205, 61060, 61605, 61080, 61045, 66606, 51200, 66595

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1211 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 61605

Systems: Expense!C117 · Ehab:  · GL: 

CATEGORY = 61010, 61011, 61012, 61050 ,61051 ,61052 ,61053 ,61054 ,61055 ,61056, 61070 ,61071 ,61072 ,61073-61100 ,61101 ,61102, 61140 ,61141 ,61142, 61190 ,61191 ,61192 ,61193 ,61194 ,61195, 61221 ,61222 ,61223 ,61224 ,61225, 61230 ,61231 ,61232 ,61233 ,61234 ,61235, 66590, 66520 ,66521 ,66531 ,66522 ,66523 ,66524 ,66525, 61110, 61205, 61060, 61605, 61080, 61045, 66606, 51200, 66595, SECTOR = 1000 -1999 & 4000 - 4004

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1212 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 61605

Systems: Expense!D117 · Ehab:  · GL: 

CATEGORY = 61010, 61011, 61012, 61050 ,61051 ,61052 ,61053 ,61054 ,61055 ,61056, 61070 ,61071 ,61072 ,61073-61100 ,61101 ,61102, 61140 ,61141 ,61142, 61190 ,61191 ,61192 ,61193 ,61194 ,61195, 61221 ,61222 ,61223 ,61224 ,61225, 61230 ,61231 ,61232 ,61233 ,61234 ,61235, 66590, 66520 ,66521 ,66531 ,66522 ,66523 ,66524 ,66525, 61110, 61205, 61060, 61605, 61080, 61045, 66606, 51200, 66595, SECTOR = 1000 -1999 & 4000 - 4004

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1213 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 61605

Systems: Expense!F117 · Ehab:  · GL: 

CATEGORY = 61010, 61011, 61012, 61050 ,61051 ,61052 ,61053 ,61054 ,61055 ,61056, 61070 ,61071 ,61072 ,61073-61100 ,61101 ,61102, 61140 ,61141 ,61142, 61190 ,61191 ,61192 ,61193 ,61194 ,61195, 61221 ,61222 ,61223 ,61224 ,61225, 61230 ,61231 ,61232 ,61233 ,61234 ,61235, 66590, 66520 ,66521 ,66531 ,66522 ,66523 ,66524 ,66525, 61110, 61205, 61060, 61605, 61080, 61045, 66606, 51200, 66595,SECTOR = 1000 -1999 & 4000 - 4004

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1214 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 61605

Systems: Expense!G117 · Ehab:  · GL: 

CATEGORY = 61010, 61011, 61012, 61050 ,61051 ,61052 ,61053 ,61054 ,61055 ,61056, 61070 ,61071 ,61072 ,61073-61100 ,61101 ,61102, 61140 ,61141 ,61142, 61190 ,61191 ,61192 ,61193 ,61194 ,61195, 61221 ,61222 ,61223 ,61224 ,61225, 61230 ,61231 ,61232 ,61233 ,61234 ,61235, 66590, 66520 ,66521 ,66531 ,66522 ,66523 ,66524 ,66525, 61110, 61205, 61060, 61605, 61080, 61045, 66606, 51200, 66595, SECTOR = 1000 -1999 & 4000 - 4004

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1215 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1216 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1217 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1218 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1219 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1220 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1221 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1222 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1223 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1224 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1225 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1226 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1227 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1228 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1229 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1230 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1231 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1232 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1233 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!C90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1234 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1235 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1236 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1237 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1238 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1239 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1240 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1241 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1242 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1243 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1244 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1245 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1246 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1247 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1248 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1249 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1250 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1251 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1252 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!D90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1253 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1254 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1255 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1256 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1257 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1258 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1259 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1260 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1261 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1262 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1263 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1264 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1265 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1266 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1267 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1268 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1269 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1270 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1271 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!F90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1272 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1273 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1274 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1275 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1276 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1277 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1278 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1279 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1280 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1281 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1282 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1283 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1284 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1285 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1286 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1287 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1288 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1289 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1290 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!G90 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2004 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1291 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1292 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1293 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1294 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1295 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1296 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1297 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1298 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1299 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1300 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1301 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1302 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1303 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1304 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1305 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1306 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1307 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1308 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1309 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!C94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1310 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1311 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1312 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1313 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1314 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1315 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1316 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1317 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1318 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1319 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1320 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1321 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1322 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1323 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1324 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1325 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1326 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1327 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1328 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!D94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1329 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1330 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1331 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1332 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1333 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1334 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1335 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1336 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1337 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1338 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1339 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1340 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1341 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1342 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1343 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1344 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1345 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1346 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1347 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!F94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1348 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1349 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1350 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1351 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1352 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1353 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1354 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1355 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1356 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1357 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1358 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1359 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1360 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1361 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1362 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1363 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1364 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1365 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1366 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!G94 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 2005 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1367 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1368 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1369 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1370 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1371 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1372 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1373 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1374 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1375 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1376 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1377 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1378 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1379 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1380 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1381 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1382 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1383 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1384 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1385 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!C98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+
LOCAL.CREDT.MVE+
LOCAL.DEBIT.MVE),
IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1386 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1387 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1388 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1389 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1390 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1391 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1392 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1393 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1394 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1395 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1396 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1397 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1398 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1399 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1400 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1401 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1402 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1403 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1404 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!D98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1405 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1406 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1407 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1408 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1409 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1410 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1411 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1412 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1413 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1414 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1415 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1416 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1417 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1418 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1419 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1420 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1421 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1422 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1423 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!F98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1424 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3100

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1425 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3110

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1426 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3111

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1427 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3112

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1428 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3148

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1429 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3301

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1430 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3302

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1431 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3303

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1432 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3304

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1433 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3305

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1434 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3314

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1435 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3501

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1436 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3502

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1437 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3503

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1438 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3504

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1439 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3591

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1440 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3601

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1441 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3609

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1442 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 3710

Systems: ASSET - 100!G98 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB>IF CURRENCY NOT EQUAL TO QAR THEN SUM(LOCAL.BALANCE+

LOCAL.CREDT.MVE+

LOCAL.DEBIT.MVE),

IF CURRENCY = QAR THEN SUM(BALANCE+CREDIT.MOVEMENT+DEBIT.MOVEMENT) WHERE ASSET TYPE = CURACCOUNT, DUEACCOUNT. GRCACCOUNT, NABACCOUNT & PDOACCOUNT, SECTOR = 1000 - 1999 & 4000 - 4005 & 2000 - 2003 & 2006 & 5001 & CATEGORY= 3000, 3001, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3148, 3149, 3301, 3302, 3303, 3304, 3305, 3314, 3701, 3717, 3720, 3730, 3501 , 3502 , 3503 , 3504 , 3591 , 3601 , 3609 , 3702 , 3703 , 3704 , 3705 , 3706 , 3707 , 3708 , 3709 , 3710 , 3711 , 3712 , 3713 , 3714 , 3715 , 3716 , 3718 , 3740 , 3791 

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1443 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 134030

Systems: ASSET - 100!C107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1444 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 134030

Systems: ASSET - 100!D107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1445 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 134030

Systems: ASSET - 100!F107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1446 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 134030

Systems: ASSET - 100!G107 · Ehab:  · GL: 

CONSOLIDATE.ASST.LIAB >
1. CATEGORY = 3000-3999, 13440-13459, 1000-1999 & ASSTE TYPE = ACCDEFERREDPFT
RECDEFERREDPFT,
DUEPRINCIPALPFT,
GRCPRINCIPALPFT,
NABPRINCIPALPFT, DEBIT , DRINTEREST
2. CATEGRY = 13470, 13489  ASSET TYPE = DEBIT
3. CATEGRY = 8025, 13400-13429
4. CATEGRY = 12180-12198 
5. CATEGRY = 12101-12179, ASSET TYPE = DEBIT
CATEGORY=6640-6649 ,  ASSET TYPE = ACCDEPOSITPFT  
6. CATEGORY = 12650-12699, 13150-13169, 14060-14069, 13490-13499, 14000-14059, 13500, 14460-14999, 13520-13529
7. CATEGORY = 134030, 12920, 12921, 12500-12599 , 16600-16619, 12800-12809, 13510-13519, 14016-14018, ASSET TYPE = DEBIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1447 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 13112

Systems: Table 17 !L9 · Ehab:  · GL: 

CATEGORY = 11001 & 11005 & ASSET TYPE = DEBIT ,CATEGORY = 11221 - 11231 & ASSET TYPE = DEBIT ,CATEGORY = 11210 & 11241 & ASSET TYPE = DEBIT ,CATEGORY = 11201 ASSET TYPE = DEBIT ,CATEGORY = 11300 ASSET TYPE = DEBIT ,CATEGORY = 11311, 13112, 11314 ASSET TYPE = DEBIT ,CATEGORY =  11315 ASSET TYPE = DEBIT
CATEGORY = 11500 , 11515 & ASSET TYPE = CREDIT ,CATEGORY = 11512 , 11513 & ASSET TYPE = CREDIT ,CATEGORY = 11511 , 11514 & ASSET TYPE = CREDIT ,CATEGORY = 11510 & ASSET TYPE = CREDIT ,CATEGORY = 11520 & ASSET TYPE = CREDIT ,CATEGORY = 11550, 11551, 11553 & ASSET TYPE = CREDIT ,CATEGORY = 11554 & ASSET TYPE = CREDIT ,CATEGORY = 11552, 11559 & ASSET TYPE = CREDIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1448 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 13112

Systems: Table 17 !B16 · Ehab:  · GL: 

CATEGORY = 11311, 13112, 11314 ASSET TYPE = DEBIT

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1449 — DIFFERENCE — Explicit category absent from both supplied dictionaries: 66022

Systems: Table 43!E44 · Ehab:  · GL: 

PLCATEGORY = 65220 ,54600 ,65220 ,65221 ,54700 ,65227 ,65228, 66022, 66043, 66044

Handling: Check the intended category against the approved CATEGORY sheet and GL trace. Do not invent a replacement.
Limits: Dictionary absence proves a source inconsistency, not absence from every possible bank configuration.

## NBS-1450 — REVIEW — Same Ehab GL selector assigned to two lines

Systems: ! · Ehab: K109, K111 · GL: 

K109 .....02 Treasury Shares - Nominal -: 3200000001. K111 .....04 Treasury Shares - Prem. / Disc.: 3200000001.

Handling: Investigate whether a split attribute or correction is missing. Retain both entries until evidenced.
Limits: 

## NBS-1451 — REVIEW — Accrued asset and deferred liability select the same profit component

Systems: TABLE 19!C10 · Ehab:  · GL: 

TABLE 19!C10 and Table 30!B7 both include categories 3000–3999 and ACCDEFERREDPFT.

Handling: Determine the intended accounting side and measurement. Reconcile the asset and liability schedules without automatically deleting either source rule.
Limits: Selector overlap is proven. Actual double counting depends on the complete source calculation and presentation sign.

## NBS-1452 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!B7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1453 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!C7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1454 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!D7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1455 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!E7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1456 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!H7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1457 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!I7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1458 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!J7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1459 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!K7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1460 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!L7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1461 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!M7 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion: L.RES.STATUS = YES then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1462 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!B16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1463 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!C16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1464 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!D16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1465 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!E16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1466 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!H16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1467 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!I16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1468 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!J16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1469 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!K16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1470 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!L16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1471 — DIFFERENCE — NBFI criterion includes the salary-card sector

Systems: Table 11!M16 · Ehab:  · GL: Current v6 SEGMENT!C30

Original criterion:  
L.RES.STATUS = NO then CUSTOMER>SECTOR = 1005, 2006 & CUSTOMER>Target = 13, 16. Current GL SEGMENT!C30: 2006 - Salary Cards.

Handling: Reconcile the configured customer-sector dictionary with the QCB institution crosswalk before activating the NBFI split.
Limits: The cross-source sector definition conflicts. It does not prove the deployed customer field uses this dictionary without a configured-field confirmation.

## NBS-1472 — CONFIRMED — Asset cash reference omits the Cash on hand row

Systems: ASSET - 100!B6 · Ehab: K5, K358 · GL: 

Original text: Table 1'!A10+'Table 1'!A11. Table 1!A9 is Cash on hand; the written references are A10 Precious Metals and A11 Others.

Handling: Correct the linked breakdown rows after confirming which cash components belong in the base line.
Limits: The written reference omission is confirmed. This cell is a specification string, not a working balance calculation.

## NBS-1473 — INPUT GAP — BO schedule 020 has no original Systems worksheet

Systems: ! · Ehab:  · GL: 

The BO target register includes table 020; no table-number worksheet is present in the 6 October Systems source.

Handling: Obtain the original specification or write a separate reviewed mapping for the missing schedule.
Limits: No original worksheet was supplied. This does not establish what is deployed in the bank report.

## NBS-1474 — INPUT GAP — BO schedule 038 has no original Systems worksheet

Systems: ! · Ehab:  · GL: 

The BO target register includes table 038; no table-number worksheet is present in the 6 October Systems source.

Handling: Obtain the original specification or write a separate reviewed mapping for the missing schedule.
Limits: No original worksheet was supplied. This does not establish what is deployed in the bank report.

## NBS-1475 — REVIEW — Category 3713 falls into Others under the existing Murabaha category filters

Systems: Table 8!A20 · Ehab:  · GL: 

Routing mismatch with the owner-provided Murabaha/CLM category 3713 scope. The Murabaha list is 3701, 3717, 3704; the Others predicate includes 3000-3999 while excluding those three and Ijara 3702/3706, leaving 3713 in Others. This establishes the route under the text predicate, not the correctness of the bank’s category taxonomy. Reclassification and the two unknown CLM balances are separate controls.

Handling: Approve category 3713’s Murabaha route, define whether category alone or additional product/arrangement conditions identify CLM, and supply the exact two extra balance identifiers, destination groups and effective date. Remove 3713 from Others when the Murabaha route is activated so one contract cannot enter both rows.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1476 — REVIEW — Category 3713 falls into Others under the existing Murabaha category filters

Systems: Table 8!A27 · Ehab:  · GL: 

Routing mismatch with the owner-provided Murabaha/CLM category 3713 scope. The Murabaha list is 3701, 3717, 3704; the Others predicate includes 3000-3999 while excluding those three and Ijara 3702/3706, leaving 3713 in Others. This establishes the route under the text predicate, not the correctness of the bank’s category taxonomy. Reclassification and the two unknown CLM balances are separate controls.

Handling: Approve category 3713’s Murabaha route, define whether category alone or additional product/arrangement conditions identify CLM, and supply the exact two extra balance identifiers, destination groups and effective date. Remove 3713 from Others when the Murabaha route is activated so one contract cannot enter both rows.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1477 — REVIEW — Deferred-income row mixes two owner groups and one unrecognized balance

Systems: Table 11!A26 · Ehab:  · GL: 

Metric ambiguity relative to the owner rules: ACCDEFERREDPFT is UNEARNED_PROFIT; DUEDEFERREDPFT, GRCDEFERREDPFT and NABDEFERREDPFT are OUTSTANDING; PDODEFERREDPFT belongs to none of the owner’s 19 codes. DEFERREDPFT, the other UNEARNED_PROFIT component, is absent. The label Deferred Interest / Income does not establish whether this row should be the owner’s unearned group or a separate legacy deferred-income measure. Row 25’s SP suspense list is a separate measure and must not be replaced by ordinary loan groups.

Handling: Choose the intended metric for row 26 and supply authoritative definitions for PDODEFERREDPFT. If the intended metric is UNEARNED_PROFIT, explicitly bind row 26 to DEFERREDPFT + ACCDEFERREDPFT. Retain any separate suspense rule until the owner defines it.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1478 — REVIEW — Remaining-maturity subtraction runs in the wrong direction

Systems: Table 10!A2 · Ehab:  · GL: 

Concrete predicate defect if the table represents remaining maturity as indicated by the future maturity headings. System Date - MATURITY.DATE is negative for future maturities, so a future contract can meet both D6 (<=1) and E6 (<=7), while longer positive bands select past-due contracts. A contract maturing 100 days after the as-of date gives -100 and qualifies for both short buckets rather than the >3 to 6 months band. This is a logic illustration, not a value observed in report data.

Handling: Set a single reporting as-of date and use maturity_date - as_of_date for remaining tenor if that is the regulatory basis. Define the disposition of matured/overdue and same-day contracts separately, and confirm contractual maturity versus any alternative reporting maturity.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1479 — REVIEW — Remaining-maturity subtraction runs in the wrong direction

Systems: Table 10!D4 · Ehab:  · GL: 

Concrete predicate defect if the table represents remaining maturity as indicated by the future maturity headings. System Date - MATURITY.DATE is negative for future maturities, so a future contract can meet both D6 (<=1) and E6 (<=7), while longer positive bands select past-due contracts. A contract maturing 100 days after the as-of date gives -100 and qualifies for both short buckets rather than the >3 to 6 months band. This is a logic illustration, not a value observed in report data.

Handling: Set a single reporting as-of date and use maturity_date - as_of_date for remaining tenor if that is the regulatory basis. Define the disposition of matured/overdue and same-day contracts separately, and confirm contractual maturity versus any alternative reporting maturity.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1480 — REVIEW — Remaining-maturity subtraction runs in the wrong direction

Systems: Table 10!E4 · Ehab:  · GL: 

Concrete predicate defect if the table represents remaining maturity as indicated by the future maturity headings. System Date - MATURITY.DATE is negative for future maturities, so a future contract can meet both D6 (<=1) and E6 (<=7), while longer positive bands select past-due contracts. A contract maturing 100 days after the as-of date gives -100 and qualifies for both short buckets rather than the >3 to 6 months band. This is a logic illustration, not a value observed in report data.

Handling: Set a single reporting as-of date and use maturity_date - as_of_date for remaining tenor if that is the regulatory basis. Define the disposition of matured/overdue and same-day contracts separately, and confirm contractual maturity versus any alternative reporting maturity.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1481 — REVIEW — Remaining-maturity subtraction runs in the wrong direction

Systems: Table 10!F4 · Ehab:  · GL: 

Concrete predicate defect if the table represents remaining maturity as indicated by the future maturity headings. System Date - MATURITY.DATE is negative for future maturities, so a future contract can meet both D6 (<=1) and E6 (<=7), while longer positive bands select past-due contracts. A contract maturing 100 days after the as-of date gives -100 and qualifies for both short buckets rather than the >3 to 6 months band. This is a logic illustration, not a value observed in report data.

Handling: Set a single reporting as-of date and use maturity_date - as_of_date for remaining tenor if that is the regulatory basis. Define the disposition of matured/overdue and same-day contracts separately, and confirm contractual maturity versus any alternative reporting maturity.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1482 — REVIEW — Maturity buckets overlap, omit exact boundaries, and do not identify missing maturity

Systems: Table 10!O6 · Ehab:  · GL: 

Concrete predicate defects independent of which balance group is selected. D6 uses <=1 and E6 <=7 so they overlap; Without Maturity is tested as <=1 day rather than a missing/undefined maturity date. Bands use strictly greater and strictly less comparisons, leaving exactly 30, 90, 180, 365, 730, 1825, 3650 and 7300 uncovered. E4’s >1 Week wording conflicts with E6’s <=7-day test. O6 sums all buckets, so overlap can double-count and gaps can omit contracts. Fixed days also differ from calendar months/years around leap days.

Handling: Define one mutually exclusive and exhaustive interval model, an explicit missing-maturity bucket, precise inclusivity at every boundary, the intended first-week label, and whether month/year limits use calendar periods or fixed day counts. Validate that each eligible contract reaches exactly one bucket.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1483 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!B3 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1484 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!D3 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1485 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!F3 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1486 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!N3 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1487 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!P3 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1488 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!B4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1489 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!C4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1490 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!F4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1491 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!G4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1492 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!N4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1493 — REVIEW — Direct credit-quality totals include performing exposures twice and indirect performing total uses the next row

Systems: Table 11!P4 · Ehab:  · GL: 

Concrete formula-reference defects relative to the supplied headings, repeated on rows 5, 7-14 and 16-21. F=B+D already totals performing Direct. N=D+F+H+J+L includes performing balances inside Total Non-performing Direct. P=B+D+F+H+J+L counts B and D twice because F=B+D. G uses next-row B/D Direct cells rather than same-row C/E Indirect cells. Illustrative inputs B=100,D=20,H=30,J=40,L=50 yield N=260 rather than 120 and P=360 rather than 240. Mapping cells currently contain specification text, so these formula defects are not evidence of an actual submitted amount.

Handling: Confirm the existing headings as the intended dimensions. The corresponding structural formulas are F=B+D, G=C+E, N=H+J+L and P=F+N on the same row. Apply only after separating specification text from numeric output and verify totals with independent reconciliation.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1494 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!H3 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1495 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!J3 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1496 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!L3 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1497 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!H4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1498 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!I4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1499 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!J4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1500 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!K4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1501 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!L4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1502 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!M4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1503 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!O4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1504 — REVIEW — Indirect credit-quality totals sum Direct columns and duplicate a subtotal

Systems: Table 11!Q4 · Ehab:  · GL: 

Concrete formula dimension and duplication defects repeated on rows 5, 7-14 and 16-21. O (Total Non-performing Indirect) sums C,E plus Direct H,J,L and Direct subtotal N, omitting Indirect I,K,M. Q (Grand Total Indirect) likewise uses Direct H,J,L,N, omits C and I/K/M, and incorporates subtotal N alongside its component H/J/L. With illustrative Direct inputs B=100,D=20,H=30,J=40,L=50 and Indirect C=10,E=2,I=3,K=4,M=5, existing O=392 and Q=382; the headed indirect dimensions would give O=12 and Q=24. These probes demonstrate formula logic, not observed reporting data.

Handling: Confirm Direct/Indirect headings. Structural same-row replacements are O=I+K+M and Q=G+O with G=C+E. Do not include direct exposure or a subtotal and its components in an indirect total.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1505 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!A5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1506 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!B5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1507 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!D5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1508 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!H5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1509 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!J5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1510 — REVIEW — Credit-quality baseline reads movements without an opening balance and changes selected balances by risk

Systems: Table 11!L5 · Ehab:  · GL: 

As-of-stock calculation ambiguity. Baseline row 5 explicitly reads DEBIT+CREDIT.MVMT but not OPEN, unlike rows 25/26 which use OPEN+DEBIT+CREDIT. Good/Low Risk selects CURACCOUNT+DUEACCOUNT, Special Mention adds GRCACCOUNT/DELACCOUNT, and nonperforming columns use six ACCOUNT balances, omitting all owner OUTSTANDING deferred-profit components. Risk is therefore controlling both contract classification and selected balance components; amount changes could reflect excluded balances as well as risk classification. A nonzero opening balance with zero movements would contribute zero under the literal movement-only baseline. No numeric source dataset was provided to establish the magnitude.

Handling: Specify whether this table requires closing outstanding stock or period movements and the exact ECB field/date alignment. For closing stock use an authorized as-of snapshot or correctly aligned opening plus signed movements once. Select the approved table metric separately from the risk-routing predicate so any deliberate risk-specific exclusions remain explicit. Verify OPEN and movement multivalues align to each balance type and reporting currency.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1511 — REVIEW — Legacy template is not a flat mapping table

Systems: ! · Ehab: A354 · GL: 

Extract section identity, complete hierarchy and report dimensions before aligning rules. The workbook contains repeated leaf descriptions and varying headers; description-only joins are unsafe.

Handling: Approve section/row crosswalk to the Temenos source before using legacy logic.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1512 — REVIEW — Ethix loan carrying amount has three metrics

Systems: ! · Ehab: K35 · GL: 

The target must keep OUTSTANDING, AMORTIZED_EARNED, and LOAN_FEES separate and compose the approved carrying amount. User-provided T24 groups cover the first two; no T24 fee group has been supplied.

Handling: Supply the bank-specific T24 source and balance types for LOAN_FEES, fee sign, valuation basis and whether already embedded in another group.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1513 — REVIEW — Loan sector and government exceptions are legacy filters

Systems: ! · Ehab: K13 · GL: 

These are Ethix client/product classifications, not T24 balance types. Resident/nonresident variants are asymmetrical in the legacy text.

Handling: Approve Ethix-to-T24 field dictionaries for SIC, RIM, personal status and residency, and resolve the K37/L37 RIM2398 asymmetry.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1514 — REVIEW — Private-sector SYN and Islamic rules can overlap

Systems: ! · Ehab: K40 · GL: 

A SYN loan with nonpersonal SIC4 may satisfy both main private-sector rules. Copying the text without a precedence/partition rule can double count; K41 also mixes loan-file and GL populations.

Handling: Approve mutually exclusive private-sector finance/product rules, SYN sector restrictions, the GL1300050001 allocation and inside/outside amount symmetry.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1515 — REVIEW — Ethix product classification codes are not T24 equivalents

Systems: ! · Ehab: L670 · GL: 

These selectors inform an approved product crosswalk. They do not establish universal T24 categories or ECB balance types.

Handling: Approve bank-specific product/category mapping, especially Murabaha category3713 and its CLM subset.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1516 — REVIEW — Credit risk, maturity and personal subdivisions require external feeds

Systems: ! · Ehab: K633 · GL: 

Required reporting dimensions cannot all be inferred from balance types. Missing risk/BO sources must remain explicit exceptions, not default assignments.

Handling: Approve risk/BO feed schemas, as-of dates, joins, classification fields and reconciliation controls.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1517 — REVIEW — Deferred income currently uses legacy GL selection

Systems: ! · Ehab: A103 · GL: 

Do not automatically equate these GL selectors or every deferred-income report row with the user UNEARNED_PROFIT group without an approved crosswalk. Principal/deferred-state and risk dimensions still require validation.

Handling: Approve replacement of legacy GL2300 rule with the appropriate loan population and T24 deferred-profit groups, including signs and performing status.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1518 — REVIEW — Formula aliases carry free-text mapping rules

Systems: ! · Ehab: L378 · GL: 

Resolve direct formula aliases with dependency evidence instead of discarding formula cells or treating them as numeric balances. Cached values can be stale; referenced source remains primary.

Handling: No owner decision is needed for safe extraction; any substantive rule change still needs approval.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1519 — REVIEW — NBS Table6 contains repeated report blocks

Systems: Table 6!B3 · Ehab:  · GL: 

Table number plus report ID identifies the report but not the NBS block. Preserve block identity and validate hierarchy/dimensions before attempting row joins or aggregating source mapping records.

Handling: Determine whether the repeated NBS block is a duplicate, separate scope, or intentional variant; approve which block(s) participate in replication.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.

## NBS-1520 — REVIEW — NBS Table6 contains repeated report blocks

Systems: Table 6!B34 · Ehab:  · GL: 

Table number plus report ID identifies the report but not the NBS block. Preserve block identity and validate hierarchy/dimensions before attempting row joins or aggregating source mapping records.

Handling: Determine whether the repeated NBS block is a duplicate, separate scope, or intentional variant; approve which block(s) participate in replication.
Limits: Previously documented source-review issue. Exact cell and immutable source hash checked; this is not a new proven balance error.
