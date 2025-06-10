# keyboards/countries_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from utils.helpers import get_flag # # تم تعديل هذا السطر لاستيراد get_flag من utils.helpers

# ✅ قائمة الدول حسب المناطق (تُستخدم رموز الدولة هنا، وسيتم جلب الاسم المترجم لاحقاً)
ARAB_COUNTRIES_CODES = [
    ("sa", "🇸🇦"), ("eg", "🇪🇬"), ("ye", "🇾🇪"), ("dz", "🇩🇿"),
    ("ma", "🇲🇦"), ("iq", "🇮🇶"), ("sd", "🇸🇩"), ("sy", "🇸🇾"),
    ("kw", "🇰🇼"), ("qa", "🇶🇦"), ("ae", "🇦🇪"), ("jo", "🇯🇴"),
    ("lb", "🇱🇧"), ("tn", "🇹🇳"),
]

AFRICA_COUNTRIES_CODES = [
    ("ng", "🇳🇬"), ("ke", "🇰🇪"), ("gh", "🇬🇭"), ("za", "🇿🇦"),
    ("et", "🇪🇹"), ("tz", "🇹🇿")
]

ASIA_COUNTRIES_CODES = [
    ("in", "🇮🇳"), ("pk", "🇵🇰"), ("id", "🇮🇩"), ("th", "🇹🇭"),
    ("my", "🇲🇾"), ("ph", "🇵🇭")
]

EUROPE_COUNTRIES_CODES = [
    ("uk", "🇬🇧"), ("fr", "🇫🇷"), ("de", "🇩🇪"), ("es", "🇪🇸"),
    ("it", "🇮🇹"), ("nl", "🇳🇱")
]

AMERICA_COUNTRIES_CODES = [
    ("us", "🇺🇸"), ("br", "🇧🇷"), ("ca", "🇨🇦"), ("mx", "🇲🇽"),
    ("co", "🇨🇴"), ("ar", "🇦🇷")
]

AUSTRALIA_COUNTRIES_CODES = [
    ("au", "🇦🇺"), ("nz", "🇳🇿")
]

# ✅ الدالة العامة التي تُستخدم من handler
def countries_keyboard(region: str, platform: str, lang_code: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    """
    ينشئ لوحة مفاتيح أزرار الدول بناءً على المنطقة والمنصة المحددة.

    Args:
        region (str): المنطقة الجغرافية (مثل "arab", "africa", "asia").
        platform (str): اسم المنصة (مثل "WhatsApp", "Telegram").
        lang_code (str): كود اللغة لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة بالدول.
    """
    messages = get_messages(lang_code)

    regions_map = {
        "arab": ARAB_COUNTRIES_CODES,
        "africa": AFRICA_COUNTRIES_CODES,
        "asia": ASIA_COUNTRIES_CODES,
        "europe": EUROPE_COUNTRIES_CODES,
        "america": AMERICA_COUNTRIES_CODES,
        "aus": AUSTRALIA_COUNTRIES_CODES
    }

    countries_to_display = regions_map.get(region, [])
    buttons = []

    for code, emoji in countries_to_display:
        country_name_key = f"country_name_{code}"
        country_name = messages.get(country_name_key, code.upper())

        label = f"{emoji} {country_name}"
        callback = f"country_{code}_{platform}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}", lang_code=lang_code))
    return create_reply_markup(buttons)