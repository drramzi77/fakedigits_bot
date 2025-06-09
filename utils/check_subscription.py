# utils/check_subscription.py

from config import REQUIRED_CHANNELS
from telegram import Update
from telegram.ext import ContextTypes

async def is_user_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    يتحقق مما إذا كان المستخدم مشتركًا في جميع القنوات المطلوبة.

    Args:
        update (Update): الكائن Update الوارد من تيليجرام.
        context (ContextTypes.DEFAULT_TYPE): كائن السياق الخاص بالبوت.

    Returns:
        bool: True إذا كان المستخدم مشتركًا في جميع القنوات، False خلاف ذلك.
    """
    user_id = update.effective_user.id

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            # إذا حدث خطأ (مثل عدم وجود البوت في القناة أو معرف القناة خاطئ)، نفترض عدم الاشتراك.
            # في بيئة الإنتاج، قد ترغب في تسجيل هذا الخطأ لمراجعته.
            return False

    return True