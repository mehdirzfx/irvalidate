import pytest

from irvalidate import (
    ValidationError,
    set_default_language,
    validate_card_number,
    validate_landline,
    validate_legal_id,
    validate_mobile,
    validate_national_id,
    validate_postal_code,
    validate_sheba,
)


def test_national_id_codes():
    assert validate_national_id(None).code == "not_a_string"
    assert validate_national_id(13542419).code == "not_a_string"
    assert validate_national_id("").code == "empty"
    assert validate_national_id(" - ").code == "empty"
    assert validate_national_id("12345abcde").code == "invalid_characters"
    assert validate_national_id("123").code == "invalid_length"
    assert validate_national_id("1111111111").code == "all_same_digits"
    assert validate_national_id("1234567890").code == "bad_checksum"


def test_ok_result_has_normalized_value():
    r = validate_national_id("۰۰۱۳۵۴۲۴۱۹")
    assert r and r.ok and r.code is None and r.value == "0013542419"


def test_other_kinds_codes():
    assert validate_legal_id("11111111111").code == "all_same_digits"
    assert validate_legal_id("14003778991").code == "bad_checksum"
    assert validate_card_number("6037991000000005").code == "bad_checksum"
    assert validate_card_number("603799").code == "invalid_length"
    assert validate_sheba("IR580540105180021273113008").code == "bad_checksum"
    assert validate_sheba("IR58").code == "invalid_length"
    assert validate_mobile("0812345678").code == "invalid_format"
    assert validate_mobile("0912+345").code == "invalid_characters"
    assert validate_postal_code("0123456789").code == "invalid_format"
    assert validate_landline("02012345678").code == "unknown_area_code"


def test_messages_both_languages():
    r = validate_national_id("1234567890")
    assert "کد ملی" in r.message_fa
    assert "national ID" in r.message_en
    assert r.message == r.message_fa  # پیش‌فرض فارسی


def test_sheba_length_message_mentions_24():
    r = validate_sheba("IR58")
    assert "24" in r.message_fa and "24" in r.message_en


def test_default_language_switch():
    r = validate_national_id("1234567890")
    set_default_language("en")
    try:
        assert r.message == r.message_en
    finally:
        set_default_language("fa")
    assert r.message == r.message_fa


def test_invalid_language():
    with pytest.raises(ValueError):
        set_default_language("de")


def test_raise_for_error():
    assert validate_mobile("+989123456789").raise_for_error() == "09123456789"
    with pytest.raises(ValidationError) as exc:
        validate_card_number("1234").raise_for_error()
    assert exc.value.code == "invalid_length"
    assert isinstance(exc.value, ValueError)


def test_other_unicode_digits_are_rejected():
    # ارقام دواناگری (۰۱۳۵...) نباید به‌عنوان رقم معتبر پذیرفته شوند
    devanagari = "".join(chr(0x0966 + int(c)) for c in "0013542419")
    assert validate_national_id(devanagari).code == "invalid_characters"
    assert validate_mobile("".join(chr(0x0966 + int(c)) for c in "09123456789")).code in (
        "invalid_characters",
        "invalid_format",
    )
