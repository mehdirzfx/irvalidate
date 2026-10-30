import pytest

from irvalidate import card_bank, format_card_number, is_valid_card_number, normalize_card_number


def test_valid_card_and_bank():
    assert is_valid_card_number("6037991000000004")
    assert is_valid_card_number("6037-9910-0000-0004")
    assert is_valid_card_number("۶۰۳۷۹۹۱۰۰۰۰۰۰۰۰۴")
    assert card_bank("6037991000000004").name_en == "Bank Melli Iran"


@pytest.mark.parametrize("v", ["6037991000000005", "603799100000000", "0000000000000000", "abcd", None, 6037991000000004])
def test_invalid_card(v):
    assert not is_valid_card_number(v)
    assert card_bank(v) is None


def test_format_and_normalize():
    assert format_card_number("۶۰۳۷۹۹۱۰۰۰۰۰۰۰۰۴") == "6037-9910-0000-0004"
    assert normalize_card_number("6037 9910 0000 0004") == "6037991000000004"
    assert normalize_card_number("123") is None
