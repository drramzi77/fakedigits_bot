# handlers/offers_handler.py
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance
from utils.data_manager import load_json_file

def get_flag(country_code):
    """
    يحول رمز كود الدولة (مثل 'sa') إلى رمز تعبيري للعلم (مثل '🇸🇦').
    """
    try:
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    except:
        return "🏳️"

def generate_offer_buttons(platform):
    """
    ينشئ لوحة مفاتيح الأزرار لعروض دولة معينة لمنصة محددة.
    يعرض أرخص سعر لكل دولة متوفرة.
    """
    data = load_json_file("data/servers.json", [])

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

async def show_platform_offers(update: Update, context: ContextTypes.DEFAULT_TYPE, platform: str):
    """
    يعرض عروض الأرقام لمنصة محددة (مثل WhatsApp أو Telegram).
    """
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    all_data = load_json_file("data/servers.json", [])

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

async def show_whatsapp_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض واتساب" لعرض العروض الخاصة بالمنصة.
    """
    await update.callback_query.answer()
    await show_platform_offers(update, context, "WhatsApp")

async def show_telegram_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض تليجرام" لعرض العروض الخاصة بالمنصة.
    """
    await update.callback_query.answer()
    await show_platform_offers(update, context, "Telegram")

async def show_general_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض صفحة العروض العامة، ويطلب من المستخدم اختيار منصة محددة لرؤية عروضها.
    """
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