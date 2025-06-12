# services/favorite_service.py
import logging
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Favorite # استيراد نموذج Favorite

logger = logging.getLogger(__name__)

def add_user_favorite(db: Session, user_id: int, platform: str, country: str, display_text: str):
    """
    يضيف مفضلة جديدة لمستخدم معين.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :param platform: المنصة (مثال: WhatsApp).
    :param country: كود الدولة (مثال: sa).
    :param display_text: النص المعروض للمفضلة (مثال: "🇸🇦 WhatsApp - SA").
    :return: True إذا تمت الإضافة بنجاح، False إذا كانت المفضلة موجودة بالفعل.
    """
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.platform == platform,
        Favorite.country == country
    ).first()
    if existing_favorite:
        logger.info(f"المفضلة موجودة بالفعل للمستخدم {user_id}: {display_text}.")
        return False # موجود بالفعل

    new_favorite = Favorite(
        user_id=user_id,
        platform=platform,
        country=country,
        display_text=display_text
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    logger.info(f"تم إضافة مفضلة للمستخدم {user_id}: {display_text}.")
    return True

def get_favorites_by_user_id(db: Session, user_id: int):
    """
    يجلب جميع مفضلات مستخدم معين.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :return: قائمة بكائنات Favorite.
    """
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()

def delete_user_favorite(db: Session, user_id: int, favorite_id: int):
    """
    يحذف مفضلة لمستخدم معين بناءً على معرف المفضلة.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم للتأكد من الملكية.
    :param favorite_id: معرف المفضلة المراد حذفها (من جدول المفضلة).
    :return: True إذا تم الحذف بنجاح، وإلا False.
    """
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.id == favorite_id
    ).first()
    if favorite:
        db.delete(favorite)
        db.commit()
        logger.info(f"تم حذف المفضلة {favorite_id} للمستخدم {user_id}.")
        return True
    logger.warning(f"محاولة حذف مفضلة غير موجودة أو لا تخص المستخدم {user_id}: favorite_id={favorite_id}.")
    return False