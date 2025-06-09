# keyboards/server_kb.py

import json
import logging
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup # تأكد من أن هذا الاستيراد موجود

logger = logging.getLogger(__name__)

SERVERS_FILE = os.path.join("data", "servers.json")

def load_all_servers_data() -> list:
    """
    يُحمّل بيانات جميع السيرفرات المتاحة من ملف JSON.

    Returns:
        list: قائمة بقواميس بيانات السيرفرات.
    """
    return load_json_file(SERVERS_FILE, [])

def save_servers_data(data: list):
    """
    يُحفظ بيانات السيرفرات إلى ملف JSON.

    Args:
        data (list): قائمة بقواميس بيانات السيرفرات المراد حفظها.
    """
    save_json_file(SERVERS_FILE, data)

def load_servers(platform: str, country_code: str) -> list:
    """
    يُحمّل السيرفرات المتاحة لمنصة ودولة معينتين (الكمية > 0 فقط).

    Args:
        platform (str): اسم المنصة (مثال: "WhatsApp").
        country_code (str): رمز كود الدولة (مثال: "sa").

    Returns:
        list: قائمة بالسيرفرات المتوفرة التي تتطابق مع المعايير.
    """
    all_data = load_all_servers_data()
    for entry in all_data:
        if entry["platform"] == platform and entry["country"] == country_code:
            # # هنا نضيف الفلترة: نرجع السيرفرات التي كميتها > 0 فقط
            available_servers = [s for s in entry.get("servers", []) if s.get("quantity", 0) > 0]
            return available_servers
    return []

def server_keyboard(platform: str, country_code: str) -> InlineKeyboardMarkup:
    """
    ينشئ لوحة مفاتيح الأزرار لعرض السيرفرات المتاحة لمنصة ودولة محددتين.

    Args:
        platform (str): اسم المنصة.
        country_code (str): رمز كود الدولة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة بالسيرفرات.
    """
    servers = load_servers(platform, country_code)

    buttons = []
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    for i, server in enumerate(servers):
        emoji = emoji_cycle[i % len(emoji_cycle)]
        label = f"{emoji} {server['name']} - 💰 {server['price']} ر.س ({server.get('quantity', 0)} متاح)"
        callback = f"buy_{platform}_{country_code}_{server['id']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))
    return create_reply_markup(buttons)