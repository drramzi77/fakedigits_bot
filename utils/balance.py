import json
from telegram import Update
from telegram.ext import ContextTypes

# ✅ معرفات المسؤولين
ADMIN_IDS = [780028688]

# ✅ ملف المستخدمين
USER_FILE = "data/users.json"

# ✅ جلب الرصيد الحالي
def get_user_balance(user_id: int) -> float:
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
        return users.get(str(user_id), {}).get("balance", 0)
    except:
        return 0

# ✅ تعديل الرصيد مباشرة
def set_user_balance(user_id: int, new_balance: float):
    try:
        with open(USER_FILE, "r+", encoding="utf-8") as f:
            users = json.load(f)
            uid = str(user_id)
            users[uid] = users.get(uid, {})
            users[uid]["balance"] = round(new_balance, 2)
            f.seek(0)
            json.dump(users, f, indent=2, ensure_ascii=False)
            f.truncate()
    except:
        pass

# ✅ تحديث الرصيد (إضافة أو خصم)
def update_balance(user_id: int, amount: float):
    try:
        with open(USER_FILE, "r+", encoding="utf-8") as f:
            users = json.load(f)
            uid = str(user_id)
            current = users.get(uid, {}).get("balance", 0)
            users[uid] = {"balance": round(current + amount, 2)}
            f.seek(0)
            json.dump(users, f, indent=2, ensure_ascii=False)
            f.truncate()
    except:
        pass

# ✅ إضافة رصيد (للإدارة فقط)
async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر مخصص فقط للمسؤولين.")
        return

    target_user_id = str(user_id)
    amount = 100  # قيمة افتراضية

    if context.args:
        if len(context.args) == 2:
            target_user_id = context.args[0]
            try:
                amount = float(context.args[1])
            except ValueError:
                await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم: /add_balance <user_id> <amount>")
                return
        elif len(context.args) == 1:
            try:
                amount = float(context.args[0])
            except ValueError:
                await update.message.reply_text("❌ أدخل مبلغًا صالحًا مثل: /add_balance 200")
                return

    try:
        update_balance(int(target_user_id), amount)
        await update.message.reply_text(f"✅ تم إضافة {amount} ر.س إلى رصيد المستخدم {target_user_id}.")
    except Exception:
        await update.message.reply_text("❌ حدث خطأ أثناء تحديث الرصيد.")

# ✅ خصم رصيد (للإدارة فقط)
async def deduct_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر مخصص فقط للمسؤولين.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❌ الصيغة: /deduct_balance <user_id> <amount>")
        return

    target_user_id = context.args[0]
    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ أدخل مبلغًا صالحًا.")
        return

    try:
        current = get_user_balance(int(target_user_id))
        if current < amount:
            await update.message.reply_text(f"❌ الرصيد غير كافٍ. الرصيد الحالي: {current} ر.س")
            return

        update_balance(int(target_user_id), -amount)
        await update.message.reply_text(f"✅ تم خصم {amount} ر.س من المستخدم {target_user_id}.")
    except Exception:
        await update.message.reply_text("❌ حدث خطأ أثناء تحديث الرصيد.")

# ✅ عرض رصيد المستخدم
async def show_my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    await update.message.reply_text(f"💰 رصيدك الحالي هو: {balance} ر.س")
