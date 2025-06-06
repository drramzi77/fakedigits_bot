# keyboards/countries_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ قائمة الدول حسب المناطق
ARAB_COUNTRIES = [
    ("🇸🇦 السعودية", "sa"),
    ("🇪🇬 مصر", "eg"),
    ("🇾🇪 اليمن", "ye"),
    ("🇩🇿 الجزائر", "dz"),
    ("🇲🇦 المغرب", "ma"),
    ("🇮🇶 العراق", "iq"),
    ("🇸🇩 السودان", "sd"),
    ("🇸🇾 سوريا", "sy"),
    ("🇰🇼 الكويت", "kw"),
    ("🇶🇦 قطر", "qa"),
    ("🇦🇪 الإمارات", "ae"),
    ("🇯🇴 الأردن", "jo"),
    ("🇱🇧 لبنان", "lb"),
    ("🇹🇳 تونس", "tn"),
]

AFRICA_COUNTRIES = [
    ("🇳🇬 نيجيريا", "ng"),
    ("🇰🇪 كينيا", "ke"),
    ("🇬🇭 غانا", "gh"),
    ("🇿🇦 جنوب أفريقيا", "za"),
    ("🇪🇹 إثيوبيا", "et"),
    ("🇹🇿 تنزانيا", "tz")
]

ASIA_COUNTRIES = [
    ("🇮🇳 الهند", "in"),
    ("🇵🇰 باكستان", "pk"),
    ("🇮🇩 إندونيسيا", "id"),
    ("🇹🇭 تايلاند", "th"),
    ("🇲🇾 ماليزيا", "my"),
    ("🇵🇭 الفلبين", "ph")
]

EUROPE_COUNTRIES = [
    ("🇬🇧 بريطانيا", "uk"),
    ("🇫🇷 فرنسا", "fr"),
    ("🇩🇪 ألمانيا", "de"),
    ("🇪🇸 إسبانيا", "es"),
    ("🇮🇹 إيطاليا", "it"),
    ("🇳🇱 هولندا", "nl")
]

AMERICA_COUNTRIES = [
    ("🇺🇸 أمريكا", "us"),
    ("🇧🇷 البرازيل", "br"),
    ("🇨🇦 كندا", "ca"),
    ("🇲🇽 المكسيك", "mx"),
    ("🇨🇴 كولومبيا", "co"),
    ("🇦🇷 الأرجنتين", "ar")
]

AUSTRALIA_COUNTRIES = [
    ("🇦🇺 أستراليا", "au"),
    ("🇳🇿 نيوزيلندا", "nz")
]

# ✅ الدالة العامة التي تُستخدم من handler
def countries_keyboard(region: str, platform: str):
    regions = {
        "arab": ARAB_COUNTRIES,
        "africa": AFRICA_COUNTRIES,
        "asia": ASIA_COUNTRIES,
        "europe": EUROPE_COUNTRIES,
        "america": AMERICA_COUNTRIES,
        "aus": AUSTRALIA_COUNTRIES
    }

    countries = regions.get(region, [])
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"country_{code}_{platform}")]
        for name, code in countries
    ]

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])
    return InlineKeyboardMarkup(buttons)
