Select  
	A.Bdate				Effective_Date,
    A.Desc_Level_10 	Level_1_Description,
    A.Desc_Level_20 	Level_2_Description,
    A.Desc_Level_30 	Level_3_Description,
    A.Desc_Level_40 	Level_4_Description,
    Case
    	When (Left(A.ledger_no,5) In ('10000','10010','10020','10090')) Then '1  - Cash In Hand & Vault'
    	When (A.ledger_no In ('1003000010','1003000011')) Then '2  - Reserve Account with QCB'
    	When (A.ledger_no In ('1003000020')) Then '3  - Current Account with QCB'
    	When ((Left(A.ledger_no,7) In ('1502000','1502010','1602000')) Or A.acct_no = '01-01-900-60-01-2305550001') Then '4  - Investment In Sukuks - Amortized Cost'
   		When (A.ledger_no  = '1101010015') Then '5  - Nostro Balances, Saving And Call Accounts'
    	When (A.ledger_no In ('1302000010') Or Left(A.ledger_no,7) IN ('1200000','2300020')) Then '6  - Wakala Placements'
    	When ((Left(A.ledger_no,5) In('13010','13020','13025','13030','13000','13060','13050','23050','14025','23055') Or Left(A.ledger_no,7) In ('2300010','2300030','2300000','2301000','2301010','2302000','2300060','2300050','2301030','2302010','2302030','2301060','2302060','2301050','2300025','2307000','1302510','2300070','1900050','1302530') Or A.ledger_no In ('2308500001','2308510001','2308520001','2308530001','2308560001','2309000001','2309010001','2309020001','2309030001','2309040001','2309060001','2308540001','1900020001')) 
    			And A.ledger_no != '1302000010' And A.acct_no != '01-01-900-60-01-2305550001' ) Then '7  - Banking Group Financing'
    	When (Left(A.ledger_no,5) In ('11000','11010') And A.ledger_no Not In ('1101010015')) Then '8  - Nostro Balances - Current Accounts'
    	When (Left(A.ledger_no,7) In ('1501000','1501020','1601000')) Then '9  - Investment In Quoted Equities And Fund - available-for-sale'
    	When (Left(A.ledger_no,7) In ('1501010','1601010','1603010','1602010')) Then '10 - Investment In Un-Quoted Equities And Fund - available-for-sale'
    	When (Left(A.ledger_no,7) In ('1500000','1600000','1600010','1500020','1606010')) Then '11 - Investment In Quoted/Unquoted Equities - Held For Trading'
    	When (Left(A.ledger_no,7) In ('1503000')) Then '12 - Investments In Subsidiaries'
    	When (Left(A.ledger_no,7) In ('1503010')) Then '13 - Investments In Associates'
    	When (Left(A.ledger_no,7) In ('1700000')) Then '14 - Investments In Properties'
    	When (Left(A.ledger_no,3) In ('190') And Left(A.ledger_no,7) Not In ('1900050') And A.ledger_no Not In ('1900000010','1900000011','1900010055','1904500010','1904505051','1904506051','1904508051','1900020001','1904508052','1904508053')) Then '15 - Other Assets'
    	When (Left(A.ledger_no,3) In ('180','280') And Left(A.ledger_no,5) Not In ('18020','28010')) Then '16 - Property And Equipment (Net Fixed Assets)'
    	When (Left(A.ledger_no,7)  In ('1504010')) Then '17 - Investment - Land'
    	When (Left(A.ledger_no,5)  In ('18020','28010')) Then '18 - Intangible Asset'
    	When (Left(A.ledger_no,7) In ('2001010','2003010')) Then '19 - Call Accounts'
    	When (A.ledger_no In ('2005010001','2006010001','2000010001','2000010090','2006010090','2005010090')) Then '20 - Saving'
    	When (A.ledger_no In ('2000010092','2000010093','2000010002','2000010003','2005010092','2005010093','2006010092','2006010093','2000010005','2000010006','2000010095','2000010007','2006010007','2000010096','2000010097','2006010097', '2000010008','2006010008', '2000010098')) Then '21 - Super Saving'
 		When (A.ledger_no In ('2000010004','2000010094')) Then '22 - Thraa'
    	When (Left(A.ledger_no,7) In ('2001030','2003020','2003030','2000020','2005020','2006020','2005030','2005040','2006040')) Then '23 - Time Deposits'
    	When (Left(A.ledger_no,7) In('2101000','2100010','2200000','2306001','1904506')) Then '24 - Inter Bank Borrowings'
    	When (Left(A.ledger_no,7) In('2306000','1904500','2305901','1904508','2305902')) Then '25 - Other Borrowings'
    	When (Left(A.ledger_no,7) In('2306005','1904505')) Then '26 - EMTN'
    	When (Left(A.ledger_no,7) In ('2001000','2002000','2003000','2000000','2005000','2006000','2007000') Or Left(A.ledger_no,5) In ('29030')) Then '27 - Current'
    	When ((Left(A.ledger_no,3) In('290','299') Or Left(A.ledger_no,5)  In ('23040','23061','29900','23080') Or A.ledger_no In ('1900000010','1900000011','1900010055','2309510001','2309530001','2306501001','2306503001','2306200001','2306200002'))  And Left(A.ledger_no,5) Not In ('29030')) Then '28 - Other Liabilities'
    	When (Left(A.ledger_no,3) In('300')) Then '29 - Capital'
    	When (A.ledger_no ='3500000001') Then '30 - Legal Reserve'
    	When (A.ledger_no ='3200000001') Then '31 - Treasury Shares'
    	When (A.ledger_no In('3503000001')) Then '32 - Investment Fair Value Reserve'
   		When (A.ledger_no In('3504000001')) Then '33 - Cash Flow Hedge Rreserve'
    	When (Left(A.ledger_no,3) In('380')) Then '34 - Period End Profit/(Loss)'
    	When (Left(A.ledger_no,3) In('390') Or A.ledger_no In ('3950000002')) Then '35 - Retained Earnings (Accumalated Loss)'
    	When (A.ledger_no In('3502000001')) Then '36 - Risk Reserve'
    	When (A.ledger_no In('3950000001')) Then '37 - AT1 Sukuk'
    Else
    	'38 - '+ A.Ledger_no
    End					Sr_level_description,
	A.Acct_no 		GL_No,
    A.Description   GL_Name,
    A.Debit_Credit	DR_CR,
    A.iso_code      CCY,
    IsNull(Convert(Decimal(21,6),(Case When(Left(A.ledger_no,5) In ('19045','23000','23010','23020','28000','28010','28020','23050','23070','23055','23085') Or A.ledger_no  In ('1900000010','1900000011','1900010055','2309000001','2309010001','2309020001','2309030001','2309040001','2309060001') ) Then    
        cur_bal_Begin * -1
    Else
        cur_bal_Begin
    End ) / 1000),0) Balance,    
	IsNull(Convert(Decimal(21,6),(Case When(Left(A.ledger_no,5) In ('19045','23000','23010','23020','28000','28010','28020','23050','23070','23055','23085') Or A.ledger_no  In ('1900000010','1900000011','1900010055','2309000001','2309010001','2309020001','2309030001','2309040001','2309060001') ) Then    
        Equiv_cur_bal_Begin * -1
    Else
        Equiv_cur_bal_Begin
    End ) / 1000),0) Balance_QAR
