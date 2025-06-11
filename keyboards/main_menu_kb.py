from telegram import InlineKeyboardButton
from keyboards.utils_kb import back_button
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE

def main_menu_keyboard(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح الأزرار الرئيسية لاختيار المنصة.
    """
    messages = get_messages(lang_code)

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
        *[ [btn] for btn in back_button(text=messages["check_balance_button"], callback_data="check_balance") ],
        *[ [btn] for btn in back_button(text=messages["back_to_dashboard_button_text"], callback_data="back_to_dashboard") ]
    ]
