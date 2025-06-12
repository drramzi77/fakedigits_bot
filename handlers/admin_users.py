# handlers/admin_users.py
# import json # لم نعد بحاجة لها
import logging
# import os # لم نعد بحاجة لها
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.main_dashboard import show_dashboard
# from utils.data_manager import load_json_file, save_json_file # لم نعد بحاجة لها
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import ADMINS, DEFAULT_LANGUAGE
# # استيراد خدمة المستخدم ودالة الحصول على الجلسة
from services import user_service
from database.database import get_db

logger = logging.getLogger(__name__)

# # لم نعد بحاجة لـ USER_FILE أو load_users/save_users القديمة
# USER_FILE = os.path.join("data", "users.json") 
# # تم حذف تعريف load_users من هنا
# # تم حذف تعريف save_users من هنا
# # تم حذف تعريف ensure_user_exists من هنا

async def handle_admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج عرض لوحة إدارة المستخدمين للمشرفين.
    يسمح بالبحث عن المستخدمين وعرض معلوماتهم الأساسية.
    """
    query = update.callback_query
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if query:
        await query.answer()
        context.user_data["awaiting_input"] = "admin_user_search"

    all_users = []
    for db in get_db(): # # استخدام get_db للحصول على جلسة
        all_users = user_service.get_all_users_data(db) # # استخدام خدمة المستخدم لجلب جميع المستخدمين

    search_term = context.user_data.get("admin_search", "").lower()
    results = []

    for user_obj in all_users: # # التكرار على كائنات المستخدم مباشرة
        uid = str(user_obj.id)
        display_name = f"{user_obj.first_name or ''} {user_obj.last_name or ''}".strip()
        if not display_name:
            display_name = messages["user_fallback_name"].format(user_id=uid)

        if search_term in uid.lower() or \
           (display_name and search_term in display_name.lower()) or \
           (user_obj.username and search_term in user_obj.username.lower()):
            results.append((uid, display_name, user_obj.balance, user_obj.banned)) # # الوصول إلى الخصائص مباشرة

    if not results:
        message_text = messages["no_matching_users"]
        reply_markup = create_reply_markup([
            back_button(text=messages["back_button_text"], callback_data="back_to_dashboard_clear_admin_search", lang_code=lang_code)
        ])
        if query:
            await query.edit_message_text(message_text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        logger.info(f"لا يوجد مستخدمون مطابقون لـ '{search_term}'.")
        context.user_data.pop("awaiting_input", None)
        return

    text = messages["admin_user_management_title"] + "\n\n"
    buttons = []

    for uid, name, balance, banned in results[:10]: # # عرض أول 10 نتائج
        ban_status = messages["banned_status"] if banned else messages["active_status"]
        text += messages["admin_user_info_line"].format(
            name=name,
            user_id=uid,
            balance=balance,
            currency=messages["price_currency"],
            status=ban_status
        ) + "\n\n"
        row = [
            InlineKeyboardButton(messages["edit_user_button"], callback_data=f"edit_{uid}"),
            InlineKeyboardButton(messages["unban_button"] if not banned else messages["ban_button"], callback_data=f"toggleban_{uid}"),
            InlineKeyboardButton(messages["delete_user_button"], callback_data=f"confirm_delete_{uid}")
        ]
        buttons.append(row)

    buttons.append(back_button(text=messages["back_button_text"], callback_data="back_to_dashboard_clear_admin_search", lang_code=lang_code))

    if query:
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=create_reply_markup(buttons))
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=create_reply_markup(buttons))
    logger.info(f"تم عرض قائمة المستخدمين الإدارية لـ '{search_term}'.")


async def handle_admin_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج البحث عن المستخدمين داخل لوحة إدارة المشرفين.
    يتم تفعيله عندما يكون awaiting_input="admin_user_search".
    """
    user_id = update.effective_user.id
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.message.reply_text(messages["not_admin_search_permission"])
        logger.warning(f"المستخدم {user_id} حاول البحث في قائمة المستخدمين بدون صلاحية.")
        context.user_data.pop("awaiting_input", None)
        return

    context.user_data["admin_search"] = update.message.text.strip()
    logger.info(f"المشرف {user_id} يبحث عن: '{context.user_data['admin_search']}'.")
    await handle_admin_users(update, context)
    context.user_data.pop("admin_search_mode", None)
    context.user_data.pop("admin_search", None)
    context.user_data.pop("awaiting_input", None)


async def handle_edit_user_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يبدأ عملية تعديل رصيد مستخدم معين.
    يطلب من المشرف إدخال الرصيد الجديد.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    user_id_to_edit = query.data.split("_")[1]
    context.user_data["editing_user_id"] = user_id_to_edit
    context.user_data["awaiting_input"] = "admin_balance_edit"
    context.user_data.pop("admin_search_mode", None)
    context.user_data.pop("admin_search", None)
    logger.info(f"المشرف {update.effective_user.id} بدأ تعديل رصيد المستخدم: {user_id_to_edit}.")

    await query.edit_message_text(
        messages["enter_new_balance"].format(user_id=user_id_to_edit),
        parse_mode="HTML"
    )

