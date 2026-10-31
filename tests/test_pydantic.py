import pytest

pytest.importorskip("pydantic")

from pydantic import BaseModel, ValidationError  # noqa: E402

from irvalidate import generate_card_number, generate_sheba, set_default_language  # noqa: E402
from irvalidate.integrations.pydantic import (  # noqa: E402
    CardNumber,
    Landline,
    LegalId,
    MobileNumber,
    NationalId,
    PostalCode,
    Sheba,
)


class Person(BaseModel):
    nid: NationalId
    mobile: MobileNumber


def test_normalizes_output():
    p = Person(nid="۰۰۱۳۵۴۲۴۱۹", mobile="+98 912 345 6789")
    assert p.nid == "0013542419"
    assert p.mobile == "09123456789"


def test_error_message_is_persian_by_default():
    with pytest.raises(ValidationError) as exc:
        Person(nid="1234567890", mobile="09123456789")
    assert "کد ملی" in str(exc.value)


def test_error_message_english():
    set_default_language("en")
    try:
        with pytest.raises(ValidationError) as exc:
            Person(nid="1234567890", mobile="09123456789")
        assert "national ID" in str(exc.value)
    finally:
        set_default_language("fa")


def test_all_types():
    class M(BaseModel):
        legal: LegalId
        card: CardNumber
        sheba: Sheba
        postal: PostalCode
        phone: Landline

    m = M(
        legal="14003778990",
        card=generate_card_number(),
        sheba=generate_sheba().lower(),
        postal="1593764856",
        phone="021-22345678",
    )
    assert m.sheba.startswith("IR") and m.phone == "02122345678"


def test_json_schema_still_works():
    assert Person.model_json_schema()["properties"]["nid"]["type"] == "string"


def test_non_string_rejected():
    with pytest.raises(ValidationError):
        Person(nid=13542419, mobile="09123456789")
