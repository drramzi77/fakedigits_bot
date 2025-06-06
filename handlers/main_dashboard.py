from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.dashboard_kb import dashboard_keyboard
from utils.check_balance import get_user_balance  # ✅ لاستدعاء الرصيد من JSON

# ✅ عرض القائمة الرئيسية
async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    balance = get_user_balance(user_id)

    # الاسم الظاهر (username أو الاسم الكامل)
    display_name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"

    message = (
        f"🏠 <b>القائمة الرئيسية</b>\n\n"
        f"👤 <b>المستخدم:</b> {display_name}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"💰 <b>الرصيد:</b> {balance} ر.س\n\n"
        f"📢 اشترك في @FakeDigitsPlus\n"
        f"🔽 اختر من القائمة التالية:"
    )

    if update.callback_query:
        await update.callback_query.message.edit_text(
            message, reply_markup=dashboard_keyboard(user_id), parse_mode="HTML"
        )
    elif update.message:
        await update.message.reply_text(
            message, reply_markup=dashboard_keyboard(user_id), parse_mode="HTML"
        )


# ✅ قائمة الأزرار السفلية الخاصة بالشحن
def recharge_options_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🧑‍💼 شحن من الإدارة", callback_data="recharge_admin")
        ],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ])


# ✅ الرسالة الرئيسية عند الضغط على "شحن رصيدك"
async def handle_recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    message = (
        "🟢 <b>مرحبًا بك في نظام شحن الرصيد!</b>\n"
        "يمكنك شحن حسابك في البوت باستخدام إحدى الطرق التالية:\n\n"

        "💸 <b>طرق الدفع المتاحة:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔹 كـريـم إيـداع / النجـم\n"
        "🔹 فودافون كاش / تحويل مباشر\n"
        "🔹 زين كاش / آسيا حوالة\n"
        "🔹 عملات رقمية: USDT / BTC / Payeer\n"
        "🔹 PayPal\n"
        "🔹 أي وسيلة أخرى يتم الاتفاق عليها\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        "📌 <i>يرجى إرسال إثبات الدفع إلى الإدارة مع معرفك التالي:</i>\n"
        f"<code>{user_id}</code>\n\n"
        "📞 <b>للتواصل مع الإدارة:</b> @DrRamzi0\n"
        "📍 <b>اضغط على أحد الأزرار بالأسفل لإتمام العملية 👇</b>"
    )

    await query.message.edit_text(
        message,
        reply_markup=recharge_options_keyboard(),
        parse_mode="HTML"
    )


# ✅ رسالة خاصة عند الضغط على "شحن من الإدارة"
async def handle_recharge_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.edit_text(
        "👨‍💼 <b>شحن من الإدارة</b>\n\n"
        "يرجى التواصل مباشرة مع المطور عبر الرابط التالي:\n"
        "🔗 <a href='https://t.me/DrRamzi0'>@DrRamzi0</a>\n\n"
        "📤 أرسل له إثبات الدفع + معرفك في البوت، وسيتم شحن الرصيد يدويًا خلال دقائق.\n\n"
        "🔙 يمكنك العودة باستخدام الزر أدناه.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 العودة", callback_data="recharge")]
        ]),
        parse_mode="HTML"
    )
