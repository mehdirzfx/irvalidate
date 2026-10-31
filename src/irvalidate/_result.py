"""Validation results with machine-readable codes and fa/en messages."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ._config import get_default_language

_LABELS = {
    "national_id": ("کد ملی", "national ID"),
    "legal_id": ("شناسه ملی", "legal ID"),
    "card": ("شماره کارت", "card number"),
    "sheba": ("شماره شبا", "Sheba number"),
    "mobile": ("شماره موبایل", "mobile number"),
    "postal_code": ("کد پستی", "postal code"),
    "landline": ("شماره تلفن ثابت", "landline number"),
}

_TEMPLATES = {
    "not_a_string": ("{label} باید به‌صورت رشته وارد شود", "{label} must be a string"),
    "empty": ("{label} وارد نشده است", "{label} is empty"),
    "invalid_characters": (
        "{label} فقط می‌تواند شامل رقم باشد",
        "{label} may only contain digits",
    ),
    "invalid_length": ("{label} باید {n} رقم باشد", "{label} must be {n} digits long"),
    "all_same_digits": (
        "{label} نمی‌تواند از ارقام یکسان تشکیل شده باشد",
        "{label} cannot consist of identical digits",
    ),
    "bad_checksum": (
        "{label} نامعتبر است (رقم کنترلی اشتباه است)",
        "{label} is invalid (checksum mismatch)",
    ),
    "invalid_format": ("قالب {label} نادرست است", "{label} has an invalid format"),
    "unknown_area_code": (
        "پیش‌شماره‌ی تلفن نامعتبر است",
        "unknown landline area code",
    ),
}


class ValidationError(ValueError):
    """Raised by :meth:`ValidationResult.raise_for_error`."""

    def __init__(self, result: "ValidationResult") -> None:
        super().__init__(result.message)
        self.result = result

    @property
    def code(self) -> Optional[str]:
        return self.result.code


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of a ``validate_*`` call.

    ``bool(result)`` is ``result.ok``. When valid, ``value`` holds the normalized
    form (English digits, no separators). When invalid, ``code`` is one of:
    ``not_a_string``, ``empty``, ``invalid_characters``, ``invalid_length``,
    ``all_same_digits``, ``bad_checksum``, ``invalid_format``, ``unknown_area_code``.
    """

    ok: bool
    code: Optional[str] = None
    message_fa: str = ""
    message_en: str = ""
    value: Optional[str] = None

    def __bool__(self) -> bool:
        return self.ok

    @property
    def message(self) -> str:
        """Message in the default language (see ``set_default_language``)."""
        return self.message_fa if get_default_language() == "fa" else self.message_en

    def raise_for_error(self) -> str:
        """Return the normalized value, or raise :class:`ValidationError`."""
        if not self.ok:
            raise ValidationError(self)
        assert self.value is not None
        return self.value


def success(value: str) -> ValidationResult:
    return ValidationResult(ok=True, value=value)


def fail(code: str, kind: str, **params: object) -> ValidationResult:
    label_fa, label_en = _LABELS[kind]
    label_fa = str(params.pop("label_fa", label_fa))
    label_en = str(params.pop("label_en", label_en))
    fa, en = _TEMPLATES[code]
    return ValidationResult(
        ok=False,
        code=code,
        message_fa=fa.format(label=label_fa, **params),
        message_en=en.format(label=label_en, **params),
    )
