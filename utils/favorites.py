import json
import os
from utils.data_manager import load_json_file, save_json_file

FAV_FILE = os.path.join("data", "favorites.json")

def add_favorite(user_id: int, item: str):
    """
    يضيف عنصراً (دولة/منصة) إلى قائمة المفضلة لمستخدم معين.

    Args:
        user_id (int): معرف المستخدم.
        item (str): العنصر المراد إضافته إلى المفضلة (مثال: "🇸🇦 WhatsApp - SA").

    Returns:
        bool: True إذا تمت الإضافة بنجاح، False إذا كان العنصر موجوداً مسبقاً.
    """
    data = load_json_file(FAV_FILE, {})
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = []
    if item not in data[user_id]:
        data[user_id].append(item)
        save_json_file(FAV_FILE, data)
        return True
    return False

def get_user_favorites(user_id: int):
    """
    يُرجع قائمة المفضلة لمستخدم معين.

    Args:
        user_id (int): معرف المستخدم.

    Returns:
        list: قائمة بالعناصر المفضلة للمستخدم، أو قائمة فارغة إذا لم يكن لديه مفضلة.
    """
    data = load_json_file(FAV_FILE, {})
    return data.get(str(user_id), [])