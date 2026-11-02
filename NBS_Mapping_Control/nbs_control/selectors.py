"""Structured selectors and component expressions.

Selectors are JSON data validated against the configured field dictionary and
compiled into closures. Free text from workbooks is never executed: there is no
eval, SQL, shell or macro path. The legacy-text parser below only drafts a
*proposal* for owner review from a few narrow CATEGORY patterns.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import Any, Callable

OPS = ("in", "not_in", "eq", "range", "prefix_in")
MAX_DEPTH = 6
NAME = re.compile(r"[A-Z][A-Z0-9_]*\Z")
TERM = re.compile(r"\s*([+-])?\s*(?:(\d+(?:\.\d+)?)\s*\*\s*)?([A-Z][A-Z0-9_]*)\s*")


class SelectorError(ValueError):
    """A selector is not valid structured data."""


def _code(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise SelectorError("Selector values must be text or integer codes")
    token = str(value).strip()
    if not token:
        raise SelectorError("Selector values cannot be empty")
    return token


def validate_selector(selector: Any, fields: dict[str, Any], require_approved: bool = True,
                      depth: int = 0, used: set[str] | None = None) -> set[str]:
    """Validate structure and field references; return the set of fields used."""
    used = set() if used is None else used
    if depth > MAX_DEPTH:
        raise SelectorError("Selector nesting is too deep")
    if not isinstance(selector, dict) or len(selector) == 0:
        raise SelectorError("Selector must be a nonempty object")
    if "all" in selector or "any" in selector:
        key = "all" if "all" in selector else "any"
        if set(selector) != {key} or not isinstance(selector[key], list) or not selector[key]:
            raise SelectorError(f"'{key}' must be the only key and hold a nonempty list")
        for child in selector[key]:
            validate_selector(child, fields, require_approved, depth + 1, used)
        return used
    if "not" in selector:
        if set(selector) != {"not"}:
            raise SelectorError("'not' must be the only key")
        return validate_selector(selector["not"], fields, require_approved, depth + 1, used)
    field, op = selector.get("field"), selector.get("op")
    if field not in fields:
        raise SelectorError(f"Unknown selector field: {field}")
    spec = fields[field]
    if spec.get("system") != "T24":
        raise SelectorError(f"Legacy field {field} cannot be used in an executable selector")
    if require_approved and spec.get("status") != "APPROVED":
        raise SelectorError(f"Selector field {field} is not owner-approved")
    if op not in OPS:
        raise SelectorError(f"Unsupported selector operator: {op}")
    allowed = {"field", "op"}
    if op == "range":
        allowed |= {"min", "max"}
        if spec.get("value_type") != "integer_code":
            raise SelectorError(f"range requires an integer_code field, not {field}")
        lo, hi = selector.get("min"), selector.get("max")
        if not all(isinstance(v, int) and not isinstance(v, bool) for v in (lo, hi)) or lo > hi:
            raise SelectorError("range needs integer min <= max")
    elif op == "eq":
        allowed |= {"value"}
        _code(selector.get("value"))
    else:
        allowed |= {"values"}
        values = selector.get("values")
        if not isinstance(values, list) or not values:
            raise SelectorError(f"{op} needs a nonempty values list")
        normalized = [_code(v) for v in values]
        if len(set(normalized)) != len(normalized):
            raise SelectorError(f"{op} has duplicate values")
    extra = set(selector) - allowed
    if extra:
        raise SelectorError(f"Unexpected selector keys: {sorted(extra)}")
    used.add(field)
    return used


def compile_selector(selector: dict[str, Any], fields: dict[str, Any],
                     require_approved: bool = True) -> Callable[[dict[str, Any]], bool | None]:
    """Compile a validated selector. The predicate returns None when a field is absent."""
    validate_selector(selector, fields, require_approved)
    return _compile(selector, fields)


def _compile(selector: dict[str, Any], fields: dict[str, Any]) -> Callable[[dict[str, Any]], bool | None]:
    if "all" in selector or "any" in selector:
        children = [_compile(c, fields) for c in selector.get("all", selector.get("any"))]
        want_all = "all" in selector

        def combine(attrs: dict[str, Any]) -> bool | None:
            results = [child(attrs) for child in children]
            if want_all:
                if any(r is False for r in results):
                    return False
                return None if any(r is None for r in results) else True
            if any(r is True for r in results):
                return True
            return None if any(r is None for r in results) else False
        return combine
    if "not" in selector:
        inner = _compile(selector["not"], fields)

        def negate(attrs: dict[str, Any]) -> bool | None:
            result = inner(attrs)
            return None if result is None else not result
        return negate
    field, op = selector["field"], selector["op"]

    def test(attrs: dict[str, Any]) -> bool | None:
        raw = attrs.get(field)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            return None
        value = _code(raw)
        if op == "range":
            if not value.isdigit():
                return None
            return selector["min"] <= int(value) <= selector["max"]
        if op == "eq":
            return value == _code(selector["value"])
        values = [_code(v) for v in selector["values"]]
        if op == "in":
            return value in values
        if op == "not_in":
            return value not in values
        return any(value.startswith(prefix) for prefix in values)
    return test


def parse_expression(text: str) -> list[tuple[Decimal, str]]:
    """Parse 'A + B - 2*C' into signed coefficients. Names only; no evaluation."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Component expression is empty")
    terms: list[tuple[Decimal, str]] = []
    position = 0
    while position < len(text):
        match = TERM.match(text, position)
        if not match or match.end() == position:
            raise ValueError(f"Invalid component expression near: {text[position:position + 20]!r}")
        sign, coefficient, name = match.groups()
        if terms and sign is None:
            raise ValueError("Terms must be separated by + or -")
        value = Decimal(coefficient) if coefficient else Decimal(1)
        if sign == "-":
            value = -value
        if any(existing == name for _, existing in terms):
            raise ValueError(f"Metric {name} repeated in expression")
        terms.append((value, name))
        position = match.end()
    return terms