async def receive_balance_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يستقبل قيمة الرصيد الجديدة من المشرف ويقوم بتحديثها للمستخدم المستهدف.
    يتم تفعيله عندما يكون awaiting_input="admin_balance_edit".
    """
    new_balance_str = update.message.text.strip()
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if not new_balance_str.replace('.', '', 1).isdigit():
        await update.message.reply_text(messages["invalid_balance_input"])
        logger.warning(f"المشرف {user_id} أدخل رصيدًا غير صالح: '{new_balance_str}'.")
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("editing_user_id", None)
        return

    try:
        new_balance = float(new_balance_str)
    except ValueError:
        await update.message.reply_text(messages["balance_conversion_error"])
        logger.error(f"خطأ في تحويل '{new_balance_str}' إلى رقم عشري بواسطة المشرف {user_id}.", exc_info=True)
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("editing_user_id", None)
        return

    user_id_to_edit = int(context.user_data.get("editing_user_id")) # # تحويل معرف المستخدم إلى int

    for db in get_db(): # # استخدام get_db
        updated_user = user_service.update_user(db, user_id_to_edit, balance=round(new_balance, 2)) # # استخدام خدمة المستخدم للتحديث
        if updated_user:
            await update.message.reply_text(messages["balance_update_success"].format(user_id=user_id_to_edit, new_balance=new_balance, currency=messages["price_currency"]))
            logger.info(f"المشرف {user_id} عدّل رصيد المستخدم {user_id_to_edit} إلى {new_balance}.")
        else:
            await update.message.reply_text(messages["user_not_found_for_edit"])
            logger.warning(f"المشرف {user_id} حاول تعديل رصيد مستخدم غير موجود: {user_id_to_edit}.")

    context.user_data.pop("edit_balance_mode", None)
    context.user_data.pop("editing_user_id", None)
    context.user_data.pop("awaiting_input", None)

async def handle_block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج حظر المستخدم أو فك الحظر عنه.
    يتم تفعيله من لوحة إدارة المستخدمين.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    user_id_to_toggle = int(query.data.split("_")[1]) # # تحويل معرف المستخدم إلى int
    admin_id = update.effective_user.id

    for db in get_db(): # # استخدام get_db
        user_obj = user_service.get_user(db, user_id_to_toggle) # # جلب المستخدم أولاً
        if user_obj:
            current_status = user_obj.banned # # الوصول لـ .banned مباشرة
            updated_user = user_service.update_user(db, user_id_to_toggle, banned=not current_status) # # تحديث الحالة
            if updated_user:
                new_status_text = messages["unbanned_text"] if not current_status else messages["banned_text"]
                await query.edit_message_text(messages["user_status_updated"].format(user_id=user_id_to_toggle, new_status=new_status_text))
                logger.info(f"المشرف {admin_id} قام بـ {new_status_text} المستخدم {user_id_to_toggle}.")
            else:
                await query.edit_message_text(messages["user_not_found"]) # في حال فشل التحديث بعد جلب المستخدم
                logger.warning(f"المشرف {admin_id} حاول حظر/فك حظر مستخدم غير موجود (بعد جلب): {user_id_to_toggle}.")
        else:
            await query.edit_message_text(messages["user_not_found"])
            logger.warning(f"المشرف {admin_id} حاول حظر/فك حظر مستخدم غير موجود: {user_id_to_toggle}.")


async def confirm_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يطلب تأكيد حذف المستخدم من المشرف قبل التنفيذ النهائي.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    user_id_to_delete = query.data.split("_")[2]
    admin_id = update.effective_user.id

    keyboard = create_reply_markup([
        [
            InlineKeyboardButton(messages["yes_delete_button"], callback_data=f"delete_user_confirmed_{user_id_to_delete}"),
            InlineKeyboardButton(messages["cancel_button"], callback_data="admin_users")
        ]
    ])

    await query.message.edit_text(
        messages["confirm_delete_user_message"].format(user_id=user_id_to_delete),
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    logger.warning(f"المشرف {admin_id} طلب تأكيد حذف المستخدم {user_id_to_delete}.")


async def handle_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    ينفذ حذف المستخدم بشكل دائم من قاعدة البيانات بعد التأكيد.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    user_id_to_delete = int(query.data.split("_")[3]) # # تحويل معرف المستخدم إلى int
    admin_id = update.effective_user.id

    for db in get_db(): # # استخدام get_db
        success = user_service.delete_user(db, user_id_to_delete) # # استخدام خدمة المستخدم للحذف
        if success:
            await query.edit_message_text(messages["user_deleted_success"].format(user_id=user_id_to_delete))
            logger.info(f"المشرف {admin_id} قام بحذف المستخدم {user_id_to_delete} بعد التأكيد.")
        else:
            await query.edit_message_text(messages["user_not_found"])
            logger.warning(f"المشرف {admin_id} حاول حذف مستخدم غير موجود بعد التأكيد: {user_id_to_delete}.")

async def back_to_dashboard_clear_admin_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعيد المشرف إلى لوحة التحكم الرئيسية بعد مسح أي وضع بحث إداري نشط.
    """
    query = update.callback_query
    await query.answer()
    context.user_data.pop("admin_search_mode", None)
    context.user_data.pop("admin_search", None)
    context.user_data.pop("awaiting_input", None)
    await show_dashboard(update, context)