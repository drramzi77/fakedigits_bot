from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.check_balance import get_user_balance
import datetime
import json
import os
import logging
from utils.data_manager import load_json_file
from keyboards.utils_kb import back_button, create_reply_markup

logger = logging.getLogger(__name__)

# 📌 مسار ملف المشتريات (يفترض وجوده أو إنشاؤه)
PURCHASES_FILE = os.path.join("data", "purchases.json")
USERS_FILE = os.path.join("data", "users.json")

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض الملف الشخصي للمستخدم.
    يعرض معلومات الحساب مثل الاسم، المعرف، الرصيد، وتاريخ التسجيل، وإحصائيات الطلبات.
    """
    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "لا يوجد"
    fullname = user.full_name
    balance = get_user_balance(int(user_id))

    # احصل على تاريخ التسجيل (افتراضي)
    first_use_date = "غير متوفر"
    users_data = load_json_file(USERS_FILE, {})
    user_data = users_data.get(user_id, {})
    if "created_at" in user_data:
        first_use_date = user_data["created_at"]
    else:
        logger.warning(f"ملف المستخدمين '{USERS_FILE}' غير موجود أو المستخدم {user_id} لا يملك تاريخ تسجيل.")


    # احصائيات الطلبات
    total_orders = 0
    total_spent = 0
    all_orders = load_json_file(PURCHASES_FILE, {})
    user_orders = all_orders.get(user_id, [])
    total_orders = len(user_orders)
    total_spent = sum([order.get("price", 0) for order in user_orders])


    message = (
        f"👤 <b>مرحباً بك</b>\n"
        f"هذا هو الأرشيف الخاص بحسابك:\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📛 الاسم: <b>{fullname}</b>\n"
        f"📎 المعرف: <b>{username}</b>\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"📆 تاريخ التسجيل: {first_use_date}\n"
        f"💰 الرصيد الحالي: <b>{balance} ر.س</b>\n"
        f"📦 عدد الطلبات: <b>{total_orders}</b>\n"
        f"💸 الرصيد المستخدم: <b>{total_spent} ر.س</b>\n"
        f"━━━━━━━━━━━━━━━"
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton("🧾 صندوق مشترياتي", callback_data="my_purchases")],
        [InlineKeyboardButton("🏧 سحب الرصيد", callback_data="withdraw_request")],
        back_button()
    ])

    await update.callback_query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"تم عرض الملف الشخصي للمستخدم {user_id}.")


async def handle_my_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب عرض سجل مشتريات المستخدم.
    يعرض آخر 5 مشتريات للمستخدم.
    """
    user_id = str(update.effective_user.id)
    query = update.callback_query
    await query.answer()

    all_orders = load_json_file(PURCHASES_FILE, {})
    purchases = all_orders.get(user_id, [])

    if not purchases:
        await query.message.edit_text("🗃 لا توجد مشتريات محفوظة لحسابك.")
        logger.info(f"المستخدم {user_id} حاول عرض المشتريات ولكن لا توجد مشتريات محفوظة لديه.")
        return

    message = "📦 <b>سجل مشترياتك</b>:\n━━━━━━━━━━━━━━━\n"
    for order in purchases[-5:]: # عرض آخر 5 فقط
        date = order.get("date", "❓")
        platform = order.get("platform", "❓")
        country = order.get("country", "❓")
        price = order.get("price", 0)
        message += f"• {platform} - {country.upper()} - {price} ر.س\n🕓 {date}\n\n"

    keyboard = create_reply_markup([
        back_button(callback_data="profile", text="🔙 العودة")
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
    balance = get_user_balance(user_id)

    buttons = create_reply_markup([
        [InlineKeyboardButton("💳 شحن رصيدي", callback_data="recharge")],
        back_button()
    ])

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"💰 <b>رصيدك الحالي:</b> {balance} ر.س\n\n"
             "يمكنك شحن رصيدك بالضغط على الزر أدناه:",
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

    message = (
        "🏧 <b>طلب سحب الرصيد</b>\n\n"
        "لضمان سرعة معالجة الطلب، يرجى إرسال بيانات التحويل بالتنسيق التالي:\n\n"
        "🔹 <b>الاسم الثلاثي:</b>\n"
        "🔹 <b>رقم الحساب أو المحفظة:</b>\n"
        "🔹 <b>نوع التحويل</b> (STC Pay / بنكي / حوالة):\n"
        "🔹 <b>المبلغ المطلوب:</b>\n\n"
        "📌 <i>سيتم مراجعة طلبك خلال 24 ساعة عمل كحد أقصى.</i>\n\n"
        "📞 في حال وجود أي مشكلة أو استفسار عاجل، يمكنك التواصل مباشرة مع الإدارة:"
    )

    buttons = create_reply_markup([
        [InlineKeyboardButton("📬 تواصل مع الإدارة", url="https://t.me/DrRamzi0")],
        back_button(text="🔙 العودة")
    ])

    await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"المستخدم {user_id} فتح صفحة طلب سحب الرصيد.")