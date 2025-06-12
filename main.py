# main.py
"""
بوت الأرقام المؤقتة (Fake Digits Bot)

هذا هو الملف الرئيسي لتشغيل البوت.
يقوم بتهيئة التطبيق، وتعريف معالجات الأوامر والأزرار،
وإدارة تفاعلات المستخدمين مع البوت.
"""
import os # # تم إضافة هذا السطر أو التأكد من وجوده
from keyboards.language_kb import language_keyboard
import logging
from datetime import datetime
from utils.logger import setup_logging
from utils.i18n import get_messages
import html

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# استيراد دوال إعداد قاعدة البيانات
from database.database import create_db_and_tables, initialize_data_from_json

# استيرادات Modules المشروع (handlers) - مجمعة ومنظمة
# ✅ هذه الدوال مستخدمة كـ handlers مباشرة
from handlers.admin_users import (
    handle_admin_users, handle_block_user, handle_delete_user, handle_edit_user_balance,
    confirm_delete_user, back_to_dashboard_clear_admin_search
)
from handlers.agent_handler import show_agent_info, apply_as_agent
from handlers.category_handler import (
    handle_category_selection, handle_most_available_countries, handle_random_country,
    handle_platform_buttons, handle_country_selection, handle_fake_purchase,
    show_ready_numbers, get_fake_code, cancel_fake_number, show_available_platforms
)
from handlers.earn_credit_handler import show_earn_credit_page, view_referrals
# # تم تحديث هذا الاستيراد لإضافة delete_favorite_item
from handlers.favorites_handler import add_to_favorites, handle_favorites, delete_favorite_item
from handlers.help_handler import handle_usage_guide, handle_contact_support, handle_faq, handle_help
from handlers.language_handler import show_language_options, set_language
from handlers.main_dashboard import show_dashboard, handle_recharge, handle_recharge_admin
from handlers.main_menu import plus, go_to_buy_number
from handlers.offers_handler import show_general_offers, show_whatsapp_offers, show_telegram_offers
from handlers.profile_handler import handle_withdraw_request, handle_profile, handle_my_purchases, show_balance_only
from handlers.quick_search_handler import start_quick_search
from handlers.transfer_handler import (
    start_transfer, show_transfer_logs, confirm_clear_transfers,
    clear_all_transfers, confirm_transfer
)
# استيرادات utils - ✅ تم تنظيف الدوال غير المستخدمة هنا
from utils.balance import add_balance, deduct_balance
from utils.check_balance import check_balance
from utils.check_subscription import is_user_subscribed
from config import BOT_TOKEN, REQUIRED_CHANNELS, ADMINS, DEFAULT_LANGUAGE

# # استيراد ensure_user_exists من طبقة الخدمة الجديدة
from services.user_service import ensure_user_exists

# ✅ هذه الدوال يتم استيرادها الآن مباشرةً من input_router
from handlers.input_router import handle_all_text_input


# تهيئة نظام التسجيل
setup_logging()
logger = logging.getLogger(__name__)

