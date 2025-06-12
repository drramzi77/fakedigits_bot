# database/database.py
import os
import json
import logging
from datetime import datetime
import re # هذا السطر يجب أن يكون موجوداً

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base, User, Purchase, Server, Favorite, Transfer

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    ينشئ جميع الجداول المعرفة في models.py إذا لم تكن موجودة.
    """
    Base.metadata.create_all(engine)
    logger.info("تم إنشاء جداول قاعدة البيانات بنجاح أو كانت موجودة بالفعل.")

def get_db():
    """
    دالة مساعدة للحصول على جلسة قاعدة بيانات.
    تُستخدم مع 'with' لضمان إغلاق الجلسة.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_data_from_json():
    """
    يقوم بتحميل البيانات الأولية من ملفات JSON إلى قاعدة البيانات
    إذا كانت قاعدة البيانات فارغة (يُنفذ مرة واحدة فقط عند التشغيل الأول).
    """
    for db in get_db():
        try:
            # التحقق مما إذا كان جدول المستخدمين فارغًا
            if db.query(User).count() == 0:
                logger.info("قاعدة بيانات المستخدمين فارغة، جاري استيراد البيانات من ملفات JSON القديمة.")

                # استيراد المستخدمين
                users_json_path = os.path.join("data", "users.json")
                if os.path.exists(users_json_path):
                    with open(users_json_path, "r", encoding="utf-8") as f:
                        users_data = json.load(f)
                        for uid, user_info in users_data.items():
                            user = User(
                                id=user_info.get("id"),
                                first_name=user_info.get("first_name"),
                                last_name=user_info.get("last_name"),
                                username=user_info.get("username"),
                                language_code=user_info.get("language_code"),
                                created_at=datetime.strptime(user_info["created_at"], "%Y-%m-%d %H:%M:%S") if "created_at" in user_info and user_info["created_at"] else datetime.now(),
                                balance=user_info.get("balance"),
                                banned=user_info.get("banned")
                            )
                            db.add(user)
                        db.commit()
                    logger.info(f"تم استيراد {len(users_data)} مستخدم من users.json.")
                else:
                    logger.warning(f"ملف {users_json_path} غير موجود. لن يتم استيراد بيانات المستخدمين.")

                # استيراد المشتريات
                purchases_json_path = os.path.join("data", "purchases.json")
                if os.path.exists(purchases_json_path):
                    with open(purchases_json_path, "r", encoding="utf-8") as f:
                        purchases_data = json.load(f)
                        for user_id_str, user_purchases in purchases_data.items():
                            for p_info in user_purchases:
                                purchase = Purchase(
                                    user_id=int(user_id_str),
                                    platform=p_info.get("platform"),
                                    country=p_info.get("country"),
                                    server_name=p_info.get("server_name"),
                                    server_id=p_info.get("server_id"),
                                    price=p_info.get("price"),
                                    fake_number=p_info.get("fake_number"),
                                    status=p_info.get("status"),
                                    date=datetime.strptime(p_info["date"], "%Y-%m-%d %H:%M:%S") if "date" in p_info and p_info["date"] else datetime.now(),
                                    fake_code=p_info.get("fake_code")
                                )
                                db.add(purchase)
                        db.commit()
                    logger.info(f"تم استيراد {sum(len(v) for v in purchases_data.values())} عملية شراء من purchases.json.")
                else:
                    logger.warning(f"ملف {purchases_json_path} غير موجود. لن يتم استيراد بيانات المشتريات.")

                # استيراد السيرفرات
                servers_json_path = os.path.join("data", "servers.json")
                if os.path.exists(servers_json_path):
                    with open(servers_json_path, "r", encoding="utf-8") as f:
                        servers_data = json.load(f)
                        for entry in servers_data:
                            platform = entry.get("platform")
                            country = entry.get("country")
                            for s_info in entry.get("servers", []):
                                server = Server(
                                    platform=platform,
                                    country=country,
                                    server_id=s_info.get("id"),
                                    server_name=s_info.get("name"),
                                    price=s_info.get("price"),
                                    quantity=s_info.get("quantity")
                                )
                                db.add(server)
                        db.commit()
                    logger.info(f"تم استيراد بيانات السيرفرات من servers.json.")
                else:
                    logger.warning(f"ملف {servers_json_path} غير موجود. لن يتم استيراد بيانات السيرفرات.")

                # استيراد المفضلة
                favorites_json_path = os.path.join("data", "favorites.json")
                if os.path.exists(favorites_json_path):
                    with open(favorites_json_path, "r", encoding="utf-8") as f:
                        favorites_data = json.load(f)
                        for user_id_str, items in favorites_data.items():
                            for item_text in items:
                                platform = "Unknown"
                                country_code = "xx"
                                if "WhatsApp" in item_text:
                                    platform = "WhatsApp"
                                elif "Telegram" in item_text:
                                    platform = "Telegram"
                                
                                # البحث عن كود الدولة (حرفين بعد " - ")
                                match = re.search(r'- ([A-Za-z]{2})$', item_text)
                                if match:
                                    country_code = match.group(1).lower()

                                favorite = Favorite(
                                    user_id=int(user_id_str),
                                    platform=platform,
                                    country=country_code,
                                    display_text=item_text
                                )
                                db.add(favorite)
                        db.commit()
                    logger.info(f"تم استيراد بيانات المفضلة من favorites.json.")
                else:
                    logger.warning(f"ملف {favorites_json_path} غير موجود. لن يتم استيراد بيانات المفضلة.")

                # استيراد التحويلات
                transfers_json_path = os.path.join("data", "transfers.json")
                if os.path.exists(transfers_json_path):
                    with open(transfers_json_path, "r", encoding="utf-8") as f:
                        transfers_data = json.load(f)
                        for t_info in transfers_data:
                            transfer = Transfer(
                                from_user_id=t_info.get("from"),
                                to_user_id=t_info.get("to"),
                                amount=t_info.get("amount"),
                                fee=t_info.get("fee"),
                                timestamp=datetime.strptime(t_info["timestamp"], "%Y-%m-%d %H:%M:%S") if "timestamp" in t_info and t_info["timestamp"] else datetime.now()
                            )
                            db.add(transfer)
                        db.commit()
                    logger.info(f"تم استيراد بيانات التحويلات من transfers.json.")
                else:
                    logger.warning(f"ملف {transfers_json_path} غير موجود. لن يتم استيراد بيانات التحويلات.")

            else:
                logger.info("قاعدة البيانات تحتوي على بيانات بالفعل. تخطي عملية الاستيراد من JSON.")

        except Exception as e:
            db.rollback()
            logger.error(f"خطأ أثناء استيراد البيانات من JSON إلى قاعدة البيانات: {e}", exc_info=True)