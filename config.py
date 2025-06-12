import os
from dotenv import load_dotenv

load_dotenv() # تحميل متغيرات البيئة من ملف .env

# ###########################################
# إعدادات البوت (يتم تحميلها من متغيرات البيئة لسهولة الإدارة والأمان)
# ###########################################

BOT_TOKEN = os.getenv("BOT_TOKEN") # توكن البوت
# قنوات الاشتراك المطلوبة (يمكن أن تكون قائمة مفصولة بفواصل في .env)
REQUIRED_CHANNELS = os.getenv("REQUIRED_CHANNELS", "").split(',')
# تحويل معرفات المشرفين من نص (من .env) إلى قائمة أرقام صحيحة
ADMINS_STR = os.getenv("ADMINS", "")
ADMINS = [int(admin_id.strip()) for admin_id in ADMINS_STR.split(',') if admin_id.strip()] if ADMINS_STR else []

# ############## إعدادات اللغة ##############
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ar") # اللغة الافتراضية للبوت
MESSAGES_PATH = os.getenv("MESSAGES_PATH", "messages") # مسار مجلد ملفات اللغة

# ###########################################
# إعدادات قاعدة البيانات
# ###########################################
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/bot.db") # مسار ملف قاعدة البيانات SQLite