# utils/balance.py
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE
from utils.i18n import get_messages
from services import user_service # # استيراد خدمة المستخدم
from database.database import get_db # # استيراد get_db لتوفير جلسة قاعدة البيانات

logger = logging.getLogger(__name__)

# # لم نعد بحاجة إلى USER_FILE لأننا لا نتعامل مع JSON مباشرة
# USER_FILE = os.path.join("data", "users.json")

def get_user_balance(user_id: int, user_info: dict) -> float:
    """
    يجلب رصيد المستخدم من قاعدة البيانات.
    يتم التأكد من وجود المستخدم أولاً.
    """
    # # التأكد من وجود المستخدم (يتم في كل طلب) - هذه الدالة تتولى الحصول على الجلسة
    user_service.ensure_user_exists(user_id, user_info)
    
    # # الآن نستخدم get_db للحصول على جلسة والتفاعل مع خدمة المستخدم
    for db in get_db():
        user = user_service.get_user(db, user_id)
        return user.balance if user else 0.0 # # إرجاع الرصيد أو 0.0 إذا لم يتم العثور على المستخدم (غير محتمل بعد ensure_user_exists)

def set_user_balance(user_id: int, new_balance: float, user_info: dict):
    """
    يعين رصيد المستخدم في قاعدة البيانات.
    """
    user_service.ensure_user_exists(user_id, user_info)
    for db in get_db():
        user_service.update_user(db, user_id, balance=round(new_balance, 2))
        logger.info(f"تم تعيين رصيد المستخدم {user_id} إلى {new_balance}.")

def update_balance(user_id: int, amount: float, user_info: dict):
    """
    يحدث رصيد المستخدم في قاعدة البيانات بزيادة أو نقصان.
    """
    user_service.ensure_user_exists(user_id, user_info)
    for db in get_db():
        user = user_service.get_user(db, user_id)
        if user:
            new_balance = round(user.balance + amount, 2)
            user_service.update_user(db, user_id, balance=new_balance)
            logger.info(f"تم تحديث رصيد المستخدم {user_id} بمقدار {amount}. الرصيد الجديد: {new_balance}.")
        else:
            logger.warning(f"لم يتم العثور على المستخدم {user_id} لتحديث الرصيد.")

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.message.reply_text(messages["admin_only_command"])
        return

    target_user_id_str = None
    amount = 0.0

    if not context.args:
        target_user_id_str = str(user_id)
        amount = 100.0
    elif len(context.args) == 2:
        target_user_id_str = context.args[0]
        try:
            amount = float(context.args[1])
        except ValueError:
            await update.message.reply_text(messages["add_balance_invalid_amount_format"])
            return
    elif len(context.args) == 1:
        target_user_id_str = str(user_id)
        try:
            amount = float(context.args[0])
        except ValueError:
            await update.message.reply_text(messages["add_balance_invalid_amount"])
            return
    else:
        await update.message.reply_text(messages["add_balance_invalid_format"])
        return
    
    if amount <= 0:
        await update.message.reply_text(messages["amount_must_be_positive"])
        return

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text(messages["invalid_user_id_after_clean"])
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text(messages["user_id_conversion_error"])
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        # # هنا نستخدم user_service.ensure_user_exists و update_balance مباشرة
        # # لا نحتاج لـ load_json_file أو users_data هنا
        user_service.ensure_user_exists(final_target_user_id, {"id": final_target_user_id}) # # التأكد من وجود المستخدم المستهدف
        update_balance(final_target_user_id, amount, {"id": final_target_user_id}) # # update_balance تتولى الحصول على الجلسة والتعامل مع DB

        await update.message.reply_text(messages["balance_added_success"].format(amount=amount, currency=messages["price_currency"], user_id=final_target_user_id))
        logger.info(f"المشرف {user_id} أضاف {amount} إلى {final_target_user_id}.")
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في إضافة {amount} إلى {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text(messages["error_updating_balance"])

async def deduct_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.message.reply_text(messages["admin_only_command"])
        return

    if len(context.args) != 2:
        await update.message.reply_text(messages["deduct_balance_invalid_format"])
        return

    target_user_id_str = context.args[0]

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text(messages["invalid_user_id_after_clean"])
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text(messages["user_id_conversion_error"])
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text(messages["deduct_balance_invalid_amount"])
        return
    
    if amount <= 0:
        await update.message.reply_text(messages["amount_must_be_positive"])
        return

    try:
        # # هنا نستخدم user_service.ensure_user_exists و get_user_balance و update_balance مباشرة
        # # لا نحتاج لـ load_json_file أو users_data هنا
        user_service.ensure_user_exists(final_target_user_id, {"id": final_target_user_id}) # # التأكد من وجود المستخدم المستهدف

        current = get_user_balance(final_target_user_id, {"id": final_target_user_id}) # # جلب الرصيد
        if current < amount:
            await update.message.reply_text(messages["insufficient_balance_deduct"].format(current_balance=current, currency=messages["price_currency"]))
            return

        update_balance(final_target_user_id, -amount, {"id": final_target_user_id}) # # تحديث الرصيد
        await update.message.reply_text(messages["balance_deducted_success"].format(amount=amount, currency=messages["price_currency"], user_id=final_target_user_id))
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في خصم {amount} من {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text(messages["error_updating_balance"])

async def show_my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    balance = get_user_balance(user_id, user.to_dict())
    await update.message.reply_text(messages["my_balance_is"].format(balance=balance, currency=messages["price_currency"]))