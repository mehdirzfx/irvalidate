"""کد پستی ۱۰ رقمی."""

from __future__ import annotations

from ._result import ValidationResult, fail, success
from ._validate import prepare_digits


def validate_postal_code(value: object) -> ValidationResult:
    """Validate the format of a 10-digit postal code (کد پستی).

    فقط قواعد مستند بررسی می‌شود: ۱۰ رقم؛ ارقام ۰ و ۲ در ۵ رقم اول (کد رهسپاری)
    به‌کار نمی‌روند؛ همه‌ی ارقام یکسان نباشند. وجود واقعی آدرس بررسی نمی‌شود.
    """
    s = prepare_digits(value, "postal_code", 10)
    if isinstance(s, ValidationResult):
        return s
    if len(set(s)) == 1:
        return fail("all_same_digits", "postal_code")
    if "0" in s[:5] or "2" in s[:5]:
        return fail("invalid_format", "postal_code")
    return success(s)


def is_valid_postal_code(value: object) -> bool:
    """Return True if ``value`` has the shape of a valid postal code."""
    return validate_postal_code(value).ok
