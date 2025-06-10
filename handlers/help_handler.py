# handlers/help_handler.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة خيارات الدعم والمساعدة للمستخدم.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = messages["help_menu_welcome_message"].format(bot_name="FakeDigits") # # استخدام النص المترجم
    keyboard = create_reply_markup([
        [InlineKeyboardButton(messages["contact_support_button"], callback_data="contact_support")], # # استخدام النص المترجم
        [InlineKeyboardButton(messages["usage_guide_button"], callback_data="usage_guide")], # # استخدام النص المترجم
        [InlineKeyboardButton(messages["faq_button"], callback_data="faq")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم لزر العودة
    ])

    await query.message.edit_text(message, reply_markup=keyboard)


async def handle_usage_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض شرحاً مفصلاً لكيفية استخدام البوت وخطوات شراء الأرقام.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = (
        messages["usage_guide_title"] + "\n\n" + # # استخدام النص المترجم
        messages["usage_step_1"] + "\n" + # # استخدام النص المترجم
        messages["usage_step_2"] + "\n" + # # استخدام النص المترجم
        messages["usage_step_3"] + "\n" + # # استخدام النص المترجم
        messages["usage_step_4"] + "\n" + # # استخدام النص المترجم
        messages["usage_step_5"] + "\n\n" + # # استخدام النص المترجم
        messages["usage_notes_title"] + "\n" + # # استخدام النص المترجم
        messages["usage_note_1"] + "\n" + # # استخدام النص المترجم
        messages["usage_note_2"] + "\n" + # # استخدام النص المترجم
        messages["usage_note_3"] + "\n\n" + # # استخدام النص المترجم
        messages["usage_problem_contact_support"] + "\n" + # # استخدام النص المترجم
        messages["back_to_menu_note"] # # استخدام النص المترجم
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم لزر العودة
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")

async def handle_contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض معلومات الاتصال بالدعم الفني للبوت.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = (
        messages["contact_support_title"] + "\n\n" + # # استخدام النص المترجم
        messages["contact_support_prompt"] + "\n" + # # استخدام النص المترجم
        messages["contact_support_link"].format(support_link="https://t.me/DrRamzi0") + "\n\n" + # # استخدام النص المترجم
        messages["contact_support_hours"] + "\n" + # # استخدام النص المترجم
        messages["contact_support_tip"] # # استخدام النص المترجم
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم لزر العودة
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")

async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض الأسئلة الشائعة وإجاباتها حول استخدام البوت.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = (
        messages["faq_title"] + "\n\n" + # # استخدام النص المترجم
        messages["faq_q1"] + "\n" + messages["faq_a1"] + "\n\n" + # # استخدام النصوص المترجمة
        messages["faq_q2"] + "\n" + messages["faq_a2"] + "\n\n" + # # استخدام النصوص المترجمة
        messages["faq_q3"] + "\n" + messages["faq_a3"] + "\n\n" + # # استخدام النصوص المترجمة
        messages["faq_more_questions"] # # استخدام النص المترجم
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم لزر العودة
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")