# أزرار الاشتراك (لا تزال دالة مساعدة)
def subscription_buttons(lang_code: str = DEFAULT_LANGUAGE):
    """
    ينشئ لوحة مفاتيح الأزرار للتحقق من الاشتراك في القنوات المطلوبة.
    """
    messages = get_messages(lang_code)

    buttons = [[InlineKeyboardButton(messages["check_subscription_button"], callback_data="check_sub")]]
    for ch in REQUIRED_CHANNELS:
        buttons.append([InlineKeyboardButton(f"📢 {messages['subscribe_to_channel']} {ch}", url=f"https://t.me/{ch.lstrip('@')}")])
    return InlineKeyboardMarkup(buttons)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج الأمر /start.
    يعرض رسالة ترحيب بلغتين مع اختيار اللغة قبل الاستمرار.
    """
    user = update.effective_user
    ensure_user_exists(user.id, user.to_dict())

    # عرض رسالة ترحيبية مع اختيار اللغة
    welcome_text = (
        "🌐 يرجى اختيار لغتك للاستمرار في استخدام البوت:\n\n"
        "🌐 Please choose your language to continue using the bot:"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=language_keyboard()
    )


# زر التحقق
async def check_subscription_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج زر التحقق من الاشتراك.
    يتحقق مرة أخرى من اشتراك المستخدم بعد النقر على الزر.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if await is_user_subscribed(update, context):
        await query.edit_message_text(messages["subscribed_success"])
    else:
        await query.edit_message_text(
            messages["not_subscribed_channel_retry"].format(channel_link=REQUIRED_CHANNELS[0]),
            reply_markup=subscription_buttons(lang_code)
        )

# Global error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالج الأخطاء العام للتطبيق.
    يسجل الأخطاء ويرسل إشعاراً للمستخدم ونسخة للمشرفين.
    """
    logger.error("Exception while handling an update:", exc_info=context.error)

    # تحديد لغة المستخدم قبل جلب النصوص
    lang_code = None
    if update.effective_user:
        user_id = update.effective_user.id
        lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)

    messages = get_messages(lang_code if lang_code else DEFAULT_LANGUAGE)


    # إشعار المستخدم برسالة خطأ ودية مع خيار الدعم
    if update and update.effective_message:
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(messages["contact_support_button_error"], url="https://t.me/DrRamzi0")],
                [InlineKeyboardButton(messages["back_to_main_menu_error"], callback_data="back_to_dashboard")]
            ])
            await update.effective_message.reply_text(
                messages["error_processing_request_user"],
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"فشل إرسال رسالة الخطأ للمستخدم: {e}", exc_info=True)

    # إرسال تفاصيل الخطأ للمشرفين
    admin_message = (
        f"⚠️ <b>{messages['bot_error_alert']}</b>\n\n"
        f"<b>{messages['update_info']}:</b> <code>{html.escape(str(update))}</code>\n"
        f"<b>{messages['error_details']}:</b> <code>{html.escape(str(context.error))}</code>"
    )
    for admin_id in ADMINS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"فشل إرسال رسالة الخطأ للمشرف {admin_id}: {e}", exc_info=True)


