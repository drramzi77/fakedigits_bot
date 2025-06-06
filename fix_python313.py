# fix_python313.py - إصلاح مشاكل التوافق مع Python 3.13

import sys

def check_removed_modules():
    """فحص الmodules المحذوفة في Python 3.13"""
    removed_modules = [
        'imghdr',    # تم إزالته في Python 3.13
        'sndhdr',    # تم إزالته في Python 3.13
        'colorsys',  # تم تعديله
        'chunk',     # تم إزالته
        'telnetlib', # تم إزالته
        'uu',        # تم إزالته
        'xdrlib',    # تم إزالته
    ]
    
    print("🔍 فحص الmodules المحذوفة في Python 3.13:")
    
    available = []
    removed = []
    
    for module in removed_modules:
        try:
            __import__(module)
            available.append(module)
            print(f"✅ {module} - متاح")
        except ImportError:
            removed.append(module)
            print(f"❌ {module} - محذوف/غير متاح")
    
    if removed:
        print(f"\n⚠️ تم إزالة {len(removed)} modules في Python 3.13")
        print("💡 هذا طبيعي ولا يؤثر على البوت")
    
    return removed

def install_alternatives():
    """تثبيت بدائل للmodules المحذوفة إذا لزم الأمر"""
    print("\n📦 بدائل للmodules المحذوفة:")
    
    alternatives = {
        'imghdr': 'pillow',  # Pillow بديل أفضل
        'sndhdr': 'soundfile',
        'telnetlib': 'telnetlib3'
    }
    
    for old_module, new_package in alternatives.items():
        print(f"• {old_module} → pip install {new_package}")
    
    print("\n💡 البوت لا يحتاج أي من هذه المكتبات!")

def check_bot_requirements():
    """فحص متطلبات البوت فقط"""
    print("\n🤖 فحص متطلبات البوت:")
    
    required = {
        'telegram': 'python-telegram-bot==21.5',
        'requests': 'requests==2.31.0'
    }
    
    all_good = True
    
    for module, package in required.items():
        try:
            imported = __import__(module)
            version = getattr(imported, '__version__', 'غير محدد')
            print(f"✅ {module} {version}")
        except ImportError:
            print(f"❌ {module} غير مثبت - قم بتشغيل: pip install {package}")
            all_good = False
    
    return all_good

def clean_environment():
    """تنظيف البيئة من المكتبات غير المطلوبة"""
    print("\n🧹 تنظيف البيئة:")
    
    # قائمة المكتبات التي قد تسبب تعارض
    problematic_packages = [
        'python-telegram-bot-raw',
        'python-telegram-bot-raw[callback-data]',
        'PTB',
        'telepot',
        'aiogram',
    ]
    
    print("💡 إذا كان لديك مكتبات telegram أخرى، احذفها:")
    for package in problematic_packages:
        print(f"   pip uninstall {package}")

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔧 إصلاح مشاكل Python 3.13")
    print("=" * 60)
    
    print(f"🐍 Python {sys.version}")
    
    # فحص الmodules المحذوفة
    removed = check_removed_modules()
    
    # عرض البدائل
    if removed:
        install_alternatives()
    
    # فحص متطلبات البوت
    bot_ready = check_bot_requirements()
    
    # تنظيف البيئة
    clean_environment()
    
    print("\n" + "=" * 60)
    print("📋 ملخص:")
    
    if bot_ready:
        print("✅ البوت جاهز للتشغيل!")
        print("🚀 شغّل: python main.py")
    else:
        print("❌ يجب تثبيت المتطلبات أولاً:")
        print("📦 شغّل: pip install -r requirements.txt")
    
    print("\n💡 تذكر: imghdr غير مطلوب للبوت!")
    print("=" * 60)

if __name__ == "__main__":
    main()