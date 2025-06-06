# fix_encoding.py - إصلاح مشاكل الترميز في Windows

import os
import sys
import locale

def fix_console_encoding():
    """إصلاح ترميز وحدة التحكم"""
    try:
        # تعيين الترميز إلى UTF-8
        if sys.platform.startswith('win'):
            os.system('chcp 65001 >nul')
        
        # تعيين متغيرات البيئة
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        print("✅ تم إصلاح ترميز وحدة التحكم")
        return True
    except Exception as e:
        print(f"❌ خطأ في إصلاح الترميز: {e}")
        return False

def check_system_encoding():
    """فحص إعدادات الترميز"""
    print("🔍 فحص إعدادات الترميز:")
    print(f"   - إصدار Python: {sys.version}")
    print(f"   - نظام التشغيل: {sys.platform}")
    print(f"   - الترميز المفضل: {locale.getpreferredencoding()}")
    print(f"   - ترميز stdout: {sys.stdout.encoding}")
    print(f"   - ترميز stdin: {sys.stdin.encoding}")
    
    # اختبار الأحرف العربية
    try:
        test_text = "مرحباً بكم في بوت الأرقام المؤقتة 🤖"
        print(f"   - اختبار العربية: {test_text}")
        return True
    except UnicodeEncodeError:
        print("   - ❌ مشكلة في ترميز الأحرف العربية")
        return False

def create_environment_file():
    """إنشاء ملف متغيرات البيئة"""
    env_content = """# متغيرات البيئة للبوت
PYTHONIOENCODING=utf-8
PYTHONLEGACYWINDOWSSTDIO=utf-8
PYTHONUTF8=1
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ تم إنشاء ملف .env")
    except Exception as e:
        print(f"❌ خطأ في إنشاء ملف .env: {e}")

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🔧 إصلاح مشاكل الترميز")
    print("=" * 50)
    
    # فحص النظام
    if not check_system_encoding():
        print("\n⚠️ تم اكتشاف مشاكل في الترميز")
        
        # إصلاح وحدة التحكم
        fix_console_encoding()
        
        # إنشاء ملف البيئة
        create_environment_file()
        
        print("\n💡 نصائح إضافية:")
        print("1. أعد تشغيل وحدة التحكم")
        print("2. استخدم Windows Terminal بدلاً من cmd")
        print("3. تأكد من أن ترميز الملفات UTF-8")
    else:
        print("\n✅ لا توجد مشاكل في الترميز")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()