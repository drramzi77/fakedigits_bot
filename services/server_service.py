# services/server_service.py
import logging
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Server # استيراد نموذج Server
from sqlalchemy import func # استيراد func لاستخدام دوال SQL التجميعية

logger = logging.getLogger(__name__)

def get_all_servers(db: Session):
    """
    يجلب جميع السيرفرات من قاعدة البيانات.
    :param db: جلسة قاعدة البيانات.
    :return: قائمة بكائنات Server.
    """
    return db.query(Server).all()

def get_servers_by_platform_and_country(db: Session, platform: str, country: str):
    """
    يجلب السيرفرات المتاحة لمنصة ودولة معينة.
    :param db: جلسة قاعدة البيانات.
    :param platform: اسم المنصة (مثال: "WhatsApp").
    :param country: كود الدولة (مثال: "sa").
    :return: قائمة بكائنات Server التي تطابق المعايير ولديها كمية > 0.
    """
    return db.query(Server).filter(
        Server.platform == platform,
        Server.country == country,
        Server.quantity > 0 # فلترة الأرقام المتاحة
    ).all()

def get_server_by_id(db: Session, platform: str, country: str, server_id: int):
    """
    يجلب سيرفراً واحداً بناءً على المنصة، الدولة، ومعرف السيرفر الخارجي (server_id).
    :param db: جلسة قاعدة البيانات.
    :param platform: اسم المنصة.
    :param country: كود الدولة.
    :param server_id: معرف السيرفر من المصدر الخارجي (JSON الأصلي).
    :return: كائن Server إذا وُجد، وإلا None.
    """
    return db.query(Server).filter(
        Server.platform == platform,
        Server.country == country,
        Server.server_id == server_id
    ).first()

def update_server_quantity(db: Session, platform: str, country: str, server_id: int, change: int):
    """
    يحدث كمية الأرقام المتاحة لسيرفر معين.
    :param db: جلسة قاعدة البيانات.
    :param platform: اسم المنصة.
    :param country: كود الدولة.
    :param server_id: معرف السيرفر الخارجي.
    :param change: مقدار التغيير في الكمية (مثال: -1 للشراء، +1 للإلغاء).
    :return: كائن Server المحدث إذا وُجد، وإلا None.
    """
    server = get_server_by_id(db, platform, country, server_id)
    if server:
        server.quantity += change
        db.commit()
        db.refresh(server)
        logger.info(f"تم تحديث كمية السيرفر {server.server_name} في {country} لـ {platform}. الكمية الجديدة: {server.quantity}.")
        return server
    logger.warning(f"لم يتم العثور على السيرفر لتحديث الكمية: platform={platform}, country={country}, server_id={server_id}.")
    return None

def get_platforms_with_available_numbers(db: Session):
    """
    يجلب جميع المنصات التي تحتوي على أرقام متاحة.
    :param db: جلسة قاعدة البيانات.
    :return: قائمة بأسماء المنصات الفريدة.
    """
    platforms = db.query(Server.platform).filter(Server.quantity > 0).distinct().all()
    return [p[0] for p in platforms]

def get_countries_with_available_numbers_for_platform(db: Session, platform: str):
    """
    يجلب أكواد الدول التي تحتوي على أرقام متاحة لمنصة معينة.
    :param db: جلسة قاعدة البيانات.
    :param platform: اسم المنصة.
    :return: قائمة بأكواد الدول الفريدة التي لديها كمية > 0.
    """
    countries_with_quantity = db.query(Server.country, func.sum(Server.quantity)).filter(
        Server.platform == platform,
        Server.quantity > 0
    ).group_by(Server.country).all()
    # نرجع فقط أكواد الدول التي مجموع كمياتها أكبر من 0
    return [country_code for country_code, total_quantity in countries_with_quantity if total_quantity > 0]

def get_cheapest_server_for_platform_country(db: Session, platform: str, country_code: str):
    """
    يجلب أرخص سيرفر متاح لمنصة ودولة معينة.
    :param db: جلسة قاعدة البيانات.
    :param platform: اسم المنصة.
    :param country_code: كود الدولة.
    :return: أرخص كائن Server متاح، وإلا None.
    """
    return db.query(Server).filter(
        Server.platform == platform,
        Server.country == country_code,
        Server.quantity > 0
    ).order_by(Server.price.asc()).first()

def get_all_available_offers(db: Session):
    """
    يجلب جميع السيرفرات المتاحة مرتبة حسب السعر.
    :param db: جلسة قاعدة البيانات.
    :return: قائمة بكائنات Server المتاحة.
    """
    return db.query(Server).filter(Server.quantity > 0).order_by(Server.price.asc()).all()