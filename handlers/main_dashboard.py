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
    balance = get_user_balance(user_id) # # هذه الدالة تحتاج للتحديث لاحقاً لقراءة من DB

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    # الاسم الظاهر (username أو الاسم الكامل)
    display_name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"

    message = (
        messages["dashboard_welcome"].format(display_name=display_name) + "\n\n" + # # استخدام النص المترجم
        messages["dashboard_id"].format(user_id=user_id) + "\n" + # # استخدام النص المترجم
        messages["dashboard_balance"].format(balance=balance, currency=messages["price_currency"]) + "\n\n" + # # **التعديل هنا: تم إضافة currency**
        messages["dashboard_channel_promo"].format(channel_link="@FakeDigitsPlus") + "\n" + # # استخدام النص المترجم
        messages["dashboard_choose_option"] # # استخدام النص المترجم
    )

    if update.callback_query:
        await update.callback_query.message.edit_text(
            message, reply_markup=dashboard_keyboard(user_id, lang_code), parse_mode="HTML" # # تمرير lang_code
        )
    elif update.message:
        await update.message.reply_text(
            message, reply_markup=dashboard_keyboard(user_id, lang_code), parse_mode="HTML" # # تمرير lang_code
        )

def recharge_options_keyboard(lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح الأزرار لخيارات شحن الرصيد.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    return create_reply_markup([
        [
            InlineKeyboardButton(messages["recharge_from_admin_button"], callback_data="recharge_admin") # # استخدام النص المترجم
        ],
        back_button(text=messages["back_button_text"]) # # استخدام النص المترجم لدوال الـ utils_kb
    ])


async def handle_recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن رصيدي".
    يعرض للمستخدم طرق الدفع المتاحة وكيفية شحن الرصيد.
    """
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    message = (
        messages["recharge_welcome_message"] + "\n\n" + # # استخدام النص المترجم
        messages["available_payment_methods"] + "\n" + # # استخدام النص المترجم
        "━━━━━━━━━━━━━━━━━━━━\n" +
        messages["payment_method_kareem"] + "\n" + # # استخدام النص المترجم
        messages["payment_method_vodafone"] + "\n" + # # استخدام النص المترجم
        messages["payment_method_zain"] + "\n" + # # استخدام النص المترجم
        messages["payment_method_crypto"] + "\n" + # # استخدام النص المترجم
        messages["payment_method_paypal"] + "\n" + # # استخدام النص المترجم
        messages["payment_method_other"] + "\n" + # # استخدام النص المترجم
        "━━━━━━━━━━━━━━━━━━━━\n\n" +
        messages["send_proof_message"].format(user_id=user_id) + "\n\n" + # # استخدام النص المترجم
        messages["contact_admin_message"].format(admin_username="@DrRamzi0") + "\n" + # # استخدام النص المترجم
        messages["press_button_to_proceed"] # # استخدام النص المترجم
    )

    await query.message.edit_text(
        message,
        reply_markup=recharge_options_keyboard(lang_code), # # تمرير lang_code
        parse_mode="HTML"
    )

async def handle_recharge_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن من الإدارة".
    يوجه المستخدم للتواصل مباشرة مع المطور لشحن الرصيد يدوياً.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    await query.message.edit_text(
        messages["recharge_admin_title"] + "\n\n" + # # استخدام النص المترجم
        messages["contact_dev_message"].format(dev_link="https://t.me/DrRamzi0") + "\n\n" + # # استخدام النص المترجم
        messages["send_proof_manual_recharge"] + "\n\n" + # # استخدام النص المترجم
        messages["back_to_previous_menu"], # # استخدام النص المترجم
        reply_markup=create_reply_markup([
            back_button(callback_data="recharge", text=messages["back_button_text"]) # # استخدام النص المترجم
        ]),
        parse_mode="HTML"
    )