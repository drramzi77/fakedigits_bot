# handlers/admin_users.py
import json
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, set_user_balance
from handlers.main_dashboard import show_dashboard
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup

logger = logging.getLogger(__name__)

# 📁 مسار ملف المستخدمين
USER_FILE = os.path.join("data", "users.json")

def load_users():
    """
    يُحمّل بيانات جميع المستخدمين من ملف JSON.

    Returns:
        dict: قاموس يحتوي على بيانات المستخدمين، أو قاموس فارغ إذا تعذر التحميل.
    """
    return load_json_file(USER_FILE, {})

def save_users(users):
    """
    يُحفظ بيانات المستخدمين إلى ملف JSON.

    Args:
        users (dict): قاموس يحتوي على بيانات المستخدمين المراد حفظها.
    """
    save_json_file(USER_FILE, users)

def ensure_user_exists(user_id: int, user_info: dict):
    """
    يتأكد من وجود المستخدم في قاعدة البيانات (users.json)، ويضيفه إذا كان جديداً.
    يقوم بتحديث معلومات المستخدم الحالية (الاسم، اليوزرنيم) إذا تغيرت.

    Args:
        user_id (int): معرف المستخدم في تيليجرام.
        user_info (dict): قاموس يحتوي على معلومات المستخدم (مثل first_name, last_name, username, language_code).
    """
    users = load_json_file(USER_FILE, {})
    user_id_str = str(user_id)

    if user_id_str not in users:
        users[user_id_str] = {
            "id": user_id,
            "first_name": user_info.get("first_name", "N/A"),
            "last_name": user_info.get("last_name", ""),
            "username": user_info.get("username", ""),
            "language_code": user_info.get("language_code", "N/A"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": 0.0,
            "banned": False
        }
        save_json_file(USER_FILE, users)
        logger.info(f"تم تسجيل مستخدم جديد: {user_id_str} ({user_info.get('username')}).")
    else:
        current_user_data = users[user_id_str]
        updated = False
        if current_user_data.get("first_name") != user_info.get("first_name", "N/A"):
            current_user_data["first_name"] = user_info.get("first_name", "N/A")
            updated = True
        if current_user_data.get("last_name") != user_info.get("last_name", ""):
            current_user_data["last_name"] = user_info.get("last_name", "")
            updated = True
        if current_user_data.get("username") != user_info.get("username", ""):
            current_user_data["username"] = user_info.get("username", "")
            updated = True

        if updated:
            save_json_file(USER_FILE, users)
            logger.info(f"تم تحديث معلومات المستخدم {user_id_str}.")


async def handle_admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج عرض لوحة إدارة المستخدمين للمشرفين.
    يسمح بالبحث عن المستخدمين وعرض معلوماتهم الأساسية.
    """
    query = update.callback_query
    if query:
        await query.answer()
        context.user_data["awaiting_input"] = "admin_user_search"

    users = load_json_file(USER_FILE, {})
    search_term = context.user_data.get("admin_search", "").lower()
    results = []

    for uid, info in users.items():
        username = info.get("name", f"مستخدم {uid}")
        if "name" not in info:
            display_name = f"{info.get('first_name', '')} {info.get('last_name', '')}".strip()
            if not display_name:
                display_name = f"مستخدم {uid}"
        else:
            display_name = username

        if search_term in uid.lower() or (display_name and search_term in display_name.lower()) or (info.get("username") and search_term in info.get("username").lower()):
            results.append((uid, display_name, info.get("balance", 0), info.get("banned", False)))

    if not results:
        message_text = "❌ لا يوجد مستخدمون مطابقون."
        reply_markup = create_reply_markup([
            back_button(callback_data="back_to_dashboard_clear_admin_search")
        ])
        if query:
            await query.edit_message_text(message_text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        logger.info(f"لا يوجد مستخدمون مطابقون لـ '{search_term}'.")
        context.user_data.pop("awaiting_input", None)
        return

    text = "<b>👥 إدارة المستخدمين</b>\n\n"
    buttons = []

    for uid, name, balance, banned in results[:10]:
        ban_status = "🚫 محظور" if banned else "✅ نشط"
        text += f"👤 <b>{name}</b> | 🆔 {uid}\n💰 {balance} ر.س | {ban_status}\n\n"
        row = [
            InlineKeyboardButton("✏️ تعديل", callback_data=f"edit_{uid}"),
            InlineKeyboardButton("🚫 حظر" if not banned else "✅ فك الحظر", callback_data=f"toggleban_{uid}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"confirm_delete_{uid}")
        ]
        buttons.append(row)

    buttons.append(back_button(callback_data="back_to_dashboard_clear_admin_search", text="🔙 العودة"))

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
    import config
    if user_id not in config.ADMINS:
        await update.message.reply_text("❌ ليس لديك صلاحية للبحث في قائمة المستخدمين.")
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

    user_id_to_edit = query.data.split("_")[1]
    context.user_data["editing_user_id"] = user_id_to_edit
    context.user_data["awaiting_input"] = "admin_balance_edit"
    context.user_data.pop("admin_search_mode", None)
    context.user_data.pop("admin_search", None)
    logger.info(f"المشرف {update.effective_user.id} بدأ تعديل رصيد المستخدم: {user_id_to_edit}.")

    await query.edit_message_text(
        f"✏️ أرسل الآن الرصيد الجديد للمستخدم\n🆔 ID: <code>{user_id_to_edit}</code>",
        parse_mode="HTML"
    )

async def receive_balance_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يستقبل قيمة الرصيد الجديدة من المشرف ويقوم بتحديثها للمستخدم المستهدف.
    يتم تفعيله عندما يكون awaiting_input="admin_balance_edit".
    """
    new_balance_str = update.message.text.strip()
    user_id = update.effective_user.id

    if not new_balance_str.replace('.', '', 1).isdigit():
        await update.message.reply_text("❌ الرجاء إدخال رقم صالح للرصيد.")
        logger.warning(f"المشرف {user_id} أدخل رصيدًا غير صالح: '{new_balance_str}'.")
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("editing_user_id", None)
        return

    try:
        new_balance = float(new_balance_str)
    except ValueError:
        await update.message.reply_text("❌ حدث خطأ في تحويل الرصيد. الرجاء إدخال رقم.")
        logger.error(f"خطأ في تحويل '{new_balance_str}' إلى رقم عشري بواسطة المشرف {user_id}.", exc_info=True)
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("editing_user_id", None)
        return

    user_id_to_edit = context.user_data.get("editing_user_id")

    users = load_json_file(USER_FILE, {})

    if user_id_to_edit in users:
        users[user_id_to_edit]["balance"] = round(new_balance, 2)
        save_json_file(USER_FILE, users)
        await update.message.reply_text(f"✅ تم تعديل رصيد المستخدم {user_id_to_edit} إلى {new_balance} ر.س.")
        logger.info(f"المشرف {user_id} عدّل رصيد المستخدم {user_id_to_edit} إلى {new_balance}.")
    else:
        await update.message.reply_text("❌ لم يتم العثور على المستخدم المطلوب تعديل رصيده.")
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

    user_id_to_toggle = query.data.split("_")[1]
    users = load_json_file(USER_FILE, {})
    admin_id = update.effective_user.id

    if user_id_to_toggle in users:
        current_status = users[user_id_to_toggle].get("banned", False)
        users[user_id_to_toggle]["banned"] = not current_status
        save_json_file(USER_FILE, users)
        new_status_text = "حظر" if not current_status else "فك الحظر"
        await query.edit_message_text(f"✅ تم تحديث حالة المستخدم {user_id_to_toggle} إلى: {new_status_text}.")
        logger.info(f"المشرف {admin_id} قام بـ {new_status_text} المستخدم {user_id_to_toggle}.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")
        logger.warning(f"المشرف {admin_id} حاول حظر/فك حظر مستخدم غير موجود: {user_id_to_toggle}.")


async def confirm_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يطلب تأكيد حذف المستخدم من المشرف قبل التنفيذ النهائي.
    """
    query = update.callback_query
    await query.answer()

    user_id_to_delete = query.data.split("_")[2]
    admin_id = update.effective_user.id

    keyboard = create_reply_markup([
        [
            InlineKeyboardButton("✅ نعم، احذف", callback_data=f"delete_user_confirmed_{user_id_to_delete}"),
            InlineKeyboardButton("❌ إلغاء", callback_data="admin_users")
        ]
    ])

    await query.message.edit_text(
        f"⚠️ هل أنت متأكد من حذف المستخدم <code>{user_id_to_delete}</code>؟ لا يمكن التراجع عن هذا الإجراء.",
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

    user_id_to_delete = query.data.split("_")[3]
    users = load_json_file(USER_FILE, {})
    admin_id = update.effective_user.id

    if user_id_to_delete in users:
        del users[user_id_to_delete]
        save_json_file(USER_FILE, users)
        await query.edit_message_text(f"🗑️ تم حذف المستخدم <code>{user_id_to_delete}</code> بنجاح.")
        logger.info(f"المشرف {admin_id} قام بحذف المستخدم {user_id_to_delete} بعد التأكيد.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")
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