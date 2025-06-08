# keyboards/utils_kb.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def back_button(callback_data: str = "back_to_dashboard", text: str = "🔙 العودة"):
    """
    يُنشئ زر "العودة" مع callback_data محدد.
    افتراضياً يعود إلى لوحة التحكم الرئيسية.
    """
    return [InlineKeyboardButton(text, callback_data=callback_data)]

def create_reply_markup(buttons: list):
    """
    يُنشئ InlineKeyboardMarkup من قائمة أزرار.
    """
    return InlineKeyboardMarkup(buttons)
