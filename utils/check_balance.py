import json
from telegram import Update
from telegram.ext import ContextTypes

# ✅ معرفات المدراء
ADMIN_IDS = [780028688]  # يمكنك إضافة المزيد داخل القائمة

# ✅ قراءة الرصيد من ملف users.json
def get_user_balance(user_id: int) -> float:
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        return users.get(str(user_id), {}).get("balance", 0)
    except:
        return 0

# ✅ أمر /balance
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if requester_id in ADMIN_IDS and len(context.args) == 1:
        try:
            target_id = int(context.args[0])
            balance = get_user_balance(target_id)

            # محاولة عرض اسم المستخدم من Telegram
            try:
                member = await update.effective_chat.get_member(target_id)
                name = member.user.username if member.user.username else f"{member.user.first_name} {member.user.last_name or ''}"
            except:
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
