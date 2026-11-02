import pytest

from irvalidate import is_valid_sheba, normalize_sheba, sheba_bank

VALID = "IR580540105180021273113007"  # نمونه‌ی مرجع (پارسیان)


def make_sheba(bank_code: str, account: str = "0000001234567890123") -> str:
    """Build a valid Sheba: IR + check + 3-digit bank code + 19 digits."""
    bban = (bank_code + account).ljust(22, "0")[:22]
    check = 98 - int(bban + "182700") % 97
    return f"IR{check:02d}{bban}"


def test_valid_variants():
    assert is_valid_sheba(VALID)
    assert is_valid_sheba(VALID.lower())
    assert is_valid_sheba(VALID[2:])  # بدون IR
    assert is_valid_sheba("IR58 0540 1051 8002 1273 1130 07")
    assert is_valid_sheba("IR۵۸۰۵۴۰۱۰۵۱۸۰۰۲۱۲۷۳۱۱۳۰۰۷")


def test_invalid():
    assert not is_valid_sheba("IR580540105180021273113008")
    assert not is_valid_sheba("IR5805401051800212731130")
    assert not is_valid_sheba("")
    assert not is_valid_sheba(None)


def test_normalize():
    assert normalize_sheba(VALID[2:]) == VALID
    assert normalize_sheba("ir58 0540 1051 8002 1273 1130 07") == VALID
    assert normalize_sheba("xx") is None


@pytest.mark.parametrize(
    "code,name", [("017", "Bank Melli Iran"), ("012", "Bank Mellat"), ("054", "Parsian Bank")]
)
def test_bank_lookup(code, name):
    s = make_sheba(code)
    assert is_valid_sheba(s)
    assert sheba_bank(s).name_en == name


def test_bank_unknown_or_invalid():
    assert sheba_bank(make_sheba("999")) is None
    assert sheba_bank("IR000000000000000000000000") is None
