"""Property-based tests (Hypothesis): things that must hold for *any* input."""

import random

from hypothesis import given
from hypothesis import strategies as st

from irvalidate import (
    format_card_number,
    format_landline,
    format_mobile,
    format_sheba,
    generate_card_number,
    generate_landline,
    generate_legal_id,
    generate_mobile,
    generate_national_id,
    generate_postal_code,
    generate_sheba,
    mask_card_number,
    normalize_card_number,
    normalize_landline,
    normalize_mobile,
    normalize_sheba,
    to_english_digits,
    to_persian_digits,
    validate_card_number,
    validate_landline,
    validate_legal_id,
    validate_mobile,
    validate_national_id,
    validate_postal_code,
    validate_sheba,
)
from irvalidate.landline import AREA_CODES

ERROR_CODES = {
    "not_a_string",
    "empty",
    "invalid_characters",
    "invalid_length",
    "all_same_digits",
    "bad_checksum",
    "invalid_format",
    "unknown_area_code",
}

VALIDATORS = [
    validate_national_id,
    validate_legal_id,
    validate_card_number,
    validate_sheba,
    validate_mobile,
    validate_landline,
    validate_postal_code,
]
GENERATORS = [
    generate_national_id,
    generate_legal_id,
    generate_card_number,
    generate_sheba,
    generate_mobile,
    generate_landline,
    generate_postal_code,
]
PAIRS = list(zip(VALIDATORS, GENERATORS, strict=True))

anything = st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True),
    st.booleans(),
    st.text(),
    st.binary(),
    st.lists(st.text(max_size=5), max_size=3),
)
seeds = st.integers(min_value=0, max_value=2**32)
digit_strings = st.text(alphabet="0123456789", min_size=0, max_size=30)
separators = st.sampled_from([" ", "-", "_", "(", ")", "\u200c", "\u00a0"])


# ---------------------------------------------------------------- totality
@given(anything)
def test_validators_never_raise_and_always_explain(value):
    for validate in VALIDATORS:
        result = validate(value)
        assert bool(result) is result.ok
        if result.ok:
            assert result.code is None and result.value
        else:
            assert result.code in ERROR_CODES
            assert result.message_fa and result.message_en
            assert result.value is None


@given(anything)
def test_normalizers_return_none_or_str(value):
    for fn in (
        normalize_card_number,
        normalize_sheba,
        normalize_mobile,
        normalize_landline,
        format_card_number,
        format_sheba,
        format_mobile,
        format_landline,
        mask_card_number,
    ):
        out = fn(value)
        assert out is None or isinstance(out, str)


# ------------------------------------------------- generators / round trips
@given(seeds)
def test_every_generated_value_is_valid_and_normalized(seed):
    for validate, generate in PAIRS:
        value = generate(rng=random.Random(seed))
        result = validate(value)
        assert result.ok, (generate.__name__, value, result.code)
        # نرمال‌شده، خودش دوباره معتبر و بدون تغییر است (idempotent)
        assert validate(result.value).value == result.value


@given(seeds)
def test_persian_digits_are_accepted_everywhere(seed):
    for validate, generate in PAIRS:
        value = generate(rng=random.Random(seed))
        assert validate(to_persian_digits(value)).value == validate(value).value


@given(digit_strings)
def test_digit_conversion_round_trips(s):
    assert to_english_digits(to_persian_digits(s)) == s


@given(seeds, st.data())
def test_separators_do_not_change_the_result(seed, data):
    for validate, generate in PAIRS:
        value = generate(rng=random.Random(seed))
        noisy = value
        for _ in range(data.draw(st.integers(1, 4))):
            pos = data.draw(st.integers(0, len(noisy)))
            noisy = noisy[:pos] + data.draw(separators) + noisy[pos:]
        assert validate(noisy).value == validate(value).value


