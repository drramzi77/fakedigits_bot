import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance
from utils.data_manager import load_json_file # ✅ تم إضافة هذا السطر

# ✅ دالة لتحويل كود الدولة إلى علم تلقائي
def get_flag(country_code):
    try:
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    except:
        return "🏳️"

# ✅ إنشاء أزرار عروض المنصة (واتساب / تليجرام)
def generate_offer_buttons(platform):
    data = load_json_file("data/servers.json", []) # ✅ تم التعديل

    country_prices = {}
    for item in data:
        if item["platform"].lower() != platform.lower():
            continue
        country = item["country"]
        for server in item.get("servers", []):
            price = server["price"]
            if country not in country_prices or price < country_prices[country]:
                country_prices[country] = price

    buttons = []
    row = []
    for i, (country_code, price) in enumerate(country_prices.items()):
        flag = get_flag(country_code)
        row.append(InlineKeyboardButton(
            f"{flag} {country_code.upper()} - {int(price)}P 🚀",
            callback_data=f"country_{country_code}_{platform}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")])
    return InlineKeyboardMarkup(buttons)

# ✅ دالة عرض عروض المنصة
async def show_platform_offers(update: Update, context: ContextTypes.DEFAULT_TYPE, platform: str):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    all_data = load_json_file("data/servers.json", []) # ✅ تم التعديل

    available_countries = {
        item["country"] for item in all_data if item["platform"].lower() == platform.lower()
    }

    flags_line = " ".join([get_flag(c) for c in sorted(available_countries)])

    text = (
        f"🔥⚡ <b>عروض {platform}</b>\n\n"
        f"💰 <b>رصيدك:</b> {balance} ر.س\n"
        f"🌍 <b>الدول المتوفرة حالياً:</b>\n{flags_line}\n"
        "━━━━━━━━━━━━━━━"
    )

    await update.callback_query.message.edit_text(
        text, reply_markup=generate_offer_buttons(platform), parse_mode="HTML"
    )

# ✅ handler لعروض واتساب
async def show_whatsapp_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await show_platform_offers(update, context, "WhatsApp")

# ✅ handler لعروض تليجرام
async def show_telegram_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await show_platform_offers(update, context, "Telegram")

# ✅ handler لعروض الأرقام العامة
async def show_general_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    text = (
        "🎯 <b>عروض الأرقام المتوفرة:</b>\n\n"
        "✅ عروض واتساب وتليجرام في جميع الدول\n"
        "✅ أقل الأسعار لأفضل جودة\n\n"
        "👇 اختر المنصة التي تريد رؤية عروضها:"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎯 عروض واتساب", callback_data="wa_offers"),
            InlineKeyboardButton("🎯 عروض تليجرام", callback_data="tg_offers")
        ],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ])

    await update.callback_query.message.edit_text(text, reply_markup=buttons, parse_mode="HTML")