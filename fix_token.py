# fix_token.py - إصلاح مشاكل التوكن

import asyncio
import re
from telegram import Bot
from telegram.error import TelegramError

def validate_token_format(token):
    """التحقق من تنسيق التوكن"""
    # تنسيق التوكن: 123456789:ABCDefGhIJKlmnopQRStuVWXyz
    pattern = r'^\d{8,10}:[A-Za-z0-9_-]{35}$'
    return re.match(pattern, token) is not None

async def test_token(token):
    """اختبار التوكن مع البوت"""
    try:
        bot = Bot(token)
        me = await bot.get_me()
        
        return {
            'valid': True,
            'bot_id': me.id,
            'bot_name': me.first_name,
            'bot_username': me.username,
            'can_join_groups': me.can_join_groups,
            'can_read_all_group_messages': me.can_read_all_group_messages,
            'supports_inline_queries': me.supports_inline_queries
        }
        
    except TelegramError as e:
        return {
            'valid': False,
            'error': str(e),
            'error_type': type(e).__name__
        }

def get_token_from_config():
    """قراءة التوكن من ملف config.py"""
    try:
        from config import BOT_TOKEN
        return BOT_TOKEN
    except ImportError:
        return None
    except AttributeError:
        return None

def update_config_token(new_token):
    """تحديث التوكن في ملف config.py"""
    try:
        # قراءة محتوى الملف
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # تحديث التوكن
        new_content = re.sub(
            r'BOT_TOKEN\s*=\s*["\'][^"\']*["\']',
            f'BOT_TOKEN = "{new_token}"',
            content
        )
        
        # كتابة المحتوى المحدث
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث config.py: {e}")
        return False

async def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔧 إصلاح مشاكل توكن البوت")
    print("=" * 60)
    
    # 1. قراءة التوكن الحالي
    current_token = get_token_from_config()
    
    if current_token and current_token != "YOUR_BOT_TOKEN_HERE":
        print(f"📱 التوكن الحالي: {current_token[:10]}...{current_token[-10:]}")
        
        # فحص تنسيق التوكن
        if validate_token_format(current_token):
            print("✅ تنسيق التوكن صحيح")
            
            # اختبار التوكن
            print("🧪 اختبار التوكن...")
            result = await test_token(current_token)
            
            if result['valid']:
                print("✅ التوكن صالح ويعمل!")
                print(f"🤖 اسم البوت: {result['bot_name']}")
                print(f"👤 معرف البوت: @{result['bot_username']}")
                print(f"🆔 معرف رقمي: {result['bot_id']}")
                print("\n🎉 البوت جاهز للتشغيل!")
                return True
            else:
                print(f"❌ التوكن غير صالح: {result['error']}")
                
                if "Unauthorized" in result['error']:
                    print("\n💡 أسباب محتملة:")
                    print("1. التوكن خاطئ أو منتهي الصلاحية")
                    print("2. البوت معطل في @BotFather")
                    print("3. تم حذف البوت")
                
        else:
            print("❌ تنسيق التوكن خاطئ")
            print("💡 التنسيق الصحيح: 123456789:ABCDefGhIJKlmnopQRStuVWXyz")
    
    else:
        print("❌ لم يتم العثور على توكن صالح")
    
    # 2. طلب توكن جديد
    print("\n" + "=" * 60)
    print("🔑 إدخال توكن جديد")
    print("=" * 60)
    
    print("📋 خطوات الحصول على التوكن:")
    print("1. ابحث عن @BotFather في تيليجرام")
    print("2. أرسل /newbot")
    print("3. اختر اسماً للبوت")
    print("4. اختر username للبوت (يجب أن ينتهي بـ bot)")
    print("5. انسخ التوكن الذي يرسله لك")
    print()
    
    # طلب التوكن الجديد
    while True:
        new_token = input("🔑 أدخل التوكن الجديد (أو 'exit' للخروج): ").strip()
        
        if new_token.lower() == 'exit':
            print("👋 تم إلغاء العملية")
            return False
        
        if not new_token:
            print("❌ يجب إدخال توكن!")
            continue
        
        # فحص التنسيق
        if not validate_token_format(new_token):
            print("❌ تنسيق التوكن خاطئ!")
            print("💡 التنسيق الصحيح: 123456789:ABCDefGhIJKlmnopQRStuVWXyz")
            continue
        
        # اختبار التوكن
        print("🧪 اختبار التوكن الجديد...")
        result = await test_token(new_token)
        
        if result['valid']:
            print("✅ التوكن الجديد صالح!")
            print(f"🤖 اسم البوت: {result['bot_name']}")
            print(f"👤 معرف البوت: @{result['bot_username']}")
            
            # تحديث config.py
            if update_config_token(new_token):
                print("✅ تم تحديث config.py بنجاح!")
                print("\n🎉 البوت جاهز للتشغيل!")
                print("🚀 شغّل: python main.py")
                return True
            else:
                print("❌ فشل في تحديث config.py")
                print(f"💡 يمكنك تحديثه يدوياً: BOT_TOKEN = \"{new_token}\"")
                return False
        else:
            print(f"❌ التوكن غير صالح: {result['error']}")
            print("🔄 جرب مرة أخرى...")

def check_botfather_status():
    """نصائح لإصلاح مشاكل BotFather"""
    print("\n" + "=" * 60)
    print("🛠️ نصائح إصلاح مشاكل BotFather")
    print("=" * 60)
    
    tips = [
        "1. تأكد من أن البوت مُفعل في @BotFather",
        "2. أرسل /mybots إلى @BotFather لرؤية بوتاتك",
        "3. اختر البوت واضغط 'Edit Bot'",
        "4. تأكد من أن البوت ليس معطلاً",
        "5. إذا لزم الأمر، احذف البوت وأنشئ واحداً جديداً",
        "6. تأكد من عدم مشاركة التوكن مع أحد",
        "7. إذا تم اختراق التوكن، قم بتجديده من @BotFather"
    ]
    
    for tip in tips:
        print(tip)

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        if not result:
            check_botfather_status()
    except KeyboardInterrupt:
        print("\n👋 تم إلغاء العملية")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")