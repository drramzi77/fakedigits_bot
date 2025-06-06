# keyboards/main_menu_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    return InlineKeyboardMarkup([
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
        [
            InlineKeyboardButton("💰 رصيدي", callback_data="check_balance"),
            InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")
        ]
    ])
