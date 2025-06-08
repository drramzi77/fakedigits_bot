# keyboards/main_menu_kb.py

from telegram import InlineKeyboardButton
from keyboards.utils_kb import back_button # ✅ تم إضافة هذا السطر

def main_menu_keyboard():
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
        back_button(text="💰 رصيدي", callback_data="check_balance"),
        back_button() # هذا الزر سيعود إلى لوحة التحكم الرئيسية (dashboard)
    ]