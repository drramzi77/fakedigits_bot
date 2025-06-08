# keyboards/server_kb.py

import json
import logging
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup # ✅ تم إضافة هذا السطر

logger = logging.getLogger(__name__)

SERVERS_FILE = os.path.join("data", "servers.json")

# ✅ تحميل بيانات السيرفرات كاملة من ملف JSON
def load_all_servers_data() -> list:
    return load_json_file(SERVERS_FILE, [])

# ✅ حفظ بيانات السيرفرات كاملة إلى ملف JSON
def save_servers_data(data: list):
    save_json_file(SERVERS_FILE, data)

# ✅ تحميل السيرفرات لمنصة ودولة معينة (مع تصفية الكمية)
def load_servers(platform: str, country_code: str) -> list:
    all_data = load_all_servers_data()
    for entry in all_data:
        if entry["platform"] == platform and entry["country"] == country_code:
            # # هنا نضيف الفلترة: نرجع السيرفرات التي كميتها > 0 فقط
            available_servers = [s for s in entry.get("servers", []) if s.get("quantity", 0) > 0]
            return available_servers
    return []

# ✅ إنشاء لوحة السيرفرات بأيقونات مميزة
def server_keyboard(platform: str, country_code: str) -> InlineKeyboardMarkup:
    servers = load_servers(platform, country_code)

    buttons = []
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    for i, server in enumerate(servers):
        emoji = emoji_cycle[i % len(emoji_cycle)]
        # # نعرض الكمية المتبقية
        label = f"{emoji} {server['name']} - 💰 {server['price']} ر.س ({server.get('quantity', 0)} متاح)"
        callback = f"buy_{platform}_{country_code}_{server['id']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))
    return create_reply_markup(buttons)