def format_expression(terms: list[tuple[Decimal, str]]) -> str:
    text = ""
    for index, (coefficient, name) in enumerate(terms):
        magnitude = abs(coefficient)
        body = name if magnitude == 1 else f"{magnitude}*{name}"
        if index == 0:
            text = f"-{body}" if coefficient < 0 else body
        else:
            text += f" {'-' if coefficient < 0 else '+'} {body}"
    return text


_CATEGORY_LIST = re.compile(r"^\s*CATEGORY\s*=\s*((?:\d+\s*,\s*)*\d+)\s*(?:[>&]|$)", re.I)
_CATEGORY_RANGE_EXCL = re.compile(
    r"^\s*CATEGORY\s*=\s*(\d+)\s*-\s*(\d+)\s+BUT\s+NOT\s+EQUAL\s+TO\s+CATEGORY\s+((?:\d+\s*,\s*)*\d+)", re.I)


def draft_category_selector(text: str) -> dict[str, Any] | None:
    """Draft a CATEGORY selector from two narrow legacy patterns, for owner review only.

    Anything that does not match exactly returns None (the owner must supply a
    structured selector). The draft is never executed until approved.
    """
    if not isinstance(text, str):
        return None
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    match = _CATEGORY_RANGE_EXCL.match(first_line)
    if match:
        lo, hi, excluded = int(match.group(1)), int(match.group(2)), match.group(3)
        if lo > hi:
            return None
        return {"all": [
            {"field": "T24.CATEGORY", "op": "range", "min": lo, "max": hi},
            {"field": "T24.CATEGORY", "op": "not_in", "values": [v.strip() for v in excluded.split(",")]},
        ]}
    match = _CATEGORY_LIST.match(first_line)
    if match:
        values = [v.strip() for v in match.group(1).split(",")]
        if len(set(values)) != len(values):
            return None
        return {"field": "T24.CATEGORY", "op": "in", "values": values}
    return None
