from telegram import Update
from telegram.ext import ContextTypes
from utils.balance import set_user_balance, get_user_balance

# أمر إضافة رصيد للمستخدم نفسه
async def add_balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    set_user_balance(user_id, 100)
    balance = get_user_balance(user_id)
    await update.message.reply_text(f"✅ تم تحديث رصيدك إلى {balance} ر.س بنجاح.")
