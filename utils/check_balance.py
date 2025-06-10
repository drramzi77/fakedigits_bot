import json
import logging
import os
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE # # تم إضافة DEFAULT_LANGUAGE
from utils.data_manager import load_json_file # ✅ تم التأكد من الوجود والآن سيتم استخدامه لـ load_json_file
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص

logger = logging.getLogger(__name__)

# ✅ قراءة الرصيد من ملف users.json
def get_user_balance(user_id: int) -> float:
    """
    يُرجع الرصيد الحالي لمستخدم معين من ملف users.json.

    Args:
        user_id (int): معرف المستخدم الذي يُراد جلب رصيده.

    Returns:
        float: رصيد المستخدم، أو 0 إذا لم يتم العثور على المستخدم أو الملف.
    """
    # # هذه الدالة ستتغير لاحقاً لاستخدام قاعدة البيانات
    try:
        users = load_json_file(os.path.join("data", "users.json"), default_data={})
        return users.get(str(user_id), {}).get("balance", 0.0)
    except Exception as e: # # يمكن أن تكون FileNotFoundError أو json.JSONDecodeError
        logger.error(f"خطأ عند جلب رصيد المستخدم {user_id} من ملف JSON: {e}", exc_info=True)
        return 0.0

# ✅ أمر /balance
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج الأمر /balance.
    يعرض الرصيد الحالي للمستخدم الذي أصدر الأمر،
    أو رصيد مستخدم آخر إذا كان المصدر مشرفاً.

    Args:
        update (Update): الكائن Update الوارد من تيليجرام.
        context (ContextTypes.DEFAULT_TYPE): كائن السياق الخاص بالبوت.
    """
    user = update.effective_user
    requester_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    # إذا لم يتم تمرير معرف مستخدم، نعرض الرصيد لنفس المستخدم
    if not context.args:
        balance = get_user_balance(requester_id)
        name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"
        
        await update.message.reply_text(
            messages["my_balance_info"].format(
                name=name,
                user_id=requester_id,
                balance=balance,
                currency=messages["price_currency"]
            ),
            parse_mode="HTML"
        )
        return

    # إذا تم تمرير معرف مستخدم، تحقق من صلاحية المدير
    if requester_id in ADMINS and len(context.args) == 1:
        try:
            target_id = int(context.args[0])
            balance = get_user_balance(target_id)

            try:
                member = await update.effective_chat.get_member(target_id)
                name = member.user.username if member.user.username else f"{member.user.first_name} {member.user.last_name or ''}"
            except Exception as e:
                logger.warning(f"لم يتمكن البوت من جلب معلومات المستخدم {target_id} (ربما ليس في المجموعة/خاص): {e}")
                name = messages["unknown_user_in_group"] # # استخدام النص المترجم

            await update.message.reply_text(
                messages["user_balance_info"].format(
                    name=name,
                    user_id=target_id,
                    balance=balance,
                    currency=messages["price_currency"]
                ),
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text(messages["invalid_user_id_balance_command"]) # # استخدام النص المترجم
    else:
        await update.message.reply_text(messages["no_permission_to_view_others_balance"]) # # استخدام النص المترجم