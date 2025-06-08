# handlers/main_menu.py

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.main_menu_kb import main_menu_keyboard
from keyboards.utils_kb import create_reply_markup # ✅ تم إضافة هذا السطر

# عند استخدام /plus أو زر العودة للقائمة السابقة
async def plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "اختر المنصة التي تريد استخدام الرقم فيها:"
    reply_markup = create_reply_markup(main_menu_keyboard()) # ✅ تم التعديل

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(message, reply_markup=reply_markup)
        except Exception:
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(message, reply_markup=reply_markup)

# ✅ جديد: ربط زر "شراء رقم" بالقائمة نفسها
async def go_to_buy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "اختر المنصة التي تريد استخدام الرقم فيها:",
        reply_markup=create_reply_markup(main_menu_keyboard()) # ✅ تم التعديل
    )