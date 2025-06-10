# handlers/category_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.server_kb import load_servers, server_keyboard, load_all_servers_data, save_servers_data # # load_servers/save_servers_data ستتغير مع DB
from utils.balance import get_user_balance, update_balance # # هذه الدوال ستتغير مع DB
import json
import os
import random
import logging
from datetime import datetime
from keyboards.category_kb import category_inline_keyboard
from keyboards.utils_kb import back_button, create_reply_markup
from utils.data_manager import load_json_file, save_json_file # # load_json_file/save_json_file ستتغير مع DB
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from utils.helpers import get_flag # # تم تعديل هذا السطر لاستيراد get_flag من utils.helpers

logger = logging.getLogger(__name__)

PURCHASES_FILE = os.path.join("data", "purchases.json") # # هذا المسار سيتغير لاحقاً مع DB
SERVERS_FILE = os.path.join("data", "servers.json") # # هذا المسار سيتغير لاحقاً مع DB

PLATFORMS = ["WhatsApp", "Telegram", "Snapchat", "Instagram", "Facebook", "TikTok"]

async def handle_platform_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على أزرار اختيار المنصة (مثل WhatsApp, Telegram).
    يوجه المستخدم لاختيار نوع الرقم (عربي، عشوائي، إلخ).
    """
    query = update.callback_query
    await query.answer()
    data = query.data
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if data.startswith("select_app_"):
        platform = data.replace("select_app_", "")
        context.user_data["selected_platform"] = platform
        await query.message.edit_text(
            messages["platform_selection_message"].format(platform=platform),
            reply_markup=category_inline_keyboard(platform, lang_code)
        )

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار المنطقة (مثل العرب، آسيا، أفريقيا) لشراء الأرقام.
    يعرض قائمة الدول المتاحة في تلك المنطقة.
    """
    # # تم تعديل هذا الاستيراد ليشير إلى الدالة الموحدة
    from keyboards.countries_kb import countries_keyboard
    query = update.callback_query
    await query.answer()
    data = query.data
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if data.startswith("region_"):
        _, region, platform = data.split("_")
        context.user_data["selected_platform"] = platform
        keyboard = countries_keyboard(region, platform, lang_code)
        await query.message.edit_text(
            messages["country_selection_message"].format(platform=platform),
            reply_markup=keyboard
        )

