# handlers/transfer_handler.py

import json
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance, update_balance
from config import ADMINS, DEFAULT_LANGUAGE
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages

logger = logging.getLogger(__name__)

TRANSFERS_FILE = os.path.join("data", "transfers.json")
USERS_FILE = os.path.join("data", "users.json") # # تم التأكد من وجود هذا المتغير

def contact_admin_button(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح صغيرة بزر للتواصل مع الدعم.
    """
    messages = get_messages(lang_code)
    return create_reply_markup([
        [InlineKeyboardButton(messages["contact_support_button_transfer"], url="https://t.me/DrRamzi0")],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

def log_transfer(sender_id, target_id, amount, fee):
    """
    يسجل تفاصيل عملية تحويل الرصيد في ملف سجل التحويلات.
    """
    transfer = {
        "from": sender_id,
        "to": target_id,
        "amount": amount,
        "fee": fee,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data = load_json_file(TRANSFERS_FILE, [])
    data.append(transfer)
    save_json_file(TRANSFERS_FILE, data)
    logger.info(f"تم تسجيل تحويل: من {sender_id} إلى {target_id} بمبلغ {amount}.")


async def start_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يبدأ عملية تحويل الرصيد.
    يتحقق من رصيد المستخدم ويطلب معرف المستلم والمبلغ.
    """
    user = update.effective_user # # الحصول على كائن المستخدم
    user_id = user.id
    balance = get_user_balance(user_id, user.to_dict()) # # # تم التعديل: تمرير user.to_dict()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    logger.info(f"start_transfer: المستخدم {user_id} ضغط على تحويل الرصيد. user_data قبل التعديل: {context.user_data}")

    if update.callback_query:
        await update.callback_query.answer()
        message_editor = update.callback_query.message.edit_text
    else:
        message_editor = update.message.reply_text

    if user_id in ADMINS:
        logger.warning(f"المشرف {user_id} حاول استخدام خيار تحويل الرصيد الخاص بالمستخدمين.")
        await message_editor(
            messages["admin_transfer_warning"],
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        return

    if balance < 5: # الرقم 5 يمكن أن يكون متغيرًا في config لاحقاً
        msg = (
            messages["transfer_balance_too_low"].format(balance=balance, currency=messages["price_currency"]) + "\n" +
            messages["transfer_fee_info"].format(fee_percentage="1") + "\n\n" +
            messages["transfer_solution_prompt"] + "\n" +
            messages["transfer_solution_recharge"] + "\n" +
            messages["transfer_solution_contact_support"]
        )
        await message_editor(msg, parse_mode="HTML", reply_markup=contact_admin_button(lang_code))
    else:
        context.user_data["transfer_stage"] = "awaiting_input"
        context.user_data["awaiting_input"] = "transfer_amount"
        logger.info(f"start_transfer: تم تعيين transfer_stage لـ {user_id} إلى 'awaiting_input' و awaiting_input إلى 'transfer_amount'. user_data بعد التعديل: {context.user_data}")
        await message_editor(
            messages["transfer_initial_prompt"].format(balance=balance, currency=messages["price_currency"]) + "\n\n" +
            messages["transfer_format_instruction"] + "\n\n" +
            messages["transfer_example"] + "\n\n" +
            messages["transfer_id_explanation"] + "\n" +
            messages["transfer_amount_explanation"] + "\n" +
            messages["transfer_fee_info"].format(fee_percentage="1"),
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                [InlineKeyboardButton(messages["cancel_button_text"], callback_data="back_to_dashboard")]
            ])
        )
        logger.info(f"المستخدم {user_id} بدأ عملية تحويل الرصيد. رصيده الحالي: {balance}.")


