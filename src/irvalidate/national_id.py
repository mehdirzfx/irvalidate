"""کد ملی (۱۰ رقمی حقیقی) و شناسه ملی (۱۱ رقمی حقوقی)."""
from __future__ import annotations

import re

from ._digits import clean

_LEGAL_COEFFS = (29, 27, 23, 19, 17, 29, 27, 23, 19, 17)


def is_valid_national_id(value: object) -> bool:
    """Validate a 10-digit Iranian national ID (کد ملی).

    ورودی باید رشته باشد (نه عدد) تا صفرهای ابتدایی از بین نرود.
    """
    s = clean(value)
    if s is None or not re.fullmatch(r"\d{10}", s):
        return False
    if len(set(s)) == 1:  # 0000000000, 1111111111, ...
        return False
    total = sum(int(s[i]) * (10 - i) for i in range(9))
    r = total % 11
    check = int(s[9])
    return check == r if r < 2 else check == 11 - r


def is_valid_legal_id(value: object) -> bool:
    """Validate an 11-digit Iranian legal entity ID (شناسه ملی اشخاص حقوقی)."""
    s = clean(value)
    if s is None or not re.fullmatch(r"\d{11}", s):
        return False
    if len(set(s)) == 1:
        return False
    d = int(s[9]) + 2
    total = sum((int(s[i]) + d) * _LEGAL_COEFFS[i] for i in range(10))
    r = total % 11
    if r == 10:
        r = 0
    return r == int(s[10])
