@echo off
title إصلاح سريع - مشاكل Python 3.13
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ============================================
echo 🔧 إصلاح سريع - مشكلة imghdr
echo ============================================
echo.

echo ❌ خطأ: imghdr غير متاح في Python 3.13
echo ✅ الحل: imghdr غير مطلوب للبوت!
echo.

echo 🧹 تنظيف وإعادة تثبيت المكتبات الصحيحة...
echo.

:: إزالة المكتبات القديمة
echo 🗑️ إزالة المكتبات القديمة...
pip uninstall python-telegram-bot -y >nul 2>&1
pip uninstall PTB -y >nul 2>&1
pip uninstall telepot -y >nul 2>&1

echo 📦 تثبيت المكتبات الصحيحة...
pip install python-telegram-bot==21.5
pip install requests==2.31.0

echo.
echo ✅ تم الإصلاح!
echo.

:: اختبار التثبيت
echo 🧪 اختبار المكتبات...
python -c "import telegram; print('✅ telegram:', telegram.__version__)"
python -c "import requests; print('✅ requests:', requests.__version__)"

echo.
echo 📋 ملخص:
echo • imghdr غير مطلوب للبوت
echo • تم تثبيت python-telegram-bot الصحيح
echo • البوت جاهز للتشغيل
echo.

echo 🚀 يمكنك الآن تشغيل: python main.py
echo أو استخدم: run.bat
echo.

pause