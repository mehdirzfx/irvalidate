# Changelog

## 0.2.0
### اضافه شد
- **دلیل خطا:** توابع `validate_*` یک `ValidationResult` با `code` (مثلاً `bad_checksum`) و پیام فارسی/انگلیسی برمی‌گردانند؛ `set_default_language("fa" | "en")`
- **یکپارچگی با فریم‌ورک‌ها:** Pydantic v2 / FastAPI، Django، WTForms (`irvalidate[pydantic]`, `[django]`, `[wtforms]`)
- **تولید داده‌ی تستی:** `generate_national_id`, `generate_legal_id`, `generate_card_number(bank=...)`, `generate_sheba(bank=...)`, `generate_mobile(operator=...)`, `generate_postal_code`, `generate_landline(area_code=...)`
- **فرمت و ماسک:** `mask_card_number`, `format_sheba`, `format_mobile`, `format_landline`, `to_persian_digits`
- **تلفن ثابت:** `validate_landline`, `landline_area` و جدول پیش‌شماره‌ی ۳۱ استان
- CLI: نوع `landline`، گزینه‌ی `--generate` و نمایش دلیل خطا

### اصلاح شد
- ارقام سایر الفباها (مثل دواناگری) که قبلاً به‌اشتباه به‌عنوان رقم پذیرفته می‌شدند، اکنون با `invalid_characters` رد می‌شوند. فقط ۰-۹ و ارقام فارسی/عربی مجازند.

### تغییر رفتار
- خروجی CLI برای مقدار نامعتبر یک خط `reason:` هم دارد (خط اول همچنان `invalid` است).

## 0.1.0
- نسخه‌ی اول: کد ملی، شناسه ملی شرکت، شماره کارت، شبا، موبایل، کد پستی
- پشتیبانی از ارقام فارسی و عربی
- تشخیص بانک (از روی کارت و شبا) و اپراتور موبایل
- ابزار خط فرمان `irvalidate`
