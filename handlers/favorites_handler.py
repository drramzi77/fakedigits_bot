from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ✅ مفضلة المستخدمين (تجريبية)
USER_FAVORITES = {
    123456789: ["🇸🇦 WhatsApp - SA", "🇺🇸 Telegram - US"],
    987654321: ["🇪🇬 WhatsApp - EG"]
}

# ✅ عرض المفضلة
async def handle_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    favorites = USER_FAVORITES.get(user_id, [])

    if not favorites:
        await query.message.edit_text("⭐️ لا توجد أرقام مفضلة محفوظة لديك حالياً.")
        return

    text = "⭐️ <b>قائمة المفضلة الخاصة بك:</b>\n\n"
    for i, fav in enumerate(favorites, 1):
        text += f"{i}. {fav}\n"

    keyboard = [[InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# ✅ إضافة إلى المفضلة
async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data  # fav_<platform>_<country>
    try:
        _, platform, country_code = data.split("_")
    except ValueError:
        await query.message.reply_text("❌ تنسيق غير صالح.")
        return

    user_id = query.from_user.id
    flag = ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    entry = f"{flag} {platform} - {country_code.upper()}"

    # أضف إلى المفضلة إذا لم تكن موجودة
    if user_id not in USER_FAVORITES:
        USER_FAVORITES[user_id] = []

    if entry not in USER_FAVORITES[user_id]:
        USER_FAVORITES[user_id].append(entry)
        await query.message.reply_text("✅ تم إضافة الدولة إلى المفضلة.")
    else:
        await query.message.reply_text("ℹ️ هذه الدولة موجودة مسبقاً في مفضلتك.")
