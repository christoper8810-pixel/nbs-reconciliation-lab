"""Monetary precision policy for the rebuild model.

Raw source amounts are preserved verbatim as text. Monetary arithmetic uses Decimal and is
stored as scaled integers of 10**-6 currency units ("micro"), quantized ROUND_HALF_EVEN at
normalization. Display rounding (for example QAR thousands, 0 dp) happens only when a value
is compared with a display-rounded reference; accounting controls use the pre-round values.
Legacy ECB/loan/deposit facts were stored as binary floats in data/bank_20260930.sqlite; they
are converted through their shortest repr, which is disclosed as a legacy precision limit.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext

SCALE_DIGITS = 6
SCALE = 10 ** SCALE_DIGITS
QUANTUM = Decimal(1).scaleb(-SCALE_DIGITS)
POLICY = {
    'storage': 'scaled integer, 1e-6 currency units',
    'rounding': 'ROUND_HALF_EVEN at normalization; display rounding only at comparison',
    'raw': 'original OOXML numeric text retained verbatim',
    'legacy_float_sources': 'ECB/LOAN/DEPOSIT/TB from bank_20260930.sqlite converted via repr(float); binary-float origin disclosed',
}


class MoneyError(ValueError):
    pass


def parse_decimal(text) -> Decimal | None:
    """Parse a raw amount. Blank -> None (missing, never zero). Non-finite -> error."""
    if text is None:
        return None
    if isinstance(text, float):
        text = repr(text)
    s = str(text).strip().replace(',', '')
    if s == '':
        return None
    try:
        d = Decimal(s)
    except InvalidOperation as exc:
        raise MoneyError(f'Amount is not numeric: {text!r}') from exc
    if not d.is_finite():
        raise MoneyError(f'Amount is not finite: {text!r}')
    return d


def to_micro(value) -> int | None:
    d = value if isinstance(value, Decimal) else parse_decimal(value)
    if d is None:
        return None
    with localcontext() as ctx:
        ctx.prec = 60
        return int((d * SCALE).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def from_micro(micro: int | None) -> Decimal | None:
    if micro is None:
        return None
    return (Decimal(micro) / SCALE).quantize(QUANTUM)


def scale_display(micro: int | None, divisor: int = 1000) -> Decimal | None:
    """Pre-round value in display units (e.g. QAR thousands), still unrounded."""
    if micro is None:
        return None
    with localcontext() as ctx:
        ctx.prec = 60
        return Decimal(micro) / (SCALE * divisor)


def round_display(value: Decimal | None, places: int = 0) -> Decimal | None:
    if value is None:
        return None
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)


def text(micro: int | None) -> str | None:
    d = from_micro(micro)
    return None if d is None else format(d, 'f')
