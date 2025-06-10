# keyboards/category_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.utils_kb import back_button # # تم استيراد back_button لأنها تستخدم الآن
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

def category_inline_keyboard(platform: str, lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح أزرار فئات الأرقام لمنصة محددة (مثل WhatsApp أو Telegram).
    تتيح للمستخدم اختيار المنطقة أو نوع الرقم (عشوائي، الأكثر توفراً).

    Args:
        platform (str): اسم المنصة (مثل "WhatsApp", "Telegram").
        lang_code (str): كود اللغة لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة للفئات.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(messages["most_available_button"].format(platform=platform), callback_data=f"most_{platform}")], # # استخدام النص المترجم
        [InlineKeyboardButton(messages["random_country_button"].format(platform=platform), callback_data=f"random_{platform}")], # # استخدام النص المترجم
        [
            InlineKeyboardButton(messages["region_arab"], callback_data=f"region_arab_{platform}"), # # استخدام النص المترجم
            InlineKeyboardButton(messages["region_africa"], callback_data=f"region_africa_{platform}") # # استخدام النص المترجم
        ],
        [
            InlineKeyboardButton(messages["region_asia"], callback_data=f"region_asia_{platform}"), # # استخدام النص المترجم
            InlineKeyboardButton(messages["region_europe"], callback_data=f"region_europe_{platform}") # # استخدام النص المترجم
        ],
        [
            InlineKeyboardButton(messages["region_america"], callback_data=f"region_america_{platform}"), # # استخدام النص المترجم
            InlineKeyboardButton(messages["region_australia"], callback_data=f"region_aus_{platform}") # # استخدام النص المترجم
        ],
        back_button(text=messages["back_button_text"], callback_data="back_to_main") # # استخدام النص المترجم وزر العودة من utils_kb
    ])