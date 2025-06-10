# keyboards/utils_kb.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.i18n import get_messages # # تم إضافة هذا السطر لاستيراد دالة جلب النصوص
from config import DEFAULT_LANGUAGE # # تم إضافة هذا السطر لاستيراد اللغة الافتراضية

def back_button(callback_data: str = "back_to_dashboard", text: str = None, lang_code: str = DEFAULT_LANGUAGE): # # تم إضافة معامل lang_code وتعديل text
    """
    يُنشئ زر "العودة" مع callback_data محدد.
    افتراضياً يعود إلى لوحة التحكم الرئيسية.
    Args:
        callback_data (str): البيانات التي سيتم إرسالها عند النقر على الزر.
        text (str, optional): النص الظاهر على الزر. إذا كان None، سيتم جلب النص المترجم الافتراضي.
        lang_code (str): كود اللغة لجلب النص المترجم الافتراضي.
    """
    messages = get_messages(lang_code) # # جلب النصوص باللغة المطلوبة
    # # إذا لم يتم تمرير نص محدد، استخدم النص الافتراضي المترجم
    button_text = text if text is not None else messages.get("back_button_text", "🔙 العودة")
    return [InlineKeyboardButton(button_text, callback_data=callback_data)]

def create_reply_markup(buttons: list):
    """
    يُنشئ InlineKeyboardMarkup من قائمة أزرار.
    """
    return InlineKeyboardMarkup(buttons)