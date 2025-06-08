# main.py

import logging
from datetime import datetime # قد تحتاجها لبعض السجلات أو الوظائف المستقبلية
from utils.logger import setup_logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# استيرادات Modules المشروع (handlers) - مجمعة ومنظمة
from handlers.admin_users import (
    handle_admin_users, handle_block_user, handle_delete_user, handle_edit_user_balance,
    confirm_delete_user, back_to_dashboard_clear_admin_search, ensure_user_exists,
    receive_balance_input, handle_admin_search
)
from handlers.agent_handler import show_agent_info, apply_as_agent
from handlers.category_handler import (
    handle_category_selection, handle_most_available_countries, handle_random_country,
    handle_platform_selection, handle_platform_buttons, handle_country_selection,
    handle_fake_purchase, show_ready_numbers, get_fake_code, cancel_fake_number,
    show_available_platforms # ✅ تم إضافة هذا السطر
)
from handlers.earn_credit_handler import show_earn_credit_page, view_referrals
from handlers.favorites_handler import add_to_favorites, handle_favorites
from handlers.help_handler import handle_usage_guide, handle_contact_support, handle_faq, handle_help
from handlers.language_handler import show_language_options, set_language
from handlers.main_dashboard import show_dashboard, handle_recharge, handle_recharge_admin
from handlers.main_menu import plus, go_to_buy_number
from handlers.offers_handler import show_general_offers, show_whatsapp_offers, show_telegram_offers
from handlers.profile_handler import handle_withdraw_request, handle_profile, handle_my_purchases, show_balance_only
from handlers.quick_search_handler import start_quick_search, handle_text_input
from handlers.transfer_handler import (
    start_transfer, show_transfer_logs, confirm_clear_transfers,
    clear_all_transfers, confirm_transfer, handle_transfer_input
)
# استيرادات utils
from utils.balance import add_balance, deduct_balance, get_user_balance as get_balance_util
from utils.check_balance import check_balance
from utils.check_subscription import is_user_subscribed
from config import BOT_TOKEN, REQUIRED_CHANNELS, ADMINS # تأكد من استيراد ADMINS هنا

# استيراد موجه المدخلات النصية
from handlers.input_router import handle_all_text_input


# تهيئة نظام التسجيل
setup_logging()
logger = logging.getLogger(__name__)

# أزرار الاشتراك (لا تزال دالة مساعدة)
def subscription_buttons():
    buttons = [[InlineKeyboardButton("🔁 تحقق من الاشتراك", callback_data="check_sub")]]
    for ch in REQUIRED_CHANNELS:
        buttons.append([InlineKeyboardButton(f"📢 اشترك في {ch}", url=f"https://t.me/{ch.lstrip('@')}")])
    return InlineKeyboardMarkup(buttons)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user_exists(user.id, user.to_dict()) # تسجيل/تحديث بيانات المستخدم عند كل أمر /start

    if await is_user_subscribed(update, context):
        await update.message.reply_text("✅ تم التحقق من اشتراكك.\nاستخدم الأمر /plus للمتابعة.")
    else:
        await update.message.reply_text(
            "📢 لضمان حصولك على الأرقام المميزة أولاً بأول، يرجى الاشتراك في القناة الرسمية للبوت.\n\n"
            "🔒 الاشتراك ضروري لتفعيل خدمات البوت والاستفادة الكاملة.\n"
            "👇 قم بالاشتراك ثم اضغط على زر 'تحقق من الاشتراك' بالأسفل:",
            reply_markup=subscription_buttons()
        )

# زر التحقق
async def check_subscription_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await is_user_subscribed(update, context):
        await query.edit_message_text("✅ تم التحقق من اشتراكك.\nاستخدم الأمر /plus للمتابعة.")
    else:
        await query.edit_message_text(
            "❗ لم نتمكن من التحقق من اشتراكك حتى الآن.\n"
            "✅ تأكد من أنك اشتركت في القناة المطلوبة.\n"
            "🔄 بعد الاشتراك، اضغط على الزر بالأسفل لإعادة التحقق.",
            reply_markup=subscription_buttons()
        )

# Global error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user/admin."""
    logger.error("Exception while handling an update:", exc_info=context.error)

    # Inform the user in case of an error
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ حدث خطأ غير متوقع! تم إبلاغ المسؤولين. يرجى المحاولة لاحقاً."
            )
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}", exc_info=True)

    # Optionally, send error details to an admin
    admin_message = (
        f"⚠️ <b>حدث خطأ في البوت!</b>\n\n"
        f"<b>Update:</b> <code>{update}</code>\n"
        f"<b>Error:</b> <code>{context.error}</code>"
    )
    for admin_id in ADMINS: # Assuming ADMINS is imported from config
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Failed to send error message to admin {admin_id}: {e}", exc_info=True)


