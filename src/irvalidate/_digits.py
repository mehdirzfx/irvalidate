"""Digit normalization helpers (Persian / Arabic-Indic <-> ASCII)."""
from __future__ import annotations

from typing import Optional

_TO_ENGLISH = str.maketrans(
    {
        **{chr(0x06F0 + i): str(i) for i in range(10)},  # ۰-۹
        **{chr(0x0660 + i): str(i) for i in range(10)},  # ٠-٩
    }
)
_TO_PERSIAN = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

# فاصله، خط تیره، نیم‌فاصله، علامت‌های جهت، پرانتز و ...
_SEPARATORS = dict.fromkeys(map(ord, " -_()\u200c\u200d\u200e\u200f\u00a0\t\n"))


def to_english_digits(text: str) -> str:
    """Convert Persian/Arabic digits in ``text`` to English digits."""
    return text.translate(_TO_ENGLISH)


def to_persian_digits(text: str) -> str:
    """Convert English/Arabic digits in ``text`` to Persian digits (۰-۹)."""
    return to_english_digits(text).translate(_TO_PERSIAN)


def clean(value: object) -> Optional[str]:
    """Return ``value`` with English digits and no separators, or None if not a str."""
    if not isinstance(value, str):
        return None
    return to_english_digits(value).translate(_SEPARATORS)


def is_ascii_digits(s: str) -> bool:
    """True only for non-empty strings made of 0-9 (not other Unicode digits)."""
    return s.isascii() and s.isdigit()
