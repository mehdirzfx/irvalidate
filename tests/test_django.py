import pytest

pytest.importorskip("django")

from django.core.exceptions import ValidationError  # noqa: E402

from irvalidate.integrations.django import (  # noqa: E402
    card_number_validator,
    landline_validator,
    legal_id_validator,
    mobile_validator,
    national_id_validator,
    postal_code_validator,
    sheba_validator,
)


def test_valid_values_pass():
    national_id_validator("0013542419")
    legal_id_validator("14003778990")
    card_number_validator("6037991000000004")
    sheba_validator("IR580540105180021273113007")
    mobile_validator("۰۹۱۲۳۴۵۶۷۸۹")
    postal_code_validator("1593764856")
    landline_validator("02122345678")


def test_invalid_raises_with_code_and_message():
    with pytest.raises(ValidationError) as exc:
        national_id_validator("1234567890")
    assert exc.value.code == "bad_checksum"
    assert "کد ملی" in exc.value.messages[0]


@pytest.mark.parametrize(
    "fn", [national_id_validator, legal_id_validator, card_number_validator, sheba_validator,
           mobile_validator, postal_code_validator, landline_validator]
)
def test_all_validators_reject_garbage(fn):
    with pytest.raises(ValidationError):
        fn("garbage")


def test_validators_are_module_level_functions():
    # برای serialize شدن در migrationها باید با import path قابل پیدا شدن باشند
    assert national_id_validator.__qualname__ == "national_id_validator"
    assert national_id_validator.__module__ == "irvalidate.integrations.django"
