# handlers/favorites_handler.py

import logging # تم إضافة هذا السطر
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
# # استيراد خدمة المفضلة ودالة الحصول على الجلسة
from services import favorite_service
from database.database import get_db
from keyboards.utils_kb import back_button, create_reply_markup
from utils.i18n import get_messages
from config import DEFAULT_LANGUAGE
from utils.helpers import get_flag

logger = logging.getLogger(__name__) # تم إضافة هذا السطر

async def handle_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعرض قائمة الدول المفضلة المحفوظة للمستخدم من قاعدة البيانات.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    
    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    favorites_list = []
    for db in get_db(): # # استخدام get_db للحصول على جلسة
        favorites_list = favorite_service.get_favorites_by_user_id(db, user_id) # # استخدام خدمة المفضلة

    if not favorites_list:
        keyboard = create_reply_markup([
            back_button(text=messages["back_button_text"], lang_code=lang_code)
        ])
        await query.message.edit_text(messages["no_favorites_yet"], reply_markup=keyboard)
        logger.info(f"المستخدم {user_id} ليس لديه أي مفضلات محفوظة.")
        return

    text = messages["favorites_list_title"] + "\n\n"
    buttons = []
    for i, fav_obj in enumerate(favorites_list, 1): # # التكرار على كائنات Favorite
        text += f"{i}. {fav_obj.display_text}\n" # # الوصول إلى .display_text مباشرة
        # # إضافة زر لحذف المفضلة (اختياري لكن مفيد)
        buttons.append([InlineKeyboardButton(
            messages["delete_favorite_button"].format(number=i),
            callback_data=f"delete_fav_{fav_obj.id}" # # استخدام ID المفضلة من DB
        )])
        
    buttons.append(back_button(text=messages["back_button_text"], lang_code=lang_code))

    await query.message.edit_text(text, reply_markup=create_reply_markup(buttons), parse_mode="HTML")
    logger.info(f"المستخدم {user_id} يعرض قائمة مفضلاته ({len(favorites_list)} عنصر).")

async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يعالج إضافة دولة إلى قائمة المفضلة الخاصة بالمستخدم إلى قاعدة البيانات.
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
        logger.error(f"خطأ في تحليل بيانات الكولباك لإضافة المفضلة: {query.data}", exc_info=True)
        return

    user_id = query.from_user.id
    
    flag = get_flag(country_code)
    country_name_key = f"country_name_{country_code}"
    country_name = messages.get(country_name_key, country_code.upper())
    display_text = messages["favorite_entry_format"].format(flag=flag, platform=platform, country_name=country_name)

    for db in get_db(): # # استخدام get_db
        if favorite_service.add_user_favorite(db, user_id, platform, country_code, display_text): # # استخدام خدمة المفضلة
            await query.message.reply_text(messages["favorite_added_success"])
            logger.info(f"المستخدم {user_id} أضاف المفضلة '{display_text}'.")
        else:
            await query.message.reply_text(messages["favorite_already_exists"])
            logger.info(f"المستخدم {user_id} حاول إضافة مفضلة موجودة بالفعل: '{display_text}'.")

# # دالة جديدة لحذف المفضلة
async def delete_favorite_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    يحذف عنصراً من قائمة المفضلة الخاصة بالمستخدم.
    """
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    try:
        _, _, favorite_id_str = query.data.split("_")
        favorite_id = int(favorite_id_str)
    except ValueError:
        await query.message.reply_text(messages["invalid_format_error"])
        logger.error(f"خطأ في تحليل بيانات الكولباك لحذف المفضلة: {query.data}", exc_info=True)
        return

    user_id = query.from_user.id

    for db in get_db(): # # استخدام get_db
        if favorite_service.delete_user_favorite(db, user_id, favorite_id): # # استخدام خدمة المفضلة
            await query.message.edit_text(messages["favorite_deleted_success"])
            logger.info(f"المستخدم {user_id} حذف المفضلة ID: {favorite_id}.")
        else:
            await query.message.edit_text(messages["favorite_not_found_or_not_owned"])
            logger.warning(f"المستخدم {user_id} حاول حذف مفضلة غير موجودة أو لا يملكها: ID={favorite_id}.")
    
    # # بعد الحذف، قد ترغب في إعادة عرض قائمة المفضلة المحدثة
    await handle_favorites(update, context) # # إعادة عرض القائمة المحدثة