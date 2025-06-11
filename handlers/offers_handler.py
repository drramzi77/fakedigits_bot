# handlers/offers_handler.py

import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance # # هذه الدالة ستتغير مع DB
from utils.data_manager import load_json_file # # هذه الدالة ستتغير مع DB
from keyboards.utils_kb import back_button # # تم إضافة هذا السطر لاستخدام زر العودة الموحد
from keyboards.countries_kb import get_flag # # تم إضافة هذا السطر للحصول على العلم
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

def generate_offer_buttons(platform: str, lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code
    """
    ينشئ لوحة مفاتيح الأزرار لعروض دولة معينة لمنصة محددة.
    يعرض أرخص سعر لكل دولة متوفرة.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة
    data = load_json_file("data/servers.json", []) # # هذا المسار والدالة ستتغير لاحقاً مع DB

    country_prices = {}
    for item in data:
        if item["platform"].lower() != platform.lower():
            continue
        country_code = item["country"] # # تغيير المتغير من country إلى country_code للوضوح
        for server in item.get("servers", []):
            price = server["price"]
            if country_code not in country_prices or price < country_prices[country_code]:
                country_prices[country_code] = price

    buttons = []
    row = []
    for i, (country_code, price) in enumerate(country_prices.items()):
        flag = get_flag(country_code)
        # # استخدام النص المترجم لزر العرض
        country_name_key = f"country_name_{country_code}"
        country_name = messages.get(country_name_key, country_code.upper()) # # جلب اسم الدولة المترجم

        row.append(InlineKeyboardButton(
            messages["offer_button_label"].format(
                flag=flag,
                country_name=country_name, # # استخدام اسم الدولة المترجم
                price=int(price), # # للتأكد من عرض السعر كعدد صحيح إذا كان كذلك
                currency=messages["price_currency"] # # استخدام العملة المترجمة
            ),
            callback_data=f"country_{country_code}_{platform}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code)) # # استخدام زر العودة الموحد وتمرير lang_code
    return InlineKeyboardMarkup(buttons)

async def show_platform_offers(update: Update, context: ContextTypes.DEFAULT_TYPE, platform: str):
    """
    يعرض عروض الأرقام لمنصة محددة (مثل WhatsApp أو Telegram).
    """
    user_id = update.effective_user.id
    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_data = load_json_file("data/servers.json", []) # # هذه الدالة ستتغير لاحقاً

    available_countries = {
        item["country"] for item in all_data if item["platform"].lower() == platform.lower()
    }

    # # استخدام دالة get_flag من keyboards.countries_kb بشكل موحد
    # # ملاحظة: get_flag معرفة هنا أيضا، يمكن حذفها إذا تم استيرادها
    # from keyboards.countries_kb import get_flag as get_country_flag # # لتجنب التضارب إذا كان هناك get_flag أخرى
    flags_line = " ".join([get_flag(c) for c in sorted(available_countries)])


    text = (
        messages["platform_offers_title"].format(platform=platform) + "\n\n" + # # استخدام النص المترجم
        messages["your_balance_info"].format(balance=balance, currency=messages["price_currency"]) + "\n" + # # استخدام النص المترجم
        messages["available_countries_title"] + "\n" + # # استخدام النص المترجم
        f"{flags_line}\n" + # # أعلام الدول
        "━━━━━━━━━━━━━━━"
    )

    await update.callback_query.message.edit_text(
        text, reply_markup=generate_offer_buttons(platform, lang_code), parse_mode="HTML" # # تمرير lang_code
    )

async def show_whatsapp_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض واتساب" لعرض العروض الخاصة بالمنصة.
    """
    await update.callback_query.answer()
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    await show_platform_offers(update, context, "WhatsApp")

async def show_telegram_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض تليجرام" لعرض العروض الخاصة بالمنصة.
    """
    await update.callback_query.answer()
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE) # # تحديد لغة المستخدم
    await show_platform_offers(update, context, "Telegram")

async def show_general_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض صفحة العروض العامة، ويطلب من المستخدم اختيار منصة محددة لرؤية عروضها.
    """
    query = update.callback_query
    await query.answer()
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    text = (
        messages["general_offers_title"] + "\n\n" +
        messages["general_offers_whatsapp_telegram"] + "\n" +
        messages["general_offers_best_prices"] + "\n\n" +
        messages["choose_platform_for_offers_prompt"]
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(messages["whatsapp_offers_button"], callback_data="wa_offers"),
            InlineKeyboardButton(messages["telegram_offers_button"], callback_data="tg_offers")
        ],
        *[back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code)]
    ])

    await query.message.edit_text(text, reply_markup=buttons, parse_mode="HTML")
