# irvalidate

[![CI](https://github.com/mehdirzfx/irvalidate/actions/workflows/ci.yml/badge.svg)](https://github.com/mehdirzfx/irvalidate/actions)
[![PyPI](https://img.shields.io/pypi/v/irvalidate.svg)](https://pypi.org/project/irvalidate/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

کتابخانه‌ی سبک و **بدون وابستگی** پایتون برای اعتبارسنجی داده‌های ایرانی:
کد ملی، شناسه ملی شرکت، شماره کارت، شبا، موبایل و کد پستی.

*A tiny, zero-dependency Python library for validating Iranian data: national ID, legal ID, bank card, Sheba (IBAN), mobile number and postal code.*

## نصب

```bash
pip install irvalidate
```

یا مستقیم از گیت‌هاب:

```bash
pip install git+https://github.com/mehdirzfx/irvalidate.git
```

نیازمند پایتون ۳.۹ به بالا.

## استفاده

```python
from irvalidate import (
    is_valid_national_id, is_valid_legal_id, is_valid_card_number,
    is_valid_sheba, is_valid_mobile, is_valid_postal_code,
    card_bank, sheba_bank, mobile_operator, normalize_mobile,
)

is_valid_national_id("0013542419")      # True
is_valid_national_id("۰۰۱۳۵۴۲۴۱۹")      # True  (ارقام فارسی هم پشتیبانی می‌شود)
is_valid_legal_id("14003778990")        # True  (شناسه ملی شرکت‌ها)

is_valid_card_number("6037-9910-0000-0004")   # True
card_bank("6037991000000004").name_fa         # 'بانک ملی ایران'

is_valid_sheba("IR580540105180021273113007")  # True (پیشوند IR اختیاری است)
sheba_bank("IR580540105180021273113007").name_en  # 'Parsian Bank'

is_valid_mobile("+98 912 345 6789")           # True
normalize_mobile("۰۹۱۲۳۴۵۶۷۸۹")                # '09123456789'
normalize_mobile("09123456789", international=True)  # '+989123456789'
mobile_operator("09351234567")                # 'Irancell'

is_valid_postal_code("1593764856")            # True
```

### خط فرمان

```bash
irvalidate national-id 0013542419
irvalidate card 6037991000000004
irvalidate sheba IR580540105180021273113007
# انواع: national-id, legal-id, card, sheba, mobile, postal-code
```

خروجی `valid` یا `invalid` است و کد خروج ۰ یا ۱ برمی‌گردد (مناسب اسکریپت‌ها).

## نکات مهم

- **ورودی را رشته بدهید، نه عدد.** کد ملی‌هایی که با صفر شروع می‌شوند در تبدیل به عدد خراب می‌شوند؛ توابع برای ورودی غیررشته‌ای `False` برمی‌گردانند.
- فاصله، خط تیره، نیم‌فاصله و پرانتز نادیده گرفته می‌شوند.
- **معتبر بودن ≠ وجود داشتن.** این کتابخانه فقط ساختار و رقم کنترلی را بررسی می‌کند؛ نمی‌تواند بگوید کارت یا کد ملی واقعاً متعلق به کسی هست یا نه.
- کد پستی فقط از نظر قالب بررسی می‌شود، نه وجود آدرس.
- لیست بانک‌ها (از روی BIN کارت و کد شبا) و پیش‌شماره‌ی اپراتورهای موبایل بر پایه‌ی اطلاعات عمومی است و ممکن است ناقص باشد. اگر موردی جا افتاده، PR بدهید (`src/irvalidate/banks.py`).

## مشارکت

```bash
git clone https://github.com/mehdirzfx/irvalidate.git
cd irvalidate
pip install -e ".[dev]"
pytest
```

Issue و Pull Request خوشحالمان می‌کند.

## مجوز

MIT — آزاد برای استفاده‌ی شخصی و تجاری.
