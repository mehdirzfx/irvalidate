import pytest

from irvalidate import is_valid_postal_code, validate_postal_code


@pytest.mark.parametrize(
    "v",
    [
        "1593764856",
        "۱۵۹۳۷۶۴۸۵۶",
        "1593-764856",
        "1593764852",  # رقم ۲ در ۵ رقم آخر: در هیچ منبعی ممنوع نیست
        "1593564856",  # رقم پنجم ۵: در هیچ منبعی ممنوع نیست
    ],
)
def test_valid(v):
    assert is_valid_postal_code(v)


@pytest.mark.parametrize(
    "v",
    [
        "0123456789",  # ۰ در ۵ رقم اول
        "2593764856",  # ۲ در ۵ رقم اول
        "1523764856",
        "1593074856",
        "1111111111",  # همه‌ی ارقام یکسان
        "159376485",
        "15937648567",
        "",
        None,
        1593764856,
    ],
)
def test_invalid(v):
    assert not is_valid_postal_code(v)


def test_codes():
    assert validate_postal_code("0123456789").code == "invalid_format"
    assert validate_postal_code("1111111111").code == "all_same_digits"
    assert validate_postal_code("159").code == "invalid_length"
