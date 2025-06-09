# handlers/earn_credit_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def show_earn_credit_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض صفحة "اربح رصيد مجانًا" للمستخدم، مع كود الإحالة الخاص به ومعلومات المكافأة.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    referral_code = f"ref_{user_id}"  # كود الإحالة المميز لهذا المستخدم

    message = (
        "🎁 <b>اربح رصيد مجانًا!</b>\n\n"
        "قم بدعوة أصدقائك باستخدام كود الإحالة الخاص بك، وكل من يسجّل عبر كودك ستحصل على رصيد تلقائيًا 💸\n\n"
        f"🔗 <b>كودك:</b> <code>{referral_code}</code>\n"
        f"💰 <b>مكافأتك:</b> 2 ر.س عن كل صديق يستخدم كودك للتسجيل\n\n"
        "👥 كلما زاد عدد المدعوين، زاد رصيدك! شارك كودك في المجموعات والمنصات 👇"
    )

    buttons = [
        [InlineKeyboardButton("📤 نسخ كود الإحالة", switch_inline_query=referral_code)],
        [InlineKeyboardButton("📊 عرض المدعوين", callback_data="view_referrals")],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
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

    # ⛔️ لاحقاً اربطها بقاعدة بيانات فعلية
    fake_referrals = [
        {"name": "User1", "joined": "2025-06-01"},
        {"name": "User2", "joined": "2025-06-04"},
    ]

    if not fake_referrals:
        await query.message.edit_text("🚫 لا يوجد مدعوون حتى الآن.")
        return

    lines = ["📊 <b>المدعوون عبر كودك:</b>\n"]
    for ref in fake_referrals:
        lines.append(f"👤 {ref['name']} — 🗓️ {ref['joined']}")

    lines.append("\n🔙 العودة")
    buttons = [[InlineKeyboardButton("🔙 العودة", callback_data="earn_credit")]]
    await query.message.edit_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")