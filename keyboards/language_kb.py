# keyboards/language_kb.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.utils_kb import back_button
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE

def language_keyboard(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح الأزرار لاختيار اللغة.

    Args:
        lang_code (str): كود اللغة الحالي للمستخدم لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة للغة.
    """
    messages = get_messages(lang_code)

    buttons = [
        [
            InlineKeyboardButton(messages["language_arabic_button"], callback_data="set_lang_ar"),
            InlineKeyboardButton(messages["language_english_button"], callback_data="set_lang_en")
        ]
    ]

    # زر العودة كصف منفصل
    back = back_button(text=messages["back_button_text"])
    if isinstance(back, list):
        buttons.append(back)

    return InlineKeyboardMarkup(buttons)
