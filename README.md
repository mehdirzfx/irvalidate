# irvalidate

[![CI](https://github.com/mehdirzfx/irvalidate/actions/workflows/ci.yml/badge.svg)](https://github.com/mehdirzfx/irvalidate/actions)
[![PyPI](https://img.shields.io/pypi/v/irvalidate.svg)](https://pypi.org/project/irvalidate/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

کتابخانه‌ی سبک و **بدون وابستگی** پایتون برای اعتبارسنجی داده‌های ایرانی:
کد ملی، شناسه ملی شرکت، شماره کارت، شبا، موبایل، تلفن ثابت و کد پستی؛
با پیام خطای فارسی، تولید داده‌ی تستی و ولیدیتور آماده برای Pydantic/FastAPI، Django و WTForms.

*A tiny, zero-dependency Python library for validating Iranian data (national ID, legal ID, bank card, Sheba/IBAN, mobile, landline, postal code), with Persian/English error messages, test-data generators and ready-made Pydantic/FastAPI, Django and WTForms validators.*

## نصب

```bash
pip install irvalidate

# با یکپارچگی فریم‌ورک موردنظر
pip install "irvalidate[pydantic]"   # Pydantic v2 / FastAPI
pip install "irvalidate[django]"
pip install "irvalidate[wtforms]"
```

یا مستقیم از گیت‌هاب: `pip install git+https://github.com/mehdirzfx/irvalidate.git`

نیازمند پایتون ۳.۹ به بالا.

## استفاده‌ی سریع

```python
from irvalidate import (
    is_valid_national_id, is_valid_legal_id, is_valid_card_number,
    is_valid_sheba, is_valid_mobile, is_valid_landline, is_valid_postal_code,
    card_bank, sheba_bank, mobile_operator, landline_area, normalize_mobile,
)

is_valid_national_id("0013542419")      # True
is_valid_national_id("۰۰۱۳۵۴۲۴۱۹")      # True  (ارقام فارسی هم پشتیبانی می‌شود)
is_valid_legal_id("14003778990")        # True  (شناسه ملی شرکت‌ها)

is_valid_card_number("6037-9910-0000-0004")        # True
card_bank("6037991000000004").name_fa              # 'بانک ملی ایران'

is_valid_sheba("IR580540105180021273113007")       # True (پیشوند IR اختیاری است)
sheba_bank("IR580540105180021273113007").name_en   # 'Parsian Bank'

is_valid_mobile("+98 912 345 6789")                # True
normalize_mobile("۰۹۱۲۳۴۵۶۷۸۹")                     # '09123456789'
mobile_operator("09351234567")                     # 'Irancell'

is_valid_landline("021-22345678")                  # True
landline_area("02122345678").province_fa           # 'تهران'

is_valid_postal_code("1593764856")                 # True
```

## دلیل خطا

توابع `validate_*` به‌جای فقط `False`، دلیل را هم می‌گویند:

```python
from irvalidate import validate_national_id, set_default_language

r = validate_national_id("1234567890")
bool(r)          # False
r.code           # 'bad_checksum'
r.message        # 'کد ملی نامعتبر است (رقم کنترلی اشتباه است)'
r.message_en     # 'national ID is invalid (checksum mismatch)'

ok = validate_national_id("۰۰۱۳۵۴۲۴۱۹")
ok.value         # '0013542419'  (مقدار نرمال‌شده)

ok.raise_for_error()   # مقدار نرمال‌شده را برمی‌گرداند، یا ValidationError (زیرکلاس ValueError)

set_default_language("en")   # زبان پیش‌فرض r.message و پیام‌های فریم‌ورک‌ها
```

کدهای خطا: `not_a_string`، `empty`، `invalid_characters`، `invalid_length`، `all_same_digits`،
`bad_checksum`، `invalid_format`، `unknown_area_code`.

برای هر نوع، `validate_national_id`، `validate_legal_id`، `validate_card_number`،
`validate_sheba`، `validate_mobile`، `validate_landline` و `validate_postal_code` وجود دارد.

## یکپارچگی با فریم‌ورک‌ها

### Pydantic / FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
from irvalidate.integrations.pydantic import NationalId, MobileNumber

class User(BaseModel):
    national_id: NationalId   # "۰۰۱۳۵۴۲۴۱۹" -> "0013542419"
    mobile: MobileNumber      # "+98 912 345 6789" -> "09123456789"

app = FastAPI()

@app.post("/users")
def create(user: User):
    return user
```

انواع موجود: `NationalId`، `LegalId`، `CardNumber`، `Sheba`، `MobileNumber`، `PostalCode`، `Landline`.
مقدار خروجی همیشه نرمال‌شده است. ورودی باید رشته باشد.

### Django

```python
from django.db import models
from irvalidate.integrations.django import national_id_validator, mobile_validator

class Profile(models.Model):
    national_id = models.CharField(max_length=10, validators=[national_id_validator])
    mobile = models.CharField(max_length=14, validators=[mobile_validator])
```

کد خطا در `ValidationError.code` قرار می‌گیرد. ولیدیتورها: `national_id_validator`، `legal_id_validator`،
`card_number_validator`، `sheba_validator`، `mobile_validator`، `postal_code_validator`، `landline_validator`.

### WTForms

```python
from wtforms import Form, StringField
from irvalidate.integrations.wtforms import NationalId, MobileNumber

class SignupForm(Form):
    national_id = StringField(validators=[NationalId()])
    mobile = StringField(validators=[MobileNumber(message="موبایل درست نیست")])
```

## تولید داده‌ی تستی

```python
import random
from irvalidate import (
    generate_national_id, generate_legal_id, generate_card_number, generate_sheba,
    generate_mobile, generate_landline, generate_postal_code,
)

generate_national_id()                        # '1043321810' (نمونه‌ی تصادفی معتبر)
generate_card_number(bank="Mellat")           # کارت معتبر با BIN بانک ملت
generate_sheba(bank="ملی")                    # شبای معتبر بانک ملی
generate_mobile("Irancell")                   # '0937xxxxxxx'
generate_landline("021")                      # '021xxxxxxxx'

rng = random.Random(42)                       # نتیجه‌ی تکرارپذیر
generate_national_id(rng=rng)
```

> مقادیر تولیدشده فقط از نظر **ساختار و رقم کنترلی** معتبرند و برای داده‌ی فیک در تست‌اند. ممکن است تصادفاً با مقدار واقعی کسی یکی باشند؛ برای جعل هویت یا کارهای مشابه استفاده نکنید. تولیدکننده‌ی پیش‌فرض برای امنیت مناسب نیست.

## فرمت و ماسک

```python
from irvalidate import (
    mask_card_number, format_card_number, format_sheba, format_mobile,
    format_landline, to_persian_digits,
)

mask_card_number("6037991000000004")     # '6037-99**-****-0004'
format_card_number("6037991000000004")   # '6037-9910-0000-0004'
format_sheba("IR580540105180021273113007")  # 'IR58 0540 1051 8002 1273 1130 07'
format_mobile("+989123456789")           # '0912 345 6789'
format_landline("02122345678")           # '021-22345678'
to_persian_digits("0912")                # '۰۹۱۲'
```

## تلفن ثابت

شماره‌ی ثابت = پیش‌شماره‌ی استان + شماره‌ی ۸ رقمی (که با ۰ یا ۱ شروع نمی‌شود). پیش‌شماره‌ی هر ۳۱ استان در `irvalidate.landline.AREA_CODES` هست.
فرمت‌های `02122345678`، `2122345678`، `+982122345678` و `00982122345678` پذیرفته می‌شوند.
شماره‌های قدیمیِ ۷ رقمی و شماره‌های خدماتی (مثل ۱۱۰) پشتیبانی نمی‌شوند.

## خط فرمان

```bash
irvalidate national-id 0013542419
irvalidate card 6037991000000004
irvalidate sheba IR580540105180021273113007
irvalidate national-id 1234567890      # invalid + reason: bad_checksum
irvalidate card --generate             # یک کارت معتبر تستی
# انواع: national-id, legal-id, card, sheba, mobile, landline, postal-code
```

کد خروج ۰ (معتبر) یا ۱ (نامعتبر) است و برای اسکریپت‌ها مناسب است.

## نکات مهم

- **ورودی را رشته بدهید، نه عدد.** کد ملی‌هایی که با صفر شروع می‌شوند در تبدیل به عدد خراب می‌شوند؛ ورودی غیررشته‌ای نامعتبر (`not_a_string`) است.
- فاصله، خط تیره، نیم‌فاصله و پرانتز نادیده گرفته می‌شوند. فقط ارقام ۰-۹ و فارسی/عربی مجازند.
- **معتبر بودن ≠ وجود داشتن.** فقط ساختار و رقم کنترلی بررسی می‌شود؛ نمی‌شود فهمید کارت یا کد ملی واقعاً متعلق به کسی است. کد پستی هم فقط از نظر قالب بررسی می‌شود.
- لیست بانک‌ها (BIN کارت و کد شبا)، پیش‌شماره‌ی اپراتورهای موبایل و پیش‌شماره‌ی استان‌ها بر پایه‌ی اطلاعات عمومی است و ممکن است ناقص یا قدیمی باشد. اگر موردی جا افتاده، PR بدهید (`src/irvalidate/banks.py`).

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
