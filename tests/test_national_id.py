import pytest

from irvalidate import is_valid_legal_id, is_valid_national_id


@pytest.mark.parametrize("v", ["0013542419", "1234567891", "۰۰۱۳۵۴۲۴۱۹", "001-354-2419", " 0013542419 "])
def test_valid_national_id(v):
    assert is_valid_national_id(v)


@pytest.mark.parametrize(
    "v",
    ["1234567890", "0000000000", "1111111111", "123", "00135424190", "abcdefghij", "", None, 13542419],
)
def test_invalid_national_id(v):
    assert not is_valid_national_id(v)


def test_legal_id():
    assert is_valid_legal_id("14003778990")
    assert is_valid_legal_id("۱۴۰۰۳۷۷۸۹۹۰")
    assert not is_valid_legal_id("14003778991")
    assert not is_valid_legal_id("11111111111")
    assert not is_valid_legal_id("1400377899")
