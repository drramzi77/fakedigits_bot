# keyboards/dashboard_kb.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMINS
from utils.i18n import get_messages  # استيراد دالة جلب النصوص

def dashboard_keyboard(user_id=None, lang_code="ar"):
    """
    ينشئ لوحة التحكم الرئيسية للبوت مع جميع الخيارات المتاحة للمستخدمين.
    يتضمن أزرارًا إضافية خاصة بالمشرفين.

    Args:
        user_id (int, optional): معرف المستخدم. يُستخدم لتحديد ما إذا كان المستخدم مشرفاً.
                                         الافتراضي هو None.
        lang_code (str, optional): كود اللغة. الافتراضي هو "ar".

    Returns:
        InlineKeyboardMarkup: لوحة التحكم الرئيسية المضمّنة.
    """
    messages = get_messages(lang_code)

    buttons = [
        # 🥇 القسم الأول: الخدمات الأساسية
        [InlineKeyboardButton(messages["buy_number_button"], callback_data="buy_number")],
        [
            InlineKeyboardButton(messages["offers_button"], callback_data="offers"),
            InlineKeyboardButton(messages["available_platforms"], callback_data="available_platforms"),
        ],
        # 💳 القسم الثاني: الرصيد والتحويلات
        [
            InlineKeyboardButton(messages["recharge_balance_button"], callback_data="recharge"),
            InlineKeyboardButton(messages["transfer_credit_button"], callback_data="transfer_balance"),
        ],
        [InlineKeyboardButton(messages["withdraw_balance_button"], callback_data="withdraw_request")],
        # 🧰 أدوات سريعة
        [
            InlineKeyboardButton(messages["quick_search"], callback_data="quick_search"),
            InlineKeyboardButton(messages["favorites_button"], callback_data="favorites"),
        ],
        [InlineKeyboardButton(messages["ready_numbers"], callback_data="ready_numbers")],
        # 👤 الحساب والدعم
        [InlineKeyboardButton(messages["profile_button"], callback_data="profile")],
        [
            InlineKeyboardButton(messages["help_button"], callback_data="help"),
            InlineKeyboardButton(messages["channel_button"], url="https://t.me/FakeDigitsPlus"),
        ],
        # 🧩 التفاعل والتوسّع
        [
            InlineKeyboardButton(messages["earn_credit_button"], callback_data="earn_credit"),
            InlineKeyboardButton(messages["become_agent_button"], callback_data="become_agent"),
        ],
        # 🌐 اللغة
        [InlineKeyboardButton(messages["language_button"], callback_data="change_language")],
    ]

    # ✅ إضافة عناصر خاصة للمشرفين فقط
    if user_id in ADMINS:
        buttons.insert(4, [InlineKeyboardButton(messages["view_transfer_logs"], callback_data="view_transfer_logs")])
        buttons.insert(5, [InlineKeyboardButton(messages["admin_users"], callback_data="admin_users")])

    return InlineKeyboardMarkup(buttons)