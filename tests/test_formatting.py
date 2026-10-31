import pytest

from irvalidate import (
    format_mobile,
    format_sheba,
    mask_card_number,
    to_english_digits,
    to_persian_digits,
)

SHEBA = "IR580540105180021273113007"


def test_persian_digits():
    assert to_persian_digits("0912 ABC 3") == "۰۹۱۲ ABC ۳"
    assert to_persian_digits("١٢٣") == "۱۲۳"  # ارقام عربی هم تبدیل می‌شوند
    assert to_english_digits(to_persian_digits("0123456789")) == "0123456789"


def test_mask_card():
    assert mask_card_number("6037991000000004") == "6037-99**-****-0004"
    assert mask_card_number("۶۰۳۷-۹۹۱۰-۰۰۰۰-۰۰۰۴") == "6037-99**-****-0004"
    assert mask_card_number("6037991000000004", sep=" ", mask_char="•") == "6037 99•• •••• 0004"
    assert mask_card_number("6037991000000004", keep_first=0, keep_last=4) == "****-****-****-0004"
    assert mask_card_number("123") is None
    with pytest.raises(ValueError):
        mask_card_number("6037991000000004", keep_first=10, keep_last=10)


def test_format_sheba():
    assert format_sheba(SHEBA) == "IR58 0540 1051 8002 1273 1130 07"
    assert format_sheba(SHEBA[2:]) == "IR58 0540 1051 8002 1273 1130 07"
    assert format_sheba("xx") is None


def test_format_mobile():
    assert format_mobile("+989123456789") == "0912 345 6789"
    assert format_mobile("09123456789", sep="-") == "0912-345-6789"
    assert format_mobile("123") is None
