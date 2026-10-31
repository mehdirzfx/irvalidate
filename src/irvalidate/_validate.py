"""Shared pre-checks for digit-only identifiers."""
from __future__ import annotations

from typing import Optional, Tuple

from ._digits import clean, is_ascii_digits
from ._result import ValidationResult, fail


def prepare_digits(
    value: object, kind: str, length: int
) -> Tuple[Optional[str], Optional[ValidationResult]]:
    """Return ``(digits, None)`` on success or ``(None, failure)``."""
    if not isinstance(value, str):
        return None, fail("not_a_string", kind)
    s = clean(value) or ""
    if not s:
        return None, fail("empty", kind)
    if not is_ascii_digits(s):
        return None, fail("invalid_characters", kind)
    if len(s) != length:
        return None, fail("invalid_length", kind, n=length)
    return s, None
