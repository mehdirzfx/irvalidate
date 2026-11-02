"""WTForms validators.

    pip install "irvalidate[wtforms]"

    from wtforms import Form, StringField
    from irvalidate.integrations.wtforms import NationalId, MobileNumber

    class SignupForm(Form):
        national_id = StringField(validators=[NationalId()])
        mobile = StringField(validators=[MobileNumber(message="موبایل درست نیست")])

برای فیلد اختیاری، ``wtforms.validators.Optional()`` را قبل از این‌ها بگذارید.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

try:
    from wtforms.validators import ValidationError
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        'WTForms is required for this module: pip install "irvalidate[wtforms]"'
    ) from exc

from .._result import ValidationResult
from ..card import validate_card_number
from ..landline import validate_landline
from ..mobile import validate_mobile
from ..national_id import validate_legal_id, validate_national_id
from ..postal_code import validate_postal_code
from ..sheba import validate_sheba


class _Base:
    _validate: Callable[[object], ValidationResult]

    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __call__(self, form: Any, field: Any) -> None:
        result = type(self)._validate(field.data)
        if not result.ok:
            raise ValidationError(self.message or result.message)


def _make(name: str, fn: Callable[[object], ValidationResult]) -> type:
    return type(name, (_Base,), {"_validate": staticmethod(fn), "__doc__": f"{name} validator."})


NationalId = _make("NationalId", validate_national_id)
LegalId = _make("LegalId", validate_legal_id)
CardNumber = _make("CardNumber", validate_card_number)
Sheba = _make("Sheba", validate_sheba)
MobileNumber = _make("MobileNumber", validate_mobile)
PostalCode = _make("PostalCode", validate_postal_code)
Landline = _make("Landline", validate_landline)

__all__ = ["NationalId", "LegalId", "CardNumber", "Sheba", "MobileNumber", "PostalCode", "Landline"]
