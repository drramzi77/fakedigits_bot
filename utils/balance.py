import json
import os
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE # # تم إضافة DEFAULT_LANGUAGE
from utils.data_manager import load_json_file, save_json_file
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص

logger = logging.getLogger(__name__)

# ✅ ملف المستخدمين
USER_FILE = os.path.join("data", "users.json") # # هذا المسار سيتغير لاحقاً مع DB


# ✅ جلب الرصيد الحالي
def get_user_balance(user_id: int) -> float:
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    users = load_json_file(USER_FILE, default_data={})
    return users.get(str(user_id), {}).get("balance", 0.0)

# ✅ تعديل الرصيد مباشرة
def set_user_balance(user_id: int, new_balance: float):
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    users = load_json_file(USER_FILE, default_data={})
    uid = str(user_id)
    users[uid] = users.get(uid, {})
    users[uid]["balance"] = round(new_balance, 2)
    save_json_file(USER_FILE, users)
    logger.info(f"تم تعيين رصيد المستخدم {user_id} إلى {new_balance}.")

# ✅ تحديث الرصيد (إضافة أو خصم)
def update_balance(user_id: int, amount: float):
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    users = load_json_file(USER_FILE, default_data={})
    uid = str(user_id)
    users[uid] = users.get(uid, {})
    current = users[uid].get("balance", 0.0) # # استخدام get لضمان وجود المفتاح
    users[uid]["balance"] = round(current + amount, 2)
    save_json_file(USER_FILE, users)
    logger.info(f"تم تحديث رصيد المستخدم {user_id} بمقدار {amount}. الرصيد الجديد: {users[uid]['balance']}.")


# ✅ إضافة رصيد (للإدارة فقط)
async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.message.reply_text(messages["admin_only_command"]) # # استخدام النص المترجم
        return

    target_user_id_str = None
    amount = 0.0

    if not context.args:
        # # افتراضيًا للمشرف نفسه بمبلغ 100
        target_user_id_str = str(user_id)
        amount = 100.0 # # يمكن جعل هذا المبلغ في config أو في ملف لغة

    elif len(context.args) == 2:
        target_user_id_str = context.args[0]
        try:
            amount = float(context.args[1])
        except ValueError:
            await update.message.reply_text(messages["add_balance_invalid_amount_format"]) # # استخدام النص المترجم
            return
    elif len(context.args) == 1:
        # # إذا تم تمرير مبلغ فقط، يضاف للمشرف نفسه
        target_user_id_str = str(user_id)
        try:
            amount = float(context.args[0])
        except ValueError:
            await update.message.reply_text(messages["add_balance_invalid_amount"]) # # استخدام النص المترجم
            return
    else:
        await update.message.reply_text(messages["add_balance_invalid_format"]) # # استخدام النص المترجم
        return
    
    # # التأكد أن المبلغ موجب
    if amount <= 0:
        await update.message.reply_text(messages["amount_must_be_positive"])
        return

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text(messages["invalid_user_id_after_clean"]) # # استخدام النص المترجم
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text(messages["user_id_conversion_error"]) # # استخدام النص المترجم
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        update_balance(final_target_user_id, amount) # # هذه الدالة ستتغير لاحقاً
        await update.message.reply_text(messages["balance_added_success"].format(amount=amount, currency=messages["price_currency"], user_id=final_target_user_id)) # # استخدام النص المترجم
        logger.info(f"المشرف {user_id} أضاف {amount} إلى {final_target_user_id}.")
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في إضافة {amount} إلى {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text(messages["error_updating_balance"]) # # استخدام النص المترجم

# ✅ خصم رصيد (للإدارة فقط)
async def deduct_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.message.reply_text(messages["admin_only_command"]) # # استخدام النص المترجم
        return

    if len(context.args) != 2:
        await update.message.reply_text(messages["deduct_balance_invalid_format"]) # # استخدام النص المترجم
        return

    target_user_id_str = context.args[0]

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text(messages["invalid_user_id_after_clean"]) # # استخدام النص المترجم
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text(messages["user_id_conversion_error"]) # # استخدام النص المترجم
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text(messages["deduct_balance_invalid_amount"]) # # استخدام النص المترجم
        return
    
    # # التأكد أن المبلغ موجب
    if amount <= 0:
        await update.message.reply_text(messages["amount_must_be_positive"])
        return

    try:
        current = get_user_balance(final_target_user_id) # # هذه الدالة ستتغير لاحقاً
        if current < amount:
            await update.message.reply_text(messages["insufficient_balance_deduct"].format(current_balance=current, currency=messages["price_currency"])) # # استخدام النص المترجم
            return

        update_balance(final_target_user_id, -amount) # # هذه الدالة ستتغير لاحقاً
        await update.message.reply_text(messages["balance_deducted_success"].format(amount=amount, currency=messages["price_currency"], user_id=final_target_user_id)) # # استخدام النص المترجم
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في خصم {amount} من {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text(messages["error_updating_balance"]) # # استخدام النص المترجم

# ✅ عرض رصيد المستخدم
async def show_my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً
    await update.message.reply_text(messages["my_balance_is"].format(balance=balance, currency=messages["price_currency"])) # # استخدام النص المترجم