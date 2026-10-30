"""Digit normalization helpers (Persian / Arabic-Indic -> ASCII)."""
from __future__ import annotations

from typing import Optional

_TABLE = str.maketrans(
    {
        **{chr(0x06F0 + i): str(i) for i in range(10)},  # ۰-۹
        **{chr(0x0660 + i): str(i) for i in range(10)},  # ٠-٩
    }
)

# فاصله، خط تیره، نیم‌فاصله، علامت‌های جهت، پرانتز و ...
_SEPARATORS = dict.fromkeys(map(ord, " -_()\u200c\u200d\u200e\u200f\u00a0\t\n"))


def to_english_digits(text: str) -> str:
    """Convert Persian/Arabic digits in ``text`` to English digits."""
    return text.translate(_TABLE)


def clean(value: object) -> Optional[str]:
    """Return ``value`` with English digits and no separators, or None if not a str."""
    if not isinstance(value, str):
        return None
    return to_english_digits(value).translate(_SEPARATORS)
