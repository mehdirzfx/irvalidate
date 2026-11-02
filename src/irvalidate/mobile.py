"""شماره موبایل ایران."""

from __future__ import annotations

import re

from ._digits import clean, is_ascii_digits
from ._result import ValidationResult, fail, success

_RE = re.compile(r"^(?:\+98|0098|98|0)?(9[0-9]{9})$")

# پیش‌شماره‌های شناخته‌شده (بر اساس تخصیص عمومی؛ ممکن است ناقص باشد)
OPERATOR_PREFIXES: dict[str, list[str]] = {
    "MCI": ["091" + str(i) for i in range(10)] + ["0990", "0991", "0992", "0993", "0994", "0996"],
    "Irancell": ["0930", "0933", "0935", "0936", "0937", "0938", "0939", "0941"]
    + ["090" + str(i) for i in range(6)],
    "Rightel": ["0920", "0921", "0922"],
    "Taliya": ["0932"],
    "Shatel Mobile": ["0998"],
    "MVNO": ["0999"],  # اپراتورهای مجازی (چند اپراتور با پیش‌شماره‌ی ۰۹۹۹)
}
_PREFIX_TO_OPERATOR = {p: op for op, prefixes in OPERATOR_PREFIXES.items() for p in prefixes}


def validate_mobile(value: object) -> ValidationResult:
    """Validate an Iranian mobile number and say why it failed, if so.

    Accepts 09121234567, 9121234567, 989121234567, +989121234567,
    00989121234567 و ارقام فارسی. مقدار نرمال‌شده: ``09121234567``.
    """
    if not isinstance(value, str):
        return fail("not_a_string", "mobile")
    s = clean(value) or ""
    if not s:
        return fail("empty", "mobile")
    body = s[1:] if s.startswith("+") else s
    if not is_ascii_digits(body):
        return fail("invalid_characters", "mobile")
    m = _RE.match(s)
    if not m:
        return fail("invalid_format", "mobile")
    return success("0" + m.group(1))


def normalize_mobile(value: object, international: bool = False) -> str | None:
    """Normalize to ``09xxxxxxxxx`` (or ``+989xxxxxxxxx`` if ``international``)."""
    res = validate_mobile(value)
    if not res.ok or res.value is None:
        return None
    return "+98" + res.value[1:] if international else res.value


def is_valid_mobile(value: object) -> bool:
    """Check that ``value`` is a well-formed Iranian mobile number."""
    return validate_mobile(value).ok


def mobile_operator(value: object) -> str | None:
    """Return the operator name (MCI, Irancell, Rightel, ...) or None if unknown."""
    n = normalize_mobile(value)
    if n is None:
        return None
    return _PREFIX_TO_OPERATOR.get(n[:4])


def format_mobile(value: object, sep: str = " ") -> str | None:
    """09123456789 -> '0912 345 6789' (None if malformed)."""
    n = normalize_mobile(value)
    if n is None:
        return None
    return sep.join((n[:4], n[4:7], n[7:]))
