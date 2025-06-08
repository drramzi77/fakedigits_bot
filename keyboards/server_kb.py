# keyboards/server_kb.py

import json
import logging
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # # أضف هذا السطر

logger = logging.getLogger(__name__)

SERVERS_FILE = "data/servers.json"

# ✅ تحميل بيانات السيرفرات كاملة من ملف JSON
def load_all_servers_data() -> list:
    try:
        if not os.path.exists(SERVERS_FILE):
            logger.warning(f"ملف السيرفرات '{SERVERS_FILE}' غير موجود. سيتم إنشاء قائمة فارغة.")
            return []
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للسيرفرات '{SERVERS_FILE}'. الملف قد يكون تالفًا.", exc_info=True)
        return []
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف السيرفرات '{SERVERS_FILE}' أثناء التحميل: {e}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تحميل بيانات السيرفرات: {e}", exc_info=True)
        return []

# ✅ حفظ بيانات السيرفرات كاملة إلى ملف JSON
def save_servers_data(data: list):
    try:
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"تم حفظ بيانات السيرفرات في '{SERVERS_FILE}'.")
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف السيرفرات '{SERVERS_FILE}' أثناء الحفظ: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند حفظ بيانات السيرفرات: {e}", exc_info=True)

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
    servers = load_servers(platform, country_code) # # هذه الدالة الآن ترجع فقط المتوفر

    buttons = []
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    for i, server in enumerate(servers):
        emoji = emoji_cycle[i % len(emoji_cycle)]
        # # نعرض الكمية المتبقية
        label = f"{emoji} {server['name']} - 💰 {server['price']} ر.س ({server.get('quantity', 0)} متاح)"
        callback = f"buy_{platform}_{country_code}_{server['id']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])
    return InlineKeyboardMarkup(buttons)