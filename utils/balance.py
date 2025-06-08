import json
import os
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS # ✅ تم إضافة هذا السطر لاستيراد ADMINS من config.py

logger = logging.getLogger(__name__)

# ✅ ملف المستخدمين
USER_FILE = "data/users.json" #

# ✅ جلب الرصيد الحالي
def get_user_balance(user_id: int) -> float:
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
        return users.get(str(user_id), {}).get("balance", 0)
    except FileNotFoundError:
        logger.warning(f"ملف المستخدمين '{USER_FILE}' غير موجود. سيبدأ برصيد 0 للمستخدم {user_id}.")
        return 0
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للمستخدمين '{USER_FILE}'.", exc_info=True)
        return 0
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند جلب رصيد المستخدم {user_id}: {e}", exc_info=True)
        return 0

# ✅ تعديل الرصيد مباشرة
def set_user_balance(user_id: int, new_balance: float):
    try:
        users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    logger.error(f"ملف المستخدمين '{USER_FILE}' تالف. سيتم إعادة إنشائه.", exc_info=True)
                    users = {}

        uid = str(user_id)
        users[uid] = users.get(uid, {})
        users[uid]["balance"] = round(new_balance, 2)

        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        logger.info(f"تم تعيين رصيد المستخدم {user_id} إلى {new_balance}.")
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف المستخدمين '{USER_FILE}': {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تعيين رصيد المستخدم {user_id}: {e}", exc_info=True)

# ✅ تحديث الرصيد (إضافة أو خصم)
def update_balance(user_id: int, amount: float):
    try:
        users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    logger.error(f"ملف المستخدمين '{USER_FILE}' تالف أثناء تحديث الرصيد. سيتم إنشاء جديد.", exc_info=True)
                    users = {}

        uid = str(user_id)
        current = users.get(uid, {}).get("balance", 0)
        users[uid] = users.get(uid, {})
        users[uid]["balance"] = round(current + amount, 2)

        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        logger.info(f"تم تحديث رصيد المستخدم {user_id} بمقدار {amount}. الرصيد الجديد: {users[uid]['balance']}.")
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف المستخدمين '{USER_FILE}' أثناء التحديث: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تحديث رصيد المستخدم {user_id}: {e}", exc_info=True)

# ✅ إضافة رصيد (للإدارة فقط)
async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS: # ✅ تم التعديل من ADMIN_IDS إلى ADMINS
        await update.message.reply_text("❌ هذا الأمر مخصص فقط للمسؤولين.")
        return

    target_user_id_str = None
    amount = 0.0

    if not context.args:
        target_user_id_str = str(user_id)
        amount = 100

    elif len(context.args) == 2:
        target_user_id_str = context.args[0]
        try:
            amount = float(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ الصيغة غير صحيحة للمبلغ. استخدم: /add_balance <user_id> <amount>")
            return
    elif len(context.args) == 1:
        target_user_id_str = str(user_id)
        try:
            amount = float(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ أدخل مبلغًا صالحًا مثل: /add_balance 200")
            return
    else:
        await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم: /add_balance <user_id> <amount> أو /add_balance <amount>")
        return

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text("❌ معرف المستخدم غير صالح أو فارغ بعد التنظيف.")
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text("❌ حدث خطأ في تحويل معرف المستخدم. يرجى التأكد من صلاحيته.")
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        update_balance(final_target_user_id, amount)
        await update.message.reply_text(f"✅ تم إضافة {amount} ر.س إلى رصيد المستخدم {final_target_user_id}.")
        logger.info(f"المشرف {user_id} أضاف {amount} إلى {final_target_user_id}.")
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في إضافة {amount} إلى {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text("❌ حدث خطأ أثناء تحديث الرصيد. يرجى مراجعة سجلات البوت.")

# ✅ خصم رصيد (للإدارة فقط)
async def deduct_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS: # ✅ تم التعديل من ADMIN_IDS إلى ADMINS
        await update.message.reply_text("❌ هذا الأمر مخصص فقط للمسؤولين.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❌ الصيغة: /deduct_balance <user_id> <amount>")
        return

    target_user_id_str = context.args[0]

    cleaned_target_user_id_str = re.sub(r'\D', '', target_user_id_str)

    if not cleaned_target_user_id_str:
        await update.message.reply_text("❌ معرف المستخدم غير صالح أو فارغ بعد التنظيف.")
        return

    try:
        final_target_user_id = int(cleaned_target_user_id_str)
    except ValueError:
        await update.message.reply_text("❌ حدث خطأ في تحويل معرف المستخدم. يرجى التأكد من صلاحيته.")
        logger.error(f"فشل تحويل معرف المستخدم '{target_user_id_str}' إلى عدد صحيح. المستخدم: {user_id}")
        return

    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ أدخل مبلغًا صالحًا.")
        return

    try:
        current = get_user_balance(final_target_user_id)
        if current < amount:
            await update.message.reply_text(f"❌ الرصيد غير كافٍ. الرصيد الحالي: {current} ر.س")
            return

        update_balance(final_target_user_id, -amount)
        await update.message.reply_text(f"✅ تم خصم {amount} ر.س من المستخدم {final_target_user_id}.")
        logger.info(f"المشرف {user_id} خصم {amount} من {final_target_user_id}.")
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في خصم {amount} من {final_target_user_id}: {e}", exc_info=True)
        await update.message.reply_text("❌ حدث خطأ أثناء تحديث الرصيد. يرجى مراجعة سجلات البوت.")

# ✅ عرض رصيد المستخدم
async def show_my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    await update.message.reply_text(f"💰 رصيدك الحالي هو: {balance} ر.س")