async def handle_transfer_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج المدخل النصي من المستخدم لعملية التحويل.
    يتحقق من صحة المعرف والمبلغ ويطلب التأكيد.
    """
    user = update.effective_user # # الحصول على كائن المستخدم
    user_id = user.id
    logger.info(f"handle_transfer_input: المستخدم {user_id} أرسل نص: '{update.message.text}'. user_data: {context.user_data}")

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text(
            messages["transfer_invalid_format_error"],
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
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
            messages["transfer_invalid_id_or_amount"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        return

    if target_id == user_id:
        await update.message.reply_text(
            messages["cannot_transfer_to_self"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.warning(f"المستخدم {user_id} حاول تحويل الرصيد إلى نفسه.")
        return

    if amount <= 0:
        await update.message.reply_text(
            messages["transfer_amount_must_be_positive"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        context.user_data.pop("transfer_stage", None)
        context.user_data.pop("awaiting_input", None)
        logger.warning(f"المستخدم {user_id} حاول تحويل مبلغ غير موجب: {amount}.")
        return

    balance = get_user_balance(user_id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()
    fee = round(amount * 0.01, 2)
    total_deduction = round(amount + fee, 2)

    if balance < total_deduction:
        await update.message.reply_text(
            messages["insufficient_balance_for_transfer"].format(
                current_balance=balance,
                required_amount=total_deduction,
                currency=messages["price_currency"]
            ),
            parse_mode="HTML",
            reply_markup=contact_admin_button(lang_code)
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
        messages["confirm_transfer_title"] + "\n\n" +
        messages["transfer_amount_confirm"].format(amount=amount, currency=messages["price_currency"]) + "\n" +
        messages["transfer_target_id_confirm"].format(target_id=target_id) + "\n" +
        messages["transfer_fee_confirm"].format(fee=fee, currency=messages["price_currency"]) + "\n" +
        messages["transfer_total_deduction_confirm"].format(total_deduction=total_deduction, currency=messages["price_currency"]) + "\n\n" +
        messages["transfer_confirmation_warning"]
    )
    confirmation_keyboard = create_reply_markup([
        [
            InlineKeyboardButton(messages["confirm_transfer_button"], callback_data="confirm_transfer_yes"),
            InlineKeyboardButton(messages["cancel_button_text"], callback_data="confirm_transfer_no")
        ],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

    await update.message.reply_text(
        confirmation_message,
        reply_markup=confirmation_keyboard,
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} على وشك تحويل {amount} إلى {target_id}. يطلب التأكيد.")


async def confirm_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    ينفذ عملية تحويل الرصيد الفعلية بعد تأكيد المستخدم.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_id = user.id
    logger.info(f"confirm_transfer: المستخدم {user_id} ضغط زر التأكيد: '{query.data}'. user_data: {context.user_data}")

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if context.user_data.get("transfer_stage") != "confirm_transfer":
        await query.edit_message_text(
            messages["transfer_expired_or_cancelled"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
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
                messages["transfer_details_missing"],
                reply_markup=create_reply_markup([
                    back_button(text=messages["back_button_text"], lang_code=lang_code)
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

        current_balance = get_user_balance(user_id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()
        if current_balance < total_deduction:
            await query.edit_message_text(
                messages["insufficient_balance_after_check"].format(
                    current_balance=current_balance,
                    required_amount=total_deduction,
                    currency=messages["price_currency"]
                ),
                reply_markup=contact_admin_button(lang_code)
            )
            logger.warning(f"المستخدم {user_id} أكد التحويل لكن رصيده أصبح غير كافٍ. الحالي: {current_balance}.")
            context.user_data.pop("transfer_stage", None)
            context.user_data.pop("transfer_details", None)
            context.user_data.pop("awaiting_input", None)
            return

        try:
            update_balance(user_id, -total_deduction, user.to_dict()) # # تم التعديل: تمرير user.to_dict()
            
            # # الحصول على معلومات المستخدم المستلم لتمريرها إلى update_balance
            users_data = load_json_file(USERS_FILE, default_data={})
            target_user_info = users_data.get(str(target_id), {"id": target_id})
            update_balance(target_id, amount, target_user_info)
            log_transfer(user_id, target_id, amount, fee)

            await query.edit_message_text(
                messages["transfer_successful_message"].format(
                    amount=amount,
                    currency=messages["price_currency"],
                    target_id=target_id,
                    fee=fee,
                    new_balance=get_user_balance(user_id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()
                ),
                parse_mode="HTML",
                reply_markup=create_reply_markup([
                    back_button(text=messages["back_button_text"], lang_code=lang_code)
                ])
            )
            logger.info(f"المستخدم {user_id} أكد وحوّل {amount} إلى {target_id}. الرصيد الجديد: {get_user_balance(user_id, user.to_dict())}.")
        except Exception as e:
            logger.error(f"خطأ أثناء تنفيذ تحويل الرصيد من {user_id} إلى {target_id} بمبلغ {amount} بعد التأكيد: {e}", exc_info=True)
            await query.edit_message_text(
                messages["transfer_unexpected_error"],
                reply_markup=contact_admin_button(lang_code)
            )

    elif query.data == "confirm_transfer_no":
        await query.edit_message_text(
            messages["transfer_cancelled_message"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        logger.info(f"المستخدم {user_id} ألغى عملية التحويل.")

    context.user_data.pop("transfer_stage", None)
    context.user_data.pop("transfer_details", None)
    context.user_data.pop("awaiting_input", None)


async def show_transfer_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض آخر 10 تحويلات رصيد بين المستخدمين (للمشرفين فقط).
    """
    user = update.effective_user # # الحصول على كائن المستخدم
    user_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.callback_query.answer(messages["no_permission_alert"], show_alert=True)
        return

    data = load_json_file(TRANSFERS_FILE, {})

    if not data:
        await update.callback_query.message.edit_text(messages["no_transfers_yet"])
        logger.info(f"المشرف {user_id} عرض سجل التحويلات، ولا يوجد أي تحويلات.")
        return

    recent_transfers = data[-10:]
    lines = []
    for t in reversed(recent_transfers):
        lines.append(
            messages["transfer_log_entry"].format(
                sender_id=t['from'],
                receiver_id=t['to'],
                amount=t['amount'],
                currency=messages["price_currency"],
                fee=t['fee'],
                date=t['timestamp']
            )
        )

    message = messages["recent_transfers_title"] + "\n\n" + "\n".join(lines)
    await update.callback_query.message.edit_text(
        message,
        parse_mode="HTML",
        reply_markup=create_reply_markup([
            back_button(text=messages["back_button_text"], lang_code=lang_code),
            [InlineKeyboardButton(messages["clear_all_transfers_button"], callback_data="confirm_clear_transfers")]
        ])
    )
    logger.info(f"المشرف {user_id} عرض آخر {len(recent_transfers)} تحويلات.")


