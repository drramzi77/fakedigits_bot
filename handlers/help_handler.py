from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards.utils_kb import back_button, create_reply_markup # ✅ تم إضافة هذا السطر

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    message = "🌹 مرحباً Dr\\Ramzi 😊\n⌁─━─━ (FakeDigits) ─━─━⌁"
    keyboard = create_reply_markup([
        [InlineKeyboardButton("📩 - التواصل مع الدعم", callback_data="contact_support")],
        [InlineKeyboardButton("📄 - شرح الاستخدام", callback_data="usage_guide")],
        [InlineKeyboardButton("❓ - الأسئلة الشائعة", callback_data="faq")],
        back_button(text="🔙 عودة")
    ])

    await query.message.edit_text(message, reply_markup=keyboard)


async def handle_usage_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    message = (
        "📘 <b>شرح استخدام البوت</b>\n\n"
        "1️⃣ اضغط على زر 💎 شراء رقم في القائمة الرئيسية.\n"
        "2️⃣ اختر المنصة التي ترغب بتفعيل الرقم فيها (واتساب، تليجرام...)\n"
        "3️⃣ اختر الدولة ثم السيرفر المناسب حسب السعر والجودة.\n"
        "4️⃣ سيتم خصم الرصيد تلقائيًا وعرض الرقم لك.\n"
        "5️⃣ تابع الكود الذي يصلك مباشرة داخل البوت.\n\n"
        "📌 ملاحظات:\n"
        "- تأكد من شحن رصيدك قبل الشراء.\n"
        "- الأسعار تختلف حسب السيرفر والدولة.\n"
        "- بعض الأرقام صالحة لفترة محدودة.\n\n"
        "⚠️ في حال واجهتك مشكلة تواصل مع الدعم.\n"
        "🔙 يمكنك العودة من الزر التالي."
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text="🔙 العودة")
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")

# ✅ التواصل مع الدعم
async def handle_contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    message = (
        "📞 <b>التواصل مع الدعم</b>\n\n"
        "لأي استفسار أو مشكلة:\n"
        "🔗 <a href='https://t.me/DrRamzi0'>@DrRamzi0</a>\n\n"
        "🕐 متاح من الساعة 10 صباحًا حتى 12 منتصف الليل.\n"
        "📌 أرسل استفسارك مع صورة/شرح إن وُجد."
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text="🔙 العودة")
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")

# ✅ الأسئلة الشائعة (FAQ)
async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    message = (
        "❓ <b>الأسئلة الشائعة</b>\n\n"
        "🟢 <b>هل الرقم يُستخدم مرة واحدة؟</b>\n"
        "نعم، كل رقم يُستخدم لتفعيل حساب واحد فقط.\n\n"
        "🟢 <b>ماذا لو لم يصلني الكود؟</b>\n"
        "حاول مرة أخرى أو استخدم سيرفر مختلف.\n\n"
        "🟢 <b>هل يمكن استرجاع الرصيد؟</b>\n"
        "فقط في حال فشل العملية ولم يُستخدم الرقم.\n\n"
        "📩 لمزيد من الأسئلة تواصل مع الدعم."
    )

    keyboard = create_reply_markup([
        back_button(callback_data="help", text="🔙 العودة")
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode="HTML")