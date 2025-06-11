# handlers/main_dashboard.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.dashboard_kb import dashboard_keyboard
from utils.balance import get_user_balance # # **تم التعديل هنا: استيراد من utils.balance بدلاً من utils.check_balance**
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض لوحة التحكم الرئيسية للبوت للمستخدم.
    يتضمن معلومات الرصيد ومعرف المستخدم.
    """
    user = update.effective_user
    user_id = user.id
    # # تم التعديل هنا لتمرير user.to_dict()
    balance = get_user_balance(user_id, user.to_dict())

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    # الاسم الظاهر (username أو الاسم الكامل)
    display_name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"

    message = (
        messages["dashboard_welcome"].format(display_name=display_name) + "\n\n" +
        messages["dashboard_id"].format(user_id=user_id) + "\n" +
        messages["dashboard_balance"].format(balance=balance, currency=messages["price_currency"]) + "\n\n" +
        messages["dashboard_channel_promo"].format(channel_link="@FakeDigitsPlus") + "\n" +
        messages["dashboard_choose_option"]
    )

    if update.callback_query:
        await update.callback_query.message.edit_text(
            message, reply_markup=dashboard_keyboard(user_id, lang_code), parse_mode="HTML"
        )
    elif update.message:
        await update.message.reply_text(
            message, reply_markup=dashboard_keyboard(user_id, lang_code), parse_mode="HTML"
        )

def recharge_options_keyboard(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح الأزرار لخيارات شحن الرصيد.
    """
    messages = get_messages(lang_code)

    return create_reply_markup([
        [
            InlineKeyboardButton(messages["recharge_from_admin_button"], callback_data="recharge_admin")
        ],
        back_button(text=messages["back_button_text"])
    ])


async def handle_recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن رصيدي".
    يعرض للمستخدم طرق الدفع المتاحة وكيفية شحن الرصيد.
    """
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = (
        messages["recharge_welcome_message"] + "\n\n" +
        messages["available_payment_methods"] + "\n" +
        "━━━━━━━━━━━━━━━━━━━━\n" +
        messages["payment_method_kareem"] + "\n" +
        messages["payment_method_vodafone"] + "\n" +
        messages["payment_method_zain"] + "\n" +
        messages["payment_method_crypto"] + "\n" +
        messages["payment_method_paypal"] + "\n" +
        messages["payment_method_other"] + "\n" +
        "━━━━━━━━━━━━━━━━━━━━\n\n" +
        messages["send_proof_message"].format(user_id=user_id) + "\n\n" +
        messages["contact_admin_message"].format(admin_username="@DrRamzi0") + "\n" +
        messages["press_button_to_proceed"]
    )

    await query.message.edit_text(
        message,
        reply_markup=recharge_options_keyboard(lang_code),
        parse_mode="HTML"
    )

async def handle_recharge_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن من الإدارة".
    يوجه المستخدم للتواصل مباشرة مع المطور لشحن الرصيد يدوياً.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    await query.message.edit_text(
        messages["recharge_admin_title"] + "\n\n" +
        messages["contact_dev_message"].format(dev_link="https://t.me/DrRamzi0") + "\n\n" +
        messages["send_proof_manual_recharge"] + "\n\n" +
        messages["back_to_previous_menu"],
        reply_markup=create_reply_markup([
            back_button(callback_data="recharge", text=messages["back_button_text"])
        ]),
        parse_mode="HTML"
    )