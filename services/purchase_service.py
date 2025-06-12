# services/purchase_service.py
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from database.database import get_db # # استيراد get_db للحصول على جلسة
from database.models import Purchase, User, Server # # استيراد نماذج الجداول

logger = logging.getLogger(__name__)

def add_purchase(
    db: Session,
    user_id: int,
    platform: str,
    country: str,
    server_name: str,
    server_id: int,
    price: float,
    fake_number: str,
    status: str = "awaiting_code",
    fake_code: str = None
):
    """
    يضيف عملية شراء جديدة إلى قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم الذي قام بالشراء.
    :param platform: المنصة (مثال: WhatsApp).
    :param country: كود الدولة (مثال: sa).
    :param server_name: اسم السيرفر الذي تم الشراء منه.
    :param server_id: معرف السيرفر من المصدر الخارجي.
    :param price: سعر الشراء.
    :param fake_number: الرقم الوهمي الذي تم شراؤه.
    :param status: حالة الشراء الافتراضية "awaiting_code".
    :param fake_code: الكود الوهمي (اختياري).
    :return: كائن Purchase الجديد.
    """
    purchase = Purchase(
        user_id=user_id,
        platform=platform,
        country=country,
        server_name=server_name,
        server_id=server_id,
        price=price,
        fake_number=fake_number,
        status=status,
        date=datetime.now(),
        fake_code=fake_code
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    logger.info(f"تم إضافة عملية شراء: user_id={user_id}, number={fake_number}.")
    return purchase

def get_user_purchases(db: Session, user_id: int):
    """
    يجلب جميع عمليات الشراء لمستخدم معين.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :return: قائمة بكائنات Purchase.
    """
    return db.query(Purchase).filter(Purchase.user_id == user_id).order_by(Purchase.date.desc()).all()

def get_purchase_by_number_and_server(db: Session, fake_number: str, server_id: int):
    """
    يجلب عملية شراء بناءً على الرقم الوهمي ومعرف السيرفر.
    :param db: جلسة قاعدة البيانات.
    :param fake_number: الرقم الوهمي.
    :param server_id: معرف السيرفر.
    :return: كائن Purchase إذا وُجد، وإلا None.
    """
    return db.query(Purchase).filter(
        Purchase.fake_number == fake_number,
        Purchase.server_id == server_id
    ).first()

def update_purchase_status(db: Session, purchase_id: int, status: str, fake_code: str = None):
    """
    يحدث حالة عملية شراء معينة.
    :param db: جلسة قاعدة البيانات.
    :param purchase_id: معرف عملية الشراء.
    :param status: الحالة الجديدة (مثال: "active", "cancelled").
    :param fake_code: الكود الوهمي إذا كانت الحالة "active".
    :return: كائن Purchase المحدث إذا وُجد، وإلا None.
    """
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase:
        purchase.status = status
        if fake_code:
            purchase.fake_code = fake_code
        db.commit()
        db.refresh(purchase)
        logger.info(f"تم تحديث حالة الشراء {purchase_id} إلى {status}.")
        return purchase
    return None

def get_total_spent_by_user(db: Session, user_id: int) -> float:
    """
    يحسب إجمالي المبلغ الذي أنفقه المستخدم على المشتريات النشطة/قيد الانتظار.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :return: إجمالي المبلغ المنفق.
    """
    # هنا نحسب مجموع الأسعار من المشتريات التي تمت بالفعل
    spent_purchases = db.query(Purchase).filter(Purchase.user_id == user_id, Purchase.status.in_(['active', 'awaiting_code'])).all()
    return sum(p.price for p in spent_purchases)

def get_total_orders_by_user(db: Session, user_id: int) -> int:
    """
    يحسب إجمالي عدد الطلبات التي قام بها المستخدم.
    :param db: جلسة قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :return: إجمالي عدد الطلبات.
    """
    return db.query(Purchase).filter(Purchase.user_id == user_id).count()