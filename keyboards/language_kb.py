from telegram import InlineKeyboardButton
from keyboards.utils_kb import back_button # ✅ تم إضافة هذا السطر

def language_keyboard():
    return [
        [
            InlineKeyboardButton("العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("English", callback_data="set_lang_en")
        ],
        back_button()
    ]