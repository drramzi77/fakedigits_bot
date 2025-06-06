from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.category_kb import category_inline_keyboard
from keyboards.server_kb import load_servers, server_keyboard
from utils.balance import get_user_balance
from handlers.favorites_handler import add_to_favorites  # ✅ تم الاستيراد هنا
import json
import random

PLATFORMS = ["WhatsApp", "Telegram", "Snapchat", "Instagram", "Facebook", "TikTok"]

# ✅ اختيار المنصة
async def handle_platform_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("select_app_"):
        platform = data.replace("select_app_", "")
        context.user_data["selected_platform"] = platform
        await query.message.edit_text(
            f"🧭 أنت الآن في قسم: {platform}\nاختر نوع الرقم الذي ترغب به:",
            reply_markup=category_inline_keyboard(platform)
        )

# ✅ اختيار المنطقة (العرب، آسيا، إلخ)
async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from keyboards.countries_kb import countries_keyboard
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("region_"):
        _, region, platform = data.split("_")
        context.user_data["selected_platform"] = platform
        keyboard = countries_keyboard(region, platform)
        await query.message.edit_text(
            f"🌍 اختر الدولة التي تريد شراء رقم {platform} منها:",
            reply_markup=keyboard
        )

# ✅ اختيار الدولة
async def handle_country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, code, platform = query.data.split("_")
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    servers = load_servers(platform, code)

    if not servers:
        await query.message.edit_text("❗ لا توجد سيرفرات متاحة حاليًا لهذه الدولة.")
        return

    if balance < min(s['price'] for s in servers):
        await query.message.edit_text(f"❌ رصيدك غير كافٍ.\nرصيدك الحالي: {balance} ر.س")
        return

    buttons = []
    for s in servers:
        buttons.append([InlineKeyboardButton(
            f"{s['name']} - 💰 {s['price']} ر.س",
            callback_data=f"buy_{platform}_{code}_{s['id']}"
        )])

    # ✅ زر المفضلة
    buttons.append([InlineKeyboardButton("⭐️ أضف إلى المفضلة", callback_data=f"fav_{platform}_{code}")])
    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])

    await query.message.edit_text(
        f"✅ رصيدك الحالي: {balance} ر.س\n"
        f"عدد السيرفرات المتوفرة: {len(servers)}\n\n"
        "اختر السيرفر الذي ترغب بتجربته:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ تجربة الشراء
async def handle_fake_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, platform, country_code, server_id = query.data.split("_")
    servers = load_servers(platform, country_code)
    selected = next((s for s in servers if str(s["id"]) == server_id), None)

    if not selected:
        await query.message.edit_text("⚠️ لم يتم العثور على السيرفر.")
        return

    await query.message.edit_text(
        f"✅ <b>شراء رقم جديد</b>\n\n"
        f"📱 <b>التطبيق:</b> {platform}\n"
        f"🌍 <b>الدولة:</b> {country_code.upper()}\n"
        f"💾 <b>السيرفر:</b> {selected['name']}\n"
        f"💰 <b>السعر:</b> {selected['price']} ر.س\n\n"
        f"⚠️ هذه تجربة فقط، لم يتم خصم أي رصيد.",
        parse_mode="HTML"
    )

# ✅ اختيار الدولة العشوائية
async def handle_random_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data.replace("random_", "")
    user_id = query.from_user.id
    balance = get_user_balance(user_id)

    with open("data/servers.json", encoding="utf-8") as f:
        all_data = json.load(f)

    candidates = [s for s in all_data if s["platform"] == platform and s["servers"]]
    if not candidates:
        await query.message.edit_text("❌ لا توجد أرقام متوفرة.")
        return

    selected = random.choice(candidates)
    country_code = selected["country"]

    if balance < min(s['price'] for s in selected["servers"]):
        await query.message.edit_text(f"❌ رصيدك غير كافٍ.\nرصيدك الحالي: {balance} ر.س")
        return

    buttons = []
    for s in selected["servers"]:
        buttons.append([InlineKeyboardButton(
            f"{s['name']} - 💰 {s['price']} ر.س",
            callback_data=f"buy_{platform}_{country_code}_{s['id']}"
        )])
    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])

    await query.message.edit_text(
        f"🎲 تم اختيار دولة عشوائية: {country_code.upper()}\n"
        f"✅ رصيدك الحالي: {balance} ر.س\n"
        "اختر السيرفر المناسب:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ الدول المتوفرة فقط
async def handle_most_available_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data.replace("most_", "")

    with open("data/servers.json", encoding="utf-8") as f:
        all_data = json.load(f)

    countries = [s["country"] for s in all_data if s["platform"] == platform and s["servers"]]
    if not countries:
        await query.message.edit_text("❗ لا توجد أرقام متوفرة حالياً.")
        return

    buttons = [[InlineKeyboardButton(f"{code.upper()}", callback_data=f"country_{code}_{platform}")]
               for code in sorted(set(countries))]
    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data=f"select_app_{platform}")])

    await query.message.edit_text(
        f"📦 الدول المتوفرة لـ {platform}:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ إدخال يدوي مثل WhatsApp
async def handle_platform_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    mapping = {
        "whatsapp": "WhatsApp",
        "telegram": "Telegram",
        "snapchat": "Snapchat",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "tiktok": "TikTok"
    }
    platform = mapping.get(text)
    if not platform:
        await update.message.reply_text("❌ لم يتم التعرف على المنصة.")
        return

    await update.message.reply_text(
        f"🧭 أنت الآن في قسم: {platform}\nاختر نوع الرقم الذي ترغب به:",
        reply_markup=category_inline_keyboard(platform)
    )

# ✅ دالة تحويل رمز الدولة إلى علم
def get_flag(country_code):
    try:
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    except:
        return "🏳️"

# ✅ زر المنصات المتاحة الآن
async def show_available_platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    with open("data/servers.json", encoding="utf-8") as f:
        data = json.load(f)

    platforms = {}
    for entry in data:
        platform = entry["platform"]
        country = entry["country"]
        if entry["servers"]:
            if platform not in platforms:
                platforms[platform] = set()
            platforms[platform].add(country)

    if not platforms:
        await query.message.edit_text("❌ لا توجد منصات متاحة حالياً.")
        return

    buttons = []
    for platform, countries in platforms.items():
        flag_line = " ".join(get_flag(code) for code in sorted(countries))
        buttons.append([
            InlineKeyboardButton(f"✅ {platform} - {len(countries)} دولة", callback_data=f"select_app_{platform}")
        ])
        buttons.append([
            InlineKeyboardButton(flag_line, callback_data=f"select_app_{platform}")
        ])

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")])

    await query.message.edit_text(
        "📲 <b>المنصات المتاحة الآن:</b>\nاختر المنصة لرؤية الأرقام المتوفرة:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )

# ✅ عرض الأرقام الفورية الجاهزة
async def show_ready_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    balance = get_user_balance(user_id)

    with open("data/servers.json", encoding="utf-8") as f:
        all_data = json.load(f)

    # جلب أرخص رقم لكل منصة (أو أفضل سيرفرات)
    ready_numbers = []
    for item in all_data:
        platform = item["platform"]
        country = item["country"]
        servers = item["servers"]
        if servers:
            cheapest = min(servers, key=lambda s: s["price"])
            ready_numbers.append({
                "platform": platform,
                "country": country,
                "flag": get_flag(country),
                "server": cheapest
            })

    # ترتيب الأرقام حسب السعر
    ready_numbers.sort(key=lambda x: x["server"]["price"])

    buttons = []
    for item in ready_numbers[:10]:  # عرض أول 10 فقط للتجربة
        btn_text = f"{item['flag']} {item['country']} - {item['platform']} 💰 {item['server']['price']} ر.س"
        callback = f"buy_{item['platform']}_{item['country']}_{item['server']['id']}"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=callback)])

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")])

    await query.message.edit_text(
        "⚡ <b>أرقام فورية جاهزة:</b>\nاختر رقمًا للشراء الفوري:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )
