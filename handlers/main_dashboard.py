# handlers/main_dashboard.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.dashboard_kb import dashboard_keyboard
from utils.check_balance import get_user_balance
from keyboards.utils_kb import back_button, create_reply_markup

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض لوحة التحكم الرئيسية للبوت للمستخدم.
    يتضمن معلومات الرصيد ومعرف المستخدم.
    """
    user = update.effective_user
    user_id = user.id
    balance = get_user_balance(user_id)

    # الاسم الظاهر (username أو الاسم الكامل)
    display_name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"

    message = (
        f"👋 أهلاً بك يا <b>{display_name}</b> في لوحة تحكمك الرئيسية! 😊\n\n"
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

def recharge_options_keyboard():
    """
    ينشئ لوحة مفاتيح الأزرار لخيارات شحن الرصيد.
    """
    return create_reply_markup([
        [
            InlineKeyboardButton("🧑‍💼 شحن من الإدارة", callback_data="recharge_admin")
        ],
        back_button()
    ])


async def handle_recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن رصيدي".
    يعرض للمستخدم طرق الدفع المتاحة وكيفية شحن الرصيد.
    """
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

async def handle_recharge_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "شحن من الإدارة".
    يوجه المستخدم للتواصل مباشرة مع المطور لشحن الرصيد يدوياً.
    """
    query = update.callback_query
    await query.answer()

    await query.message.edit_text(
        "👨‍💼 <b>شحن من الإدارة</b>\n\n"
        "يرجى التواصل مباشرة مع المطور عبر الرابط التالي:\n"
        "🔗 <a href='https://t.me/DrRamzi0'>@DrRamzi0</a>\n\n"
        "📤 أرسل له إثبات الدفع + معرفك في البوت، وسيتم شحن الرصيد يدويًا خلال دقائق.\n\n"
        "🔙 يمكنك العودة باستخدام الزر أدناه.",
        reply_markup=create_reply_markup([
            back_button(callback_data="recharge", text="🔙 العودة")
        ]),
        parse_mode="HTML"
    )