import json
import logging # # إضافة هذا السطر
import os # # إضافة هذا السطر
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup # # إضافة هذا السطر
from telegram.ext import ContextTypes # # إضافة هذا السطر
from utils.balance import get_user_balance, set_user_balance

logger = logging.getLogger(__name__) # # تعريف logger على مستوى الوحدة

# 📁 مسار ملف المستخدمين
USER_FILE = "data/users.json"

# ✅ تحميل بيانات المستخدمين من الملف
def load_users():
    try:
        if not os.path.exists(USER_FILE):
            logger.warning(f"ملف المستخدمين '{USER_FILE}' غير موجود. سيتم إنشاء ملف فارغ.")
            return {}
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للمستخدمين '{USER_FILE}'. الملف قد يكون تالفًا.", exc_info=True)
        return {} # # إرجاع قاموس فارغ إذا كان الملف تالفًا
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف المستخدمين '{USER_FILE}' أثناء التحميل: {e}", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تحميل المستخدمين: {e}", exc_info=True)
        return {}

# ✅ حفظ بيانات المستخدمين بعد التعديل
def save_users(users):
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        logger.info(f"تم حفظ بيانات المستخدمين في '{USER_FILE}'.")
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف المستخدمين '{USER_FILE}' أثناء الحفظ: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند حفظ المستخدمين: {e}", exc_info=True)

