# keyboards/category_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# لا تحتاج لاستيراد back_button أو create_reply_markup هنا لأنها لا تستخدم مباشرة.

def category_inline_keyboard(platform: str):
    """
    ينشئ لوحة مفاتيح أزرار فئات الأرقام لمنصة محددة (مثل WhatsApp أو Telegram).
    تتيح للمستخدم اختيار المنطقة أو نوع الرقم (عشوائي، الأكثر توفراً).

    Args:
        platform (str): اسم المنصة (مثل "WhatsApp", "Telegram").

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة للفئات.
    """
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
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_main")] # هذا الزر يجب أن يستخدم back_button إذا تم استيراده.
    ])