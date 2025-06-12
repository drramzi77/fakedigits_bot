# services/user_service.py
import logging
from datetime import datetime
from sqlalchemy.orm import Session # # استيراد Session للتعامل مع قاعدة البيانات
from database.database import get_db # # استيراد get_db للحصول على جلسة قاعدة بيانات
from database.models import User # # استيراد نموذج User

logger = logging.getLogger(__name__)

def get_user(db: Session, user_id: int):
    """
    يجلب معلومات المستخدم من قاعدة البيانات بواسطة معرف المستخدم.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :return: كائن User إذا وُجد، وإلا None.
    """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_id: int, user_info: dict):
    """
    ينشئ مستخدمًا جديدًا في قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :param user_info: قاموس يحتوي على معلومات المستخدم (مثل الاسم الأول، اسم المستخدم).
    :return: كائن User الجديد.
    """
    new_user = User(
        id=user_id,
        first_name=user_info.get("first_name", "N/A"), # استخدام "N/A" كقيمة افتراضية إذا لم يتوفر الاسم الأول
        last_name=user_info.get("last_name", ""),
        username=user_info.get("username", ""),
        language_code=user_info.get("language_code", "ar"),
        created_at=datetime.now(),
        balance=0.0,
        banned=False
    )
    db.add(new_user)
    db.commit() # حفظ التغييرات في قاعدة البيانات
    db.refresh(new_user) # تحديث الكائن ليعكس أي قيم تم إنشاؤها في قاعدة البيانات (مثل الـ ID التلقائي إذا كان موجوداً)
    return new_user

def update_user(db: Session, user_id: int, **kwargs):
    """
    يقوم بتحديث معلومات مستخدم موجود في قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم المراد تحديثه.
    :param kwargs: قاموس من المفتاح=قيمة يمثل الأعمدة المراد تحديثها (مثال: balance=100.0, banned=True).
    :return: كائن User المحدث إذا وُجد، وإلا None.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value) # تعيين قيمة الخاصية
        db.commit() # حفظ التغييرات
        db.refresh(user) # تحديث الكائن
        return user
    return None

def ensure_user_exists(user_id: int, user_info: dict):
    """
    يتأكد من وجود المستخدم في قاعدة البيانات، ويضيفه إذا كان جديداً.
    يقوم بتحديث معلومات المستخدم الحالية (الاسم، اليوزرنيم) إذا تغيرت.
    هذه الدالة تستخدم get_db لتوفير جلسة، مما يجعلها قابلة للاستدعاء مباشرة.
    :param user_id: معرف المستخدم.
    :param user_info: قاموس يحتوي على معلومات المستخدم من Telegram API.
    """
    for db in get_db(): # # استخدام get_db للحصول على جلسة، وتُغلق تلقائياً
        user = get_user(db, user_id)
        if not user:
            user = create_user(db, user_id, user_info)
            logger.info(f"تم تسجيل مستخدم جديد: {user_id} ({user_info.get('username')}).")
        else:
            updated = False
            # تحديث حقول المستخدم إذا تغيرت قيمتها
            if user.first_name != user_info.get("first_name", "N/A"):
                user.first_name = user_info.get("first_name", "N/A")
                updated = True
            if user.last_name != user_info.get("last_name", ""):
                user.last_name = user_info.get("last_name", "")
                updated = True
            if user.username != user_info.get("username", ""):
                user.username = user_info.get("username", "")
                updated = True
            if user.language_code != user_info.get("language_code", "ar"):
                user.language_code = user_info.get("language_code", "ar")
                updated = True
            
            if updated:
                db.commit() # حفظ التغييرات إذا حدث تحديث
                db.refresh(user)
                logger.info(f"تم تحديث معلومات المستخدم {user_id}.")

def get_all_users_data(db: Session):
    """
    يجلب جميع المستخدمين من قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :return: قائمة بكائنات User.
    """
    return db.query(User).all()

def delete_user(db: Session, user_id: int):
    """
    يحذف مستخدمًا من قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم المراد حذفه.
    :return: True إذا تم الحذف بنجاح، وإلا False.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        logger.info(f"تم حذف المستخدم {user_id} من قاعدة البيانات.")
        return True
    logger.warning(f"محاولة حذف مستخدم غير موجود: {user_id}.")
    return False