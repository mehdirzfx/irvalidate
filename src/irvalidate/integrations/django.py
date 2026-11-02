"""Django validators.

    pip install "irvalidate[django]"

    from django.db import models
    from irvalidate.integrations.django import national_id_validator, mobile_validator

    class Profile(models.Model):
        national_id = models.CharField(max_length=10, validators=[national_id_validator])
        mobile = models.CharField(max_length=14, validators=[mobile_validator])

توابع در سطح ماژول تعریف شده‌اند تا در migrationها قابل serialize باشند.
کد خطا (مثلاً ``bad_checksum``) در ``ValidationError.code`` قرار می‌گیرد.
"""

from __future__ import annotations

from collections.abc import Callable

try:
    from django.core.exceptions import ValidationError
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        'Django is required for this module: pip install "irvalidate[django]"'
    ) from exc

from .._result import ValidationResult
from ..card import validate_card_number
from ..landline import validate_landline
from ..mobile import validate_mobile
from ..national_id import validate_legal_id, validate_national_id
from ..postal_code import validate_postal_code
from ..sheba import validate_sheba


def _run(validate: Callable[[object], ValidationResult], value: object) -> None:
    result = validate(value)
    if not result.ok:
        raise ValidationError(result.message, code=result.code)


def national_id_validator(value: object) -> None:
    _run(validate_national_id, value)


def legal_id_validator(value: object) -> None:
    _run(validate_legal_id, value)


def card_number_validator(value: object) -> None:
    _run(validate_card_number, value)


def sheba_validator(value: object) -> None:
    _run(validate_sheba, value)


def mobile_validator(value: object) -> None:
    _run(validate_mobile, value)


def postal_code_validator(value: object) -> None:
    _run(validate_postal_code, value)


def landline_validator(value: object) -> None:
    _run(validate_landline, value)


__all__ = [
    "national_id_validator",
    "legal_id_validator",
    "card_number_validator",
    "sheba_validator",
    "mobile_validator",
    "postal_code_validator",
    "landline_validator",
]
