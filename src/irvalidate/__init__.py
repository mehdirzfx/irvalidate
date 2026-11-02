"""irvalidate — اعتبارسنجی داده‌های ایرانی (کد ملی، کارت، شبا، موبایل، تلفن ثابت، کد پستی)."""

from ._config import get_default_language, set_default_language
from ._digits import to_english_digits, to_persian_digits
from ._result import ValidationError, ValidationResult
from .banks import Bank, merged_into
from .card import (
    card_bank,
    format_card_number,
    is_valid_card_number,
    mask_card_number,
    normalize_card_number,
    validate_card_number,
)
from .generate import (
    generate_card_number,
    generate_landline,
    generate_legal_id,
    generate_mobile,
    generate_national_id,
    generate_postal_code,
    generate_sheba,
)
from .landline import (
    AreaCode,
    format_landline,
    is_valid_landline,
    landline_area,
    normalize_landline,
    validate_landline,
)
from .mobile import (
    format_mobile,
    is_valid_mobile,
    mobile_operator,
    normalize_mobile,
    validate_mobile,
)
from .national_id import (
    is_valid_legal_id,
    is_valid_national_id,
    validate_legal_id,
    validate_national_id,
)
from .postal_code import is_valid_postal_code, validate_postal_code
from .sheba import (
    format_sheba,
    is_valid_sheba,
    normalize_sheba,
    sheba_bank,
    validate_sheba,
)

__version__ = "0.3.0"

__all__ = [
    "AreaCode",
    "Bank",
    "ValidationError",
    "ValidationResult",
    "card_bank",
    "format_card_number",
    "format_landline",
    "format_mobile",
    "format_sheba",
    "generate_card_number",
    "generate_landline",
    "generate_legal_id",
    "generate_mobile",
    "generate_national_id",
    "generate_postal_code",
    "generate_sheba",
    "get_default_language",
    "is_valid_card_number",
    "is_valid_landline",
    "is_valid_legal_id",
    "is_valid_mobile",
    "is_valid_national_id",
    "is_valid_postal_code",
    "is_valid_sheba",
    "landline_area",
    "mask_card_number",
    "merged_into",
    "mobile_operator",
    "normalize_card_number",
    "normalize_landline",
    "normalize_mobile",
    "normalize_sheba",
    "set_default_language",
    "sheba_bank",
    "to_english_digits",
    "to_persian_digits",
    "validate_card_number",
    "validate_landline",
    "validate_legal_id",
    "validate_mobile",
    "validate_national_id",
    "validate_postal_code",
    "validate_sheba",
]
