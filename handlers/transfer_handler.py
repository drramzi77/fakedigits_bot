# handlers/transfer_handler.py

import json
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, update_balance
from config import ADMINS
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup # ✅ تم إضافة هذا السطر

logger = logging.getLogger(__name__)

TRANSFER_LOG_FILE = os.path.join("data", "transfers.json")

# 🔘 زر تواصل مع الإدارة
def contact_admin_button():
    return create_reply_markup([
        [InlineKeyboardButton("💬 تواصل مع الدعم", url="https://t.me/DrRamzi0")],
        back_button()
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

    data = load_json_file(TRANSFER_LOG_FILE, [])
    data.append(transfer)
    save_json_file(TRANSFER_LOG_FILE, data)
    logger.info(f"تم تسجيل تحويل: من {sender_id} إلى {target_id} بمبلغ {amount}.")

# ✅ عند الضغط على زر "تحويل الرصيد"
async def start_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    logger.info(f"start_transfer: المستخدم {user_id} ضغط على تحويل الرصيد. user_data قبل التعديل: {context.user_data}")

    if update.callback_query:
        await update.callback_query.answer()
        message_editor = update.callback_query.message.edit_text
    else:
        message_editor = update.message.reply_text

    if user_id in ADMINS:
        logger.warning(f"المشرف {user_id} حاول استخدام خيار تحويل الرصيد الخاص بالمستخدمين.")
        await message_editor(
            "⚠️ هذا الخيار مخصص فقط للمستخدمين.\n"
            "🔋 لشحن رصيد مستخدم، استخدم القسم المخصص لذلك في لوحة التحكم.",
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button()
            ])
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
        await message_editor(msg, parse_mode="HTML", reply_markup=contact_admin_button())
    else:
        context.user_data["transfer_stage"] = "awaiting_input"
        context.user_data["awaiting_input"] = "transfer_amount"
        logger.info(f"start_transfer: تم تعيين transfer_stage لـ {user_id} إلى 'awaiting_input' و awaiting_input إلى 'transfer_amount'. user_data بعد التعديل: {context.user_data}")
        await message_editor(
            f"💰 رصيدك الحالي: <b>{balance} ر.س</b>\n\n"
            "🔁 <b>تحويل الرصيد</b>\n\n"
            "📥 أرسل المعرف والمبلغ بالشكل التالي:\n\n"
            "<code>123456789 20</code>\n\n"
            "✅ <b>123456789</b>: معرف المستخدم\n"
            "✅ <b>20</b>: المبلغ المطلوب تحويله\n"
            "💸 عمولة التحويل: <b>1%</b>",
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                [InlineKeyboardButton("❌ إلغاء", callback_data="back_to_dashboard")]
            ])
        )
        logger.info(f"المستخدم {user_id} بدأ عملية تحويل الرصيد. رصيده الحالي: {balance}.")


