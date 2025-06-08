# handlers/quick_search_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.server_kb import load_servers
from utils.balance import get_user_balance
from utils.data_manager import load_json_file
from keyboards.utils_kb import back_button, create_reply_markup # ✅ تم إضافة هذا السطر


# ✅ خريطة البحث باللغتين
ALL_COUNTRIES = {
    "السعودية": "sa", "saudi arabia": "sa", "🇸🇦": "sa",
    "مصر": "eg", "egypt": "eg", "🇪🇬": "eg",
    "اليمن": "ye", "yemen": "ye", "🇾🇪": "ye",
    "الجزائر": "dz", "algeria": "dz", "🇩🇿": "dz",
    "المغرب": "ma", "morocco": "ma", "🇲🇦": "ma",
    "العراق": "iq", "iraq": "iq", "🇮🇶": "iq",
    "السودان": "sd", "sudan": "sd", "🇸🇩": "sd",
    "سوريا": "sy", "syria": "sy", "🇸🇾": "sy",
    "الهند": "in", "india": "in", "🇮🇳": "in",
    "باكستان": "pk", "pakistan": "pk", "🇵🇰": "pk",
    "اندونيسيا": "id", "indonesia": "id", "🇮🇩": "id",
    "فرنسا": "fr", "france": "fr", "🇫🇷": "fr",
    "أمريكا": "us", "usa": "us", "🇺🇸": "us",
    "البرازيل": "br", "brazil": "br", "🇧🇷": "br",
    "الأردن": "jo", "jordan": "jo", "🇯🇴": "jo",
    "قطر": "qa", "qatar": "qa", "🇶🇦": "qa",
    "الإمارات": "ae", "uae": "ae", "🇦🇪": "ae"
}

# ✅ عند الضغط على "البحث السريع"
async def start_quick_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["awaiting_country_input"] = True
    context.user_data["awaiting_input"] = "quick_search_country_general"

    await query.message.edit_text(
        "🌹 مرحباً 😊\nDr\\Ramzi\n\n— قم بإرسال اسم الدولة (بالعربية أو الإنجليزية أو بالرمز 🇸🇦) للبحث عنها:\n\n──────────────",
        reply_markup=create_reply_markup([
            back_button(callback_data="back_to_main", text="❌ إلغاء")
        ])
    )

# ✅ عندما يكتب المستخدم اسم الدولة
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    text = update.message.text.strip().lower()

    platform = context.user_data.get("selected_platform", "WhatsApp")

    country_code = ALL_COUNTRIES.get(text)
    if not country_code:
        await update.message.reply_text("❌ لم يتم العثور على هذه الدولة. تأكد من كتابة الاسم بشكل صحيح.",
                                        reply_markup=create_reply_markup([
                                            back_button()
                                        ]))
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("awaiting_country_input", None)
        return

    servers = load_servers(platform, country_code)
    if not servers:
        await update.message.reply_text("❗ لا توجد سيرفرات متاحة حاليًا لهذه الدولة.",
                                        reply_markup=create_reply_markup([
                                            back_button()
                                        ]))
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("awaiting_country_input", None)
        return

    balance = get_user_balance(user_id)

    buttons = []
    for s in servers:
        buttons.append([InlineKeyboardButton(
            f"{s['name']} - 💰 {s['price']} ر.س",
            callback_data=f"buy_{platform}_{country_code}_{s['id']}"
        )])
    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))

    await update.message.reply_text(
        f"📍 <b>الدولة:</b> {text.title()}\n"
        f"📱 <b>المنصة:</b> {platform}\n"
        f"💰 <b>رصيدك:</b> {balance} ر.س\n\n"
        f"اختر السيرفر المناسب لتجربته:",
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    context.user_data.pop("awaiting_input", None)
    context.user_data.pop("awaiting_country_input", None)