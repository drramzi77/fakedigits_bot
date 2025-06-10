# keyboards/main_menu_kb.py

from telegram import InlineKeyboardButton
from keyboards.utils_kb import back_button
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

def main_menu_keyboard(lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح الأزرار الرئيسية لاختيار المنصة.

    Args:
        lang_code (str): كود اللغة لعرض النصوص الصحيحة.

    Returns:
        list: قائمة بصفوف الأزرار.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    return [
        [
            InlineKeyboardButton("📞 WhatsApp", callback_data="select_app_WhatsApp"),
            InlineKeyboardButton("✈️ Telegram", callback_data="select_app_Telegram")
        ],
        [
            InlineKeyboardButton("👻 Snapchat", callback_data="select_app_Snapchat"),
            InlineKeyboardButton("📸 Instagram", callback_data="select_app_Instagram")
        ],
        [
            InlineKeyboardButton("📘 Facebook", callback_data="select_app_Facebook"),
            InlineKeyboardButton("🎵 TikTok", callback_data="select_app_TikTok")
        ],
        back_button(text=messages["check_balance_button"], callback_data="check_balance"), # # استخدام النص المترجم
        back_button(text=messages["back_to_dashboard_button_text"], callback_data="back_to_dashboard") # # استخدام النص المترجم للعودة إلى لوحة التحكم الرئيسية
    ]