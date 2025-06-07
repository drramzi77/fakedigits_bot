# handlers/input_router.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

# # استيراد جميع دوال معالجة المدخلات النصية الممكنة
from handlers.transfer_handler import handle_transfer_input as transfer_handler
from handlers.admin_users import receive_balance_input as balance_input_handler
from handlers.admin_users import handle_admin_search as admin_search_handler
from handlers.quick_search_handler import handle_text_input as quick_search_text_handler

logger = logging.getLogger(__name__)

async def handle_all_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    awaiting_input_type = context.user_data.get("awaiting_input", "none")

    logger.info(f"handle_all_text_input: المستخدم {user_id} أرسل نص: '{user_message}'. نوع المدخل المنتظر: '{awaiting_input_type}'. user_data: {context.user_data}")

    if awaiting_input_type == "transfer_amount":
        context.user_data["awaiting_input"] = "none" 
        await transfer_handler(update, context)
    elif awaiting_input_type == "admin_balance_edit":
        context.user_data["awaiting_input"] = "none"
        await balance_input_handler(update, context)
    elif awaiting_input_type == "admin_user_search":
        context.user_data["awaiting_input"] = "none"
        await admin_search_handler(update, context)
    elif awaiting_input_type == "quick_search_country_general":
        # # لا نقوم بمسح awaiting_input هنا، بل داخل handle_text_input نفسها
        await quick_search_text_handler(update, context)
    else:
        logger.warning(f"handle_all_text_input: المستخدم {user_id} أرسل نصًا غير متوقع: '{user_message}'. لا يوجد نوع إدخال منتظر.")
        await update.message.reply_text("👋 عفواً، لم أفهم طلبك. يرجى استخدام الأوامر أو الأزرار المتاحة.")
    
    return True