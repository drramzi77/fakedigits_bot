# handlers/offers_handler.py

import logging
# import os # لم نعد بحاجة لـ os.path.join لملفات البيانات
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.balance import get_user_balance # هذه الدالة تم تحديثها لاستخدام DB
# from utils.data_manager import load_json_file # لم نعد بحاجة لها
from keyboards.utils_kb import back_button, create_reply_markup
from keyboards.countries_kb import get_flag # هذه الدالة لا تزال تستخدم get_flag
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
# # استيراد خدمة السيرفرات ودالة الحصول على الجلسة
from services import server_service
from database.database import get_db

logger = logging.getLogger(__name__)

# # لم نعد بحاجة لـ SERVERS_FILE لأننا سنتعامل مع DB مباشرة
# SERVERS_FILE = os.path.join("data", "servers.json")

# # هذه الدالة (generate_offer_buttons) لم يتم استخدامها في الكود السابق،
# # وهي غير مطلوبة بالهيكل الجديد. يمكن حذفها.
# # سنتركها هنا ولكن لن يتم استدعاؤها.
def generate_offer_buttons(platform: str, lang_code: str = DEFAULT_LANGUAGE):
    """
    ملاحظة: هذه الدالة لم يتم استخدامها بشكل مباشر من show_platform_offers في الكود السابق.
    إذا كنت تستخدمها في مكان آخر، فستحتاج إلى تحديثها بنفس منطق العروض الجديدة.
    """
    messages = get_messages(lang_code)
    # # هذا الجزء من الدالة لم يعد مناسباً بعد التحول إلى DB
    # data = load_json_file("data/servers.json", [])
    # # ... الكود القديم ...
    buttons = []
    buttons.append(back_button(text=messages["back_button_text"], callback_data="back_to_dashboard", lang_code=lang_code))
    return InlineKeyboardMarkup(buttons)


async def show_platform_offers(update: Update, context: ContextTypes.DEFAULT_TYPE, platform_filter: str = None):
    """
    يعرض العروض المتاحة (السيرفرات ذات الكمية والسعر المحدد) لمنصة معينة أو لجميع المنصات.
    """
    query = update.callback_query
    await query.answer(text=get_messages(context.user_data.get("lang_code", DEFAULT_LANGUAGE)).get("fetching_data", "جارٍ جلب البيانات..."), show_alert=False) # # أضفنا answer هنا

    user = update.effective_user
    user_id = user.id
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    balance = get_user_balance(user_id, user.to_dict()) # # استخدام get_user_balance (تم تحديثها)

    available_offers_list = []
    for db in get_db(): # # استخدام get_db
        if platform_filter:
            # # جلب السيرفرات المتاحة لمنصة معينة
            # # server_service.get_servers_by_platform_and_country تقوم بالفلترة حسب الكمية > 0
            servers = server_service.get_servers_by_platform_and_country(db, platform_filter, None) # هنا لا نفرق بالبلد
            # # نحتاج جلب الكل ثم الفلترة أو جلب الكل ثم الفرز
            all_available_servers = server_service.get_all_available_offers(db) # جلب كل العروض المتاحة
            available_offers_list = [s for s in all_available_servers if s.platform == platform_filter]
        else:
            # # جلب جميع السيرفرات المتاحة
            available_offers_list = server_service.get_all_available_offers(db)
    
    # # لا حاجة لفلترة الكمية هنا مرة أخرى لأن الدوال في server_service تقوم بذلك
    # # لا حاجة لتحويلها إلى قواميس، سنتعامل مع كائنات Server مباشرة

    # # ترتيب العروض حسب السعر (من الأقل للأعلى) - لا يزال مطلوباً
    available_offers_list.sort(key=lambda s: s.price)

    buttons = []
    MAX_OFFERS_DISPLAY = 10 # # عدد العروض المراد عرضها في البداية

    if not available_offers_list:
        text = messages["offers_title"] + "\n\n" + messages["no_offers_available"]
    else:
        text = messages["offers_title"] + "\n\n"
        text += messages["your_balance_is"].format(balance=balance, currency=messages["price_currency"]) + "\n\n"
        text += messages["available_offers_list"] + "\n"

        # # إضافة أزرار لكل عرض
        for offer_obj in available_offers_list[:MAX_OFFERS_DISPLAY]: # # التكرار على كائنات Server
            country_name_key = f"country_name_{offer_obj.country}"
            country_name = messages.get(country_name_key, offer_obj.country.upper())
            
            btn_text = messages["offer_button_label_new"].format( # # مفتاح جديد لرسالة الزر
                flag=get_flag(offer_obj.country), # # استخدام .country
                country_name=country_name,
                platform=offer_obj.platform, # # استخدام .platform
                price=offer_obj.price, # # استخدام .price
                currency=messages["price_currency"],
                quantity=offer_obj.quantity # # استخدام .quantity
            )
            # # callback_data لزر الشراء المباشر (يجب أن تتطابق مع handle_fake_purchase)
            callback_data = f"buy_{offer_obj.platform}_{offer_obj.country}_{offer_obj.server_id}" # # استخدام .server_id
            buttons.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])
        
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
    # # تم حذف await update.callback_query.answer() من هنا لأنه تم نقله إلى show_platform_offers
    await show_platform_offers(update, context, "WhatsApp")

async def show_telegram_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج النقر على زر "عروض تليجرام" لعرض العروض الخاصة بالمنصة.
    """
    # # تم حذف await update.callback_query.answer() من هنا لأنه تم نقله إلى show_platform_offers
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