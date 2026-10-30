"""کد پستی ۱۰ رقمی."""
from __future__ import annotations

import re

from ._digits import clean

# قاعده‌ی رایج: رقم‌های اول تا چهارم صفر و ۲ نیستند، رقم پنجم ۰/۲/۵ نیست،
# رقم‌های آخر ۲ ندارند، و چهار رقم اول یکسان نیست.
_RE = re.compile(r"^(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}$")


def is_valid_postal_code(value: object) -> bool:
    """Check the format of a 10-digit Iranian postal code (کد پستی).

    توجه: این تابع فقط ساختار کد را بررسی می‌کند، نه وجود واقعی آدرس.
    """
    s = clean(value)
    return s is not None and _RE.match(s) is not None
