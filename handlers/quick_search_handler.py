import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.server_kb import load_servers
from utils.balance import get_user_balance
import logging 

logger = logging.getLogger(__name__)

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

# ✅ دالة مساعدة لتحويل كود الدولة إلى علم
def get_flag(country_code):
    try:
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    except:
        return "🏳️"

# ✅ عند الضغط على "البحث السريع" (الآن سيطلب الدولة مباشرة)
async def start_quick_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # # تنظيف حالات user_data المتعلقة بانتظار المدخلات الأخرى
    context.user_data.pop("transfer_stage", None)
    context.user_data.pop("admin_search_mode", None)
    context.user_data.pop("edit_balance_mode", None)
    context.user_data.pop("awaiting_country_input", None) 
    context.user_data.pop("selected_platform", None) 
    context.user_data.pop("admin_search", None) 
    context.user_data.pop("awaiting_input", None) # # مسح حالة التوجيه العامة

    context.user_data["awaiting_input"] = "quick_search_country_general" # # حالة جديدة للبحث العام عن الدول

    message = "🌹 مرحباً 😊\nDr\\Ramzi\n\n— قم بإرسال اسم الدولة (بالعربية أو الإنجليزية أو بالرمز 🇸🇦) للبحث عنها:\n\n──────────────"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_dashboard")]
    ])

    await query.message.edit_text(
        message,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    logger.info(f"المستخدم {update.effective_user.id} بدأ البحث السريع العام عن الدول.")

# # تم حذف handle_quick_search_platform_selection لأننا لن نطلب اختيار المنصة أولاً

# ✅ عندما يكتب المستخدم اسم الدولة (لبحث عام)
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"handle_text_input: تم استدعاء الدالة. user_data: {context.user_data}")
    
    text = update.message.text.strip().lower()
    user_id = update.effective_user.id
    
    # # التحقق من الحالة الصحيحة للبحث العام
    if context.user_data.get("awaiting_input") == "quick_search_country_general":
        logger.info(f"handle_text_input: الحالة صحيحة للبحث العام. النص: '{text}'")

        country_code = ALL_COUNTRIES.get(text)
        
        if not country_code:
            logger.info(f"handle_text_input: لم يتم العثور على كود الدولة لـ '{text}'.")
            await update.message.reply_text(
                "❌ لم يتم العثور على هذه الدولة. تأكد من كتابة الاسم بشكل صحيح.\n"
                "أو حاول البحث عن دولة أخرى.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]])
            )
            context.user_data["awaiting_input"] = "quick_search_country_general" # # إعادة تعيين الحالة للسماح بالمحاولة
            return
        
        logger.info(f"handle_text_input: تم العثور على كود الدولة: '{country_code}' لـ '{text}'.")
        # # البحث عن سيرفرات لهذه الدولة عبر جميع المنصات
        all_servers_for_country = []
        try:
            with open("data/servers.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for entry in data:
                if entry["country"] == country_code and entry.get("servers"):
                    for server in entry["servers"]:
                        all_servers_for_country.append({
                            "platform": entry["platform"],
                            "country": entry["country"],
                            "server_id": server["id"],
                            "server_name": server["name"],
                            "price": server["price"]
                        })
        except FileNotFoundError:
            logger.error("ملف servers.json غير موجود.", exc_info=True)
            all_servers_for_country = []
        except json.JSONDecodeError:
            logger.error("خطأ في قراءة ملف servers.json.", exc_info=True)
            all_servers_for_country = []
        except Exception as e:
            logger.error(f"خطأ غير متوقع أثناء تحميل السيرفرات: {e}", exc_info=True)
            all_servers_for_country = []

        if not all_servers_for_country:
            logger.info(f"handle_text_input: لا توجد سيرفرات لدولة {text.title()}.")
            await update.message.reply_text(
                f"❗ لا توجد أرقام متاحة حاليًا لدولة {text.title()} على أي منصة.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back_to_dashboard")]])
            )
            context.user_data.pop("awaiting_input", None) # # إنهاء حالة البحث
            return

        balance = get_user_balance(user_id)
        
        # # بناء الرسالة والأزرار
        message_parts = [
            f"📍 <b>نتائج البحث عن:</b> {get_flag(country_code)} {text.title()}",
            f"💰 <b>رصيدك:</b> {balance} ر.س",
            "━━━━━━━━━━━━━━━"
        ]
        
        buttons = []
        
        # # فرز النتائج حسب المنصة ثم السعر (اختياري، لكن يحسن العرض)
        all_servers_for_country.sort(key=lambda x: (x['platform'], x['price']))
        
        current_platform = ""
        for s in all_servers_for_country:
            if s["platform"] != current_platform:
                message_parts.append(f"\n📱 <b>{s['platform']}</b>:")
                current_platform = s["platform"]
            
            message_parts.append(f"  • {s['server_name']} - 💰 {s['price']} ر.س")
            
            # # إضافة زر شراء لكل سيرفر
            buttons.append([InlineKeyboardButton(
                f"شراء {s['platform']} - {s['server_name']} ({s['price']} ر.س)",
                callback_data=f"buy_{s['platform']}_{country_code}_{s['server_id']}"
            )])
        
        message = "\n".join(message_parts)

        buttons.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_dashboard")])

        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
        context.user_data.pop("awaiting_input", None) # # مسح الحالة عند عرض النتائج بنجاح
        logger.info(f"handle_text_input: المستخدم {user_id} بحث عن {text} وتم عرض النتائج.")
        return # # تم التعامل مع الرسالة

    else:
        logger.debug(f"handle_text_input: حالة غير متوقعة، تم تمرير الرسالة. user_data: {context.user_data}")
        # # إذا لم تكن في حالة awaiting_country_input_general، دعه يمر إلى المعالجات الأخرى.
        return None