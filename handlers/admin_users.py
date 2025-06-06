import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, set_user_balance

# 📁 مسار ملف المستخدمين
USER_FILE = "data/users.json"

# ✅ تحميل بيانات المستخدمين من الملف
def load_users():
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# ✅ حفظ بيانات المستخدمين بعد التعديل
def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# ✅ عرض قائمة المستخدمين مع خيارات الإدارة (بحث، تعديل، حظر، حذف)
async def handle_admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    users = load_users()
    search_term = context.user_data.get("admin_search", "")
    results = []

    for uid, info in users.items():
        username = info.get("name", f"مستخدم {uid}")
        if search_term.lower() in uid.lower() or search_term.lower() in username.lower():
            results.append((uid, username, info.get("balance", 0), info.get("banned", False)))

    if not results:
        await query.edit_message_text(
            "❌ لا يوجد مستخدمون مطابقون.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
            ])
        )
        return

    # 📝 بناء النص والواجهة
    text = "<b>👥 إدارة المستخدمين</b>\n\n"
    buttons = []

    for uid, name, balance, banned in results[:10]:  # عرض أول 10 فقط
        ban_status = "🚫 محظور" if banned else "✅ نشط"
        text += f"👤 <b>{name}</b> | 🆔 {uid}\n💰 {balance} ر.س | {ban_status}\n\n"
        row = [
            InlineKeyboardButton("✏️ تعديل", callback_data=f"edit_{uid}"),
            InlineKeyboardButton("🚫 حظر" if not banned else "✅ فك الحظر", callback_data=f"toggleban_{uid}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"delete_{uid}")
        ]
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")])
    await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))

# ✅ دعم البحث داخل الإدارة باسم المستخدم أو الـ ID
async def handle_admin_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["admin_search"] = update.message.text.strip()
    await handle_admin_users(update, context)

# ✅ بدء عملية تعديل رصيد مستخدم معين
async def handle_edit_user_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]
    context.user_data["editing_user_id"] = user_id
    context.user_data["edit_balance_mode"] = True

    await query.edit_message_text(
        f"✏️ أرسل الآن الرصيد الجديد للمستخدم\n🆔 ID: <code>{user_id}</code>",
        parse_mode="HTML"
    )

# ✅ استلام قيمة الرصيد الجديدة وتحديثها
async def receive_balance_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("edit_balance_mode"):
        new_balance = update.message.text.strip()

        if not new_balance.isdigit():
            await update.message.reply_text("❌ الرجاء إدخال رقم صالح.")
            return

        user_id = context.user_data.get("editing_user_id")
        users = load_users()

        if user_id in users:
            users[user_id]["balance"] = int(new_balance)
            save_users(users)
            await update.message.reply_text(f"✅ تم تعديل رصيد المستخدم إلى {new_balance} ر.س.")
        else:
            await update.message.reply_text("❌ لم يتم العثور على المستخدم.")

        context.user_data["edit_balance_mode"] = False
        context.user_data.pop("editing_user_id", None)

# ✅ تنفيذ الحظر أو فك الحظر
async def handle_block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]
    users = load_users()

    if user_id in users:
        current = users[user_id].get("banned", False)
        users[user_id]["banned"] = not current
        save_users(users)
        await query.edit_message_text("✅ تم تحديث حالة الحظر.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")

# ✅ تنفيذ الحذف النهائي للمستخدم
async def handle_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]
    users = load_users()

    if user_id in users:
        del users[user_id]
        save_users(users)
        await query.edit_message_text("🗑️ تم حذف المستخدم بنجاح.")
    else:
        await query.edit_message_text("❌ المستخدم غير موجود.")
