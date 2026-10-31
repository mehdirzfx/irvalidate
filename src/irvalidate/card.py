"""شماره کارت بانکی ۱۶ رقمی."""
from __future__ import annotations

from typing import Optional

from ._result import ValidationResult, fail, success
from ._validate import prepare_digits
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


def luhn_check_digit(payload: str) -> str:
    """Luhn check digit to append to ``payload`` (the card number without its last digit)."""
    total = 0
    for i, ch in enumerate(reversed(payload)):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return str((10 - total % 10) % 10)


def validate_card_number(value: object) -> ValidationResult:
    """Validate a 16-digit card number (Luhn) and say why it failed, if so."""
    s, err = prepare_digits(value, "card", 16)
    if err or s is None:
        return err  # type: ignore[return-value]
    if len(set(s)) == 1:
        return fail("all_same_digits", "card")
    if not _luhn(s):
        return fail("bad_checksum", "card")
    return success(s)


def normalize_card_number(value: object) -> Optional[str]:
    """Return the 16-digit card number (English digits) or None if malformed.

    فقط ساختار را بررسی می‌کند، نه رقم کنترلی.
    """
    s, _ = prepare_digits(value, "card", 16)
    return s


def is_valid_card_number(value: object) -> bool:
    """Return True if ``value`` is a valid 16-digit card number."""
    return validate_card_number(value).ok


def card_bank(value: object) -> Optional[Bank]:
    """Return the issuing bank of a valid card number, or None if unknown/invalid."""
    res = validate_card_number(value)
    if not res.ok or res.value is None:
        return None
    return CARD_BINS.get(res.value[:6])


def format_card_number(value: object, sep: str = "-") -> Optional[str]:
    """6037991234567890 -> 6037-9912-3456-7890"""
    s = normalize_card_number(value)
    if s is None:
        return None
    return sep.join(s[i : i + 4] for i in range(0, 16, 4))


def mask_card_number(
    value: object,
    mask_char: str = "*",
    sep: str = "-",
    keep_first: int = 6,
    keep_last: int = 4,
) -> Optional[str]:
    """6037991000000004 -> 6037-99**-****-0004 (None if malformed)."""
    s = normalize_card_number(value)
    if s is None:
        return None
    hidden = 16 - keep_first - keep_last
    if hidden < 0:
        raise ValueError("keep_first + keep_last must not exceed 16")
    masked = s[:keep_first] + mask_char * hidden + s[16 - keep_last :]
    return sep.join(masked[i : i + 4] for i in range(0, 16, 4))
