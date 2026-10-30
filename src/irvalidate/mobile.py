"""شماره موبایل ایران."""
from __future__ import annotations

import re
from typing import Optional

from ._digits import clean

_RE = re.compile(r"^(?:\+98|0098|98|0)?(9\d{9})$")

# پیش‌شماره‌های شناخته‌شده (بر اساس تخصیص عمومی؛ ممکن است ناقص باشد)
_OPERATOR_PREFIXES = {
    "MCI": ["091" + str(i) for i in range(10)] + ["0990", "0991", "0992", "0993", "0994"],
    "Irancell": ["0930", "0933", "0935", "0936", "0937", "0938", "0939", "0941"]
    + ["090" + str(i) for i in range(6)],
    "Rightel": ["0920", "0921", "0922"],
    "Taliya": ["0932"],
    "Shatel Mobile": ["0998"],
    "Aptel": ["0999"],
}
_PREFIX_TO_OPERATOR = {p: op for op, prefixes in _OPERATOR_PREFIXES.items() for p in prefixes}


def normalize_mobile(value: object, international: bool = False) -> Optional[str]:
    """Normalize to ``09xxxxxxxxx`` (or ``+989xxxxxxxxx`` if ``international``).

    Accepts: 09121234567, 9121234567, 989121234567, +989121234567,
    00989121234567 و ارقام فارسی. Returns None if not a valid mobile format.
    """
    s = clean(value)
    if s is None:
        return None
    m = _RE.match(s)
    if not m:
        return None
    local = m.group(1)
    return f"+98{local}" if international else f"0{local}"


def is_valid_mobile(value: object) -> bool:
    """Check that ``value`` is a well-formed Iranian mobile number."""
    return normalize_mobile(value) is not None


def mobile_operator(value: object) -> Optional[str]:
    """Return the operator name (MCI, Irancell, Rightel, ...) or None if unknown."""
    n = normalize_mobile(value)
    if n is None:
        return None
    return _PREFIX_TO_OPERATOR.get(n[:4])