Into #BS
From
    Bo..Tbl_GL_Daily_Bo A
Where
		1 = 1
    And	A.bdate 		= 	{?DBdate}
    And A.ledger_type 	In 	('Asset','Liability','Capital');
        
Select 
	Convert(Int,RTrim(LTrim(Substring(Sr_level_description,1,3)))) Sr, RTrim(LTrim(Substring(Sr_level_description,6,250))) BS_Description,  
	Sum(Balance_QAR) Balance_QAR 
Into #BS001
From #BS
Group By 
	Convert(Int,RTrim(LTrim(Substring(Sr_level_description,1,3)))), RTrim(LTrim(Substring(Sr_level_description,6,250))) 
Order By 1

Select 1 As No, 'ASSETS' Description, 0 As Balance
Union
Select 2 As No, 'Cash and balances with central banks' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (1,2,3)
Union 
Select 3 As No, 'Due from banks' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (5,6,8)
Union 
Select 4 As No, 'Financing assets' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (7)
Union 
Select 5 As No, 'Investment securities' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (4,9,10,11)
Union 
Select 6 As No, 'Investment in associates and joint ventures' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (12,13)
Union 
Select 7 As No, 'Investment property' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (14)
Union 
Select 8 As No, 'Fixed assets' Description, Sum(Balance_QAR) As Balance
From #BS001 
Where Sr In (16)
Union 
Select 9 As No, 'Intangible assets' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (18)
Union 
Select 10 As No, 'Other assets' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (15)
Union 
Select 11 As No, 'TOTAL ASSETS' Description, 0 As Balance
Union 
Select 12 As No, ' ' Description, 0 As Balance
Union 
Select 13 As No, 'LIABILITIES' Description, 0 As Balance
Union 
Select 14 As No, 'Due to banks' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (24,25)
Union 
Select 15 As No, 'EMTN Sukuk' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (26)
Union 
Select 16 As No, 'Customer current accounts' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (27)
Union 
Select 17 As No, 'Other liabilities' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (28)
Union 
Select 18 As No, 'TOTAL LIABILITIES ' Description, 0 As Balance
Union 
Select 19 As No, ' ' Description, 0 As Balance
Union 
Select 20 As No, 'Unrestricted investment accounts ' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (19,20,21,22,23)
Union 
Select 21 As No, ' ' Description, 0 As Balance
Union 
Select 22 As No, 'OWNERS’ EQUITY ' Description, 0 As Balance
Union 
Select 23 As No, 'Share capital' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (29)
Union 
Select 24 As No, 'Legal reserve' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (30)
Union 
Select 25 As No, 'Treasury reserve' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (31)
Union 
Select 26 As No, 'Risk reserve' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (36)
Union 
Select 27 As No, 'General reserve' Description, 0 As Balance
Union 
Select 28 As No, 'Fair value reserves (incl CFH reserve)' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (32,33)
Union 
Select 29 As No, 'Retained earnings' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (34,35)
Union 
Select 30 As No, 'TOTAL EQUITY ATTRIBUTABLE TO EQUITY HOLDERS OF THE BANK' Description, 0 As Balance
Union 
Select 31 As No, 'AT-1 Issuance' Description, Sum(Balance_QAR) As Balance
From #BS001
Where Sr In (37)
Union 
Select 32 As No, 'Non-controlling interests' Description, 0 As Balance
Union 
Select 33 As No, 'TOTAL OWNERS EQUITY' Description, 0 As Balance
Union 
Select 34 As No, ' ' Description, 0 As Balance
Union 
Select 35 As No, 'TOTAL LIABILITIES, URIA and Equity' Description, 0 As Balance
Union 
Select 36 As No, ' ' Description, 0 As Balance
Union 
Select 37 As No, 'Total Deposits' Description, 0 As Balance
Order By No

Drop Table #BS
Drop Table #BS001


