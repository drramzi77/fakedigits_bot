# handlers/language_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards.language_kb import language_keyboard
from handlers.main_dashboard import show_dashboard
from keyboards.utils_kb import back_button, create_reply_markup # # تم التأكد من استيرادها
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

async def show_language_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض خيارات اختيار لغة البوت للمستخدم.
    """
    query = update.callback_query
    await query.answer()

    # # تحديد لغة المستخدم الحالية لجلب نصوص الأزرار بشكل صحيح
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    await query.message.edit_text(
        messages["select_your_language"], # # استخدام النص المترجم
        reply_markup=create_reply_markup(language_keyboard(lang_code)) # # تمرير lang_code
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج تعيين لغة البوت المفضلة للمستخدم.
    """
    query = update.callback_query
    await query.answer() # # يجب أن يتم الإجابة على الكويري أولاً

    lang_code_selected = query.data.replace("set_lang_", "") # # الحصول على كود اللغة من الـ callback_data
    
    # # تحديث لغة المستخدم في context.user_data
    context.user_data["lang_code"] = lang_code_selected 
    
    messages = get_messages(lang_code_selected) # # جلب النصوص باللغة الجديدة

    # # استخدام النصوص المترجمة للتأكيد
    if lang_code_selected == "ar":
        confirmation_msg = messages["language_changed_to_arabic"]
    else: # assuming 'en' is the other option
        confirmation_msg = messages["language_changed_to_english"]
    
    await query.message.edit_text(confirmation_msg)

    # العودة إلى القائمة الرئيسية (الآن ستظهر باللغة الجديدة)
    await show_dashboard(update, context)