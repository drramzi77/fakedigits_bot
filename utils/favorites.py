# utils/favorites.py
import logging
import re # هذا السطر مطلوب لتحليل النص في دالة add_favorite
from sqlalchemy.orm import Session
from database.database import get_db
from services import favorite_service # # استيراد خدمة المفضلة

logger = logging.getLogger(__name__)

# # لم نعد بحاجة إلى FAV_FILE أو استيرادات JSON/os هنا
# import json
# import os
# from utils.data_manager import load_json_file, save_json_file
# FAV_FILE = os.path.join("data", "favorites.json")

def add_favorite(user_id: int, item: str):
    """
    يضيف عنصراً (دولة/منصة) إلى قائمة المفضلة لمستخدم معين باستخدام خدمة المفضلة.

    Args:
        user_id (int): معرف المستخدم.
        item (str): العنصر المراد إضافته إلى المفضلة (مثال: "🇸🇦 WhatsApp - SA").

    Returns:
        bool: True إذا تمت الإضافة بنجاح، False إذا كان العنصر موجوداً مسبقاً.
    """
    # # يجب تحليل الـ item string هنا للحصول على platform و country_code
    # # بناءً على التنسيق "🇸🇦 WhatsApp - SA"
    parts = item.split(' ')
    platform = "Unknown"
    country_code = "xx"
    
    # محاولة استخراج المنصة (مثال: WhatsApp, Telegram)
    if "WhatsApp" in item:
        platform = "WhatsApp"
    elif "Telegram" in item:
        platform = "Telegram"
    
    # البحث عن كود الدولة (حرفين بعد " - " في نهاية النص)
    match = re.search(r'- ([A-Za-z]{2})$', item)
    if match:
        country_code = match.group(1).lower() # تحويل لـ lowercase ليتناسب مع التخزين

    for db in get_db(): # # استخدام get_db للحصول على جلسة
        return favorite_service.add_user_favorite(db, user_id, platform, country_code, item)

def get_user_favorites(user_id: int):
    """
    يُرجع قائمة المفضلة لمستخدم معين من قاعدة البيانات.

    Args:
        user_id (int): معرف المستخدم.

    Returns:
        list: قائمة بالعناصر المفضلة للمستخدم (النصوص المعروضة)، أو قائمة فارغة إذا لم يكن لديه مفضلة.
    """
    for db in get_db(): # # استخدام get_db للحصول على جلسة
        favorites = favorite_service.get_favorites_by_user_id(db, user_id)
        return [fav.display_text for fav in favorites]