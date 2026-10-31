"""تلفن ثابت و پیش‌شماره‌ی استان‌ها."""
from __future__ import annotations

import re
from typing import Dict, NamedTuple, Optional

from ._digits import clean, is_ascii_digits
from ._result import ValidationResult, fail, success


class AreaCode(NamedTuple):
    code: str  # e.g. "021"
    province_fa: str
    province_en: str


_ROWS = [
    ("011", "مازندران", "Mazandaran"),
    ("013", "گیلان", "Gilan"),
    ("017", "گلستان", "Golestan"),
    ("021", "تهران", "Tehran"),
    ("023", "سمنان", "Semnan"),
    ("024", "زنجان", "Zanjan"),
    ("025", "قم", "Qom"),
    ("026", "البرز", "Alborz"),
    ("028", "قزوین", "Qazvin"),
    ("031", "اصفهان", "Isfahan"),
    ("034", "کرمان", "Kerman"),
    ("035", "یزد", "Yazd"),
    ("038", "چهارمحال و بختیاری", "Chaharmahal and Bakhtiari"),
    ("041", "آذربایجان شرقی", "East Azerbaijan"),
    ("044", "آذربایجان غربی", "West Azerbaijan"),
    ("045", "اردبیل", "Ardabil"),
    ("051", "خراسان رضوی", "Razavi Khorasan"),
    ("054", "سیستان و بلوچستان", "Sistan and Baluchestan"),
    ("056", "خراسان جنوبی", "South Khorasan"),
    ("058", "خراسان شمالی", "North Khorasan"),
    ("061", "خوزستان", "Khuzestan"),
    ("066", "لرستان", "Lorestan"),
    ("071", "فارس", "Fars"),
    ("074", "کهگیلویه و بویراحمد", "Kohgiluyeh and Boyer-Ahmad"),
    ("076", "هرمزگان", "Hormozgan"),
    ("077", "بوشهر", "Bushehr"),
    ("081", "همدان", "Hamedan"),
    ("083", "کرمانشاه", "Kermanshah"),
    ("084", "ایلام", "Ilam"),
    ("086", "مرکزی", "Markazi"),
    ("087", "کردستان", "Kurdistan"),
]

AREA_CODES: Dict[str, AreaCode] = {c: AreaCode(c, fa, en) for c, fa, en in _ROWS}

# پیش‌شماره (۲ رقم بدون صفر) + شماره‌ی مشترک ۸ رقمی
_RE = re.compile(r"^(?:\+98|0098|98|0)?([1-8][0-9])([0-9]{8})$")


def validate_landline(value: object) -> ValidationResult:
    """Validate an Iranian landline: area code + 8-digit number.

    Accepts 02112345678, 2112345678, +982112345678, 00982112345678 و ارقام فارسی.
    مقدار نرمال‌شده: ``02112345678``.
    """
    if not isinstance(value, str):
        return fail("not_a_string", "landline")
    s = clean(value) or ""
    if not s:
        return fail("empty", "landline")
    body = s[1:] if s.startswith("+") else s
    if not is_ascii_digits(body):
        return fail("invalid_characters", "landline")
    m = _RE.match(s)
    if not m:
        return fail("invalid_format", "landline")
    area = "0" + m.group(1)
    if area not in AREA_CODES:
        return fail("unknown_area_code", "landline")
    if m.group(2)[0] in "01":  # شماره‌ی مشترک با ۰ یا ۱ شروع نمی‌شود
        return fail("invalid_format", "landline")
    return success(area + m.group(2))


def is_valid_landline(value: object) -> bool:
    """Return True if ``value`` is a valid Iranian landline number."""
    return validate_landline(value).ok


def normalize_landline(value: object, international: bool = False) -> Optional[str]:
    """Normalize to ``021xxxxxxxx`` (or ``+9821xxxxxxxx`` if ``international``)."""
    res = validate_landline(value)
    if not res.ok or res.value is None:
        return None
    return "+98" + res.value[1:] if international else res.value


def landline_area(value: object) -> Optional[AreaCode]:
    """Return the province / area code info of a valid landline number."""
    n = normalize_landline(value)
    return None if n is None else AREA_CODES.get(n[:3])


def format_landline(value: object, sep: str = "-") -> Optional[str]:
    """02112345678 -> '021-12345678' (None if invalid)."""
    n = normalize_landline(value)
    if n is None:
        return None
    return n[:3] + sep + n[3:]