# تشغيل البوت
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ————————————————————————————————
    # الأوامر (Commands)
    # ————————————————————————————————
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plus", show_dashboard))
    app.add_handler(CommandHandler("add_balance", add_balance))
    app.add_handler(CommandHandler("deduct_balance", deduct_balance))
    app.add_handler(CommandHandler(
        "balance", check_balance)) # أمر عرض الرصيد

    # ————————————————————————————————
    # المعالجات لأزرار Callback Queries
    # ————————————————————————————————

    # الاشتراك
    app.add_handler(CallbackQueryHandler(check_subscription_button, pattern="^check_sub$"))

    # التنقل الأساسي
    app.add_handler(CallbackQueryHandler(show_dashboard, pattern="^back_to_dashboard$"))
    app.add_handler(CallbackQueryHandler(plus, pattern="^back_to_main$"))
    app.add_handler(CallbackQueryHandler(go_to_buy_number, pattern="^buy_number$"))

    # الشحن والرصيد
    app.add_handler(CallbackQueryHandler(handle_recharge, pattern="^recharge$"))
    app.add_handler(CallbackQueryHandler(handle_recharge_admin, pattern="^recharge_admin$"))
    app.add_handler(CallbackQueryHandler(show_balance_only, pattern="^check_balance$"))
    app.add_handler(CallbackQueryHandler(handle_withdraw_request, pattern="^withdraw_request$"))

    # التحويلات
    app.add_handler(CallbackQueryHandler(start_transfer, pattern="^transfer_balance$"))
    app.add_handler(CallbackQueryHandler(confirm_transfer, pattern="^confirm_transfer_"))
    app.add_handler(CallbackQueryHandler(show_transfer_logs, pattern="^view_transfer_logs$"))
    app.add_handler(CallbackQueryHandler(confirm_clear_transfers, pattern="^confirm_clear_transfers$"))
    app.add_handler(CallbackQueryHandler(clear_all_transfers, pattern="^clear_transfers$"))

    # شراء الأرقام والخدمات
    app.add_handler(CallbackQueryHandler(handle_platform_buttons, pattern="^select_app_"))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^region_"))
    app.add_handler(CallbackQueryHandler(handle_country_selection, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(handle_most_available_countries, pattern="^most_"))
    app.add_handler(CallbackQueryHandler(handle_random_country, pattern="^random_"))
    app.add_handler(CallbackQueryHandler(handle_fake_purchase, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(show_ready_numbers, pattern="^ready_numbers$"))
    app.add_handler(CallbackQueryHandler(show_available_platforms, pattern="^available_platforms$"))

    # العروض والبحث السريع والمفضلة
    app.add_handler(CallbackQueryHandler(show_general_offers, pattern="^offers$"))
    app.add_handler(CallbackQueryHandler(show_whatsapp_offers, pattern="^wa_offers$"))
    app.add_handler(CallbackQueryHandler(show_telegram_offers, pattern="^tg_offers$"))
    app.add_handler(CallbackQueryHandler(start_quick_search, pattern="^quick_search$"))
    app.add_handler(CallbackQueryHandler(handle_favorites, pattern="^favorites$"))
    app.add_handler(CallbackQueryHandler(add_to_favorites, pattern="^fav_"))

    # الملف الشخصي والمساعدة
    app.add_handler(CallbackQueryHandler(handle_profile, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(handle_my_purchases, pattern="^my_purchases$"))
    app.add_handler(CallbackQueryHandler(handle_help, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(handle_usage_guide, pattern="^usage_guide$"))
    app.add_handler(CallbackQueryHandler(handle_contact_support, pattern="^contact_support$"))
    app.add_handler(CallbackQueryHandler(handle_faq, pattern="^faq$"))

    # اللغة
    app.add_handler(CallbackQueryHandler(show_language_options, pattern="^change_language$"))
    app.add_handler(CallbackQueryHandler(set_language, pattern="^set_lang_"))

    # ربح رصيد مجانًا
    app.add_handler(CallbackQueryHandler(show_earn_credit_page, pattern="^earn_credit$"))
    app.add_handler(CallbackQueryHandler(view_referrals, pattern="^view_referrals$"))

    # إدارة المستخدمين (للمشرفين)
    app.add_handler(CallbackQueryHandler(handle_admin_users, pattern="^admin_users$"))
    app.add_handler(CallbackQueryHandler(handle_block_user, pattern="^toggleban_"))
    app.add_handler(CallbackQueryHandler(handle_edit_user_balance, pattern="^edit_"))
    app.add_handler(CallbackQueryHandler(confirm_delete_user, pattern="^confirm_delete_"))
    app.add_handler(CallbackQueryHandler(handle_delete_user, pattern="^delete_user_confirmed_"))
    app.add_handler(CallbackQueryHandler(back_to_dashboard_clear_admin_search, pattern="^back_to_dashboard_clear_admin_search$"))

    # كن وكيلا معنا
    app.add_handler(CallbackQueryHandler(show_agent_info, pattern="^become_agent$"))
    app.add_handler(CallbackQueryHandler(apply_as_agent, pattern="^apply_agent$"))

    # ————————————————————————————————
    # معالج الأخطاء (Error Handler)
    # ————————————————————————————————
    app.add_error_handler(error_handler) # ✅ إضافة معالج الأخطاء هنا


    # ————————————————————————————————
    # معالج المدخلات النصية (يجب أن يكون في النهاية)
    # ————————————————————————————————
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_text_input))


    logger.info("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()