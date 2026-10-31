"""شماره شبا (IBAN ایران): IR + ۲ رقم کنترلی + ۲۲ رقم."""
from __future__ import annotations

from typing import Optional, Tuple

from ._digits import clean, is_ascii_digits
from ._result import ValidationResult, fail, success
from .banks import SHEBA_CODES, Bank


def _split(value: object) -> Tuple[Optional[str], Optional[ValidationResult]]:
    """Return the 24 digits after ``IR`` (shape-checked only) or a failure."""
    if not isinstance(value, str):
        return None, fail("not_a_string", "sheba")
    s = (clean(value) or "").upper()
    if not s:
        return None, fail("empty", "sheba")
    if s.startswith("IR"):
        s = s[2:]
    if not is_ascii_digits(s):
        return None, fail("invalid_characters", "sheba")
    if len(s) != 24:
        return None, fail(
            "invalid_length",
            "sheba",
            n=24,
            label_fa="ارقام شبا (بعد از IR)",
            label_en="Sheba digits (after IR)",
        )
    return s, None


def validate_sheba(value: object) -> ValidationResult:
    """Validate an Iranian IBAN (ISO 7064 mod-97) and say why it failed, if so.

    پیشوند IR اختیاری است. مقدار نرمال‌شده به شکل ``IR`` + ۲۴ رقم است.
    """
    digits, err = _split(value)
    if err or digits is None:
        return err  # type: ignore[return-value]
    if int(digits[2:] + "1827" + digits[:2]) % 97 != 1:  # I=18, R=27
        return fail("bad_checksum", "sheba")
    return success("IR" + digits)


def normalize_sheba(value: object) -> Optional[str]:
    """Return ``IR`` + 24 digits, or None if the shape is wrong (checksum not checked)."""
    digits, _ = _split(value)
    return None if digits is None else "IR" + digits


def is_valid_sheba(value: object) -> bool:
    """Return True if ``value`` is a valid Sheba number."""
    return validate_sheba(value).ok


def sheba_bank(value: object) -> Optional[Bank]:
    """Return the bank of a valid Sheba number, or None if unknown/invalid."""
    res = validate_sheba(value)
    if not res.ok or res.value is None:
        return None
    return SHEBA_CODES.get(res.value[4:7])


def format_sheba(value: object) -> Optional[str]:
    """IR580540105180021273113007 -> 'IR58 0540 1051 8002 1273 1130 07' (None if malformed)."""
    s = normalize_sheba(value)
    if s is None:
        return None
    return " ".join(s[i : i + 4] for i in range(0, len(s), 4))
