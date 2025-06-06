import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, update_balance

ADMIN_IDS = [780028688]  # ← ضع معرفك كمشرف
TRANSFER_LOG_FILE = "data/transfers.json"

# 🔘 زر تواصل مع الإدارة
def contact_admin_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 تواصل مع الدعم", url="https://t.me/DrRamzi0")]  # ← عدّل هذا الرابط
    ])

# 📁 سجل التحويلات
def log_transfer(sender_id, target_id, amount, fee):
    transfer = {
        "from": sender_id,
        "to": target_id,
        "amount": amount,
        "fee": fee,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(TRANSFER_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(transfer)
    with open(TRANSFER_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ✅ عند الضغط على زر "تحويل الرصيد"
async def start_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    if user_id in ADMIN_IDS:
        await update.callback_query.message.edit_text(
            "⚠️ هذا الخيار مخصص فقط للمستخدمين.\n"
            "🔋 لشحن رصيد مستخدم، استخدم القسم المخصص لذلك في لوحة التحكم.",
            parse_mode="HTML"
        )
        return

    if balance < 5:
        msg = (
            "❌ - لا يمكنك تحويل الرصيد الآن.\n"
            f"📊 - رصيدك الحالي: <b>{balance} ر.س</b>\n"
            "💸 - عمولة التحويل: <b>1%</b>\n\n"
            "🔄 <b>ما الحل؟</b>\n"
            "1️⃣ قم بشحن رصيدك.\n"
            "2️⃣ أو تواصل مع الدعم عبر الزر: 💬"
        )
        await update.callback_query.message.edit_text(msg, parse_mode="HTML", reply_markup=contact_admin_button())
    else:
        context.user_data["transfer_stage"] = True
        await update.callback_query.message.edit_text(
            "🔁 <b>تحويل الرصيد</b>\n\n"
            "📥 أرسل المعرف والمبلغ بالشكل التالي:\n\n"
            "<code>123456789 20</code>\n\n"
            "✅ <b>123456789</b>: معرف المستخدم\n"
            "✅ <b>20</b>: المبلغ المطلوب تحويله\n"
            "💸 عمولة التحويل: <b>1%</b>",
            parse_mode="HTML"
        )

# ✅ تنفيذ التحويل الفعلي
async def handle_transfer_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم:\n<code>123456789 20</code>", parse_mode="HTML")
        return

    try:
        target_id = int(parts[0])
        amount = float(parts[1])
    except ValueError:
        await update.message.reply_text("❌ تأكد من أن المعرف والمبلغ أرقام صحيحة.")
        return

    if target_id == user_id:
        await update.message.reply_text("❌ لا يمكنك تحويل الرصيد إلى نفسك.")
        return

    balance = get_user_balance(user_id)
    fee = round(amount * 0.01, 2)
    total = round(amount + fee, 2)

    if balance < total:
        await update.message.reply_text(
            f"❌ رصيدك غير كافٍ.\nرصيدك: {balance} ر.س\nالمطلوب: {total} ر.س\n\n"
            "💬 تواصل مع الدعم عبر الزر:",
            parse_mode="HTML",
            reply_markup=contact_admin_button()
        )
        return

    update_balance(user_id, -total)
    update_balance(target_id, amount)
    log_transfer(user_id, target_id, amount, fee)

    await update.message.reply_text(
        f"✅ تم تحويل <b>{amount} ر.س</b> إلى المستخدم <b>{target_id}</b>.\n"
        f"💸 تم خصم عمولة <b>{fee} ر.س</b>.\n"
        f"💰 رصيدك الجديد: <b>{get_user_balance(user_id)} ر.س</b>",
        parse_mode="HTML"
    )
    context.user_data["transfer_stage"] = False

# ✅ عرض سجل التحويلات (للمشرفين فقط)
# ✅ عرض سجل التحويلات (للمشرفين فقط)
async def show_transfer_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.callback_query.answer("❌ لا تملك صلاحية الوصول لهذا السجل.", show_alert=True)
        return

    try:
        with open(TRANSFER_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if not data:
        await update.callback_query.message.edit_text("📭 لا يوجد أي تحويلات حتى الآن.")
        return

    recent_transfers = data[-10:]
    lines = []
    for t in reversed(recent_transfers):
        lines.append(
            f"🔁 <b>{t['from']}</b> ← <b>{t['to']}</b>\n"
            f"💸 المبلغ: <b>{t['amount']} ر.س</b> | العمولة: <b>{t['fee']} ر.س</b>\n"
            f"📅 التاريخ: {t['timestamp']}\n"
            f"— — — — — —"
        )

    message = "<b>📊 آخر التحويلات بين المستخدمين:</b>\n\n" + "\n".join(lines)
    await update.callback_query.message.edit_text(
    message,
    parse_mode="HTML",
    reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard"),
            InlineKeyboardButton("🗑️ حذف الكل", callback_data="confirm_clear_transfers")
        ]
    ])
)
    
async def confirm_clear_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.callback_query.answer("❌ غير مصرح لك.", show_alert=True)
        return

    await update.callback_query.message.edit_text(
        "⚠️ هل أنت متأكد من حذف جميع سجل التحويلات؟ لا يمكن التراجع.\n\n"
        "اضغط للتأكيد:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ نعم، احذف", callback_data="clear_transfers"),
                InlineKeyboardButton("🔙 إلغاء", callback_data="back_to_dashboard")
            ]
        ]),
        parse_mode="HTML"
    )

async def clear_all_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.callback_query.answer("❌ غير مصرح لك.", show_alert=True)
        return

    try:
        with open(TRANSFER_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        await update.callback_query.message.edit_text("✅ تم حذف جميع سجل التحويلات.")
    except Exception as e:
        await update.callback_query.message.edit_text("❌ حدث خطأ أثناء الحذف.")

