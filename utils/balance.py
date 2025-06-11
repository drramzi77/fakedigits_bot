# utils/balance.py
import json
import os
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE
from utils.data_manager import load_json_file, save_json_file
from utils.i18n import get_messages
from services.user_service import ensure_user_exists # <-- تم التعديل هنا لاستيرادها من services.user_service

logger = logging.getLogger(__name__)

USER_FILE = os.path.join("data", "users.json")

def get_user_balance(user_id: int, user_info: dict) -> float:
    ensure_user_exists(user_id, user_info)
    users = load_json_file(USER_FILE, default_data={})
    return users.get(str(user_id), {}).get("balance", 0.0)

def set_user_balance(user_id: int, new_balance: float, user_info: dict):
    ensure_user_exists(user_id, user_info)
    users = load_json_file(USER_FILE, default_data={})
    uid = str(user_id)
    users[uid] = users.get(uid, {})
    users[uid]["balance"] = round(new_balance, 2)
    save_json_file(USER_FILE, users)
    logger.info(f"تم تعيين رصيد المستخدم {user_id} إلى {new_balance}.")

def update_balance(user_id: int, amount: float, user_info: dict):
    ensure_user_exists(user_id, user_info)
    users = load_json_file(USER_FILE, default_data={})
    uid = str(user_id)
    users[uid] = users.get(uid, {})
    current = users[uid].get("balance", 0.0)
    users[uid]["balance"] = round(current + amount, 2)
    save_json_file(USER_FILE, users)
    logger.info(f"تم تحديث رصيد المستخدم {user_id} بمقدار {amount}. الرصيد الجديد: {users[uid]['balance']}.")

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
        users_data = load_json_file(USER_FILE, default_data={})
        target_user_info = users_data.get(str(final_target_user_id), {"id": final_target_user_id})
        
        update_balance(final_target_user_id, amount, target_user_info)
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
        users_data = load_json_file(USER_FILE, default_data={})
        target_user_info = users_data.get(str(final_target_user_id), {"id": final_target_user_id})

        current = get_user_balance(final_target_user_id, target_user_info)
        if current < amount:
            await update.message.reply_text(messages["insufficient_balance_deduct"].format(current_balance=current, currency=messages["price_currency"]))
            return

        update_balance(final_target_user_id, -amount, target_user_info)
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