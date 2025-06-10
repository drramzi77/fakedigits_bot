# handlers/profile_handler.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.check_balance import get_user_balance # # هذه الدالة ستتغير مع DB
import datetime
import json
import os
import logging
from utils.data_manager import load_json_file # # هذه الدالة ستتغير مع DB
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

logger = logging.getLogger(__name__)

# 📌 مسار ملف المشتريات (يفترض وجوده أو إنشاؤه)
PURCHASES_FILE = os.path.join("data", "purchases.json") # # هذا المسار سيتغير لاحقاً مع DB
USERS_FILE = os.path.join("data", "users.json") # # هذا المسار سيتغير لاحقاً مع DB

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض الملف الشخصي للمستخدم.
    يعرض معلومات الحساب مثل الاسم، المعرف، الرصيد، وتاريخ التسجيل، وإحصائيات الطلبات.
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "لا يوجد"
    fullname = user.full_name
    balance = get_user_balance(int(user_id)) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    # احصل على تاريخ التسجيل (افتراضي)
    first_use_date = messages["not_available"] # # استخدام النص المترجم
    users_data = load_json_file(USERS_FILE, {}) # # هذه الدالة ستتغير لاحقاً
    user_data = users_data.get(user_id, {})
    if "created_at" in user_data:
        first_use_date = user_data["created_at"]
    else:
        logger.warning(f"ملف المستخدمين '{USERS_FILE}' غير موجود أو المستخدم {user_id} لا يملك تاريخ تسجيل.")


    # احصائيات الطلبات
    total_orders = 0
    total_spent = 0
    all_orders = load_json_file(PURCHASES_FILE, {}) # # هذه الدالة ستتغير لاحقاً
    user_orders = all_orders.get(user_id, [])
    total_orders = len(user_orders)
    total_spent = sum([order.get("price", 0) for order in user_orders])


    message = (
        messages["profile_welcome"].format(fullname=fullname) + "\n" + # # استخدام النص المترجم
        messages["profile_archive_intro"] + "\n" + # # استخدام النص المترجم
        "━━━━━━━━━━━━━━━\n" +
        messages["profile_name"].format(fullname=fullname) + "\n" + # # استخدام النص المترجم
        messages["profile_username"].format(username=username) + "\n" + # # استخدام النص المترجم
        messages["profile_id"].format(user_id=user_id) + "\n" + # # استخدام النص المترجم
        messages["profile_registration_date"].format(date=first_use_date) + "\n" + # # استخدام النص المترجم
        messages["profile_current_balance"].format(balance=balance, currency=messages["price_currency"]) + "\n" + # # استخدام النص المترجم
        messages["profile_total_orders"].format(total_orders=total_orders) + "\n" + # # استخدام النص المترجم
        messages["profile_total_spent"].format(total_spent=total_spent, currency=messages["price_currency"]) + "\n" + # # استخدام النص المترجم
        "━━━━━━━━━━━━━━━"
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["my_purchases_button"], callback_data="my_purchases")], # # استخدام النص المترجم
        [InlineKeyboardButton(messages["withdraw_balance_button_profile"], callback_data="withdraw_request")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم وتمرير lang_code
    ])

    await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"تم عرض الملف الشخصي للمستخدم {user_id}.")


async def handle_my_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض سجل مشتريات المستخدم.
    يعرض آخر 5 مشتريات للمستخدم.
    """
    user_id = str(update.effective_user.id)
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_orders = load_json_file(PURCHASES_FILE, {}) # # هذه الدالة ستتغير لاحقاً
    purchases = all_orders.get(user_id, [])

    if not purchases:
        await query.message.edit_text(messages["no_purchases_found"]) # # استخدام النص المترجم
        logger.info(f"المستخدم {user_id} حاول عرض المشتريات ولكن لا توجد مشتريات محفوظة لديه.")
        return

    message = messages["purchase_history_title"] + "\n━━━━━━━━━━━━━━━\n" # # استخدام النص المترجم
    for order in purchases[-5:]: # عرض آخر 5 فقط
        date = order.get("date", messages["unknown_value_char"]) # # استخدام النص المترجم
        platform = order.get("platform", messages["unknown_value_char"]) # # استخدام النص المترجم
        country_code = order.get("country", messages["unknown_value_char"]) # # تغيير country إلى country_code
        price = order.get("price", 0)

        # # جلب اسم الدولة المترجم
        country_name_key = f"country_name_{country_code}"
        country_name = messages.get(country_name_key, country_code.upper()) # # إذا لم يتم العثور على ترجمة، استخدم الكود

        message += messages["purchase_item_format"].format(
            platform=platform,
            country_name=country_name,
            price=price,
            currency=messages["price_currency"],
            date=date
        ) + "\n\n"

    keyboard = create_reply_markup([
        back_button(callback_data="profile", text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم وتمرير lang_code
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"تم عرض سجل مشتريات المستخدم {user_id}.")


async def show_balance_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض الرصيد الحالي للمستخدم فقط.
    """
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["recharge_balance_button"], callback_data="recharge")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم وتمرير lang_code
    ])

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=messages["current_balance_prompt"].format(balance=balance, currency=messages["price_currency"]), # # استخدام النص المترجم
        reply_markup=buttons,
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} طلب عرض الرصيد فقط: {balance} ر.س.")


async def handle_withdraw_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض صفحة سحب الرصيد.
    يوجه المستخدم لإرسال بيانات السحب ويتيح التواصل مع الإدارة.
    """
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    message = (
        messages["withdraw_request_title"] + "\n\n" + # # استخدام النص المترجم
        messages["withdraw_instructions"] + "\n\n" + # # استخدام النص المترجم
        messages["withdraw_full_name_field"] + "\n" + # # استخدام النص المترجم
        messages["withdraw_account_number_field"] + "\n" + # # استخدام النص المترجم
        messages["withdraw_type_field"] + "\n" + # # استخدام النص المترجم
        messages["withdraw_amount_field"] + "\n\n" + # # استخدام النص المترجم
        messages["withdraw_review_notice"] + "\n\n" + # # استخدام النص المترجم
        messages["withdraw_contact_admin_prompt"] # # استخدام النص المترجم
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["contact_admin_button_withdraw"], url="https://t.me/DrRamzi0")], # # استخدام النص المترجم
        back_button(text=messages["back_button_text"], lang_code=lang_code) # # استخدام النص المترجم وتمرير lang_code
    ])

    await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"المستخدم {user_id} فتح صفحة طلب سحب الرصيد.")