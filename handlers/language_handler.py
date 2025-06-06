from telegram import Update
from telegram.ext import ContextTypes
from keyboards.language_kb import language_keyboard
from handlers.main_dashboard import show_dashboard

async def show_language_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "🌐 اختر اللغة التي تفضل استخدامها في البوت:\n\nChoose the bot language:",
        reply_markup=language_keyboard()
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data  # set_lang_ar أو set_lang_en
    context.user_data["lang"] = "ar" if "ar" in lang else "en"

    msg = "✅ تم تعيين اللغة إلى العربية." if "ar" in lang else "✅ Language set to English."
    await query.answer()
    await query.message.edit_text(msg)

    # العودة إلى القائمة الرئيسية
    await show_dashboard(update, context)
