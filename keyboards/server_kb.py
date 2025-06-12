# keyboards/server_kb.py

import logging
# import json # لم نعد بحاجة لها
# import os # لم نعد بحاجة لها
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from utils.data_manager import load_json_file, save_json_file # لم نعد بحاجة لها
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
# # استيراد خدمة السيرفرات ودالة get_db
from services import server_service
from database.database import get_db

logger = logging.getLogger(__name__)

# # لم نعد بحاجة لـ SERVERS_FILE
# SERVERS_FILE = os.path.join("data", "servers.json")

# # هذه الدوال لم تعد ضرورية بعد الانتقال إلى services/server_service
# def load_all_servers_data() -> list:
#     """
#     هذه الدالة لم تعد مستخدمة بعد الانتقال إلى قاعدة البيانات.
#     """
#     pass

# def save_servers_data(data: list):
#     """
#     هذه الدالة لم تعد مستخدمة بعد الانتقال إلى قاعدة البيانات.
#     """
#     pass

def load_servers(platform: str, country_code: str) -> list:
    """
    يُحمّل السيرفرات المتاحة لمنصة ودولة معينتين من قاعدة البيانات.

    Args:
        platform (str): اسم المنصة (مثال: "WhatsApp").
        country_code (str): رمز كود الدولة (مثال: "sa").

    Returns:
        list: قائمة بكائنات Server المتوفرة التي تتطابق مع المعايير.
    """
    for db in get_db(): # # استخدام get_db للحصول على جلسة
        # # استخدام server_service لجلب السيرفرات
        return server_service.get_servers_by_platform_and_country(db, platform, country_code)
    return [] # إرجاع قائمة فارغة إذا لم يتمكن من الحصول على جلسة أو أي خطأ


def server_keyboard(platform: str, country_code: str, lang_code: str = DEFAULT_LANGUAGE) -> InlineKeyboardMarkup:
    """
    ينشئ لوحة مفاتيح الأزرار لعرض السيرفرات المتاحة لمنصة ودولة محددتين.

    Args:
        platform (str): اسم المنصة.
        country_code (str): رمز كود الدولة.
        lang_code (str): كود اللغة لعرض النصوص الصحيحة.

    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح المضمّنة بالسيرفرات.
    """
    messages = get_messages(lang_code)
    servers = load_servers(platform, country_code) # # استخدام دالة load_servers المحلية التي تستخدم service

    buttons = []
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    if not servers:
        # إذا لم تكن هناك سيرفرات متاحة، اعرض رسالة مناسبة وزر العودة.
        # هذا السيناريو يجب أن يكون قد تم التعامل معه في category_handler
        # ولكن للتأكد، يمكن إضافة رسالة احتياطية هنا.
        buttons.append([InlineKeyboardButton(messages["no_servers_available_general"], callback_data=f"select_app_{platform}")])
    else:
        for i, server in enumerate(servers): # # التكرار على كائنات Server
            emoji = emoji_cycle[i % len(emoji_cycle)]
            label = messages["server_button_label"].format(
                emoji=emoji,
                server_name=server.server_name, # # الوصول لـ .server_name
                price=server.price, # # الوصول لـ .price
                currency=messages["price_currency"],
                quantity=server.quantity, # # الوصول لـ .quantity
                available_text=messages["available_quantity"]
            )
            callback = f"buy_{platform}_{country_code}_{server.server_id}" # # استخدام .server_id
            buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}"))
    return create_reply_markup(buttons)