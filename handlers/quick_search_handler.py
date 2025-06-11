# handlers/quick_search_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.server_kb import load_servers
from utils.balance import get_user_balance
from utils.data_manager import load_json_file
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from keyboards.countries_kb import get_flag # # تم استيراد get_flag للحصول على الأعلام

# ✅ خريطة البحث باللغتين (ستظل كما هي في هذه المرحلة)
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

async def start_quick_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يبدأ عملية البحث السريع عن الأرقام.
    يطلب من المستخدم إرسال اسم الدولة للبحث عنها.
    """
    query = update.callback_query
    await query.answer()
    context.user_data["awaiting_country_input"] = True
    context.user_data["awaiting_input"] = "quick_search_country_general"

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    await query.message.edit_text(
        messages["quick_search_prompt"],
        reply_markup=create_reply_markup([
            back_button(callback_data="back_to_dashboard", text=messages["cancel_button"], lang_code=lang_code)
        ])
    )

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج إدخال المستخدم لاسم الدولة في وضع البحث السريع.
    يعرض السيرفرات المتاحة للدولة والمنصة المختارة.
    """
    user = update.effective_user
    user_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    text = update.message.text.strip().lower()

    platform = context.user_data.get("selected_platform", "WhatsApp") # # الافتراضي WhatsApp إذا لم يتم تحديد منصة

    country_code = ALL_COUNTRIES.get(text)
    if not country_code:
        await update.message.reply_text(
            messages["country_not_found"].format(bot_name="Dr\\Ramzi"),
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("awaiting_country_input", None)
        return

    servers = load_servers(platform, country_code)
    if not servers:
        await update.message.reply_text(
            messages["no_servers_available_country_quick_search"],
            reply_markup=create_reply_markup([
                back_button(text=messages["back_button_text"], lang_code=lang_code)
            ])
        )
        context.user_data.pop("awaiting_input", None)
        context.user_data.pop("awaiting_country_input", None)
        return

    balance = get_user_balance(user_id, user.to_dict()) # # تم التعديل: تمرير user.to_dict()

    buttons = []
    country_name_key = f"country_name_{country_code}"
    country_name = messages.get(country_name_key, text.title())

    for s in servers:
        label = messages["server_button_label"].format(
            emoji="✨",
            server_name=s['name'],
            price=s['price'],
            currency=messages["price_currency"],
            quantity=s.get('quantity', 0),
            available_text=messages["available_quantity"]
        )
        buttons.append([InlineKeyboardButton(
            label,
            callback_data=f"buy_{platform}_{country_code}_{s['id']}"
        )])
    buttons.append(back_button(callback_data=f"select_app_{platform}", text=messages["back_button_text"], lang_code=lang_code))

    await update.message.reply_text(
        messages["quick_search_results"].format(
            country_name=country_name,
            platform=platform,
            balance=balance,
            currency=messages["price_currency"]
        ) + "\n\n" + messages["choose_server_prompt"],
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    context.user_data.pop("awaiting_input", None)
    context.user_data.pop("awaiting_country_input", None)