# handlers/main_menu.py

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.main_menu_kb import main_menu_keyboard
from keyboards.utils_kb import create_reply_markup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

async def plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج الأمر /plus أو زر "العودة للقائمة الرئيسية" (في بعض السياقات).
    يعرض لوحة المفاتيح الرئيسية لاختيار المنصة.
    """
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    message = messages["choose_platform_to_use_number"] # # استخدام النص المترجم
    reply_markup = create_reply_markup(main_menu_keyboard(lang_code)) # # تمرير lang_code للوحة المفاتيح

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(message, reply_markup=reply_markup)
        except Exception: # يمكن تحسين هذا الاستثناء ليكون أكثر تحديداً لاحقاً
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(message, reply_markup=reply_markup)

async def go_to_buy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شراء رقم جديد".
    يعرض نفس لوحة المفاتيح الرئيسية لاختيار المنصة.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    await query.message.edit_text(
        messages["choose_platform_to_use_number"], # # استخدام النص المترجم
        reply_markup=create_reply_markup(main_menu_keyboard(lang_code)) # # تمرير lang_code للوحة المفاتيح
    )