# handlers/category_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.server_kb import load_servers, server_keyboard, load_all_servers_data, save_servers_data
from utils.balance import get_user_balance, update_balance
import json
import os
import random
import logging
from datetime import datetime
from keyboards.category_kb import category_inline_keyboard
from utils.data_manager import load_json_file, save_json_file
from keyboards.utils_kb import back_button, create_reply_markup # ✅ تم التأكد من استيرادها

logger = logging.getLogger(__name__)
PURCHASES_FILE = os.path.join("data", "purchases.json")
SERVERS_FILE = os.path.join("data", "servers.json")

PLATFORMS = ["WhatsApp", "Telegram", "Snapchat", "Instagram", "Facebook", "TikTok"]

async def handle_platform_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على أزرار اختيار المنصة (مثل WhatsApp, Telegram).
    يوجه المستخدم لاختيار نوع الرقم (عربي، عشوائي، إلخ).
    """
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("select_app_"):
        platform = data.replace("select_app_", "")
        context.user_data["selected_platform"] = platform
        await query.message.edit_text(
            f"🧭 أنت الآن في قسم: {platform}\nاختر نوع الرقم الذي ترغب به:",
            reply_markup=category_inline_keyboard(platform)
        )

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار المنطقة (مثل العرب، آسيا، أفريقيا) لشراء الأرقام.
    يعرض قائمة الدول المتاحة في تلك المنطقة.
    """
    from keyboards.countries_kb import countries_keyboard
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("region_"):
        _, region, platform = data.split("_")
        context.user_data["selected_platform"] = platform
        keyboard = countries_keyboard(region, platform)
        await query.message.edit_text(
            f"🌍 اختر الدولة التي تريد شراء رقم {platform} منها:",
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
    balance = get_user_balance(user_id)

    all_servers_data = load_json_file(SERVERS_FILE, [])
    country_entry = next((entry for entry in all_servers_data if entry["platform"] == platform and entry["country"] == country_code), None)

    available_servers_for_display = []
    if country_entry:
        for s in country_entry.get("servers", []):
            if s.get("quantity", 0) > 0:
                available_servers_for_display.append(s)

    if not available_servers_for_display:
        await query.message.edit_text("❗ لا توجد سيرفرات متاحة حاليًا لهذه الدولة أو المنصة.")
        logger.info(f"المستخدم {user_id} حاول اختيار دولة {country_code} لمنصة {platform} ولا توجد سيرفرات متاحة.")
        return

    if balance < min(s['price'] for s in available_servers_for_display):
        await query.message.edit_text(f"❌ رصيدك غير كافٍ لشراء أي رقم من هذه السيرفرات.\nرصيدك الحالي: {balance} ر.س")
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({balance}) لشراء من {country_code} لـ {platform}.")
        return

    buttons = []
    for s in available_servers_for_display:
        buttons.append([InlineKeyboardButton(
            f"{s['name']} - 💰 {s['price']} ر.س ({s.get('quantity', 0)} متاح)",
            callback_data=f"buy_{platform}_{country_code}_{s['id']}"
        )])

    buttons.append([InlineKeyboardButton("⭐️ أضف إلى المفضلة", callback_data=f"fav_{platform}_{country_code}")])
    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))

    await query.message.edit_text(
        f"✅ رصيدك الحالي: {balance} ر.س\n"
        f"عدد السيرفرات المتوفرة: {len(available_servers_for_display)}\n\n"
        "اختر السيرفر الذي ترغب بتجربته:",
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

    try:
        _, platform, country_code, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك للشراء الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text("❌ حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.")
        return

    all_servers_data = load_json_file(SERVERS_FILE, [])
    selected_server_entry = None
    for entry in all_servers_data:
        if entry["platform"] == platform and entry["country"] == country_code:
            selected_server_entry = entry
            break

    selected = None
    if selected_server_entry:
        selected = next((s for s in selected_server_entry.get("servers", []) if s["id"] == server_id), None)

    if not selected:
        await query.message.edit_text("⚠️ لم يتم العثور على السيرفر المطلوب.")
        logger.warning(f"المستخدم {user_id} حاول شراء سيرفر غير موجود: {platform}-{country_code}-{server_id}.")
        return

    current_quantity = selected.get("quantity", 0)
    price = selected.get("price", 0)
    user_balance = get_user_balance(user_id)

    if current_quantity <= 0:
        # ✅ تحسين رسالة الخطأ وزر العودة لسيناريو الكمية صفر
        await query.message.edit_text(
            f"❌ عذراً، لا توجد أرقام متاحة حالياً في سيرفر <b>{selected['name']}</b> لـ <b>{platform}</b> في <b>{country_code.upper()}</b>.\n"
            f"💰 رصيدك الحالي: {user_balance} ر.س",
            parse_mode="HTML",
            reply_markup=create_reply_markup([
                back_button(callback_data=f"country_{country_code}_{platform}", text="🔙 العودة لاختيار دولة/سيرفر آخر")
            ])
        )
        logger.info(f"المستخدم {user_id} حاول شراء سيرفر بكمية 0: {platform}-{country_code}-{server_id}.")
        return

    if user_balance < price:
        # ✅ تحسين رسالة الخطأ وزر العودة لسيناريو الرصيد غير كافٍ
        await query.message.edit_text(
            f"❌ رصيدك الحالي ({user_balance} ر.س) غير كافٍ لشراء هذا الرقم الذي يكلف {price} ر.س. يرجى شحن رصيدك.\n"
            f"👇 يمكنك شحن رصيدك الآن:",
            reply_markup=create_reply_markup([
                [InlineKeyboardButton("💳 شحن رصيدي", callback_data="recharge")],
                back_button(callback_data=f"country_{country_code}_{platform}", text="🔙 العودة")
            ]),
            parse_mode="HTML"
        )
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({user_balance}) لشراء سيرفر {platform}-{country_code}-{server_id} بسعر {price}.")
        return

    selected["quantity"] -= 1
    save_servers_data(all_servers_data)

    update_balance(user_id, -price)

    purchases = load_json_file(PURCHASES_FILE, {})

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

    save_json_file(PURCHASES_FILE, purchases)

    buttons = create_reply_markup([
        [InlineKeyboardButton("💬 طلب الكود", callback_data=f"get_code_{fake_number}_{server_id}")],
        [InlineKeyboardButton("❌ إلغاء الرقم", callback_data=f"cancel_number_{fake_number}_{server_id}")],
        back_button()
    ])

    await query.message.edit_text(
        f"✅ <b>تم شراء الرقم بنجاح!</b>\n\n"
        f"📱 <b>التطبيق:</b> {platform}\n"
        f"🌍 <b>الدولة:</b> {country_code.upper()}\n"
        f"💾 <b>السيرفر:</b> {selected['name']}\n"
        f"💰 <b>السعر:</b> {price} ر.س\n"
        f"🔢 <b>الرقم الخاص بك:</b> <code>{fake_number}</code>\n\n"
        f"⏳ <i>في انتظار الكود...</i>\n"
        f"💡 رصيدك الحالي: {get_user_balance(user_id)} ر.س",
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
    balance = get_user_balance(user_id)

    all_data = load_json_file(SERVERS_FILE, [])
    candidates = [
        s for s in all_data
        if s["platform"] == platform and
           any(server.get("quantity", 0) > 0 for server in s.get("servers", []))
    ]
    if not candidates:
        await query.message.edit_text("❌ لا توجد أرقام متوفرة حالياً لهذه المنصة.")
        logger.info(f"المستخدم {user_id} حاول اختيار دولة عشوائية لـ {platform} ولا توجد أرقام متوفرة.")
        return

    selected_country_entry = random.choice(candidates)
    country_code = selected_country_entry["country"]

    available_servers_in_country = [s for s in selected_country_entry["servers"] if s.get("quantity", 0) > 0]

    if not available_servers_in_country:
        await query.message.edit_text("❌ عذراً، لا توجد أرقام متوفرة في الدولة العشوائية المختارة حالياً. يرجى المحاولة مرة أخرى.")
        logger.warning(f"المستخدم {user_id} اختار دولة عشوائية {country_code} لـ {platform} ولكن لا يوجد سيرفرات متاحة فيها.")
        return

    if balance < min(s['price'] for s in available_servers_in_country):
        await query.message.edit_text(f"❌ رصيدك غير كافٍ لشراء أي رقم من السيرفرات المتوفرة في هذه الدولة.\nرصيدك الحالي: {balance} ر.س")
        logger.info(f"المستخدم {user_id} لديه رصيد غير كافٍ ({balance}) لشراء من الدولة العشوائية {country_code} لـ {platform}.")
        return

    buttons = []
    for s in available_servers_in_country:
        buttons.append([InlineKeyboardButton(
            f"{s['name']} - 💰 {s['price']} ر.س ({s.get('quantity', 0)} متاح)",
            callback_data=f"buy_{platform}_{country_code}_{s['id']}"
        )])
    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))

    await query.message.edit_text(
        f"🎲 تم اختيار دولة عشوائية: {country_code.upper()}\n"
        f"✅ رصيدك الحالي: {balance} ر.س\n"
        "اختر السيرفر المناسب:",
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

    all_data = load_json_file(SERVERS_FILE, [])

    countries_with_availability = set()
    for entry in all_data:
        if entry["platform"] == platform:
            if any(s.get("quantity", 0) > 0 for s in entry.get("servers", [])):
                countries_with_availability.add(entry["country"])

    if not countries_with_availability:
        await query.message.edit_text("❗ لا توجد أرقام متوفرة حالياً لهذه المنصة.")
        logger.info(f"لا توجد أرقام متوفرة لـ {platform} عند طلب الأكثر توفراً.")
        return

    buttons = []
    for code in sorted(list(countries_with_availability)):
        buttons.append([InlineKeyboardButton(f"{get_flag(code)} {code.upper()}", callback_data=f"country_{code}_{platform}")])

    buttons.append(back_button(callback_data=f"select_app_{platform}", text="🔙 العودة"))

    await query.message.edit_text(
        f"📦 الدول المتوفرة حالياً لـ {platform}:",
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info(f"تم عرض الدول الأكثر توفراً لـ {platform}.")

async def handle_platform_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج اختيار المنصة يدوياً عن طريق إرسال اسمها كنص (بدلاً من زر).
    """
    text = update.message.text.strip().lower()
    mapping = {
        "whatsapp": "WhatsApp",
        "telegram": "Telegram",
        "snapchat": "Snapchat",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "tiktok": "TikTok"
    }
    platform = mapping.get(text)
    if not platform:
        await update.message.reply_text("❌ لم يتم التعرف على المنصة.")
        logger.warning(f"المستخدم {update.effective_user.id} أدخل منصة غير معروفة: '{text}'.")
        return

    await update.message.reply_text(
        f"🧭 أنت الآن في قسم: {platform}\nاختر نوع الرقم الذي ترغب به:",
        reply_markup=category_inline_keyboard(platform)
    )

def get_flag(country_code):
    """
    يحول رمز كود الدولة (مثل 'sa') إلى علم الدولة (مثل '🇸🇦').
    """
    try:
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    except:
        return "🏳️"

async def show_available_platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة بالمنصات المتاحة حالياً مع عدد الدول المتوفرة لكل منها.
    """
    query = update.callback_query
    await query.answer()

    all_data = load_json_file(SERVERS_FILE, [])

    platforms_with_availability = {}
    for entry in all_data:
        platform = entry["platform"]
        country = entry["country"]
        if any(s.get("quantity", 0) > 0 for s in entry.get("servers", [])):
            if platform not in platforms_with_availability:
                platforms_with_availability[platform] = set()
            platforms_with_availability[platform].add(country)

    if not platforms_with_availability:
        await query.message.edit_text("❌ لا توجد منصات متاحة حالياً بأي أرقام متوفرة.")
        logger.info("لا توجد منصات متاحة بأي أرقام متوفرة عند طلب show_available_platforms.")
        return

    buttons = []
    for platform, countries in platforms_with_availability.items():
        flag_line = " ".join(get_flag(code) for code in sorted(countries))
        buttons.append([
            InlineKeyboardButton(f"✅ {platform} - {len(countries)} دولة", callback_data=f"select_app_{platform}")
        ])
        buttons.append([
            InlineKeyboardButton(flag_line, callback_data=f"select_app_{platform}")
        ])

    buttons.append(back_button())

    await query.message.edit_text(
        "📲 <b>المنصات المتاحة الآن:</b>\nاختر المنصة لرؤية الأرقام المتوفرة:",
        reply_markup=create_reply_markup(buttons),
        parse_mode="HTML"
    )
    logger.info("تم عرض المنصات المتاحة حاليا.")

async def show_ready_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة بالأرقام الفورية الجاهزة للشراء عبر مختلف المنصات والدول.
    """
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    balance = get_user_balance(user_id)

    all_data = load_json_file(SERVERS_FILE, [])

    ready_numbers = []
    for item in all_data:
        platform = item["platform"]
        country = item["country"]
        servers = item["servers"]
        available_servers = [s for s in servers if s.get("quantity", 0) > 0]
        if available_servers:
            cheapest = min(available_servers, key=lambda s: s["price"])
            ready_numbers.append({
                "platform": platform,
                "country": country,
                "flag": get_flag(country),
                "server": cheapest
            })

    ready_numbers.sort(key=lambda x: x["server"]["price"])

    buttons = []
    if not ready_numbers:
        await query.message.edit_text("❌ لا توجد أرقام فورية جاهزة حالياً.")
        logger.info("لا توجد أرقام فورية جاهزة لعرضها.")
        return

    for item in ready_numbers[:10]:
        btn_text = f"{item['flag']} {item['country']} - {item['platform']} 💰 {item['server']['price']} ر.س ({item['server'].get('quantity', 0)} متاح)"
        callback = f"buy_{item['platform']}_{item['country']}_{item['server']['id']}"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=callback)])

    buttons.append(back_button())

    await query.message.edit_text(
        "⚡ <b>أرقام فورية جاهزة:</b>\nاختر رقمًا للشراء الفوري:",
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

    try:
        _, _, fake_number, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك لطلب الكود الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text("❌ حدث خطأ في معالجة طلبك.")
        return

    purchases = load_json_file(PURCHASES_FILE, {})

    user_purchases = purchases.get(str(user_id), [])
    target_purchase = None

    for record in user_purchases:
        if record.get("fake_number") == fake_number and record.get("server_id") == server_id:
            target_purchase = record
            break

    if not target_purchase:
        await query.message.edit_text("❌ لم يتم العثور على هذا الرقم في سجل مشترياتك.")
        logger.warning(f"المستخدم {user_id} حاول طلب كود لرقم غير موجود في سجل مشترياته: {fake_number}.")
        return

    if target_purchase.get("status") == "active":
        await query.edit_message_text(f"✅ الكود لهذا الرقم ({fake_number}) تم إرساله مسبقاً. الكود الوهمي: <code>{target_purchase.get('fake_code', 'غير متوفر')}</code>", parse_mode="HTML")
        logger.info(f"المستخدم {user_id} طلب كودًا لرقم {fake_number} وهو نشط بالفعل.")
        return

    if target_purchase.get("status") == "cancelled":
        await query.edit_message_text(f"❌ هذا الرقم ({fake_number}) تم إلغاؤه مسبقاً. لا يمكن طلب الكود.")
        logger.warning(f"المستخدم {user_id} حاول طلب كود لرقم {fake_number} تم إلغاؤه.")
        return

    fake_code = str(random.randint(100000, 999999))
    target_purchase["status"] = "active"
    target_purchase["fake_code"] = fake_code

    purchases[str(user_id)] = user_purchases

    save_json_file(PURCHASES_FILE, purchases)

    await query.message.edit_text(
        f"✅ تم إرسال الكود بنجاح!\n\n"
        f"🔢 الرقم: <code>{fake_number}</code>\n"
        f"🔑 الكود الخاص بك: <code>{fake_code}</code>\n\n"
        f"⏳ <i>ملاحظة: هذا كود وهمي لأغراض الاختبار.</i>",
        parse_mode="HTML",
        reply_markup=create_reply_markup([
            back_button()
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

    try:
        _, _, fake_number, server_id_str = query.data.split("_")
        server_id = int(server_id_str)
    except ValueError:
        logger.error(f"خطأ في تحليل بيانات الكولباك لإلغاء الرقم الوهمي: {query.data}", exc_info=True)
        await query.message.edit_text("❌ حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.")
        return

    purchases = load_json_file(PURCHASES_FILE, {})

    user_purchases = purchases.get(str(user_id), [])
    target_purchase_index = -1
    target_purchase = None

    for i, record in enumerate(user_purchases):
        if record.get("fake_number") == fake_number and record.get("server_id") == server_id:
            target_purchase_index = i
            target_purchase = record
            break

    if not target_purchase:
        await query.message.edit_text("❌ لم يتم العثور على هذا الرقم في سجل مشترياتك.")
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم غير موجود في سجل مشترياته: {fake_number}.")
        return

    if target_purchase.get("status") == "active":
        await query.edit_message_text("❌ لا يمكن إلغاء الرقم بعد الحصول على الكود.")
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم {fake_number} بعد حصوله على الكود.")
        return

    if target_purchase.get("status") == "cancelled":
        await query.edit_message_text(f"❌ هذا الرقم ({fake_number}) تم إلغاؤه مسبقاً.")
        logger.warning(f"المستخدم {user_id} حاول إلغاء رقم {fake_number} تم إلغاؤه مسبقاً.")
        return

    price = target_purchase.get("price", 0)
    update_balance(user_id, price)

    user_purchases[target_purchase_index]["status"] = "cancelled"
    purchases[str(user_id)] = user_purchases

    save_json_file(PURCHASES_FILE, purchases)

    all_servers_data = load_json_file(SERVERS_FILE, [])
    for entry in all_servers_data:
        if entry["platform"] == target_purchase["platform"] and entry["country"] == target_purchase["country"]:
            for s in entry.get("servers", []):
                if s["id"] == server_id:
                    s["quantity"] = s.get("quantity", 0) + 1
                    break
            break
    save_servers_data(all_servers_data)

    await query.message.edit_text(
        f"✅ تم إلغاء الرقم <code>{fake_number}</code> بنجاح.\n"
        f"💰 تم استرداد <b>{price} ر.س</b> إلى رصيدك.\n"
        f"💡 رصيدك الجديد: {get_user_balance(user_id)} ر.س",
        parse_mode="HTML",
        reply_markup=create_reply_markup([
            back_button()
        ])
    )
    logger.info(f"المستخدم {user_id} ألغى الرقم {fake_number} (سيرفر {server_id}). تم استرداد {price} ر.س. الكمية الجديدة للسيرفر: {s.get('quantity', 0)}.")