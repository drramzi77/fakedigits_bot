import json
import logging
import os
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS # تأكد من أن هذا الاستيراد موجود

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
    try:
        with open(os.path.join("data", "users.json"), "r", encoding="utf-8") as f:
            users = json.load(f)
        return users.get(str(user_id), {}).get("balance", 0)
    except FileNotFoundError:
        logger.warning(f"ملف المستخدمين 'data/users.json' غير موجود. سيبدأ رصيد المستخدم {user_id} بـ 0.")
        return 0
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للمستخدمين 'data/users.json'. الملف قد يكون تالفًا.", exc_info=True)
        return 0
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند جلب رصيد المستخدم {user_id} في check_balance: {e}", exc_info=True)
        return 0

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

    # إذا لم يتم تمرير معرف مستخدم، نعرض الرصيد لنفس المستخدم
    if not context.args:
        balance = get_user_balance(requester_id)
        name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"
        await update.message.reply_text(
            f"👤 المستخدم: {name}\n"
            f"🆔 المعرف: <code>{requester_id}</code>\n"
            f"💰 الرصيد الحالي: {balance} ر.س", parse_mode="HTML"
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
                name = "غير معروف (ربما ليس في المجموعة)"

            await update.message.reply_text(
                f"👤 المستخدم: {name}\n"
                f"🆔 المعرف: <code>{target_id}</code>\n"
                f"💰 الرصيد: {balance} ر.س", parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text("❌ أدخل معرفًا صالحًا مثل: /balance 123456789")
    else:
        await update.message.reply_text("❌ ليس لديك صلاحية لعرض رصيد الآخرين.")