from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.language_kb import language_keyboard
from handlers.main_dashboard import show_dashboard
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE, REQUIRED_CHANNELS
from utils.check_subscription import is_user_subscribed

def subscription_buttons(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة أزرار تحقق الاشتراك.
    """
    messages = get_messages(lang_code)
    buttons = [[InlineKeyboardButton(messages["check_subscription_button"], callback_data="check_sub")]]
    for ch in REQUIRED_CHANNELS:
        buttons.append([InlineKeyboardButton(f"📢 {messages['subscribe_to_channel']} {ch}", url=f"https://t.me/{ch.lstrip('@')}")])
    return InlineKeyboardMarkup(buttons)

async def show_language_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض خيارات اختيار لغة البوت للمستخدم.
    """
    query = update.callback_query
    await query.answer()

    # تحديد لغة المستخدم الحالية لجلب نصوص الأزرار بشكل صحيح
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    await query.message.edit_text(
        messages["select_your_language"],
        reply_markup=language_keyboard(lang_code)
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج تعيين لغة البوت المفضلة للمستخدم.
    بعد التعيين، يتحقق من الاشتراك، ويعرض لوحة التحكم أو يطلب الاشتراك.
    """
    query = update.callback_query
    await query.answer()

    lang_code_selected = query.data.replace("set_lang_", "")
    context.user_data["lang_code"] = lang_code_selected
    messages = get_messages(lang_code_selected)

    # تحقق من الاشتراك بعد اختيار اللغة
    if await is_user_subscribed(update, context):
        await query.edit_message_text(messages["subscribed_success"])
        await show_dashboard(update, context)
    else:
        await query.edit_message_text(
            messages["not_subscribed_channel"].format(channel_link=REQUIRED_CHANNELS[0]),
            reply_markup=subscription_buttons(lang_code_selected)
        )