async def confirm_clear_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يطلب تأكيد من المشرف قبل حذف جميع سجلات التحويلات.
    """
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.callback_query.answer(messages["unauthorized_alert"], show_alert=True)
        logger.warning(f"المستخدم {user_id} حاول تأكيد حذف التحويلات بدون صلاحية.")
        return

    await update.callback_query.message.edit_text(
        messages["confirm_clear_transfers_message"],
        reply_markup=create_reply_markup([
            [
                InlineKeyboardButton(messages["yes_delete_button"], callback_data="clear_transfers"),
                InlineKeyboardButton(messages["cancel_button_text"], callback_data="back_to_dashboard")
            ]
        ]),
        parse_mode="HTML"
    )
    logger.info(f"المشرف {user_id} طلب تأكيد حذف جميع التحويلات.")


async def clear_all_transfers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    ينفذ حذف جميع سجلات التحويلات بعد تأكيد المشرف.
    """
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if user_id not in ADMINS:
        await update.callback_query.answer(messages["unauthorized_alert"], show_alert=True)
        logger.warning(f"المستخدم {user_id} حاول حذف جميع التحويلات بدون صلاحية.")
        return

    save_json_file(TRANSFERS_FILE, [])
    await update.callback_query.message.edit_text(messages["transfers_cleared_success"])
    logger.info(f"المشرف {user_id} قام بحذف جميع سجلات التحويلات.")