async def handle_country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار الدولة لشراء الأرقام.
    يعرض السيرفرات المتاحة لهذه الدولة مع أسعارها وكمياتها.
    """
    query = update.callback_query
    await query.answer()
    _, country_code, platform = query.data.split("_")
    user_id = update.effective_user.id
    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)
    
    all_servers_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً
    country_entry = next((entry for entry in all_servers_data if entry["platform"] == platform and entry["country"] == country_code), None)

    available_servers_for_display = []
    if country_entry:
        for s in country_entry.get("servers", []):
            if s.get("quantity", 0) > 0:
                available_servers_for_display.append(s)

    if not available_servers_for_display:
        await query.message.edit_text(messages["no_servers_available"])
        logger.info(f"المستخدم {user_id} حاول اختيار دولة {country_code} لمنصة {platform} ولا توجد سيرفرات متاحة.")
        return

    # # يمكن تحسين هذا الجزء باستخدام المفاتيح المناسبة من `messages`
    if balance < min(s['price'] for s in available_servers_for_display):
        await query.message.edit_text(
            messages["insufficient_balance_for_country"].format(balance=balance, currency=messages["price_currency"]),
            parse_mode="HTML"
        )
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({balance}) لشراء من {country_code} لـ {platform}.")
        return

    buttons = []
    for s in available_servers_for_display:
        # # استخدام النص المترجم لـ "server_button_label" كما في server_kb
        label = messages["server_button_label"].format(
            emoji="✨", # # يمكن اختيار ايموجي مختلف أو جعله ديناميكي
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

    buttons.append([InlineKeyboardButton(messages["add_to_favorites_button"], callback_data=f"fav_{platform}_{country_code}")])
    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}", lang_code=lang_code))

    await query.message.edit_text(
        messages["balance_and_server_count"].format(
            balance=balance,
            currency=messages["price_currency"],
            server_count=len(available_servers_for_display)
        ) + "\n\n" + messages["choose_server_prompt"],
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} يعرض سيرفرات {country_code} لـ {platform}. رصيده: {balance}.")

async def handle_fake_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج عملية الشراء الوهمية للرقم.
    يخصم الرصيد، يقلل الكمية، ويُنشئ سجل شراء مؤقت.
    """
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    try:
        _, platform, country_code, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك للشراء الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text(messages["error_processing_request"])
        return

    all_servers_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً
    selected_server_entry = None
    for entry in all_servers_data:
        if entry["platform"] == platform and entry["country"] == country_code:
            selected_server_entry = entry
            break

    selected = None
    if selected_server_entry:
        selected = next((s for s in selected_server_entry.get("servers", []) if s["id"] == server_id), None)

    if not selected:
        await query.message.edit_text(messages["server_not_found_message"])
        logger.warning(f"المستخدم {user_id} حاول شراء سيرفر غير موجود: {platform}-{country_code}-{server_id}.")
        return

    current_quantity = selected.get("quantity", 0)
    price = selected.get("price", 0)
    user_balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    if current_quantity <= 0:
        await query.message.edit_text(
            messages["no_numbers_available_server"].format(
                server_name=selected['name'],
                platform=platform,
                country_code=country_code.upper(), # # يمكن جلب اسم الدولة المترجم هنا
                balance=user_balance,
                currency=messages["price_currency"]
            ),
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button(text=messages["back_to_country_server_selection_button"], callback_data=f"country_{country_code}_{platform}", lang_code=lang_code)
            ])
        )
        logger.info(f"المستخدم {user_id} حاول شراء سيرفر بكمية 0: {platform}-{country_code}-{server_id}.")
        return

    if user_balance < price:
        await query.message.edit_text(
            messages["insufficient_balance_recharge_prompt"].format(
                current_balance=user_balance,
                price=price,
                currency=messages["price_currency"]
            ),
            reply_markup=create_reply_markup([
                [InlineKeyboardButton(messages["recharge_balance_button"], callback_data="recharge")],
                back_button(text=messages["back_button_text"], callback_data=f"country_{country_code}_{platform}", lang_code=lang_code)
            ]),
            parse_mode="HTML"
        )
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({user_balance}) لشراء سيرفر {platform}-{country_code}-{server_id} بسعر {price}.")
        return

    selected["quantity"] -= 1
    save_servers_data(all_servers_data) # # هذه الدالة ستتغير لاحقاً

    update_balance(user_id, -price) # # هذه الدالة ستتغير لاحقاً

    purchases = load_json_file(PURCHASES_FILE, {}) # # هذه الدالة ستتغير لاحقاً

    user_purchases = purchases.get(str(user_id), [])
    fake_number = f"9665{random.randint(10000000, 99999999)}"

    purchase_record = {
        "platform": platform,
        "country": country_code,
        "server_name": selected["name"],
        "server_id": server_id,
        "price": price,
        "fake_number": fake_number,
        "status": "awaiting_code",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    user_purchases.append(purchase_record)
    purchases[str(user_id)] = user_purchases

    save_json_file(PURCHASES_FILE, purchases) # # هذه الدالة ستتغير لاحقاً

    buttons = create_reply_markup([
        [InlineKeyboardButton(messages["request_code_button"], callback_data=f"get_code_{fake_number}_{server_id}")],
        [InlineKeyboardButton(messages["cancel_number_button"], callback_data=f"cancel_number_{fake_number}_{server_id}")],
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])

    await query.message.edit_text(
        messages["purchase_success_message"].format(
            platform=platform,
            country=country_code.upper(), # # يمكن جلب اسم الدولة المترجم هنا
            server_name=selected['name'],
            price=price,
            currency=messages["price_currency"],
            fake_number=fake_number
        ) + "\n\n" + messages["waiting_for_code_message"] + "\n" +
        messages["current_balance_info"].format(balance=get_user_balance(user_id), currency=messages["price_currency"]),
        parse_mode="HTML",
        reply_markup=buttons
    )
    logger.info(f"المستخدم {user_id} اشترى رقماً وهمياً: {fake_number} من سيرفر {selected['name']} بسعر {price}. الكمية المتبقية: {selected['quantity']}.")

async def handle_random_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار دولة عشوائية لشراء الأرقام.
    يعرض السيرفرات المتاحة في الدولة المختارة عشوائياً.
    """
    query = update.callback_query
    await query.answer()
    platform = query.data.replace("random_", "")
    user_id = query.from_user.id
    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً
    candidates = [
        s for s in all_data
        if s["platform"] == platform and
            any(server.get("quantity", 0) > 0 for server in s.get("servers", []))
    ]
    if not candidates:
        await query.message.edit_text(messages["no_numbers_available_platform"])
        logger.info(f"المستخدم {user_id} حاول اختيار دولة عشوائية لـ {platform} ولا توجد أرقام متوفرة.")
        return

    selected_country_entry = random.choice(candidates)
    country_code = selected_country_entry["country"]
    country_name_key = f"country_name_{country_code}"
    country_name = messages.get(country_name_key, country_code.upper())

    available_servers_in_country = [s for s in selected_country_entry["servers"] if s.get("quantity", 0) > 0]

    if not available_servers_in_country:
        await query.message.edit_text(messages["no_numbers_available_random_country"])
        logger.warning(f"المستخدم {user_id} اختار دولة عشوائية {country_code} لـ {platform} ولكن لا يوجد سيرفرات متاحة فيها.")
        return

    if balance < min(s['price'] for s in available_servers_in_country):
        await query.message.edit_text(messages["insufficient_balance_for_country"].format(balance=balance, currency=messages["price_currency"]))
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({balance}) لشراء من الدولة العشوائية {country_code} لـ {platform}.")
        return

    buttons = []
    for s in available_servers_in_country:
        # # استخدام النص المترجم لـ "server_button_label"
        label = messages["server_button_label"].format(
            emoji="✨", # # يمكن اختيار ايموجي مختلف أو جعله ديناميكي
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
    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}", lang_code=lang_code))

    await query.message.edit_text(
        messages["random_country_selected"].format(country_name=country_name) + "\n" +
        messages["balance_and_server_count"].format(balance=balance, currency=messages["price_currency"], server_count=len(available_servers_in_country)) + "\n\n" +
        messages["choose_server_prompt"],
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {user_id} يعرض سيرفرات الدولة العشوائية {country_code} لـ {platform}.")

async def handle_most_available_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج عرض الدول التي تحتوي على أكثر عدد من الأرقام المتاحة لمنصة معينة.
    """
    query = update.callback_query
    await query.answer()
    platform = query.data.replace("most_", "")

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً

    countries_with_availability = set()
    for entry in all_data:
        if entry["platform"] == platform:
            if any(s.get("quantity", 0) > 0 for s in entry.get("servers", [])):
                countries_with_availability.add(entry["country"])

    if not countries_with_availability:
        await query.message.edit_text(messages["no_numbers_available_platform"])
        logger.info(f"لا توجد أرقام متوفرة لـ {platform} عند طلب الأكثر توفراً.")
        return

    buttons = []
    for code in sorted(list(countries_with_availability)):
        country_name_key = f"country_name_{code}"
        country_name = messages.get(country_name_key, code.upper())
        buttons.append([InlineKeyboardButton(f"{get_flag(code)} {country_name}", callback_data=f"country_{code}_{platform}")])

    buttons.append(back_button(text=messages["back_button_text"], callback_data=f"select_app_{platform}", lang_code=lang_code))

    await query.message.edit_text(
        messages["most_available_countries_message"].format(platform=platform),
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info(f"تم عرض الدول الأكثر توفراً لـ {platform}.")

async def handle_platform_selection_by_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار المنصة يدوياً عن طريق إرسال اسمها كنص (بدلاً من زر).
    """
    text = update.message.text.strip().lower()
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    mapping = {
        "whatsapp": "WhatsApp",
        "telegram": "Telegram",
        "snapchat": "Snapchat",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "tiktok": "TikTok",
        # # إضافة ترجمات للأسماء العربية أو الإنجليزية إذا كان المستخدم سيكتبها
        messages.get("platform_whatsapp_text_input_key", "واتساب").lower(): "WhatsApp",
        messages.get("platform_telegram_text_input_key", "تليجرام").lower(): "Telegram",
        # ... وهكذا لبقية المنصات ...
    }
    platform = mapping.get(text)
    if not platform:
        await update.message.reply_text(messages["unrecognized_platform"])
        logger.warning(f"المستخدم {update.effective_user.id} أدخل منصة غير معروفة: '{text}'.")
        return

    await update.message.reply_text(
        messages["platform_selection_message"].format(platform=platform),
        reply_markup=category_inline_keyboard(platform, lang_code)
    )

# # تم حذف هذه الدالة لأن get_flag أصبحت في utils.helpers
# def get_flag(country_code):
#     """
#     يحول رمز كود الدولة (مثل 'sa') إلى علم الدولة (مثل '🇸🇦').
#     """
#     try:
#         return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
#     except:
#         return "🏳️"

async def show_available_platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة بالمنصات المتاحة حالياً مع عدد الدول المتوفرة لكل منها.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً

    platforms_with_availability = {}
    for entry in all_data:
        platform = entry["platform"]
        country = entry["country"]
        if any(s.get("quantity", 0) > 0 for s in entry.get("servers", [])):
            if platform not in platforms_with_availability:
                platforms_with_availability[platform] = set()
            platforms_with_availability[platform].add(country)

    if not platforms_with_availability:
        await query.message.edit_text(messages["no_platforms_available"])
        logger.info("لا توجد منصات متاحة بأي أرقام متوفرة عند طلب show_available_platforms.")
        return

    buttons = []
    # # تم تعديل هذا الاستيراد ليشير إلى الدالة الموحدة
    # # from keyboards.countries_kb import get_flag as get_country_flag
    for platform_name, countries in platforms_with_availability.items():
        flag_line = " ".join(get_flag(code) for code in sorted(countries)) # # استخدام get_flag الموحدة
        buttons.append([
            InlineKeyboardButton(messages["platform_country_count"].format(platform=platform_name, count=len(countries)), callback_data=f"select_app_{platform_name}")
        ])
        buttons.append([
            InlineKeyboardButton(flag_line, callback_data=f"select_app_{platform_name}")
        ])

    buttons.append(back_button(text=messages["back_button_text"], lang_code=lang_code))

    await query.message.edit_text(
        messages["available_platforms_title"] + "\n" + messages["choose_platform_prompt"],
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info("تم عرض المنصات المتاحة حاليا.")

async def show_ready_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة بالأرقام الفورية الجاهزة للشراء عبر مختلف المنصات والدول.
    """
    # # تم تعديل هذا الاستيراد ليشير إلى الدالة الموحدة
    # # from keyboards.countries_kb import get_flag
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    balance = get_user_balance(user_id) # # هذه الدالة ستتغير لاحقاً

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    all_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً

    ready_numbers = []
    for item in all_data:
        platform = item["platform"]
        country_code = item["country"]
        servers = item["servers"]
        available_servers = [s for s in servers if s.get("quantity", 0) > 0]
        if available_servers:
            cheapest = min(available_servers, key=lambda s: s["price"])
            country_name_key = f"country_name_{country_code}"
            country_name = messages.get(country_name_key, country_code.upper())

            ready_numbers.append({
                "platform": platform,
                "country": country_code,
                "country_name": country_name,
                "flag": get_flag(country_code), # # استخدام get_flag الموحدة
                "server": cheapest
            })

    ready_numbers.sort(key=lambda x: x["server"]["price"])

    buttons = []
    if not ready_numbers:
        await query.message.edit_text(messages["no_ready_numbers_available"])
        logger.info("لا توجد أرقام فورية جاهزة لعرضها.")
        return

    for item in ready_numbers[:10]: # # عرض أول 10 فقط
        btn_text = messages["ready_number_button_label"].format(
            flag=item['flag'],
            country_name=item['country_name'],
            platform=item['platform'],
            price=item['server']['price'],
            currency=messages["price_currency"],
            quantity=item['server'].get('quantity', 0),
            available_text=messages["available_quantity"]
        )
        callback = f"buy_{item['platform']}_{item['country']}_{item['server']['id']}"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=callback)])

    buttons.append(back_button(text=messages["back_button_text"], lang_code=lang_code))

    await query.message.edit_text(
        messages["ready_numbers_title"] + "\n" + messages["choose_number_prompt"],
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info(f"تم عرض {len(ready_numbers[:10])} أرقام فورية جاهزة للمستخدم {user_id}.")

async def get_fake_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج طلب الحصول على الكود الوهمي لرقم تم شراؤه.
    يُرسل كوداً وهمياً ويُحدث حالة الرقم إلى 'active'.
    """
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    try:
        _, _, fake_number, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك لطلب الكود الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text(messages["error_processing_request"])
        return

    purchases = load_json_file(PURCHASES_FILE, {}) # # هذه الدالة ستتغير لاحقاً

    user_purchases = purchases.get(str(user_id), [])
    target_purchase = None

    for record in user_purchases:
        if record.get("fake_number") == fake_number and record.get("server_id") == server_id:
            target_purchase = record
            break

    if not target_purchase:
        await query.message.edit_text(messages["purchase_not_found"])
        logger.warning(f"المستخدم {user_id} حاول طلب كود لرقم غير موجود في سجل مشترياته: {fake_number}.")
        return

    if target_purchase.get("status") == "active":
        await query.edit_message_text(messages["code_already_sent"].format(fake_number=fake_number, fake_code=target_purchase.get('fake_code', messages["not_available_code_text"])), parse_mode="HTML")
        logger.info(f"المستخدم {user_id} طلب كودًا لرقم {fake_number} وهو نشط بالفعل.")
        return

    if target_purchase.get("status") == "cancelled":
        await query.edit_message_text(messages["number_cancelled_cannot_request_code"].format(fake_number=fake_number))
        logger.warning(f"المستخدم {user_id} حاول طلب كود لرقم {fake_number} تم إلغاؤه.")
        return

    fake_code = str(random.randint(100000, 999999))
    target_purchase["status"] = "active"
    target_purchase["fake_code"] = fake_code

    purchases[str(user_id)] = user_purchases

    save_json_file(PURCHASES_FILE, purchases) # # هذه الدالة ستتغير لاحقاً

    await query.message.edit_text(
        messages["code_sent_success"].format(fake_number=fake_number, fake_code=fake_code) + "\n\n" +
        messages["test_code_note"],
        parse_mode="HTML",
        reply_markup=create_reply_markup([
            back_button(text=messages["back_button_text"], lang_code=lang_code)
        ])
    )
    logger.info(f"المستخدم {user_id} طلب كودًا وهميًا لرقم {fake_number}. الكود: {fake_code}.")


async def cancel_fake_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج إلغاء الرقم الوهمي واسترداد الرصيد.
    يُحدث حالة الرقم إلى 'cancelled' ويُعيد الرصيد للمستخدم.
    """
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    try:
        _, _, fake_number, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك لإلغاء الرقم الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text(messages["error_processing_request"])
        return

    purchases = load_json_file(PURCHASES_FILE, {}) # # هذه الدالة ستتغير لاحقاً

    user_purchases = purchases.get(str(user_id), [])
    target_purchase_index = -1
    target_purchase = None

    for i, record in enumerate(user_purchases):
        if record.get("fake_number") == fake_number and record.get("server_id") == server_id:
            target_purchase_index = i
            target_purchase = record
            break

    if not target_purchase:
        await query.message.edit_text(messages["purchase_not_found_to_cancel"])
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم غير موجود في سجل مشترياته: {fake_number}.")
        return

    if target_purchase.get("status") == "active":
        await query.edit_message_text(messages["cannot_cancel_after_code"])
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم {fake_number} بعد حصوله على الكود.")
        return

    if target_purchase.get("status") == "cancelled":
        await query.edit_message_text(messages["number_already_cancelled"].format(fake_number=fake_number))
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم {fake_number} تم إلغاؤه مسبقاً.")
        return

    price = target_purchase.get("price", 0)
    update_balance(user_id, price) # # هذه الدالة ستتغير لاحقاً

    user_purchases[target_purchase_index]["status"] = "cancelled"
    purchases[str(user_id)] = user_purchases

    save_json_file(PURCHASES_FILE, purchases) # # هذه الدالة ستتغير لاحقاً

    all_servers_data = load_json_file(SERVERS_FILE, []) # # هذه الدالة ستتغير لاحقاً
    for entry in all_servers_data:
        if entry["platform"] == target_purchase["platform"] and entry["country"] == target_purchase["country"]:
            for s in entry.get("servers", []):
                if s["id"] == server_id:
                    s["quantity"] = s.get("quantity", 0) + 1
                    break
            break
    save_servers_data(all_servers_data) # # هذه الدالة ستتغير لاحقاً

    await query.message.edit_text(
        messages["number_cancelled_success"].format(
            fake_number=fake_number,
            price=price,
            currency=messages["price_currency"]
        ) + "\n" +
        messages["new_balance_info"].format(balance=get_user_balance(user_id), currency=messages["price_currency"]),
        parse_mode="HTML",
        reply_markup=create_reply_markup([
            back_button(text=messages["back_button_text"], lang_code=lang_code)
        ])
    )
    logger.info(f"المستخدم {user_id} ألغى الرقم {fake_number} (سيرفر {server_id}). تم استرداد {price} {messages['price_currency']}. الكمية الجديدة للسيرفر: {s.get('quantity', 0)}.")