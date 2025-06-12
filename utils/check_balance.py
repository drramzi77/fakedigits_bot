# utils/check_balance.py

import logging
# import json # لم نعد بحاجة لها
# import os # لم نعد بحاجة لها
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS, DEFAULT_LANGUAGE
# from utils.data_manager import load_json_file # لم نعد بحاجة لها
from utils.i18n import get_messages
# # استيراد خدمة المستخدم ودالة get_db
from services import user_service
from database.database import get_db

logger = logging.getLogger(__name__)

# # هذه الدالة لم تعد ضرورية هنا لأن get_user_balance في utils.balance.py تتولى المهمة
# # ويمكننا استخدامها مباشرة.
# def get_user_balance(user_id: int) -> float:
#     """
#     تم نقل هذه الوظيفة إلى utils.balance.py وهي تستخدم الآن قاعدة البيانات.
#     """
#     # يمكن استدعاء get_user_balance من utils.balance هنا
#     from utils.balance import get_user_balance as get_balance_from_utils
#     return get_balance_from_utils(user_id, {"id": user_id})


# ✅ أمر /balance
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج الأمر /balance.
    يعرض الرصيد الحالي للمستخدم الذي أصدر الأمر،
    أو رصيد مستخدم آخر إذا كان المصدر مشرفاً.
    """
    user = update.effective_user
    requester_id = user.id

    lang_code = context.user_data.get("lang_code", DEFAULT_LANGUAGE)
    messages = get_messages(lang_code)

    # # استيراد get_user_balance هنا لضمان استخدام الدالة المحدثة
    from utils.balance import get_user_balance as get_current_user_balance 

    # إذا لم يتم تمرير معرف مستخدم، نعرض الرصيد لنفس المستخدم
    if not context.args:
        balance = get_current_user_balance(requester_id, user.to_dict()) # # استخدام الدالة المحدثة
        name = user.username if user.username else f"{user.first_name} {user.last_name or ''}"
        
        await update.message.reply_text(
            messages["my_balance_info"].format(
                name=name,
                user_id=requester_id,
                balance=balance,
                currency=messages["price_currency"]
            ),
            parse_mode="HTML"
        )
        return

    # إذا تم تمرير معرف مستخدم، تحقق من صلاحية المدير
    if requester_id in ADMINS and len(context.args) == 1:
        try:
            target_id = int(context.args[0])
            
            # # التأكد من وجود المستخدم المستهدف
            target_user_info_for_ensure = {"id": target_id} # معلومات بسيطة لإنشاء المستخدم إذا لم يكن موجودا
            user_service.ensure_user_exists(target_id, target_user_info_for_ensure) # # التأكد من وجود المستخدم
            
            balance = get_current_user_balance(target_id, target_user_info_for_ensure) # # استخدام الدالة المحدثة

            # # محاولة جلب معلومات المستخدم لعرض اسمه (من Telegram API)
            try:
                member = await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=target_id)
                name = member.user.username if member.user.username else f"{member.user.first_name} {member.user.last_name or ''}"
            except Exception as e:
                logger.warning(f"لم يتمكن البوت من جلب معلومات المستخدم {target_id} (ربما ليس في المجموعة/خاص): {e}")
                
                # # في حالة الفشل، حاول جلب الاسم من قاعدة البيانات إذا كان متاحًا
                for db in get_db():
                    user_db_obj = user_service.get_user(db, target_id)
                    if user_db_obj and (user_db_obj.username or user_db_obj.first_name):
                        name = user_db_obj.username if user_db_obj.username else f"{user_db_obj.first_name} {user_db_obj.last_name or ''}"
                    else:
                        name = messages["unknown_user_in_group"] # # استخدام النص المترجم


            await update.message.reply_text(
                messages["user_balance_info"].format(
                    name=name,
                    user_id=target_id,
                    balance=balance,
                    currency=messages["price_currency"]
                ),
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text(messages["invalid_user_id_balance_command"])
        except Exception as e: # # معالجة الأخطاء العامة
            logger.error(f"خطأ عند جلب رصيد مستخدم آخر بواسطة المشرف {requester_id}: {e}", exc_info=True)
            await update.message.reply_text(messages["error_fetching_user_balance"]) # # رسالة خطأ جديدة
    else:
        await update.message.reply_text(messages["no_permission_to_view_others_balance"])