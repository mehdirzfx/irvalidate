"""Pydantic v2 (and FastAPI) types.

    pip install "irvalidate[pydantic]"

    from pydantic import BaseModel
    from irvalidate.integrations.pydantic import NationalId, MobileNumber

    class User(BaseModel):
        national_id: NationalId   # "۰۰۱۳۵۴۲۴۱۹" -> "0013542419"
        mobile: MobileNumber      # "+98 912 345 6789" -> "09123456789"

مقدار خروجی همیشه نرمال‌شده است (ارقام انگلیسی، بدون فاصله و خط تیره).
پیام خطا طبق ``irvalidate.set_default_language`` فارسی یا انگلیسی است.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

try:
    from pydantic import AfterValidator
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        'pydantic is required for this module: pip install "irvalidate[pydantic]"'
    ) from exc

from .._result import ValidationResult
from ..card import validate_card_number
from ..landline import validate_landline
from ..mobile import validate_mobile
from ..national_id import validate_legal_id, validate_national_id
from ..postal_code import validate_postal_code
from ..sheba import validate_sheba


def _validator(validate: Callable[[object], ValidationResult]) -> AfterValidator:
    def check(value: str) -> str:
        result = validate(value)
        if not result.ok:
            raise ValueError(result.message)
        assert result.value is not None
        return result.value

    return AfterValidator(check)


NationalId = Annotated[str, _validator(validate_national_id)]
LegalId = Annotated[str, _validator(validate_legal_id)]
CardNumber = Annotated[str, _validator(validate_card_number)]
Sheba = Annotated[str, _validator(validate_sheba)]
MobileNumber = Annotated[str, _validator(validate_mobile)]
PostalCode = Annotated[str, _validator(validate_postal_code)]
Landline = Annotated[str, _validator(validate_landline)]

__all__ = [
    "NationalId",
    "LegalId",
    "CardNumber",
    "Sheba",
    "MobileNumber",
    "PostalCode",
    "Landline",
]
