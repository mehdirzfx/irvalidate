# Contributing / مشارکت

Thanks for helping! irvalidate is a small library, and most useful contributions are small too.
از کمکت ممنونیم! بیشتر مشارکت‌های مفید در این پروژه کوچیکن.

## The most valuable contribution: data fixes / مهم‌ترین مشارکت: اصلاح داده

The lookup tables (bank BINs, Sheba codes, mobile prefixes, area codes) are the weakest part of the library, because **no official list was available** when they were verified. See [`DATA_SOURCES.md`](DATA_SOURCES.md) for what is confirmed and what is open.

A good data pull request:

1. changes **one fact** (one BIN, one code, one prefix) in `src/irvalidate/banks.py`, `mobile.py` or `landline.py`;
2. links a **source** in the PR description, preferably an official one (Central Bank of Iran, Shetab, CRA, Iran Post) and otherwise two independent ones;
3. updates `DATA_SOURCES.md` if it settles one of the open questions;
4. keeps the tests passing. `tests/test_data.py` checks every BIN and every Sheba code end to end.

> یک PR خوب برای داده: فقط **یک واقعیت** رو عوض کنه، **لینک منبع** داشته باشه (ترجیحاً رسمی، وگرنه دو منبع مستقل) و `DATA_SOURCES.md` رو اگه پرسشی رو حل کرد به‌روز کنه.

Not sure whether something is wrong? Open a **Data correction** issue; the form asks for the source.

## Code changes / تغییرات کد

```bash
git clone https://github.com/mehdirzfx/irvalidate.git
cd irvalidate
pip install -e ".[dev]"

pytest                       # tests (includes the README examples)
ruff check . && ruff format --check .
mypy
```

Please:

- add a test for every behaviour change; bug fixes need a regression test;
- keep the core **dependency-free** (framework integrations stay optional);
- reject only what is **documented** as impossible. If a rule has no source, don't add it;
- keep `README.md` and `README.fa.md` in sync. Every `# value` comment in their Python examples is executed by `tests/test_readme.py`.

## Releasing (maintainer) / انتشار

1. Bump `__version__` in `src/irvalidate/__init__.py` and add a section to `CHANGELOG.md`.
2. Commit and push to `main`; wait for CI to pass.
3. Create a GitHub Release whose tag is exactly `v<version>`. The publish workflow checks that the tag matches `__version__` and uploads to PyPI.

PyPI never accepts the same version twice, so a failed release needs a new version number or a recreated tag **before anything was uploaded**.

## Conduct

Be kind and assume good faith. Questions in Persian or English are both welcome. / فارسی یا انگلیسی، هر دو خوش‌آمدن.
