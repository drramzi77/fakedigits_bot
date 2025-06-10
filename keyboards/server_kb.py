# keyboards/server_kb.py

import json
import logging
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from utils.data_manager import load_json_file, save_json_file # # هذه الدوال ستتغير لاحقاً مع DB
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

logger = logging.getLogger(__name__)

SERVERS_FILE = os.path.join("data", "servers.json") # # هذا المسار سيتغير لاحقاً مع DB

def load_all_servers_data() -> list:
    """
    يُحمّل بيانات جميع السيرفرات المتاحة من ملف JSON.

    Returns:
        list: قائمة بقواميس بيانات السيرفرات.
    """
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    return load_json_file(SERVERS_FILE, [])

def save_servers_data(data: list):
    """
    يُحفظ بيانات السيرفرات إلى ملف JSON.

    Args:
        data (list): قائمة بقواميس بيانات السيرفرات المراد حفظها.
    """
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
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
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    all_data = load_all_servers_data()
    for entry in all_data:
        if entry["platform"] == platform and entry["country"] == country_code:
            # # هنا نضيف الفلترة: نرجع السيرفرات التي كميتها > 0 فقط
            available_servers = [s for s in entry.get("servers", []) if s.get("quantity", 0) > 0]
            return available_servers
    return []

def server_keyboard(platform: str, country_code: str, lang_code: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup: # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح الأزرار لعرض السيرفرات المتاحة لمنصة ودولة محددتين.

    Args:
        platform (str): اسم المنصة.
        country_code (str): رمز كود الدولة.
        lang_code (str): كود اللغة لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة بالسيرفرات.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة
    servers = load_servers(platform, country_code)

    buttons = []
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    for i, server in enumerate(servers):
        emoji = emoji_cycle[i % len(emoji_cycle)]
        # # استخدام النص المترجم لـ "price_currency" و "available_quantity"
        label = messages["server_button_label"].format(
            emoji=emoji,
            server_name=server['name'],
            price=server['price'],
            currency=messages["price_currency"], # # استخدام نص العملة المترجم
            quantity=server.get('quantity', 0),
            available_text=messages["available_quantity"] # # استخدام نص "متاح" المترجم
        )
        callback = f"buy_{platform}_{country_code}_{server['id']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    # # استخدام النص المترجم لزر العودة
    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}"))
    return create_reply_markup(buttons)