import json
import os
import logging # # إضافة هذا السطر
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, update_balance

logger = logging.getLogger(__name__) # # إضافة هذا السطر

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

    data = []
    try:
        if os.path.exists(TRANSFER_LOG_FILE): # # التحقق من وجود الملف
            with open(TRANSFER_LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
    except json.JSONDecodeError:
        logger.error(f"ملف سجل التحويلات '{TRANSFER_LOG_FILE}' تالف. سيتم إعادة إنشائه.", exc_info=True)
        data = [] # # إذا كان الملف تالفًا، ابدأ بقائمة فارغة
    except FileNotFoundError:
        logger.warning(f"ملف سجل التحويلات '{TRANSFER_LOG_FILE}' غير موجود. سيتم إنشاؤه.")

    data.append(transfer)
    try:
        with open(TRANSFER_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"تم تسجيل تحويل: من {sender_id} إلى {target_id} بمبلغ {amount}.") # # تسجيل العملية
    except IOError as e:
        logger.error(f"خطأ في كتابة ملف سجل التحويلات '{TRANSFER_LOG_FILE}': {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تسجيل التحويل: {e}", exc_info=True)

# ✅ عند الضغط على زر "تحويل الرصيد"
async def start_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    if user_id in ADMIN_IDS:
        logger.warning(f"المشرف {user_id} حاول استخدام خيار تحويل الرصيد الخاص بالمستخدمين.") # # تسجيل تحذير
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

   # ...
    try:
        target_id = int(parts[0])
        amount = float(parts[1])
    except ValueError as e: # # تحديد نوع الخطأ
        logger.warning(f"المستخدم {user_id} أدخل تنسيقًا غير صالح للتحويل: '{text}'. الخطأ: {e}") # # تسجيل تحذير
        await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم:\n<code>123456789 20</code>", parse_mode="HTML")
        return
# ...
    try:
        update_balance(user_id, -total)
        update_balance(target_id, amount)
        log_transfer(user_id, target_id, amount, fee)
        logger.info(f"المستخدم {user_id} حول {amount} إلى {target_id}. الرصيد الجديد: {get_user_balance(user_id)}.") # # تسجيل نجاح العملية
    except Exception as e: # # أي خطأ آخر
        logger.error(f"خطأ أثناء تنفيذ تحويل الرصيد من {user_id} إلى {target_id} بمبلغ {amount}: {e}", exc_info=True) # # تسجيل خطأ
        await update.message.reply_text("❌ حدث خطأ غير متوقع أثناء عملية التحويل. يرجى التواصل مع الدعم.", reply_markup=contact_admin_button())
        return

    await update.message.reply_text(
        f"✅ تم تحويل <b>{amount} ر.س</b> إلى المستخدم <b>{target_id}</b>.\n"
        f"💸 تم خصم عمولة <b>{fee} ر.س</b>.\n"
        f"💰 رصيدك الجديد: <b>{get_user_balance(user_id)} ر.س</b>",
        parse_mode="HTML"
    )
    context.user_data["transfer_stage"] = False


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
        logger.warning(f"ملف سجل التحويلات '{TRANSFER_LOG_FILE}' غير موجود عند محاولة عرضه.") # # تسجيل تحذير
        data = []
    except json.JSONDecodeError:
        logger.error(f"ملف سجل التحويلات '{TRANSFER_LOG_FILE}' تالف.", exc_info=True) # # تسجيل خطأ
        data = []
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند محاولة عرض سجل التحويلات: {e}", exc_info=True) # # تسجيل خطأ
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
        logger.info(f"المشرف {user_id} قام بحذف جميع سجلات التحويلات.") # # تسجيل نجاح
    except Exception as e:
        logger.error(f"المشرف {user_id} فشل في حذف سجل التحويلات: {e}", exc_info=True) # # تسجيل خطأ
        await update.callback_query.message.edit_text("❌ حدث خطأ أثناء الحذف. يرجى مراجعة سجلات البوت.")