# ✅ معالجة مدخلات التحويل وطلب التأكيد
async def handle_transfer_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"handle_transfer_input: المستخدم {user_id} أرسل نص: '{update.message.text}'. user_data: {context.user_data}")

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text(
            "❌ الصيغة غير صحيحة. استخدم:\n<code>123456789 20</code>",
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.warning(f"المستخدم {user_id} أدخل تنسيقًا غير صالح للتحويل: '{text}'.")
        return

    try:
        target_id = int(parts[0])
        amount = float(parts[1])
    except ValueError as e:
        logger.warning(f"المستخدم {user_id} أدخل معرفًا أو مبلغًا غير رقمي للتحويل: '{text}'. الخطأ: {e}")
        await update.message.reply_text(
            "❌ تأكد من أن المعرف والمبلغ أرقام صحيحة.",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        return

    if target_id == user_id:
        await update.message.reply_text(
            "❌ لا يمكنك تحويل الرصيد إلى نفسك.",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.warning(f"المستخدم {user_id} حاول تحويل الرصيد إلى نفسه.")
        return

    if amount <= 0:
        await update.message.reply_text(
            "❌ المبلغ يجب أن يكون أكبر من صفر.",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.warning(f"المستخدم {user_id} حاول تحويل مبلغ غير موجب: {amount}.")
        return

    balance = get_user_balance(user_id)
    fee = round(amount * 0.01, 2)
    total_deduction = round(amount + fee, 2)

    if balance < total_deduction:
        await update.message.reply_text(
            f"❌ رصيدك غير كافٍ لإتمام التحويل المطلوب.\nرصيدك الحالي: {balance} ر.س\nالمطلوب: {total_deduction} ر.س",
            parse_mode="HTML",
            reply_markup=contact_admin_button()
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.info(f"المستخدم {user_id} ليس لديه رصيد كافٍ لتحويل {amount} إلى {target_id}. الرصيد: {balance}.")
        return

    context.user_data["transfer_details"] = {
        "target_id": target_id,
        "amount": amount,
        "fee": fee,
        "total_deduction": total_deduction
    }
    context.user_data["transfer_stage"] = "confirm_transfer"

    confirmation_message = (
        f"🔁 <b>تأكيد تحويل الرصيد</b>\n\n"
        f"✅ سيتم تحويل: <b>{amount} ر.س</b>\n"
        f"👤 إلى معرف: <code>{target_id}</code>\n"
        f"💸 عمولة التحويل: <b>{fee} ر.س</b>\n"
        f"💰 إجمالي الخصم من رصيدك: <b>{total_deduction} ر.س</b>\n\n"
        "⚠️ يرجى التأكد من صحة المعرف. لا يمكن التراجع عن هذه العملية."
    )
    confirmation_keyboard = create_reply_markup([
        [
            InlineKeyboardButton("✅ تأكيد التحويل", callback_data="confirm_transfer_yes"),
            InlineKeyboardButton("❌ إلغاء", callback_data="confirm_transfer_no")
        ],
        back_button()
    ])

    await update.message.reply_text(
        confirmation_message,
        reply_markup=confirmation_keyboard,
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} على وشك تحويل {amount} إلى {target_id}. يطلب التأكيد.")


# ✅ تنفيذ التحويل الفعلي بعد التأكيد
async def confirm_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    logger.info(f"confirm_transfer: المستخدم {user_id} ضغط زر التأكيد: '{query.data}'. user_data: {context.user_data}")

    if context.user_data.get("transfer_stage") != "confirm_transfer":
        await query.edit_message_text(
            "❌ انتهت صلاحية عملية التحويل أو تم إلغاؤها.",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        logger.warning(f"المستخدم {user_id} حاول تأكيد تحويل في مرحلة غير صحيحة.")
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("transfer_details", None)
        context.user_data.pop("awaiting_input", None)
        return

    if query.data == "confirm_transfer_yes":
        details = context.user_data.get("transfer_details")
        if not details:
            await query.edit_message_text(
                "❌ بيانات التحويل غير موجودة. يرجى البدء من جديد.",
                reply_markup=create_reply_markup([
                    back_button()
                ])
            )
            logger.error(f"المستخدم {user_id} حاول تأكيد تحويل بدون تفاصيل. محتمل خطأ منطقي.")
            context.user_data.pop("transfer_stage", None)
            context.user_data.pop("awaiting_input", None)
            return

        target_id = details["target_id"]
        amount = details["amount"]
        fee = details["fee"]
        total_deduction = details["total_deduction"]

        current_balance = get_user_balance(user_id)
        if current_balance < total_deduction:
            await query.edit_message_text(
                f"❌ عذراً، رصيدك أصبح غير كافٍ ({current_balance} ر.س) لإتمام التحويل المطلوب ({total_deduction} ر.س).\n"
                "يرجى شحن رصيدك أو التواصل مع الدعم.",
                reply_markup=contact_admin_button()
            )
            logger.warning(f"المستخدم {user_id} أكد التحويل لكن رصيده أصبح غير كافٍ. الحالي: {current_balance}.")
            context.user_data.pop("transfer_stage", None)
            context.user_data.pop("transfer_details", None)
            context.user_data.pop("awaiting_input", None)
            return

        try:
            update_balance(user_id, -total_deduction)
            update_balance(target_id, amount)
            log_transfer(user_id, target_id, amount, fee)

            await query.edit_message_text(
                f"✅ تم تحويل <b>{amount} ر.س</b> إلى المستخدم <b>{target_id}</b>.\n"
                f"💸 تم خصم عمولة <b>{fee} ر.س</b>.\n"
                f"💰 رصيدك الجديد: <b>{get_user_balance(user_id)} ر.س</b>",
                parse_mode="HTML",
                reply_markup=create_reply_markup([
                    back_button()
                ])
            )
            logger.info(f"المستخدم {user_id} أكد وحوّل {amount} إلى {target_id}. الرصيد الجديد: {get_user_balance(user_id)}.")
        except Exception as e:
            logger.error(f"خطأ أثناء تنفيذ تحويل الرصيد من {user_id} إلى {target_id} بمبلغ {amount} بعد التأكيد: {e}", exc_info=True)
            await query.edit_message_text(
                "❌ حدث خطأ غير متوقع أثناء عملية التحويل بعد التأكيد. يرجى التواصل مع الدعم.",
                reply_markup=contact_admin_button()
            )

    elif query.data == "confirm_transfer_no":
        await query.edit_message_text(
            "❌ تم إلغاء عملية التحويل.",
            reply_markup=create_reply_markup([
                back_button()
            ])
        )
        logger.info(f"المستخدم {user_id} ألغى عملية التحويل.")

    context.user_data.pop("transfer_stage", None)
    context.user_data.pop("transfer_details", None)
    context.user_data.pop("awaiting_input", None)


# ✅ عرض سجل التحويلات (للمشرفين فقط)
async def show_transfer_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.callback_query.answer("❌ لا تملك صلاحية الوصول لهذا السجل.", show_alert=True)
        return

    data = load_json_file(TRANSFER_LOG_FILE, [])

    if not data:
        await update.callback_query.message.edit_text("📭 لا يوجد أي تحويلات حتى الآن.")
        logger.info(f"المشرف {user_id} عرض سجل التحويلات، ولا يوجد أي تحويلات.")
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
        reply_markup=create_reply_markup([
            back_button(text="🔙 العودة"),
            [InlineKeyboardButton("🗑️ حذف الكل", callback_data="confirm_clear_transfers")]
        ])
    )
    logger.info(f"المشرف {user_id} عرض آخر {len(recent_transfers)} تحويلات.")


async def confirm_clear_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.callback_query.answer("❌ غير مصرح لك.", show_alert=True)
        logger.warning(f"المستخدم {user_id} حاول تأكيد حذف التحويلات بدون صلاحية.")
        return

    await update.callback_query.message.edit_text(
        "⚠️ هل أنت متأكد من حذف جميع سجل التحويلات؟ لا يمكن التراجع.\n\n"
        "اضغط للتأكيد:",
        reply_markup=create_reply_markup([
            [
                InlineKeyboardButton("✅ نعم، احذف", callback_data="clear_transfers"),
                InlineKeyboardButton("❌ إلغاء", callback_data="back_to_dashboard")
            ]
        ]),
        parse_mode="HTML"
    )
    logger.info(f"المشرف {user_id} طلب تأكيد حذف جميع التحويلات.")


async def clear_all_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.callback_query.answer("❌ غير مصرح لك.", show_alert=True)
        logger.warning(f"المستخدم {user_id} حاول حذف جميع التحويلات بدون صلاحية.")
        return

    save_json_file(TRANSFER_LOG_FILE, [])
    await update.callback_query.message.edit_text("✅ تم حذف جميع سجل التحويلات.")
    logger.info(f"المشرف {user_id} قام بحذف جميع سجلات التحويلات.")