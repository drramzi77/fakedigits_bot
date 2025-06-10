# handlers/input_router.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

# # استيراد جميع دوال معالجة المدخلات النصية الممكنة
from handlers.transfer_handler import handle_transfer_input as transfer_handler
from handlers.admin_users import receive_balance_input as balance_input_handler
from handlers.admin_users import handle_admin_search as admin_search_handler
from handlers.quick_search_handler import handle_text_input as quick_search_text_handler

logger = logging.getLogger(__name__)

async def handle_all_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج عام لجميع المدخلات النصية غير الأوامر.
    يقوم بتوجيه الرسالة إلى المعالج المناسب بناءً على حالة المستخدم المخزنة.
    """
    user_id = update.effective_user.id
    user_message = update.message.text

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    awaiting_input_type = context.user_data.get("awaiting_input", "none")

    logger.info(f"handle_all_text_input: المستخدم {user_id} أرسل نص: '{user_message}'. نوع المدخل المنتظر: '{awaiting_input_type}'. user_data: {context.user_data}")

    if awaiting_input_type == "transfer_amount":
        await transfer_handler(update, context)
    elif awaiting_input_type == "admin_balance_edit":
        await balance_input_handler(update, context)
    elif awaiting_input_type == "admin_user_search":
        await admin_search_handler(update, context)
    elif awaiting_input_type == "quick_search_country_general":
        await quick_search_text_handler(update, context)
    else:
        logger.warning(f"handle_all_text_input: المستخدم {user_id} أرسل نصًا غير متوقع: '{user_message}'. لا يوجد نوع إدخال منتظر.")
        await update.message.reply_text(messages["unrecognized_text_input"]) # # استخدام النص المترجم
        context.user_data.pop("awaiting_input", None) # ✅ مسح الحالة عند رسالة غير متوقعة