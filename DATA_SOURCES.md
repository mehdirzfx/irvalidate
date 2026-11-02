# Data sources & verification / منابع و راستی‌آزمایی داده‌ها

**خلاصه‌ی فارسی:** جدول‌های بانک (BIN کارت و کد شبا)، پیش‌شماره‌ی موبایل، پیش‌شماره‌ی استان‌ها و قواعد کد پستی روز ۲ نوامبر ۲۰۲۶ (۱۱ آبان ۱۴۰۵) با چند منبع عمومی مستقل تطبیق داده شدن. **به هیچ سند رسمی** (بانک مرکزی، شتاب، سازمان تنظیم مقررات و ارتباطات رادیویی، شرکت ملی پست) **دسترسی پیدا نکردم**؛ همه‌ی منبع‌ها ثانویه‌ان. این فایل می‌گه چی تأیید شد، چی عوض شد، و چی بی‌پاسخ موند.

This file records how the lookup tables were checked, what changed in 0.3.0 and, just as important, what could **not** be confirmed.

## What this is, and what it is not

- Verified on **2 November 2026** by cross-checking several independent public sources.
- **No official document was obtained** (Central Bank of Iran, Shetab, the Communications Regulatory Authority, Iran Post). Every source below is secondary: open-source datasets, payment-provider docs, news and blog posts, Wikipedia.
- Two Iranian sites (`pishkhanak.com`, `banker.ir`) disallow automated access, so only the excerpts shown in search results were read. Their data is cited as "excerpt".
- Sources often copy each other, so agreement between them is weaker evidence than it looks.

## Policy

| Case | Rule |
|---|---|
| Existing entry, at least 1 source confirms, none contradicts | keep |
| New entry | add only if **2 or more** independent sources agree |
| Entry contradicted by sources | fix, and add a regression test |
| Rule with **no** source | remove (the library should only reject what is documented as impossible) |
| Entry seen in a single source only | not added; listed under "Open questions" |

## Sources read

