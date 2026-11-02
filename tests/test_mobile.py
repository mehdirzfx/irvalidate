import pytest

from irvalidate import is_valid_mobile, mobile_operator, normalize_mobile


@pytest.mark.parametrize(
    "v",
    [
        "09123456789",
        "9123456789",
        "989123456789",
        "+989123456789",
        "00989123456789",
        "۰۹۱۲۳۴۵۶۷۸۹",
        "0912-345-6789",
        "+98 (912) 345 6789",
    ],
)
def test_valid_mobile(v):
    assert is_valid_mobile(v)
    assert normalize_mobile(v) == "09123456789"


@pytest.mark.parametrize(
    "v",
    ["02112345678", "0812345678", "0912345678", "091234567890", "+9891234", "", None, 9123456789],
)
def test_invalid_mobile(v):
    assert not is_valid_mobile(v)
    assert normalize_mobile(v) is None


def test_international():
    assert normalize_mobile("09123456789", international=True) == "+989123456789"


@pytest.mark.parametrize(
    "v,op",
    [
        ("09121234567", "MCI"),
        ("09351234567", "Irancell"),
        ("09211234567", "Rightel"),
        ("09321234567", "Taliya"),
        ("09861234567", None),
    ],
)
def test_operator(v, op):
    assert mobile_operator(v) == op
