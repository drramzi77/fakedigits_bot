# keyboards/server_kb.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import json

# ✅ تحميل السيرفرات من ملف JSON
def load_servers(platform: str, country_code: str) -> list:
    with open("data/servers.json", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        if entry["platform"] == platform and entry["country"] == country_code:
            return entry.get("servers", [])
    return []

# ✅ إنشاء لوحة السيرفرات بأيقونات مميزة
def server_keyboard(platform: str, country_code: str) -> InlineKeyboardMarkup:
    servers = load_servers(platform, country_code)
    emoji_cycle = ["⚡", "🎯", "💎", "🚀", "🎲", "🧩"]

    buttons = []
    for i, server in enumerate(servers):
        emoji = emoji_cycle[i % len(emoji_cycle)]
        label = f"{emoji} {server['name']} - 💰 {server['price']} ر.س"
        callback = f"buy_{platform}_{country_code}_{server['id']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])
    return InlineKeyboardMarkup(buttons)
