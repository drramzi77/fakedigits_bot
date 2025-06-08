from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS # ✅ تم التعديل ليصبح استيراد مباشر لـ ADMINS

# ✅ صفحة كن وكيلاً معنا
async def show_agent_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🤝 <b>فرصتك لتكون وكيلًا معتمدًا لدينا!</b>\n\n"
        "✅ <b>مميزات الوكلاء:</b>\n"
        "• تسعيرات حصرية أقل من المستخدم العادي.\n"
        "• لوحة تحكم متقدمة لمتابعة المستخدمين.\n"
        "• ربح تلقائي من عمليات عملائك.\n"
        "• دعم فني مباشر وأولوية في الرد.\n\n"
        "💼 <b>مثال على الربح:</b>\n"
        "إذا أشرف الوكيل على 10 مستخدمين، وكل واحد استخدم رصيدًا بقيمة 50 ر.س:\n"
        "🪙 <b>الربح الشهري:</b> 100 ر.س (نسبة 20%)\n\n"
        "📌 <b>الشروط:</b>\n"
        "• أن يكون لديك مستخدمين حقيقيين.\n"
        "• الالتزام بشروط الاستخدام.\n\n"
        "إذا كنت مهتمًا، اضغط على الزر أدناه وسنتواصل معك."
    )

    buttons = [
        [InlineKeyboardButton("📩 إرسال طلب الانضمام", callback_data="apply_agent")],
        [InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]
    ]

    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )

# ✅ استقبال طلب الانضمام كوكيل
async def apply_as_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    # إرسال الطلب إلى المشرفين
    msg = (
        f"📬 <b>طلب وكيل جديد</b>\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 المعرف: @{user.username if user.username else 'لا يوجد'}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
    )

    for admin_id in ADMINS: # ✅ تم التعديل من ADMIN_IDS إلى ADMINS
        await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode="HTML")

    await query.message.edit_text(
        "✅ تم إرسال طلبك إلى الإدارة بنجاح.\n"
        "📌 سنقوم بمراجعة الطلب والتواصل معك قريبًا بإذن الله.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 العودة إلى القائمة", callback_data="back_to_dashboard")]
        ])
    )