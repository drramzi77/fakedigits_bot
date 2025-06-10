# keyboards/language_kb.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup # # تم إضافة InlineKeyboardMarkup
from keyboards.utils_kb import back_button
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

def language_keyboard(lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح الأزرار لاختيار اللغة.

    Args:
        lang_code (str): كود اللغة الحالي للمستخدم لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة للغة.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    return InlineKeyboardMarkup([ # # تم إضافة InlineKeyboardMarkup لتغليف القائمة
        [
            InlineKeyboardButton(messages["language_arabic_button"], callback_data="set_lang_ar"), # # استخدام النص المترجم
            InlineKeyboardButton(messages["language_english_button"], callback_data="set_lang_en") # # استخدام النص المترجم
        ],
        back_button(text=messages["back_button_text"]) # # استخدام النص المترجم لزر العودة
    ])