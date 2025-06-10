# handlers/favorites_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.favorites import add_favorite, get_user_favorites # # هذه الدوال ستتغير مع DB
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from utils.helpers import get_flag # # تم تعديل هذا السطر لاستيراد get_flag من utils.helpers

async def handle_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة الدول المفضلة المحفوظة للمستخدم.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    favorites = get_user_favorites(user_id) # # هذه الدالة ستتغير لاحقاً
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    if not favorites:
        # # هنا يمكن إضافة زر للعودة أيضاً، أو للذهاب لقائمة شراء الأرقام
        keyboard = create_reply_markup([
            back_button(text=messages["back_button_text"], lang_code=lang_code)
        ])
        await query.message.edit_text(messages["no_favorites_yet"], reply_markup=keyboard)
        return

    text = messages["favorites_list_title"] + "\n\n"
    for i, fav in enumerate(favorites, 1):
        text += f"{i}. {fav}\n" # # المفضلة مخزنة كنص مباشر، سيتم تحسينها لاحقاً مع DB

    keyboard = create_reply_markup([
        back_button(text=messages["back_button_text"], lang_code=lang_code)
    ])
    await query.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج إضافة دولة إلى قائمة المفضلة الخاصة بالمستخدم.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    data = query.data  # fav_<platform>_<country>
    try:
        _, platform, country_code = data.split("_")
    except ValueError:
        await query.message.reply_text(messages["invalid_format_error"])
        return

    user_id = query.from_user.id
    # # استخدام get_flag من utils.helpers
    flag = get_flag(country_code)
    # # هنا، بدلاً من تخزين النص المباشر، يجب أن نفكر في تخزين platform و country_code
    # # في قاعدة البيانات لسهولة عرضها مترجمة لاحقاً.
    # # حالياً، سنبقى على نفس منطق تخزين النص لتجنب تغيير كبير قبل DB migration
    country_name_key = f"country_name_{country_code}"
    country_name = messages.get(country_name_key, country_code.upper())
    entry = messages["favorite_entry_format"].format(flag=flag, platform=platform, country_name=country_name)

    if add_favorite(user_id, entry): # # هذه الدالة ستتغير لاحقاً
        await query.message.reply_text(messages["favorite_added_success"])
    else:
        await query.message.reply_text(messages["favorite_already_exists"])