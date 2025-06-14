# handlers/profile_handler.py

import logging
# import os # لم نعد بحاجة لـ os.path.join لملفات البيانات
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.balance import get_user_balance # هذه الدالة تم تحديثها لاستخدام DB
# import datetime # لم نعد بحاجة لها هنا لكونها مستخدمة في models.py و database.py
# import json # لم نعد بحاجة لها
# from utils.data_manager import load_json_file # لم نعد بحاجة لها
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from telegram.error import BadRequest
# # استيراد الخدمات الجديدة ودالة get_db
from services import user_service, purchase_service
from database.database import get_db

logger = logging.getLogger(__name__)

# # لم نعد بحاجة لـ PURCHASES_FILE و USERS_FILE لأننا سنتعامل مع DB مباشرة
# PURCHASES_FILE = os.path.join("data", "purchases.json")
# USERS_FILE = os.path.join("data", "users.json")

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض الملف الشخصي للمستخدم.
    يعرض معلومات الحساب مثل الاسم، المعرف، الرصيد، وتاريخ التسجيل، وإحصائيات الطلبات.
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id # # معرف المستخدم كـ int
    username = f"@{user.username}" if user.username else "لا يوجد"
    fullname = user.full_name
    balance = get_user_balance(user.id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    first_use_date = messages["not_available"]
    total_orders = 0
    total_spent = 0

    for db in get_db(): # # استخدام get_db
        user_db_obj = user_service.get_user(db, user_id) # # جلب كائن المستخدم من DB
        if user_db_obj:
            first_use_date = user_db_obj.created_at.strftime("%Y-%m-%d %H:%M:%S") # # الوصول إلى .created_at مباشرة
        
        # # جلب إحصائيات المشتريات من خدمة المشتريات
        total_orders = purchase_service.get_total_orders_by_user(db, user_id)
        total_spent = purchase_service.get_total_spent_by_user(db, user_id)


    message = (
        messages["profile_welcome"].format(fullname=fullname) + "\n" +
        messages["profile_archive_intro"] + "\n" +
        "━━━━━━━━━━━━━━━\n" +
        messages["profile_name"].format(fullname=fullname) + "\n" +
        messages["profile_username"].format(username=username) + "\n" +
        messages["profile_id"].format(user_id=user_id) + "\n" +
        messages["profile_registration_date"].format(date=first_use_date) + "\n" +
        messages["profile_current_balance"].format(balance=balance, currency=messages["price_currency"]) + "\n" +
        messages["profile_total_orders"].format(total_orders=total_orders) + "\n" +
        messages["profile_total_spent"].format(total_spent=total_spent, currency=messages["price_currency"]) + "\n" +
        "━━━━━━━━━━━━━━━"
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["my_purchases_button"], callback_data="my_purchases")],
        [InlineKeyboardButton(messages["withdraw_balance_button_profile"], callback_data="withdraw_request")],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

    try:
        await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    except BadRequest as e:
        if "Message is not modified" in str(e):
            logger.info(f"المستخدم {user_id}: تم محاولة تعديل رسالة الملف الشخصي بمحتوى مطابق. تم تجاهل الخطأ.")
        else:
            logger.error(f"خطأ غير متوقع عند تعديل رسالة الملف الشخصي للمستخدم {user_id}: {e}", exc_info=True)
    logger.info(f"تم عرض الملف الشخصي للمستخدم {user_id}.")


async def handle_my_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض سجل مشتريات المستخدم.
    يعرض آخر 5 مشتريات للمستخدم.
    """
    user = update.effective_user
    user_id = user.id # # معرف المستخدم كـ int
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    purchases_list = []
    for db in get_db(): # # استخدام get_db
        purchases_list = purchase_service.get_user_purchases(db, user_id) # # جلب مشتريات المستخدم من DB

    if not purchases_list:
        try:
            await query.message.edit_text(messages["no_purchases_found"],
                                          reply_markup=create_reply_markup([
                                              back_button(callback_data="profile", text=messages["back_button_text"], lang_code=lang_code)
                                          ]))
        except BadRequest as e:
            if "Message is not modified" in str(e):
                logger.info(f"المستخدم {user_id}: تم محاولة تعديل رسالة المشتريات بمحتوى مطابق. تم تجاهل الخطأ.")
            else:
                logger.error(f"خطأ غير متوقع عند تعديل رسالة المشتريات للمستخدم {user_id}: {e}", exc_info=True)
        logger.info(f"المستخدم {user_id} حاول عرض المشتريات ولكن لا توجد مشتريات محفوظة لديه.")
        return

    message = messages["purchase_history_title"] + "\n━━━━━━━━━━━━━━━\n"
    # # عرض آخر 5 مشتريات
    for order_obj in purchases_list[-5:]:
        # # الوصول إلى الخصائص مباشرة من كائن Purchase
        date_str = order_obj.date.strftime("%Y-%m-%d %H:%M:%S") if order_obj.date else messages["unknown_value_char"]
        platform = order_obj.platform
        country_code = order_obj.country
        price = order_obj.price

        country_name_key = f"country_name_{country_code}"
        country_name = messages.get(country_name_key, country_code.upper())

        message += messages["purchase_item_format"].format(
            platform=platform,
            country_name=country_name,
            price=price,
            currency=messages["price_currency"],
            date=date_str
        ) + "\n\n"

    keyboard = create_reply_markup([
        back_button(callback_data="profile", text=messages["back_button_text"], lang_code=lang_code)
    ])

    try:
        await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")
    except BadRequest as e:
        if "Message is not modified" in str(e):
            logger.info(f"المستخدم {user_id}: تم محاولة تعديل رسالة المشتريات بمحتوى مطابق (بعد العرض). تم تجاهل الخطأ.")
        else:
            logger.error(f"خطأ غير متوقع عند تعديل رسالة المشتريات للمستخدم {user_id}: {e}", exc_info=True)
    logger.info(f"تم عرض سجل مشتريات المستخدم {user_id}.")


async def show_balance_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض الرصيد الحالي للمستخدم فقط.
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    balance = get_user_balance(user_id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["recharge_balance_button"], callback_data="recharge")],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

    try:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=messages["current_balance_prompt"].format(balance=balance, currency=messages["price_currency"]),
            reply_markup=buttons,
            parse_mode="HTML"
        )
    except BadRequest as e:
        logger.error(f"خطأ BadRequest عند إرسال رسالة الرصيد للمستخدم {user_id}: {e}", exc_info=True)
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
        messages["withdraw_request_title"] + "\n\n" +
        messages["withdraw_instructions"] + "\n\n" +
        messages["withdraw_full_name_field"] + "\n" +
        messages["withdraw_account_number_field"] + "\n" +
        messages["withdraw_type_field"] + "\n" +
        messages["withdraw_amount_field"] + "\n\n" +
        messages["withdraw_review_notice"] + "\n\n" +
        messages["withdraw_contact_admin_prompt"]
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["contact_admin_button_withdraw"], url="https://t.me/DrRamzi0")],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

    try:
        await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    except BadRequest as e:
        if "Message is not modified" in str(e):
            logger.info(f"المستخدم {user_id}: تم محاولة تعديل رسالة السحب بمحتوى مطابق. تم تجاهل الخطأ.")
        else:
            logger.error(f"خطأ غير متوقع عند تعديل رسالة السحب للمستخدم {user_id}: {e}", exc_info=True)
    logger.info(f"المستخدم {user_id} فتح صفحة طلب سحب الرصيد.")