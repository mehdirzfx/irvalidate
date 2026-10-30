"""شماره کارت بانکی ۱۶ رقمی."""
from __future__ import annotations

import re
from typing import Optional

from ._digits import clean
from .banks import CARD_BINS, Bank


def _luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def normalize_card_number(value: object) -> Optional[str]:
    """Return the 16-digit card number (English digits) or None if malformed."""
    s = clean(value)
    if s is None or not re.fullmatch(r"\d{16}", s):
        return None
    return s


def is_valid_card_number(value: object) -> bool:
    """Validate a 16-digit card number using the Luhn checksum."""
    s = normalize_card_number(value)
    return s is not None and len(set(s)) > 1 and _luhn(s)


def card_bank(value: object) -> Optional[Bank]:
    """Return the issuing bank of a valid card number, or None if unknown/invalid."""
    s = normalize_card_number(value)
    if s is None or not _luhn(s):
        return None
    return CARD_BINS.get(s[:6])


def format_card_number(value: object, sep: str = "-") -> Optional[str]:
    """6037991234567890 -> 6037-9912-3456-7890"""
    s = normalize_card_number(value)
    if s is None:
        return None
    return sep.join(s[i : i + 4] for i in range(0, 16, 4))
