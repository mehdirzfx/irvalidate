"""Integrity + regression tests for the lookup tables (see DATA_SOURCES.md)."""

from pathlib import Path

import pytest

from irvalidate import (
    card_bank,
    merged_into,
    sheba_bank,
    to_persian_digits,
)
from irvalidate.banks import CARD_BINS, MERGED_INTO, SHEBA_CODES, all_banks
from irvalidate.card import luhn_check_digit
from irvalidate.landline import AREA_CODES
from irvalidate.mobile import OPERATOR_PREFIXES

ROOT = Path(__file__).resolve().parents[1]


def card_with_bin(bin6: str) -> str:
    payload = bin6 + "000000000"
    return payload + luhn_check_digit(payload)


def sheba_with_code(code: str) -> str:
    bban = (code + "0000001234567890123").ljust(22, "0")[:22]
    return f"IR{98 - int(bban + '182700') % 97:02d}{bban}"


def test_table_shapes():
    assert all(len(b) == 6 and b.isascii() and b.isdigit() for b in CARD_BINS)
    assert all(len(c) == 3 and c.isascii() and c.isdigit() for c in SHEBA_CODES)
    assert all(len(c) == 3 and c.startswith("0") for c in AREA_CODES)
    banks = set(all_banks())
    assert set(CARD_BINS.values()) <= banks
    assert set(SHEBA_CODES.values()) <= banks


@pytest.mark.parametrize("bin6", sorted(CARD_BINS))
def test_every_bin_resolves_end_to_end(bin6):
    assert card_bank(card_with_bin(bin6)) == CARD_BINS[bin6]


@pytest.mark.parametrize("code", sorted(SHEBA_CODES))
def test_every_sheba_code_resolves_end_to_end(code):
    assert sheba_bank(sheba_with_code(code)) == SHEBA_CODES[code]


def test_operator_prefixes_are_unique_and_well_formed():
    seen = {}
    for op, prefixes in OPERATOR_PREFIXES.items():
        for p in prefixes:
            assert len(p) == 4 and p.startswith("09") and p.isdigit()
            assert p not in seen, f"{p} belongs to both {seen[p]} and {op}"
            seen[p] = op


# ---- regressions for entries corrected after verification against sources ----
def test_sheba_079_is_mehr_eghtesad_and_090_is_not_mapped():
    assert sheba_bank(sheba_with_code("079")).name_en == "Mehr Eqtesad Bank"
    assert "090" not in SHEBA_CODES  # قبلاً اشتباهاً به مهر اقتصاد نسبت داده می‌شد
    assert sheba_bank(sheba_with_code("090")) is None


def test_sheba_095_is_iran_venezuela():
    assert sheba_bank(sheba_with_code("095")).name_en == "Iran-Venezuela Bilateral Bank"


@pytest.mark.parametrize(
    "bin6,name",
    [
        ("170019", "Bank Melli Iran"),
        ("636797", "Central Bank of Iran"),
        ("505426", "Tourism Bank"),
        ("505809", "Middle East Bank"),
        ("207177", "Export Development Bank of Iran"),
        ("603769", "Bank Saderat Iran"),  # در برخی منابع جابه‌جا با ۶۰۳۷۷۰ نوشته شده
        ("603770", "Bank Keshavarzi"),
    ],
)
def test_specific_bins(bin6, name):
    assert card_bank(card_with_bin(bin6)).name_en == name


def test_mobile_operator_table_fixes():
    assert "0996" in OPERATOR_PREFIXES["MCI"]
    assert "Aptel" not in OPERATOR_PREFIXES  # برچسب بی‌منبع؛ جایگزین: MVNO
    assert OPERATOR_PREFIXES["MVNO"] == ["0999"]


# ---- mergers ----
def test_merged_into():
    names = {b.name_en: merged_into(b).name_en for b in MERGED_INTO}
    assert names == {
        "Ansar Bank": "Bank Sepah",
        "Ghavamin Bank": "Bank Sepah",
        "Hekmat Iranian Bank": "Bank Sepah",
        "Mehr Eqtesad Bank": "Bank Sepah",
        "Kosar Credit Institution": "Bank Sepah",
        "Noor Credit Institution": "Bank Melli Iran",
    }
    assert merged_into(card_bank(card_with_bin("627381"))).name_en == "Bank Sepah"
    assert merged_into(card_bank(card_with_bin("603799"))) is None
    assert merged_into(None) is None


# ---- README numbers must match the real tables ----
def test_readme_counts_match_tables():
    en = (ROOT / "README.md").read_text(encoding="utf-8")
    fa = (ROOT / "README.fa.md").read_text(encoding="utf-8")
    n_bins, n_codes, n_areas = len(CARD_BINS), len(SHEBA_CODES), len(AREA_CODES)
    assert f"from {n_bins} BIN prefixes" in en
    assert f"from {n_codes} bank codes" in en
    assert f"from all {n_areas} area codes" in en
    fa_n = to_persian_digits
    assert f"از روی {fa_n(str(n_bins))} پیش‌شماره (BIN)" in fa
    assert f"از روی {fa_n(str(n_codes))} کد بانک" in fa
    assert f"از روی هر {fa_n(str(n_areas))} پیش‌شماره" in fa


def test_resolve_bank_errors():
    import pytest

    from irvalidate.banks import resolve_bank

    for bad in ("", "   ", 123, None):
        with pytest.raises(ValueError):
            resolve_bank(bad)  # type: ignore[arg-type]


def test_bank_without_a_card_bin_cannot_generate_cards():
    import pytest

    from irvalidate import generate_card_number

    # بانک ایران و ونزوئلا کد شبا دارد ولی BIN کارت ندارد
    with pytest.raises(ValueError, match="no card BIN"):
        generate_card_number(bank="Venezuela")


def test_clean_ignores_non_strings():
    from irvalidate._digits import clean

    assert clean(123) is None
    assert clean(None) is None
