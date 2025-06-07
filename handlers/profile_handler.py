from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.check_balance import get_user_balance
import datetime
import json
import os
import logging # # إضافة هذا السطر

logger = logging.getLogger(__name__) # # تعريف logger على مستوى الوحدة

# 📌 مسار ملف المشتريات (يفترض وجوده أو إنشاؤه)
PURCHASES_FILE = "data/purchases.json"
USERS_FILE = "data/users.json" # # إضافة مسار ملف المستخدمين

# ✅ عرض صفحة الحساب الشخصي
async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "لا يوجد"
    fullname = user.full_name
    balance = get_user_balance(int(user_id))

    # احصل على تاريخ التسجيل (افتراضي)
    first_use_date = "غير متوفر"
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users_data = json.load(f)
                user_data = users_data.get(user_id, {})
                if "created_at" in user_data:
                    first_use_date = user_data["created_at"]
        else:
            logger.warning(f"ملف المستخدمين '{USERS_FILE}' غير موجود عند جلب تاريخ التسجيل.")
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للمستخدمين '{USERS_FILE}' عند جلب تاريخ التسجيل.", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند جلب تاريخ تسجيل المستخدم {user_id}: {e}", exc_info=True)


    # احصائيات الطلبات
    total_orders = 0
    total_spent = 0
    try:
        if os.path.exists(PURCHASES_FILE):
            with open(PURCHASES_FILE, encoding="utf-8") as f:
                all_orders = json.load(f)
                user_orders = all_orders.get(user_id, [])
                total_orders = len(user_orders)
                total_spent = sum([order.get("price", 0) for order in user_orders])
        else:
            logger.warning(f"ملف المشتريات '{PURCHASES_FILE}' غير موجود عند جلب احصائيات الطلبات.")
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON للمشتريات '{PURCHASES_FILE}' عند جلب احصائيات الطلبات.", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند جلب احصائيات طلبات المستخدم {user_id}: {e}", exc_info=True)


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

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧾 صندوق مشترياتي", callback_data="my_purchases")],
        [InlineKeyboardButton("🏧 سحب الرصيد", callback_data="withdraw_request")],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ])
    
    await update.callback_query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"تم عرض الملف الشخصي للمستخدم {user_id}.")


# ✅ عرض سجل المشتريات
async def handle_my_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    query = update.callback_query
    await query.answer()

    purchases = []
    try:
        if not os.path.exists(PURCHASES_FILE):
            await query.message.edit_text("🗃 لا توجد مشتريات محفوظة حالياً.")
            logger.info(f"المستخدم {user_id} حاول عرض المشتريات ولكن ملف '{PURCHASES_FILE}' غير موجود.")
            return

        with open(PURCHASES_FILE, encoding="utf-8") as f:
            all_orders = json.load(f)
        purchases = all_orders.get(user_id, [])
    except json.JSONDecodeError:
        await query.message.edit_text("❌ حدث خطأ في قراءة سجل المشتريات. يرجى التواصل مع الدعم.")
        logger.error(f"خطأ في قراءة ملف JSON للمشتريات '{PURCHASES_FILE}' للمستخدم {user_id}.", exc_info=True)
        return
    except IOError as e:
        await query.message.edit_text("❌ حدث خطأ في الوصول إلى سجل المشتريات. يرجى التواصل مع الدعم.")
        logger.error(f"خطأ في الوصول إلى ملف المشتريات '{PURCHASES_FILE}' للمستخدم {user_id}: {e}", exc_info=True)
        return
    except Exception as e:
        await query.message.edit_text("❌ حدث خطأ غير متوقع عند جلب سجل المشتريات. يرجى التواصل مع الدعم.")
        logger.error(f"خطأ غير متوقع عند جلب مشتريات المستخدم {user_id}: {e}", exc_info=True)
        return


    if not purchases:
        await query.message.edit_text("🗃 لا توجد مشتريات محفوظة لحسابك.")
        logger.info(f"المستخدم {user_id} حاول عرض المشتريات ولكن لا توجد مشتريات محفوظة لديه.")
        return

    message = "📦 <b>سجل مشترياتك</b>:\n━━━━━━━━━━━━━━━\n"
    # عرض آخر 5 فقط
    for order in purchases[-5:]:
        date = order.get("date", "❓")
        platform = order.get("platform", "❓")
        country = order.get("country", "❓")
        price = order.get("price", 0)
        message += f"• {platform} - {country.upper()} - {price} ر.س\n🕓 {date}\n\n"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 العودة", callback_data="profile")]
    ])

    await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"تم عرض سجل مشتريات المستخدم {user_id}.")


# ✅ عرض الرصيد فقط
async def show_balance_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 شحن رصيدي", callback_data="recharge")],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ])

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"💰 <b>رصيدك الحالي:</b> {balance} ر.س\n\n"
             "يمكنك شحن رصيدك بالضغط على الزر أدناه:",
        reply_markup=buttons,
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} طلب عرض الرصيد فقط: {balance} ر.س.")


# ✅ صفحة طلب سحب الرصيد
async def handle_withdraw_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📬 تواصل مع الإدارة", url="https://t.me/DrRamzi0")],
        [InlineKeyboardButton("🔙 العودة  ", callback_data="back_to_dashboard")]
    ])

    await query.message.edit_text(message, reply_markup=buttons, parse_mode="HTML")
    logger.info(f"المستخدم {user_id} فتح صفحة طلب سحب الرصيد.")