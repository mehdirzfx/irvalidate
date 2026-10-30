import pytest

from irvalidate import is_valid_postal_code


@pytest.mark.parametrize("v", ["1593764856", "۱۵۹۳۷۶۴۸۵۶", "1593-764856"])
def test_valid(v):
    assert is_valid_postal_code(v)


@pytest.mark.parametrize("v", ["0123456789", "1111111111", "1593764852", "159376485", "15937648567", "", None, 1593764856])
def test_invalid(v):
    assert not is_valid_postal_code(v)
