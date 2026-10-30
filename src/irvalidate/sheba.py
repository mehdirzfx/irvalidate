"""شماره شبا (IBAN ایران): IR + ۲ رقم کنترلی + ۲۲ رقم."""
from __future__ import annotations

import re
from typing import Optional

from ._digits import clean
from .banks import SHEBA_CODES, Bank


def normalize_sheba(value: object) -> Optional[str]:
    """Return the canonical ``IR`` + 24 digits form, or None if malformed.

    پیشوند IR اختیاری است (``IR58...`` و ``58...`` هر دو پذیرفته می‌شوند).
    """
    s = clean(value)
    if s is None:
        return None
    s = s.upper()
    if re.fullmatch(r"\d{24}", s):
        s = "IR" + s
    if not re.fullmatch(r"IR\d{24}", s):
        return None
    return s


def is_valid_sheba(value: object) -> bool:
    """Validate an Iranian IBAN using the ISO 7064 mod-97 check."""
    s = normalize_sheba(value)
    if s is None:
        return False
    rearranged = s[4:] + "1827" + s[2:4]  # I=18, R=27
    return int(rearranged) % 97 == 1


def sheba_bank(value: object) -> Optional[Bank]:
    """Return the bank of a valid Sheba number, or None if unknown/invalid."""
    s = normalize_sheba(value)
    if s is None or not is_valid_sheba(s):
        return None
    return SHEBA_CODES.get(s[4:7])
