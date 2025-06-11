from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE

def back_button(callback_data: str = "back_to_dashboard", text: str = None, lang_code: str = DEFAULT_LANGUAGE):
    messages = get_messages(lang_code)
    button_text = text if text is not None else messages.get("back_button_text", "🔙 العودة")
    return [InlineKeyboardButton(button_text, callback_data=callback_data)]

def create_reply_markup(buttons: list):
    return InlineKeyboardMarkup(buttons)
