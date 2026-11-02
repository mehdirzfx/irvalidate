"""Shared pre-checks for digit-only identifiers."""

from __future__ import annotations

from ._digits import clean, is_ascii_digits
from ._result import ValidationResult, fail


def prepare_digits(value: object, kind: str, length: int) -> str | ValidationResult:
    """Return the cleaned digit string, or a failed :class:`ValidationResult`."""
    if not isinstance(value, str):
        return fail("not_a_string", kind)
    s = clean(value) or ""
    if not s:
        return fail("empty", kind)
    if not is_ascii_digits(s):
        return fail("invalid_characters", kind)
    if len(s) != length:
        return fail("invalid_length", kind, n=length)
    return s
