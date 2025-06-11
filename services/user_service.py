# services/user_service.py

import json
import os
import logging
from datetime import datetime
from utils.data_manager import load_json_file, save_json_file

logger = logging.getLogger(__name__)

USER_FILE = os.path.join("data", "users.json") # مسار ملف المستخدمين

def load_users() -> dict:
    """
    يُحمّل بيانات جميع المستخدمين من ملف JSON.
    Returns:
        dict: قاموس يحتوي على بيانات المستخدمين، أو قاموس فارغ إذا تعذر التحميل.
    """
    return load_json_file(USER_FILE, {})

def save_users(users: dict):
    """
    يُحفظ بيانات المستخدمين إلى ملف JSON.
    Args:
        users (dict): قاموس يحتوي على بيانات المستخدمين المراد حفظها.
    """
    save_json_file(USER_FILE, users)

def ensure_user_exists(user_id: int, user_info: dict):
    """
    يتأكد من وجود المستخدم في قاعدة البيانات (users.json)، ويضيفه إذا كان جديداً.
    يقوم بتحديث معلومات المستخدم الحالية (الاسم، اليوزرنيم) إذا تغيرت.
    Args:
        user_id (int): معرف المستخدم في تيليجرام.
        user_info (dict): قاموس يحتوي على معلومات المستخدم (مثل first_name, last_name, username, language_code).
    """
    users = load_users() # استخدام الدالة المحلية load_users
    user_id_str = str(user_id)

    if user_id_str not in users:
        users[user_id_str] = {
            "id": user_id,
            "first_name": user_info.get("first_name", "N/A"),
            "last_name": user_info.get("last_name", ""),
            "username": user_info.get("username", ""),
            "language_code": user_info.get("language_code", "N/A"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": 0.0, # الرصيد الافتراضي للمستخدم الجديد
            "banned": False
        }
        save_users(users) # استخدام الدالة المحلية save_users
        logger.info(f"تم تسجيل مستخدم جديد: {user_id_str} ({user_info.get('username')}).")
    else:
        current_user_data = users[user_id_str]
        updated = False
        if current_user_data.get("first_name") != user_info.get("first_name", "N/A"):
            current_user_data["first_name"] = user_info.get("first_name", "N/A")
            updated = True
        if current_user_data.get("last_name") != user_info.get("last_name", ""):
            current_user_data["last_name"] = user_info.get("last_name", "")
            updated = True
        if current_user_data.get("username") != user_info.get("username", ""):
            current_user_data["username"] = user_info.get("username", "")
            updated = True
        
        if updated:
            save_users(users) # استخدام الدالة المحلية save_users
            logger.info(f"تم تحديث معلومات المستخدم {user_id_str}.")