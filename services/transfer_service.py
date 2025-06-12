# services/transfer_service.py
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Transfer # استيراد نموذج Transfer

logger = logging.getLogger(__name__)

def record_transfer(db: Session, from_user_id: int, to_user_id: int, amount: float, fee: float):
    """
    يسجل عملية تحويل رصيد بين مستخدمين في قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :param from_user_id: معرف المستخدم المرسل.
    :param to_user_id: معرف المستخدم المستلم.
    :param amount: المبلغ المحول.
    :param fee: رسوم التحويل.
    :return: كائن Transfer الجديد.
    """
    transfer = Transfer(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        amount=amount,
        fee=fee,
        timestamp=datetime.now()
    )
    db.add(transfer)
    db.commit()
    db.refresh(transfer)
    logger.info(f"تم تسجيل تحويل: من {from_user_id} إلى {to_user_id} بمبلغ {amount} مع رسوم {fee}.")
    return transfer

def get_recent_transfers(db: Session, limit: int = 10):
    """
    يجلب آخر عدد من سجلات التحويلات.
    :param db: جلسة قاعدة البيانات.
    :param limit: الحد الأقصى لعدد التحويلات المراد جلبها.
    :return: قائمة بكائنات Transfer مرتبة تنازلياً حسب الوقت.
    """
    return db.query(Transfer).order_by(Transfer.timestamp.desc()).limit(limit).all()

def delete_all_transfers(db: Session):
    """
    يحذف جميع سجلات التحويلات من قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :return: عدد السجلات التي تم حذفها.
    """
    num_deleted = db.query(Transfer).delete()
    db.commit()
    logger.info(f"تم حذف {num_deleted} سجل تحويل.")
    return num_deleted