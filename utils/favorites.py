import json
import os

FAV_FILE = "data/favorites.json"

def load_favorites():
    if not os.path.exists(FAV_FILE):
        return {}
    with open(FAV_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_favorites(data):
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_favorite(user_id: int, item: str):
    data = load_favorites()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = []
    if item not in data[user_id]:
        data[user_id].append(item)
        save_favorites(data)
        return True
    return False

def get_user_favorites(user_id: int):
    data = load_favorites()
    return data.get(str(user_id), [])
