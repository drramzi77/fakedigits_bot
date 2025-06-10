# handlers/agent_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE # # تم إضافة DEFAULT_LANGUAGE
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from keyboards.utils_kb import back_button # # تم إضافة هذا السطر لاستخدام زر العودة الموحد

# ✅ صفحة كن وكيلاً معنا
async def show_agent_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض معلومات حول برنامج الوكلاء ومميزاته وشروطه.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    text = (
        messages["agent_program_title"] + "\n\n" + # # استخدام النص المترجم
        messages["agent_benefits_title"] + "\n" + # # استخدام النص المترجم
        messages["agent_benefit_1"] + "\n" + # # استخدام النص المترجم
        messages["agent_benefit_2"] + "\n" + # # استخدام النص المترجم
        messages["agent_benefit_3"] + "\n" + # # استخدام النص المترجم
        messages["agent_benefit_4"] + "\n\n" + # # استخدام النص المترجم
        messages["agent_profit_example_title"] + "\n" + # # استخدام النص المترجم
        messages["agent_profit_example_scenario"] + "\n" + # # استخدام النص المترجم
        messages["agent_monthly_profit"].format(profit="100", currency=messages["price_currency"], commission_percentage="20") + "\n\n" + # # استخدام النص المترجم
        messages["agent_terms_title"] + "\n" + # # استخدام النص المترجم
        messages["agent_term_1"] + "\n" + # # استخدام النص المترجم
        messages["agent_term_2"] + "\n\n" + # # استخدام النص المترجم
        messages["agent_call_to_action"] # # استخدام النص المترجم
    )

    buttons = [
        [InlineKeyboardButton(messages["send_agent_request_button"], callback_data="apply_agent")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code) # # استخدام زر العودة الموحد
    ]

    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )

# ✅ استقبال طلب الانضمام كوكيل
async def apply_as_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب المستخدم للانضمام كوكيل.
    يرسل تفاصيل الطلب إلى المشرفين.
    """
    query = update.callback_query
    user = query.from_user
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة

    # إرسال الطلب إلى المشرفين
    msg = (
        messages["new_agent_request_title"] + "\n\n" + # # استخدام النص المترجم
        messages["agent_request_name"].format(full_name=user.full_name) + "\n" + # # استخدام النص المترجم
        messages["agent_request_username"].format(username=user.username if user.username else messages["not_available"]) + "\n" + # # استخدام النص المترجم
        messages["agent_request_id"].format(user_id=user.id) # # استخدام النص المترجم
    )

    for admin_id in ADMINS:
        await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode="HTML")

    await query.message.edit_text(
        messages["agent_request_sent_success"] + "\n" + # # استخدام النص المترجم
        messages["agent_request_review_notice"], # # استخدام النص المترجم
        reply_markup=InlineKeyboardMarkup([
            back_button(text=messages["back_to_dashboard_button_text"], callback_data="back_to_dashboard", lang_code=lang_code) # # استخدام زر العودة الموحد
        ])
    )