# handlers/favorites_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.favorites import add_favorite, get_user_favorites
from keyboards.utils_kb import back_button, create_reply_markup

async def handle_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة الدول المفضلة المحفوظة للمستخدم.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    favorites = get_user_favorites(user_id)

    if not favorites:
        await query.message.edit_text("⭐️ لا توجد أرقام مفضلة محفوظة لديك حالياً.")
        return

    text = "⭐️ <b>قائمة المفضلة الخاصة بك:</b>\n\n"
    for i, fav in enumerate(favorites, 1):
        text += f"{i}. {fav}\n"

    keyboard = create_reply_markup([
        back_button()
    ])
    await query.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج إضافة دولة إلى قائمة المفضلة الخاصة بالمستخدم.
    """
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

    if add_favorite(user_id, entry):
        await query.message.reply_text("✅ تم إضافة الدولة إلى المفضلة.")
    else:
        await query.message.reply_text("ℹ️ هذه الدولة موجودة مسبقاً في مفضلتك.")