# تشغيل البوت
def main():
    """
    الوظيفة الرئيسية لتشغيل البوت.
    تقوم بإنشاء التطبيق، وإضافة جميع المعالجات، وبدء استلام التحديثات.
    """
    # # إنشاء مجلد البيانات إذا لم يكن موجوداً
    if not os.path.exists('data'):
        os.makedirs('data')

    create_db_and_tables() # # إنشاء الجداول
    initialize_data_from_json() # # استيراد البيانات من JSON (لأول مرة فقط)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ————————————————————————————————
    # الأوامر (Commands)
    # ————————————————————————————————
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plus", show_dashboard))
    app.add_handler(CommandHandler("balance", check_balance))
    app.add_handler(CommandHandler("add_balance", add_balance))
    app.add_handler(CommandHandler("deduct_balance", deduct_balance))


    # ————————————————————————————————
    # المعالجات لأزرار Callback Queries
    # ————————————————————————————————

    # 1. الاشتراك (Subscription Check)
    app.add_handler(CallbackQueryHandler(check_subscription_button_handler, pattern="^check_sub$"))

    # 2. التنقل الأساسي (Core Navigation)
    app.add_handler(CallbackQueryHandler(show_dashboard, pattern="^back_to_dashboard$"))
    app.add_handler(CallbackQueryHandler(plus, pattern="^back_to_main$"))
    app.add_handler(CallbackQueryHandler(go_to_buy_number, pattern="^buy_number$"))
    app.add_handler(CallbackQueryHandler(show_available_platforms, pattern="^available_platforms$"))

    # 3. إدارة الرصيد (Balance Management)
    app.add_handler(CallbackQueryHandler(show_balance_only, pattern="^check_balance$"))
    app.add_handler(CallbackQueryHandler(handle_recharge, pattern="^recharge$"))
    app.add_handler(CallbackQueryHandler(handle_recharge_admin, pattern="^recharge_admin$"))
    app.add_handler(CallbackQueryHandler(start_transfer, pattern="^transfer_balance$"))
    app.add_handler(CallbackQueryHandler(confirm_transfer, pattern="^confirm_transfer_"))
    app.add_handler(CallbackQueryHandler(handle_withdraw_request, pattern="^withdraw_request$"))

    # 4. شراء الأرقام والخدمات (Number Purchase & Services)
    app.add_handler(CallbackQueryHandler(handle_platform_buttons, pattern="^select_app_"))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^region_"))
    app.add_handler(CallbackQueryHandler(handle_country_selection, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(handle_most_available_countries, pattern="^most_"))
    app.add_handler(CallbackQueryHandler(handle_random_country, pattern="^random_"))
    app.add_handler(CallbackQueryHandler(show_ready_numbers, pattern="^ready_numbers$"))
    app.add_handler(CallbackQueryHandler(handle_fake_purchase, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(get_fake_code, pattern="^get_code_"))
    app.add_handler(CallbackQueryHandler(cancel_fake_number, pattern="^cancel_number_"))

    # 5. العروض والبحث السريع والمفضلة (Offers, Quick Search & Favorites)
    app.add_handler(CallbackQueryHandler(show_general_offers, pattern="^offers$"))
    app.add_handler(CallbackQueryHandler(show_whatsapp_offers, pattern="^wa_offers$"))
    app.add_handler(CallbackQueryHandler(show_telegram_offers, pattern="^tg_offers$"))
    app.add_handler(CallbackQueryHandler(start_quick_search, pattern="^quick_search$"))
    app.add_handler(CallbackQueryHandler(handle_favorites, pattern="^favorites$"))
    app.add_handler(CallbackQueryHandler(add_to_favorites, pattern="^fav_"))
    app.add_handler(CallbackQueryHandler(delete_favorite_item, pattern="^delete_fav_")) # # تم إضافة هذا السطر

    # 6. الملف الشخصي والمشتريات (Profile & Purchases)
    app.add_handler(CallbackQueryHandler(handle_profile, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(handle_my_purchases, pattern="^my_purchases$"))

    # 7. الدعم والمساعدة (Support & Help)
    app.add_handler(CallbackQueryHandler(handle_help, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(handle_usage_guide, pattern="^usage_guide$"))
    app.add_handler(CallbackQueryHandler(handle_contact_support, pattern="^contact_support$"))
    app.add_handler(CallbackQueryHandler(handle_faq, pattern="^faq$"))

    # 8. ربح رصيد مجانًا وكن وكيلاً (Earn Credit & Be an Agent)
    app.add_handler(CallbackQueryHandler(show_earn_credit_page, pattern="^earn_credit$"))
    app.add_handler(CallbackQueryHandler(view_referrals, pattern="^view_referrals$"))
    app.add_handler(CallbackQueryHandler(show_agent_info, pattern="^become_agent$"))
    app.add_handler(CallbackQueryHandler(apply_as_agent, pattern="^apply_agent$"))

    # 9. إدارة المستخدمين (للمشرفين فقط) (Admin User Management)
    app.add_handler(CallbackQueryHandler(handle_admin_users, pattern="^admin_users$"))
    app.add_handler(CallbackQueryHandler(handle_block_user, pattern="^toggleban_"))
    app.add_handler(CallbackQueryHandler(handle_edit_user_balance, pattern="^edit_"))
    app.add_handler(CallbackQueryHandler(confirm_delete_user, pattern="^confirm_delete_"))
    app.add_handler(CallbackQueryHandler(handle_delete_user, pattern="^delete_user_confirmed_"))
    app.add_handler(CallbackQueryHandler(back_to_dashboard_clear_admin_search, pattern="^back_to_dashboard_clear_admin_search$"))
    app.add_handler(CallbackQueryHandler(show_transfer_logs, pattern="^view_transfer_logs$"))
    app.add_handler(CallbackQueryHandler(confirm_clear_transfers, pattern="^confirm_clear_transfers$"))
    app.add_handler(CallbackQueryHandler(clear_all_transfers, pattern="^clear_transfers$"))

    # 10. اللغة (Language)
    app.add_handler(CallbackQueryHandler(show_language_options, pattern="^change_language$"))
    app.add_handler(CallbackQueryHandler(set_language, pattern="^set_lang_"))

    # ————————————————————————————————
    # معالج الأخطاء (Error Handler)
    # ————————————————————————————————
    app.add_error_handler(error_handler)


    # ————————————————————————————————
    # معالجات المدخلات النصية (Text Input Handlers - يجب أن تكون في النهاية)
    # ————————————————————————————————
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_text_input))


    logger.info("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()