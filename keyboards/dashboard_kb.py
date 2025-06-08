from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS



def dashboard_keyboard(user_id=None):
    buttons = [

        # 🥇 القسم الأول: الخدمات الأساسية
        [InlineKeyboardButton("💎 شراء رقم جديد", callback_data="buy_number")],
        [
            InlineKeyboardButton("🎯 عروض الأرقام", callback_data="offers"),
            InlineKeyboardButton("📲 المنصات المتاحة الآن", callback_data="available_platforms")
        ],

        # 💳 القسم الثاني: الرصيد والتحويلات
        [
            InlineKeyboardButton("💳 شحن رصيدي", callback_data="recharge"),
            InlineKeyboardButton("🔁 تحويل رصيد", callback_data="transfer_balance")
        ],
        [
            InlineKeyboardButton("📤 سحب الرصيد", callback_data="withdraw_request")
        ],

        # 🧰 أدوات سريعة
        [
            InlineKeyboardButton("🔎 البحث السريع", callback_data="quick_search"),
            InlineKeyboardButton("⭐️ المفضلة", callback_data="favorites")  # ✅ تم إضافة زر المفضلة هنا
        ],
         [InlineKeyboardButton("🚀 أرقام فورية جاهزة", callback_data="ready_numbers")],

        # 👤 الحساب والدعم
        [
            InlineKeyboardButton("👤 ملفي الشخصي", callback_data="profile")
        ],
        [
            InlineKeyboardButton("❓ الدعم والمساعدة", callback_data="help"),
            InlineKeyboardButton("📢 قناة البوت", url="https://t.me/FakeDigitsPlus")
        ],

        # 🧩 التفاعل والتوسّع
        [
            InlineKeyboardButton("🆓 ربح رصيد مجانًا", callback_data="earn_credit"),
            InlineKeyboardButton("🤝 كن وكيلًا معنا", callback_data="become_agent")
        ],

        # 🌐 اللغة
        [InlineKeyboardButton(" اللغة 🌐 Language", callback_data="change_language")]
    ]

    # ✅ إضافة عناصر خاصة للمشرفين فقط
    if user_id in ADMINS:
        buttons.insert(4, [InlineKeyboardButton("📜 عرض التحويلات السابقة", callback_data="view_transfer_logs")])
        buttons.insert(5, [InlineKeyboardButton("🛠️ إدارة المستخدمين", callback_data="admin_users")])


    return InlineKeyboardMarkup(buttons)
