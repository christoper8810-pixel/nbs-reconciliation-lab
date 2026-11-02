"""Semantic maturity buckets, independent of any worksheet column letters.

States are distinct: NO_MATURITY (evidenced open-ended product), MISSING (no contractual date),
OVERDUE (date before the report date) and the explicit future bands. Only NO_MATURITY and the
future bands are reported in bucket columns; OVERDUE and MISSING stay visible exceptions.

The actual Ethix boundary logic has not been supplied, so the convention is a named,
configurable provisional choice: CALENDAR (add calendar months/years to the report date) or
DAY_COUNT (fixed day counts). Upper boundaries are inclusive; the report date itself is in 1W.
"""
from __future__ import annotations
import calendar
from datetime import date, timedelta

LOAN_BANDS = ('MAT_1W', 'MAT_1M', 'MAT_3M', 'MAT_6M', 'MAT_12M', 'MAT_2Y', 'MAT_5Y', 'MAT_10Y', 'MAT_20Y', 'MAT_GT20Y')
DEPOSIT_BANDS = ('MAT_1W', 'MAT_1M', 'MAT_3M', 'MAT_6M', 'MAT_12M', 'MAT_2Y', 'MAT_GT2Y')
LIMITS = {'MAT_1W': ('d', 7), 'MAT_1M': ('m', 1), 'MAT_3M': ('m', 3), 'MAT_6M': ('m', 6), 'MAT_12M': ('m', 12),
          'MAT_2Y': ('m', 24), 'MAT_5Y': ('m', 60), 'MAT_10Y': ('m', 120), 'MAT_20Y': ('m', 240)}
DAY_COUNTS = {'MAT_1W': 7, 'MAT_1M': 30, 'MAT_3M': 90, 'MAT_6M': 180, 'MAT_12M': 365, 'MAT_2Y': 730,
              'MAT_5Y': 1825, 'MAT_10Y': 3650, 'MAT_20Y': 7300}
CONVENTIONS = ('CALENDAR', 'CALENDAR_EOM', 'DAY_COUNT')

# Existing live template, Table 10 header row 769 (validated against the workbook text in tests).
TEMPLATE_T10 = {'MAT_NONE': 'B', 'MAT_1W': 'C', 'MAT_1M': 'D', 'MAT_3M': 'E', 'MAT_6M': 'F', 'MAT_12M': 'G',
                'MAT_2Y': 'H', 'MAT_5Y': 'I', 'MAT_10Y': 'J', 'MAT_20Y': 'K', 'MAT_GT20Y': 'L', 'TOTAL': 'M'}
TEMPLATE_T10_HEADERS = {'B': 'Without Maturity', 'C': '>1 Week', 'D': '>1 Week To1 Month', 'E': '>1 to3 Months',
                        'F': '>3 To6 Months', 'G': '>6 To 12 Months', 'H': '>1 Year To 2 Years', 'I': '>2 Year To 5 Years',
                        'J': '>5 Years To 10 Years', 'K': '>10 Years to 20 Years', 'L': '>20 Years', 'M': 'Total Amount'}
# Table 24 (row 1240): current/call, saving, then time-deposit bands D..J and total K.
TEMPLATE_T24 = {'DEP_CURRENT_CALL': 'B', 'DEP_SAVING': 'C', 'MAT_1W': 'D', 'MAT_1M': 'E', 'MAT_3M': 'F', 'MAT_6M': 'G',
                'MAT_12M': 'H', 'MAT_2Y': 'I', 'MAT_GT2Y': 'J', 'TOTAL': 'K'}


def add_months(d: date, months: int) -> date:
    y, m = divmod(d.month - 1 + months, 12)
    y += d.year
    m += 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def is_month_end(d: date) -> bool:
    return d.day == calendar.monthrange(d.year, d.month)[1]


def limit(report: date, band: str, convention: str) -> date:
    """CALENDAR adds calendar months (day clamped); CALENDAR_EOM keeps month-end to month-end
    (30 Sep + 3 months = 31 Dec); DAY_COUNT uses fixed day counts."""
    if convention == 'DAY_COUNT':
        return report + timedelta(days=DAY_COUNTS[band])
    unit, n = LIMITS[band]
    if unit == 'd':
        return report + timedelta(days=n)
    d = add_months(report, n)
    if convention == 'CALENDAR_EOM' and is_month_end(report):
        d = date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])
    return d


def bucket(maturity: str | date | None, report: str | date, bands=LOAN_BANDS, convention='CALENDAR', open_ended=False) -> str:
    if convention not in CONVENTIONS:
        raise ValueError('Unknown maturity convention')
    report = date.fromisoformat(report) if isinstance(report, str) else report
    if maturity in (None, ''):
        return 'MAT_NONE' if open_ended else 'MISSING'
    d = date.fromisoformat(str(maturity)[:10]) if not isinstance(maturity, date) else maturity
    if d < report:
        return 'OVERDUE'
    for band in bands[:-1]:
        if d <= limit(report, band, convention):
            return band
    return bands[-1]
