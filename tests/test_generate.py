import random

import pytest

from irvalidate import (
    card_bank,
    generate_card_number,
    generate_landline,
    generate_legal_id,
    generate_mobile,
    generate_national_id,
    generate_postal_code,
    generate_sheba,
    is_valid_card_number,
    is_valid_landline,
    is_valid_legal_id,
    is_valid_mobile,
    is_valid_national_id,
    is_valid_postal_code,
    is_valid_sheba,
    landline_area,
    mobile_operator,
    sheba_bank,
)

N = 300


def test_everything_generated_is_valid():
    rng = random.Random(1234)
    for _ in range(N):
        assert is_valid_national_id(generate_national_id(rng))
        assert is_valid_legal_id(generate_legal_id(rng))
        assert is_valid_card_number(generate_card_number(rng=rng))
        assert is_valid_sheba(generate_sheba(rng=rng))
        assert is_valid_mobile(generate_mobile(rng=rng))
        assert is_valid_postal_code(generate_postal_code(rng))
        assert is_valid_landline(generate_landline(rng=rng))


def test_default_rng_also_valid():
    assert is_valid_national_id(generate_national_id())
    assert is_valid_sheba(generate_sheba())


def test_reproducible_with_seed():
    assert generate_national_id(random.Random(1)) == generate_national_id(random.Random(1))
    assert generate_sheba(rng=random.Random(5)) == generate_sheba(rng=random.Random(5))


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Mellat", "Bank Mellat"),
        ("melli", "Bank Melli Iran"),
        ("بانک ملت", "Bank Mellat"),
        ("Parsian", "Parsian Bank"),
    ],
)
def test_bank_selection(name, expected):
    rng = random.Random(7)
    for _ in range(30):
        assert card_bank(generate_card_number(bank=name, rng=rng)).name_en == expected
        assert sheba_bank(generate_sheba(bank=name, rng=rng)).name_en == expected


def test_bank_errors():
    with pytest.raises(ValueError):
        generate_card_number(bank="no such bank")
    with pytest.raises(ValueError):
        generate_sheba(bank="Mehr")  # مبهم: چند بانک


def test_mobile_operator_selection():
    rng = random.Random(3)
    for op in ["MCI", "irancell", "Rightel"]:
        for _ in range(20):
            assert mobile_operator(generate_mobile(op, rng)).lower() == op.lower()
    with pytest.raises(ValueError):
        generate_mobile("nope")


def test_landline_area_selection():
    rng = random.Random(9)
    assert landline_area(generate_landline("021", rng)).province_en == "Tehran"
    assert landline_area(generate_landline("31", rng)).province_en == "Isfahan"
    with pytest.raises(ValueError):
        generate_landline("999")