**Card BINs and Sheba codes**
- [masoudv/iranbanks](https://github.com/masoudv/iranbanks) v2: 37 banks with BINs, Sheba codes and merge status (read in full). Its changelog states that `603769` is Saderat and `603770` is Keshavarzi.
- [mehrnet/IranianBanks](https://github.com/mehrnet/IranianBanks) (excerpt)
- [hasanparasteh/bank-identify.js](https://gist.github.com/hasanparasteh/4744845b41a260a0128f275058b9c3b3) (read in full; contains typos such as `67381` for Ansar, which were ignored)
- [ahbanavi/iranian-banks-bin.json](https://gist.github.com/ahbanavi/7bc6dff01b13d7c718209a5785e6c495) and [khooz gist](https://gist.github.com/khooz/72af33763eafc42282bb9f65eec3c1cb) (excerpts)
- [BaseMax/Iran-Bank-Detector-JS](https://github.com/BaseMax/Iran-Bank-Detector-JS): **outlier**, swaps `603769`/`603770`; disagrees with every other source and was not followed
- `pishkhanak.com/tools/iran-banks-directory` (excerpts): BINs, Sheba codes and merge status
- Lists derived from the Shetab "card pre-numbers" table: [rezvanco.ir](https://www.rezvanco.ir/index.php/learning-articles/other/593-the-complete-list-of-shatabsi-card-pre-numbers-of-the-country-s-banks-according-to-the-name-of-the-bank-and-the-pre-number-of-the-card), banker.ir (excerpt), bankavl.com, iranbanking.blogfa.com, asrebank.ir
- Sheba codes: [Vandar docs](https://vandarpay.github.io/docs/banks/), [rade.ir/sheba](https://www.rade.ir/sheba/), [bank.khanesarmaye.com/sheba](https://bank.khanesarmaye.com/sheba), [nextofx.com](https://nextofx.com/blog/iban-sheba-guide), [almico.ir](https://almico.ir/blog/sheba), nabzebourse.com
- **Ignored as unreliable:** `zimapay.com/mag/what-is-iban` (its Sheba codes are garbled, e.g. 070 for Mehr Eqtesad)

**Mobile prefixes**
- Persian Wikipedia, "شماره‌های تلفن در ایران" (excerpt), [iran912.com](https://iran912.com/article/mobile-phone-prefix-in-iran/), [webcookdigital.ir](https://webcookdigital.ir/free/mobile-validator), jalebestan.ir, eghtesaad24.ir, ounbaman.ir

**Landline area codes**
- [areaphonecodes.com](https://areaphonecodes.com/iran/) (full list of 31), [English Wikipedia](https://en.wikipedia.org/wiki/Telephone_numbers_in_Iran), [howtocallabroad.com](https://www.howtocallabroad.com/iran/)

**Postal code rules**
- [mag.postex.ir](https://mag.postex.ir/what-is-a-postal-code/), [peivast.com](https://peivast.com/p/128944), address.ir, factorial.tax, shadmag.com, virgool.io, akhbarrasmi.com, [sanjoor.ir](https://sanjoor.ir/utility/postal-code-validator/)

## Confirmed without change

- All 44 BINs that were already in the table: each is confirmed by at least one source, most by many (the 603769 = Saderat and 603770 = Keshavarzi assignment is the majority view and is also stated in masoudv/iranbanks' changelog).
- 991975 (Mellat) and 502910 (Karafarin), which had looked single-sourced, appear in six and five sources respectively.
- Sheba codes `010 011 012 013 014 015 016 017 018 019 020 021 022 051 052 053 054 055 056 057 058 059 060 061 062 063 064 065 066 069 070 073 075 078 080`.
- All 31 landline area codes: identical to the full list on areaphonecodes.com, consistent with Wikipedia and howtocallabroad.
- Irancell prefixes (`0900-0905`, `0930`, `0933`, `0935-0939`, `0941`): exactly the 14 prefixes one source counts, consistent with the others.
- Rightel `0920-0922`, MCI `0910-0919` and `0990-0994`.
- Mergers: Ansar, Ghavamin, Hekmat Iranian, Mehr Eqtesad and Kosar into Sepah; Noor into Melli (masoudv/iranbanks, pishkhanak, khanesarmaye).

## Changed in 0.3.0

| What | Before | After | Evidence |
|---|---|---|---|
| Sheba `090` | Mehr Eqtesad | **removed** (now unknown) | Mehr Eqtesad is `079` per masoudv, pishkhanak (several pages), khanesarmaye. Only one pishkhanak table lists `090`, and for Mehr Iran. |
| Sheba `079` | missing | Mehr Eqtesad | masoudv, pishkhanak, khanesarmaye |
| Sheba `095` | missing | Iran-Venezuela Bilateral Bank (no card BIN) | Vandar docs, rade.ir, pishkhanak, masoudv |
| BIN `170019` | missing | Melli | mehrnet, masoudv, pishkhanak |
| BIN `636797` | missing | Central Bank | masoudv, pishkhanak |
| BIN `505426` | missing | Tourism Bank | mehrnet, masoudv |
| BIN `505809` | missing | Middle East Bank | two gists (hasanparasteh, khooz) |
| BIN `207177` | missing | Export Development Bank | masoudv, pishkhanak, banker.ir, almico |
| MCI `0996` | missing | MCI | Persian Wikipedia, jalebestan |
| `0999` operator label | "Aptel" | generic **MVNO** | Persian Wikipedia says all MVNO prefixes start with `0998`/`0999`; iran912 lists Samantel under `0999`. "Aptel" had no support. |
| Postal code rules | first 4 digits not identical; 5th digit not 5; no digit 2 in the last five | only: 10 digits, no `0`/`2` in the first five, not all digits identical | The `0`/`2` rule is stated by 7+ sources. The extra rules had **no source** (they came from a community regex written from memory) and could reject real codes. |
| Landline subscriber number | first digit not 0 or 1 | no restriction | no source for that rule |
| `merged_into()` | n/a | new helper | see mergers above |

Two of these removals loosen validation: a few numbers that 0.2.x rejected (postal codes, landlines) are now accepted. That is intended: only impossibilities that are documented are rejected.

## Open questions (not in the library)

| Item | Why it is not included |
|---|---|
| BIN `903769` (Saderat) | single source (masoudv) |
| BIN `604932` (Sepah) | single source (hasanparasteh) |
| BIN `581874` | appears in one gist without a readable bank name |
| Sheba `090` | one source says Mehr Iran has both `060` and `090`; three others list only `060` |
| MCI `0995` | listed by one blog only |
| Rightel `0923` | three sources list `0920-0923`, three list only `0920-0922`. Kept `0920-0922`. |
| Spadan `0931`, TeleKish `0934` | only 2012-era blogs and a Wikipedia sentence saying they were assigned "previously" |
| Taliya `0932` | kept (it was already in the table), but the sources are old |
| BIN `636214` | some lists name it "Tat" (Tose'e va Tejarat); all other sources, and Tat's merge into Ayandeh, support Ayandeh |
| `504172` Resalat, `627760` Post Bank | mehrnet groups them under Sepah; every other source lists them as separate banks. Followed the majority. |
| `62198618` (8-digit, BluBank) | neo-bank prefix, out of scope |
| Landline subscriber-number rules | no source describes any beyond "8 digits" |
| Whether a bank's BIN/Sheba "merged" status is final | names are kept as of the original allocation |

## Helping

If you have an **official** document, or a source that contradicts something here, please open a "Data correction" issue (the template asks for the source). A one-line change to `src/irvalidate/banks.py`, `mobile.py` or `landline.py` plus the source link is the ideal pull request.

Re-verification is worth repeating about once a year; mergers, new MVNO prefixes and new BIN ranges do appear.
