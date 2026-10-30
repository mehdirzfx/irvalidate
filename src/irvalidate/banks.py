"""Iranian bank metadata (best-effort, based on public BIN / Sheba prefixes)."""
from __future__ import annotations

from typing import Dict, NamedTuple


class Bank(NamedTuple):
    name_fa: str
    name_en: str


MELLI = Bank("بانک ملی ایران", "Bank Melli Iran")
SEPAH = Bank("بانک سپه", "Bank Sepah")
SADERAT = Bank("بانک صادرات ایران", "Bank Saderat Iran")
TOSEE_SADERAT = Bank("بانک توسعه صادرات", "Export Development Bank of Iran")
SANAT_MADAN = Bank("بانک صنعت و معدن", "Bank of Industry and Mine")
KESHAVARZI = Bank("بانک کشاورزی", "Bank Keshavarzi")
MASKAN = Bank("بانک مسکن", "Bank Maskan")
POST_BANK = Bank("پست بانک ایران", "Post Bank of Iran")
TOSEE_TAAVON = Bank("بانک توسعه تعاون", "Tose'e Ta'avon Bank")
EGHTESAD_NOVIN = Bank("بانک اقتصاد نوین", "Eghtesad Novin Bank")
PARSIAN = Bank("بانک پارسیان", "Parsian Bank")
PASARGAD = Bank("بانک پاسارگاد", "Bank Pasargad")
KARAFARIN = Bank("بانک کارآفرین", "Karafarin Bank")
SAMAN = Bank("بانک سامان", "Saman Bank")
SINA = Bank("بانک سینا", "Sina Bank")
SARMAYEH = Bank("بانک سرمایه", "Sarmayeh Bank")
AYANDEH = Bank("بانک آینده", "Ayandeh Bank")
SHAHR = Bank("بانک شهر", "Shahr Bank")
DEY = Bank("بانک دی", "Day Bank")
MELLAT = Bank("بانک ملت", "Bank Mellat")
TEJARAT = Bank("بانک تجارت", "Tejarat Bank")
REFAH = Bank("بانک رفاه کارگران", "Refah Bank")
ANSAR = Bank("بانک انصار", "Ansar Bank")
MEHR_EGHTESAD = Bank("بانک مهر اقتصاد", "Mehr Eqtesad Bank")
GHAVAMIN = Bank("بانک قوامین", "Ghavamin Bank")
MEHR_IRAN = Bank("بانک قرض‌الحسنه مهر ایران", "Qarz al-Hasna Mehr Iran Bank")
GARDESHGARI = Bank("بانک گردشگری", "Tourism Bank")
HEKMAT = Bank("بانک حکمت ایرانیان", "Hekmat Iranian Bank")
TOSEE_ETEBARI = Bank("موسسه اعتباری توسعه", "Tose'e Credit Institution")
KOSAR = Bank("موسسه اعتباری کوثر", "Kosar Credit Institution")
NOOR = Bank("موسسه اعتباری نور", "Noor Credit Institution")
MELAL = Bank("موسسه اعتباری ملل", "Melal Credit Institution")
RESALAT = Bank("بانک قرض‌الحسنه رسالت", "Resalat Bank")
IRAN_ZAMIN = Bank("بانک ایران زمین", "Iran Zamin Bank")
MARKAZI = Bank("بانک مرکزی", "Central Bank of Iran")
KHAVARMIANEH = Bank("بانک خاورمیانه", "Middle East Bank")

# شش رقم اول شماره کارت (BIN)
CARD_BINS: Dict[str, Bank] = {
    "603799": MELLI,
    "589210": SEPAH,
    "603769": SADERAT,
    "627648": TOSEE_SADERAT,
    "627961": SANAT_MADAN,
    "603770": KESHAVARZI,
    "639217": KESHAVARZI,
    "628023": MASKAN,
    "627760": POST_BANK,
    "502908": TOSEE_TAAVON,
    "627412": EGHTESAD_NOVIN,
    "622106": PARSIAN,
    "627884": PARSIAN,
    "639194": PARSIAN,
    "502229": PASARGAD,
    "639347": PASARGAD,
    "627488": KARAFARIN,
    "502910": KARAFARIN,
    "621986": SAMAN,
    "639346": SINA,
    "639607": SARMAYEH,
    "636214": AYANDEH,
    "502806": SHAHR,
    "504706": SHAHR,
    "502938": DEY,
    "610433": MELLAT,
    "991975": MELLAT,
    "585983": TEJARAT,
    "627353": TEJARAT,
    "589463": REFAH,
    "627381": ANSAR,
    "639370": MEHR_EGHTESAD,
    "639599": GHAVAMIN,
    "606373": MEHR_IRAN,
    "505416": GARDESHGARI,
    "636949": HEKMAT,
    "628157": TOSEE_ETEBARI,
    "505801": KOSAR,
    "507677": NOOR,
    "606256": MELAL,
    "504172": RESALAT,
    "505785": IRAN_ZAMIN,
    "636795": MARKAZI,
    "585947": KHAVARMIANEH,
}

# کد بانک در شبا (رقم‌های پنجم تا هفتم)
SHEBA_CODES: Dict[str, Bank] = {
    "010": MARKAZI,
    "011": SANAT_MADAN,
    "012": MELLAT,
    "013": REFAH,
    "014": MASKAN,
    "015": SEPAH,
    "016": KESHAVARZI,
    "017": MELLI,
    "018": TEJARAT,
    "019": SADERAT,
    "020": TOSEE_SADERAT,
    "021": POST_BANK,
    "022": TOSEE_TAAVON,
    "051": TOSEE_ETEBARI,
    "052": GHAVAMIN,
    "053": KARAFARIN,
    "054": PARSIAN,
    "055": EGHTESAD_NOVIN,
    "056": SAMAN,
    "057": PASARGAD,
    "058": SARMAYEH,
    "059": SINA,
    "060": MEHR_IRAN,
    "061": SHAHR,
    "062": AYANDEH,
    "063": ANSAR,
    "064": GARDESHGARI,
    "065": HEKMAT,
    "066": DEY,
    "069": IRAN_ZAMIN,
    "070": RESALAT,
    "073": KOSAR,
    "075": MELAL,
    "078": KHAVARMIANEH,
    "080": NOOR,
    "090": MEHR_EGHTESAD,
}