# ✅ عرض قائمة المستخدمين مع خيارات الإدارة (بحث، تعديل، حظر، حذف)
async def handle_admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query: # # تحقق لتجنب الخطأ إذا لم يكن هناك callback_query
        await query.answer()

    users = load_users()
    search_term = context.user_data.get("admin_search", "").lower()
    results = []

    for uid, info in users.items():
        username = info.get("name", f"مستخدم {uid}")
        # # التحقق من username قبل تحويله إلى lower() لتجنب NoneType error
        if search_term in uid.lower() or (username and search_term in username.lower()):
            results.append((uid, username, info.get("balance", 0), info.get("banned", False)))

    if not results:
        message_text = "❌ لا يوجد مستخدمون مطابقون."
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
        ])
        if query:
            await query.edit_message_text(message_text, reply_markup=reply_markup)
        else: # # إذا تم استدعاؤها من MessageHandler (مثلاً من handle_admin_search)
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        logger.info(f"لا يوجد مستخدمون مطابقون لـ '{search_term}'.")
        return

    text = "<b>👥 إدارة المستخدمين</b>\n\n"
    buttons = []

    for uid, name, balance, banned in results[:10]: # عرض أول 10 فقط
        ban_status = "🚫 محظور" if banned else "✅ نشط"
        text += f"👤 <b>{name}</b> | 🆔 {uid}\n💰 {balance} ر.س | {ban_status}\n\n"
        row = [
            InlineKeyboardButton("✏️ تعديل", callback_data=f"edit_{uid}"),
            InlineKeyboardButton("🚫 حظر" if not banned else "✅ فك الحظر", callback_data=f"toggleban_{uid}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"delete_{uid}")
        ]
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")])
    
    if query:
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
    else: # # إذا تم استدعاؤها من MessageHandler
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
    logger.info(f"تم عرض قائمة المستخدمين الإدارية لـ '{search_term}'.")


# ✅ دعم البحث داخل الإدارة باسم المستخدم أو الـ ID
async def handle_admin_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # # تحقق مما إذا كان المستخدم يملك صلاحية المدير قبل معالجة البحث
    # # (يمكن إضافة هذا التحقق هنا أو تركه في handle_admin_users)
    user_id = update.effective_user.id
    from config import ADMINS # # استيراد ADMINS من config.py
    if user_id not in ADMINS:
        await update.message.reply_text("❌ ليس لديك صلاحية للبحث في قائمة المستخدمين.")
        return

    context.user_data["admin_search"] = update.message.text.strip()
    logger.info(f"المشرف {user_id} يبحث عن: '{context.user_data['admin_search']}'.")
    await handle_admin_users(update, context)

# ✅ بدء عملية تعديل رصيد مستخدم معين
async def handle_edit_user_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id_to_edit = query.data.split("_")[1]
    context.user_data["editing_user_id"] = user_id_to_edit
    context.user_data["edit_balance_mode"] = True
    logger.info(f"المشرف {update.effective_user.id} بدأ تعديل رصيد المستخدم: {user_id_to_edit}.")

    await query.edit_message_text(
        f"✏️ أرسل الآن الرصيد الجديد للمستخدم\n🆔 ID: <code>{user_id_to_edit}</code>",
        parse_mode="HTML"
    )

# ✅ استلام قيمة الرصيد الجديدة وتحديثها
async def receive_balance_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("edit_balance_mode"):
        new_balance_str = update.message.text.strip()
        user_id = update.effective_user.id # # المشرف الذي ينفذ العملية

        if not new_balance_str.replace('.', '', 1).isdigit(): # # يسمح بالأرقام العشرية
            await update.message.reply_text("❌ الرجاء إدخال رقم صالح للرصيد.")
            logger.warning(f"المشرف {user_id} أدخل رصيدًا غير صالح: '{new_balance_str}'.")
            return

        try:
            new_balance = float(new_balance_str)
        except ValueError:
            await update.message.reply_text("❌ حدث خطأ في تحويل الرصيد. الرجاء إدخال رقم.")
            logger.error(f"خطأ في تحويل '{new_balance_str}' إلى رقم عشري بواسطة المشرف {user_id}.", exc_info=True)
            return

        user_id_to_edit = context.user_data.get("editing_user_id")
        
        users = load_users()

        if user_id_to_edit in users:
            users[user_id_to_edit]["balance"] = round(new_balance, 2)
            save_users(users)
            await update.message.reply_text(f"✅ تم تعديل رصيد المستخدم {user_id_to_edit} إلى {new_balance} ر.س.")
            logger.info(f"المشرف {user_id} عدّل رصيد المستخدم {user_id_to_edit} إلى {new_balance}.")
        else:
            await update.message.reply_text("❌ لم يتم العثور على المستخدم المطلوب تعديل رصيده.")
            logger.warning(f"المشرف {user_id} حاول تعديل رصيد مستخدم غير موجود: {user_id_to_edit}.")

        context.user_data["edit_balance_mode"] = False
        context.user_data.pop("editing_user_id", None)
    else: # # إذا كانت الرسالة ليست لإدخال رصيد
        # # هذا الجزء من الكود قد يتعارض مع MessageHandler أخرى
        # # يفضل عدم ترك هذا الجزء فارغًا أو توجيه الرسائل
        pass # # لا تفعل شيئًا، أو يمكنك توجيهها لمعالج آخر


# ✅ تنفيذ الحظر أو فك الحظر
async def handle_block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id_to_toggle = query.data.split("_")[1]
    users = load_users()
    admin_id = update.effective_user.id

    if user_id_to_toggle in users:
        current_status = users[user_id_to_toggle].get("banned", False)
        users[user_id_to_toggle]["banned"] = not current_status
        save_users(users)
        new_status_text = "حظر" if not current_status else "فك الحظر"
        await query.edit_message_text(f"✅ تم تحديث حالة المستخدم {user_id_to_toggle} إلى: {new_status_text}.")
        logger.info(f"المشرف {admin_id} قام بـ {new_status_text} المستخدم {user_id_to_toggle}.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")
        logger.warning(f"المشرف {admin_id} حاول حظر/فك حظر مستخدم غير موجود: {user_id_to_toggle}.")


# ✅ تنفيذ الحذف النهائي للمستخدم
async def handle_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id_to_delete = query.data.split("_")[1]
    users = load_users()
    admin_id = update.effective_user.id

    if user_id_to_delete in users:
        del users[user_id_to_delete]
        save_users(users)
        await query.edit_message_text(f"🗑️ تم حذف المستخدم {user_id_to_delete} بنجاح.")
        logger.info(f"المشرف {admin_id} قام بحذف المستخدم {user_id_to_delete}.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")
        logger.warning(f"المشرف {admin_id} حاول حذف مستخدم غير موجود: {user_id_to_delete}.")