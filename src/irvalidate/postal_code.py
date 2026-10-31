"""کد پستی ۱۰ رقمی."""
from __future__ import annotations

import re

from ._result import ValidationResult, fail, success
from ._validate import prepare_digits

# قاعده‌ی رایج: رقم‌های اول تا چهارم صفر و ۲ نیستند، رقم پنجم ۰/۲/۵ نیست،
# رقم‌های آخر ۲ ندارند، و چهار رقم اول یکسان نیست.
_RE = re.compile(r"^(?!([0-9])\1{3})[13-9]{4}[1346-9][013-9]{5}$")


def validate_postal_code(value: object) -> ValidationResult:
    """Validate the format of a 10-digit postal code (کد پستی).

    توجه: فقط ساختار کد را بررسی می‌کند، نه وجود واقعی آدرس.
    """
    s, err = prepare_digits(value, "postal_code", 10)
    if err or s is None:
        return err  # type: ignore[return-value]
    if not _RE.match(s):
        return fail("invalid_format", "postal_code")
    return success(s)


def is_valid_postal_code(value: object) -> bool:
    """Return True if ``value`` has the shape of a valid postal code."""
    return validate_postal_code(value).ok
