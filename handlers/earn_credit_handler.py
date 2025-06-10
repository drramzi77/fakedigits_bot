# handlers/earn_credit_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية
from keyboards.utils_kb import back_button # # تم إضافة هذا السطر لاستخدام زر العودة الموحد

async def show_earn_credit_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض صفحة "اربح رصيد مجانًا" للمستخدم، مع كود الإحالة الخاص به ومعلومات المكافأة.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    user_id = query.from_user.id
    referral_code = f"ref_{user_id}"  # كود الإحالة المميز لهذا المستخدم

    message = (
        messages["earn_credit_title"] + "\n\n" + # # استخدام النص المترجم
        messages["earn_credit_description"] + "\n\n" + # # استخدام النص المترجم
        messages["your_referral_code"].format(referral_code=referral_code) + "\n" + # # استخدام النص المترجم
        messages["your_reward"].format(amount="2", currency=messages["price_currency"]) + "\n\n" + # # استخدام النص المترجم
        messages["more_referrals_more_credit"] # # استخدام النص المترجم
    )

    buttons = [
        [InlineKeyboardButton(messages["copy_referral_code_button"], switch_inline_query=referral_code)], # # استخدام النص المترجم
        [InlineKeyboardButton(messages["view_referrals_button"], callback_data="view_referrals")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code) # # استخدام زر العودة الموحد
    ]

    await query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )


async def view_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة وهمية بالمدعوين عبر كود الإحالة (في انتظار الربط بقاعدة بيانات).
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    # ⛔️ لاحقاً اربطها بقاعدة بيانات فعلية
    fake_referrals = [
        {"name": "User1", "joined": "2025-06-01"},
        {"name": "User2", "joined": "2025-06-04"},
    ]

    if not fake_referrals:
        await query.message.edit_text(messages["no_referrals_yet"]) # # استخدام النص المترجم
        return

    lines = [messages["referrals_list_title"] + "\n"] # # استخدام النص المترجم
    for ref in fake_referrals:
        lines.append(messages["referral_entry"].format(name=ref['name'], joined_date=ref['joined'])) # # استخدام النص المترجم

    # # النص "العودة" في نهاية الرسالة ليس ضرورياً لأنه يوجد زر
    # lines.append(messages["back_button_text"])
    
    buttons = [back_button(text=messages["back_button_text"], callback_data="earn_credit", lang_code=lang_code)] # # استخدام زر العودة الموحد

    await query.message.edit_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")