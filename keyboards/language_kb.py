from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("English", callback_data="set_lang_en")
        ],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ])
