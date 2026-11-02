"""کد ملی (۱۰ رقمی حقیقی) و شناسه ملی (۱۱ رقمی حقوقی)."""

from __future__ import annotations

from ._result import ValidationResult, fail, success
from ._validate import prepare_digits

_LEGAL_COEFFS = (29, 27, 23, 19, 17, 29, 27, 23, 19, 17)


def national_id_check_digit(first9: str) -> str:
    """Check digit for the first 9 digits of a national ID."""
    total = sum(int(first9[i]) * (10 - i) for i in range(9))
    r = total % 11
    return str(r if r < 2 else 11 - r)


def legal_id_check_digit(first10: str) -> str:
    """Check digit for the first 10 digits of a legal ID."""
    d = int(first10[9]) + 2
    total = sum((int(first10[i]) + d) * _LEGAL_COEFFS[i] for i in range(10))
    r = total % 11
    return str(0 if r == 10 else r)


def validate_national_id(value: object) -> ValidationResult:
    """Validate a 10-digit national ID (کد ملی) and say why it failed, if so.

    ورودی باید رشته باشد (نه عدد) تا صفرهای ابتدایی از بین نرود.
    """
    s = prepare_digits(value, "national_id", 10)
    if isinstance(s, ValidationResult):
        return s
    if len(set(s)) == 1:  # 0000000000, 1111111111, ...
        return fail("all_same_digits", "national_id")
    if s[9] != national_id_check_digit(s[:9]):
        return fail("bad_checksum", "national_id")
    return success(s)


def validate_legal_id(value: object) -> ValidationResult:
    """Validate an 11-digit legal entity ID (شناسه ملی اشخاص حقوقی)."""
    s = prepare_digits(value, "legal_id", 11)
    if isinstance(s, ValidationResult):
        return s
    if len(set(s)) == 1:
        return fail("all_same_digits", "legal_id")
    if s[10] != legal_id_check_digit(s[:10]):
        return fail("bad_checksum", "legal_id")
    return success(s)


def is_valid_national_id(value: object) -> bool:
    """Return True if ``value`` is a valid 10-digit national ID."""
    return validate_national_id(value).ok


def is_valid_legal_id(value: object) -> bool:
    """Return True if ``value`` is a valid 11-digit legal ID."""
    return validate_legal_id(value).ok