@given(seeds)
def test_format_and_mask_keep_the_digits(seed):
    card = generate_card_number(rng=random.Random(seed))
    assert normalize_card_number(format_card_number(card)) == card
    masked = mask_card_number(card)
    assert masked is not None and len(masked) == 19
    assert masked.replace("-", "")[:6] == card[:6]
    assert masked.replace("-", "")[-4:] == card[-4:]
    assert set(masked.replace("-", "")[6:12]) == {"*"}

    sheba = generate_sheba(rng=random.Random(seed))
    assert normalize_sheba(format_sheba(sheba)) == sheba
    mobile = generate_mobile(rng=random.Random(seed))
    assert normalize_mobile(format_mobile(mobile)) == mobile
    landline = generate_landline(rng=random.Random(seed))
    assert normalize_landline(format_landline(landline)) == landline


# ------------------------------------------- checksum error-detection claims
@given(seeds, st.data())
def test_luhn_and_mod97_catch_every_single_digit_change(seed, data):
    card = generate_card_number(rng=random.Random(seed))
    i = data.draw(st.integers(0, len(card) - 1))
    wrong = data.draw(st.sampled_from([d for d in "0123456789" if d != card[i]]))
    assert not validate_card_number(card[:i] + wrong + card[i + 1 :]).ok

    sheba = generate_sheba(rng=random.Random(seed))
    j = data.draw(st.integers(2, len(sheba) - 1))  # بعد از «IR»
    wrong = data.draw(st.sampled_from([d for d in "0123456789" if d != sheba[j]]))
    assert not validate_sheba(sheba[:j] + wrong + sheba[j + 1 :]).ok


@given(seeds, st.data())
def test_changing_only_the_check_digit_always_invalidates(seed, data):
    for validate, generate in (
        (validate_national_id, generate_national_id),
        (validate_legal_id, generate_legal_id),
    ):
        value = generate(rng=random.Random(seed))
        wrong = data.draw(st.sampled_from([d for d in "0123456789" if d != value[-1]]))
        assert not validate(value[:-1] + wrong).ok


# --------------------------------------------------------- documented rules
@given(st.from_regex(r"[0-9]{10}", fullmatch=True))
def test_postal_code_matches_its_documented_rule(s):
    expected = len(set(s)) > 1 and not (set(s[:5]) & {"0", "2"})
    assert validate_postal_code(s).ok is expected


@given(st.from_regex(r"[0-9]{2}[0-9]{8}", fullmatch=True))
def test_landline_ok_iff_area_code_exists(s):
    expected = ("0" + s[:2]) in AREA_CODES
    assert validate_landline(s).ok is expected


@given(st.from_regex(r"9[0-9]{9}", fullmatch=True))
def test_any_nine_prefixed_ten_digits_is_a_mobile(s):
    assert validate_mobile(s).value == "0" + s
    assert validate_mobile("+98" + s).value == "0" + s
    assert validate_mobile("0098" + s).value == "0" + s


# ------------------------------------------- exact checksum conditions (mutants)
@given(seeds)
def test_sheba_remainder_must_be_exactly_one(seed):
    """مجموع باید دقیقاً ۱ (mod 97) باشد، نه ۰ و نه هر مقدار دیگر."""
    sheba = generate_sheba(rng=random.Random(seed))
    bban = sheba[4:]
    x = int(bban + "182700") % 97
    assert validate_sheba(f"IR{(98 - x) % 100:02d}{bban}").ok  # باقی‌مانده ۱
    for wrong_remainder in (0, 2, 3, 96):
        check = (wrong_remainder - x) % 97
        assert not validate_sheba(f"IR{check:02d}{bban}").ok


def test_every_single_digit_change_is_detected_exhaustively():
    rng = random.Random(2026)
    for _ in range(40):
        card = generate_card_number(rng=rng)
        for i in range(len(card)):
            for d in "0123456789":
                if d != card[i]:
                    assert not validate_card_number(card[:i] + d + card[i + 1 :]).ok
        sheba = generate_sheba(rng=rng)
        for i in range(2, len(sheba)):
            for d in "0123456789":
                if d != sheba[i]:
                    assert not validate_sheba(sheba[:i] + d + sheba[i + 1 :]).ok


def test_operator_of_garbage_is_none():
    from irvalidate import mobile_operator

    assert mobile_operator("garbage") is None
    assert mobile_operator(None) is None
