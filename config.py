import os
from dotenv import load_dotenv

load_dotenv() # تحميل متغيرات البيئة من ملف .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
REQUIRED_CHANNELS = [
    "@FakeDigitsPlus",     # قم بتغييرها إلى قنواتك الحقيقية
]

ADMINS = [780028688]  # قائمة الـ user_id للمشرفين