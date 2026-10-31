import pytest

from irvalidate import (
    format_landline,
    is_valid_landline,
    landline_area,
    normalize_landline,
)
from irvalidate.landline import AREA_CODES


@pytest.mark.parametrize(
    "v",
    ["02122345678", "2122345678", "+982122345678", "00982122345678", "021-22345678", "(021) 2234 5678", "۰۲۱۲۲۳۴۵۶۷۸"],
)
def test_valid(v):
    assert is_valid_landline(v)
    assert normalize_landline(v) == "02122345678"


@pytest.mark.parametrize(
    "v",
    ["02022345678", "02101234567", "0211234567", "09223456789", "021223456789", "", None, 2122345678],
)
def test_invalid(v):
    assert not is_valid_landline(v)
    assert normalize_landline(v) is None


def test_international_and_format():
    assert normalize_landline("02122345678", international=True) == "+982122345678"
    assert format_landline("02122345678") == "021-22345678"
    assert format_landline("bad") is None


def test_area():
    assert landline_area("02122345678").province_en == "Tehran"
    assert landline_area("03122345678").province_fa == "اصفهان"
    assert landline_area("05122345678").province_en == "Razavi Khorasan"
    assert landline_area("123") is None


def test_area_table_is_complete():
    assert len(AREA_CODES) == 31  # یک پیش‌شماره برای هر استان
    assert all(c.startswith("0") and len(c) == 3 for c in AREA_CODES)
