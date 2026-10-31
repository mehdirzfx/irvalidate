"""تولید داده‌ی تستی معتبر (فقط برای تست و داده‌ی فیک).

مقادیر تولیدشده از نظر ساختار و رقم کنترلی معتبرند، ولی ممکن است تصادفاً با
مقدار واقعیِ شخصی یکی باشند. هرگز برای جعل هویت یا کارهای مشابه استفاده نکنید.
تولیدکننده‌ی تصادفیِ پیش‌فرض برای امنیت مناسب نیست؛ برای نتیجه‌ی تکرارپذیر
یک ``random.Random(seed)`` به پارامتر ``rng`` بدهید.
"""
from __future__ import annotations

import random
from typing import Any, Optional, Union

from .banks import CARD_BINS, SHEBA_CODES, Bank, resolve_bank
from .card import luhn_check_digit
from .landline import AREA_CODES
from .mobile import OPERATOR_PREFIXES
from .national_id import legal_id_check_digit, national_id_check_digit
from .postal_code import is_valid_postal_code

BankLike = Union[Bank, str, None]


def _r(rng: Optional[random.Random]) -> Any:
    return rng if rng is not None else random


def _digits(r: Any, n: int) -> str:
    return "".join(str(r.randrange(10)) for _ in range(n))


def generate_national_id(rng: Optional[random.Random] = None) -> str:
    """A valid 10-digit national ID."""
    r = _r(rng)
    while True:
        base = _digits(r, 9)
        s = base + national_id_check_digit(base)
        if len(set(s)) > 1:
            return s


def generate_legal_id(rng: Optional[random.Random] = None) -> str:
    """A valid 11-digit legal entity ID."""
    r = _r(rng)
    while True:
        base = _digits(r, 10)
        s = base + legal_id_check_digit(base)
        if len(set(s)) > 1:
            return s


def generate_card_number(bank: BankLike = None, rng: Optional[random.Random] = None) -> str:
    """A valid 16-digit card number, optionally for a given bank (name or Bank)."""
    r = _r(rng)
    if bank is None:
        bins = sorted(CARD_BINS)
    else:
        b = resolve_bank(bank)
        bins = sorted(k for k, v in CARD_BINS.items() if v == b)
        if not bins:
            raise ValueError(f"no card BIN known for {b.name_en}")
    payload = r.choice(bins) + _digits(r, 9)
    return payload + luhn_check_digit(payload)


def generate_sheba(bank: BankLike = None, rng: Optional[random.Random] = None) -> str:
    """A valid Sheba number (``IR`` + 24 digits), optionally for a given bank."""
    r = _r(rng)
    if bank is None:
        codes = sorted(SHEBA_CODES)
    else:
        b = resolve_bank(bank)
        codes = sorted(k for k, v in SHEBA_CODES.items() if v == b)
        if not codes:
            raise ValueError(f"no Sheba code known for {b.name_en}")
    bban = r.choice(codes) + _digits(r, 19)
    check = 98 - int(bban + "182700") % 97
    return f"IR{check:02d}{bban}"


def generate_mobile(operator: Optional[str] = None, rng: Optional[random.Random] = None) -> str:
    """A well-formed mobile number (``09xxxxxxxxx``), optionally for an operator."""
    r = _r(rng)
    if operator is None:
        prefixes = [p for plist in OPERATOR_PREFIXES.values() for p in plist]
    else:
        matches = [k for k in OPERATOR_PREFIXES if k.lower() == operator.strip().lower()]
        if not matches:
            raise ValueError(
                f"unknown operator {operator!r}; choose one of {sorted(OPERATOR_PREFIXES)}"
            )
        prefixes = OPERATOR_PREFIXES[matches[0]]
    return r.choice(prefixes) + _digits(r, 7)


def generate_postal_code(rng: Optional[random.Random] = None) -> str:
    """A postal code that passes the format rules."""
    r = _r(rng)
    while True:
        code = (
            "".join(r.choice("13456789") for _ in range(4))
            + r.choice("1346789")
            + "".join(r.choice("013456789") for _ in range(5))
        )
        if is_valid_postal_code(code):
            return code


def generate_landline(area_code: Optional[str] = None, rng: Optional[random.Random] = None) -> str:
    """A well-formed landline number; ``area_code`` like ``"021"`` or ``"21"``."""
    r = _r(rng)
    if area_code is None:
        area = r.choice(sorted(AREA_CODES))
    else:
        area = area_code.strip()
        if len(area) == 2:
            area = "0" + area
        if area not in AREA_CODES:
            raise ValueError(f"unknown area code {area_code!r}")
    return area + r.choice("23456789") + _digits(r, 7)
