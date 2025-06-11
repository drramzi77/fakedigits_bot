# handlers/offers_handler.py

import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance
from utils.data_manager import load_json_file
from keyboards.utils_kb import back_button, create_reply_markup
from keyboards.countries_kb import get_flag
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

SERVERS_FILE = os.path.join("data", "servers.json")

def generate_offer_buttons(platform: str, lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح الأزرار لعروض دولة معينة لمنصة محددة.
    يعرض أرخص سعر لكل دولة متوفرة. (هذه الدالة تبدو مكررة في غرضها مع show_platform_offers)
    ملاحظة: هذه الدالة لم يتم استخدامها بشكل مباشر من show_platform_offers في الكود السابق.
    إذا كنت تستخدمها في مكان آخر، فستحتاج إلى تحديثها بنفس منطق العروض الجديدة.
    """
    messages = get_messages(lang_code)
    data = load_json_file("data/servers.json", [])

    country_prices = {}
    for item in data:
        if item["platform"].lower() == platform.lower():
            for server in item.get("servers", []):
                price = server["price"]
                country_code = item["country"]
                if country_code not in country_prices or price < country_prices[country_code]:
                    country_prices[country_code] = price

    buttons = []
    row = []
    # # سيتم استبدال هذا المنطق بمصفوفة أزرار مباشرة في show_platform_offers
    # # هذا الكود هو مجرد مثال على كيفية بناء الأزرار إذا تم استخدام generate_offer_buttons
    for i, (country_code, price) in enumerate(country_prices.items()):
        flag = get_flag(country_code)
        country_name_key = f"country_name_{country_code}"
        country_name = messages.get(country_name_key, country_code.upper())

        # بناء نص الزر بشكل مشابه لما سيتم في show_platform_offers
        label = messages["offer_button_label"].format(
            flag=flag,
            country_name=country_name,
            price=int(price),
            currency=messages["price_currency"]
        )
        # # يجب أن تتضمن الـ callback_data تفاصيل الشراء (platform, country_code, server_id)
        # # هذه الدالة تحتاج لمعرفة server_id الأرخص لكل دولة، وهو غير متوفر هنا حالياً.
        # # لذلك، الأفضل أن تعتمد show_platform_offers على نفسها في بناء الأزرار.
        # row.append(InlineKeyboardButton(label, callback_data=f"country_{country_code}_{platform}"))
        # if len(row) == 2:
        #     buttons.append(row)
        #     row = []
    
    # if row:
    #     buttons.append(row)

    buttons.append(back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code))
    return InlineKeyboardMarkup(buttons)

async def show_platform_offers(update: Update, context: ContextTypes.DEFAULT_TYPE, platform_filter: str = None):
    """
    يعرض العروض المتاحة (السيرفرات ذات الكمية والسعر المحدد) لمنصة معينة أو لجميع المنصات.
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    balance = get_user_balance(user_id, user.to_dict())

    all_servers_data = load_json_file(SERVERS_FILE, [])

    # # تجميع العروض المتاحة (التي تحتوي على كمية > 0)
    available_offers_list = []
    for entry in all_servers_data:
        platform_name_from_data = entry["platform"]
        country_code = entry["country"]
        
        if platform_filter and platform_name_from_data != platform_filter:
            continue

        for server in entry.get("servers", []):
            if server.get("quantity", 0) > 0: # # عرض فقط السيرفرات المتوفرة
                country_name_key = f"country_name_{country_code}"
                country_name = messages.get(country_name_key, country_code.upper())
                available_offers_list.append({
                    "platform": platform_name_from_data,
                    "country_name": country_name, # # تم إضافة اسم الدولة المترجم هنا
                    "country_code": country_code,
                    "server_name": server["name"],
                    "server_id": server["id"],
                    "price": server["price"],
                    "quantity": server.get("quantity", 0)
                })
    
    # # ترتيب العروض حسب السعر (من الأقل للأعلى)
    available_offers_list.sort(key=lambda x: x["price"])

    buttons = [] # # لوحة المفاتيح الجديدة ستكون كلها أزرار
    rows_added = 0
    MAX_OFFERS_DISPLAY = 10 # # عدد العروض المراد عرضها في البداية

    if not available_offers_list:
        text = messages["offers_title"] + "\n\n" + messages["no_offers_available"]
    else:
        # # عنوان الرسالة
        text = messages["offers_title"] + "\n\n"
        text += messages["your_balance_is"].format(balance=balance, currency=messages["price_currency"]) + "\n\n"
        text += messages["available_offers_list"] + "\n"

        # # إضافة أزرار لكل عرض
        for offer in available_offers_list[:MAX_OFFERS_DISPLAY]:
            # # بناء نص الزر (يجب أن يكون مختصراً وواضحاً)
            btn_text = messages["offer_button_label_new"].format( # # مفتاح جديد لرسالة الزر
                flag=get_flag(offer["country_code"]),
                country_name=offer["country_name"],
                platform=offer["platform"],
                price=offer["price"],
                currency=messages["price_currency"],
                quantity=offer["quantity"]
            )
            # # callback_data لزر الشراء المباشر
            callback_data = f"buy_{offer['platform']}_{offer['country_code']}_{offer['server_id']}"
            buttons.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])
            rows_added += 1
        
        # # إذا كان هناك المزيد من العروض بعد الحد الأقصى، أضف زر "عرض المزيد"
        if len(available_offers_list) > MAX_OFFERS_DISPLAY:
            buttons.append([InlineKeyboardButton(messages["view_more_offers_button"], callback_data=f"show_more_offers_{platform_filter}")]) # # مفتاح جديد

    # # أزرار التنقل بين أنواع العروض
    category_buttons = []
    if not platform_filter: # # إذا كانت هذه القائمة العامة (لم يتم اختيار منصة محددة بعد)
        category_buttons.append(InlineKeyboardButton(messages["whatsapp_offers_button"], callback_data="wa_offers"))
        category_buttons.append(InlineKeyboardButton(messages["telegram_offers_button"], callback_data="tg_offers"))
    
    # # أضف أزرار الفئات في صف منفصل، ثم أضف زر العودة
    if category_buttons:
        buttons.append(category_buttons) # # إضافة صف أزرار الفئات

    buttons.append(back_button(text=messages["back_button_text"], callback_data="back_to_dashboard")) # # زر العودة العام

    await query.message.edit_text(text, reply_markup=create_reply_markup(buttons), parse_mode="HTML")
    logger.info(f"المستخدم {user_id} عرض العروض المتاحة. فلتر المنصة: {platform_filter if platform_filter else 'الكل'}.")


async def show_whatsapp_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض واتساب" لعرض العروض الخاصة بالمنصة.
    """
    # # تم حذف await update.callback_query.answer() من هنا
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    await show_platform_offers(update, context, "WhatsApp")

async def show_telegram_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض تليجرام" لعرض العروض الخاصة بالمنصة.
    """
    # # تم حذف await update.callback_query.answer() من هنا
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
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