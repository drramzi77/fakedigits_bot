# keyboards/category_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def category_inline_keyboard(platform: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 الأكثر توفراً ({platform})", callback_data=f"most_{platform}")],
        [InlineKeyboardButton(f"🚀 دولة عشوائية ({platform})", callback_data=f"random_{platform}")],
        [
            InlineKeyboardButton("🌍 العرب", callback_data=f"region_arab_{platform}"),
            InlineKeyboardButton("🌍 أفريقيا", callback_data=f"region_africa_{platform}")
        ],
        [
            InlineKeyboardButton("🌍 آسيا", callback_data=f"region_asia_{platform}"),
            InlineKeyboardButton("🌍 أوروبا", callback_data=f"region_europe_{platform}")
        ],
        [
            InlineKeyboardButton("🌍 أمريكا", callback_data=f"region_america_{platform}"),
            InlineKeyboardButton("🌍 أستراليا", callback_data=f"region_aus_{platform}")
        ],
        [InlineKeyboardButton("📦 رقم جاهز", callback_data=f"ready_{platform}")],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_main")]
    ])
