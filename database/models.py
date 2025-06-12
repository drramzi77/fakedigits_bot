# database/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# تعريف Base لإنشاء الكلاسات الديكلاريتيف
# هذا هو الأساس الذي ستعتمد عليه جميع جداولك
Base = declarative_base()

class User(Base):
    __tablename__ = 'users' # اسم الجدول في قاعدة البيانات

    id = Column(Integer, primary_key=True, index=True, autoincrement=False) # معرف المستخدم، وهو مفتاح أساسي ولا يزيد تلقائياً لأنه معرف تيليجرام
    first_name = Column(String) # الاسم الأول للمستخدم
    last_name = Column(String, nullable=True) # اسم العائلة (يمكن أن يكون فارغاً)
    username = Column(String, nullable=True) # اسم المستخدم في تيليجرام (يمكن أن يكون فارغاً)
    language_code = Column(String, default="ar") # كود اللغة المفضلة للمستخدم
    created_at = Column(DateTime, default=datetime.now) # تاريخ ووقت إنشاء الحساب
    balance = Column(Float, default=0.0) # رصيد المستخدم
    banned = Column(Boolean, default=False) # هل المستخدم محظور؟

    # علاقات (Relationships) مع جداول أخرى
    purchases = relationship("Purchase", back_populates="buyer")
    favorites = relationship("Favorite", back_populates="user")
    transfers_sent = relationship("Transfer", foreign_keys='[Transfer.from_user_id]', back_populates="sender")
    transfers_received = relationship("Transfer", foreign_keys='[Transfer.to_user_id]', back_populates="receiver")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', balance={self.balance})>"

class Purchase(Base):
    __tablename__ = 'purchases' # اسم الجدول

    id = Column(Integer, primary_key=True, index=True) # معرف الشراء، مفتاح أساسي ويزيد تلقائياً
    user_id = Column(Integer, ForeignKey('users.id')) # مفتاح خارجي يربط بالشراء بالمستخدم
    platform = Column(String) # مثال: WhatsApp, Telegram
    country = Column(String) # كود الدولة، مثال: sa, eg
    server_name = Column(String) # اسم السيرفر (مثال: Server 1)
    server_id = Column(Integer) # ID السيرفر الحقيقي (من API أو ملف JSON الأصلي)
    price = Column(Float) # سعر الشراء
    fake_number = Column(String) # الرقم الوهمي الذي تم شراؤه
    status = Column(String, default="awaiting_code") # حالة الشراء (awaiting_code, active, cancelled)
    date = Column(DateTime, default=datetime.now) # تاريخ ووقت الشراء
    fake_code = Column(String, nullable=True) # الكود الذي تم إرساله للرقم (يمكن أن يكون فارغاً في البداية)

    # علاقة (Relationship)
    buyer = relationship("User", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase(id={self.id}, user_id={self.user_id}, number='{self.fake_number}')>"

class Server(Base):
    __tablename__ = 'servers' # اسم الجدول

    id = Column(Integer, primary_key=True, index=True) # معرف السيرفر (خاص بهذا الجدول، يزيد تلقائياً)
    platform = Column(String) # المنصة (مثال: WhatsApp)
    country = Column(String) # كود الدولة (مثال: sa)
    server_id = Column(Integer) # معرف السيرفر من المصدر الخارجي (API أو JSON)
    server_name = Column(String) # اسم السيرفر
    price = Column(Float) # سعر السيرفر
    quantity = Column(Integer) # الكمية المتاحة من الأرقام في هذا السيرفر

    def __repr__(self):
        return f"<Server(platform='{self.platform}', country='{self.country}', server_id={self.server_id}, name='{self.server_name}')>"

class Favorite(Base):
    __tablename__ = 'favorites' # اسم الجدول

    id = Column(Integer, primary_key=True, index=True) # معرف المفضلة (يزيد تلقائياً)
    user_id = Column(Integer, ForeignKey('users.id')) # مفتاح خارجي يربط المفضلة بالمستخدم
    platform = Column(String) # المنصة المفضلة
    country = Column(String) # الدولة المفضلة
    display_text = Column(String) # النص الذي يتم عرضه للمفضلة (مثال: "🇸🇦 WhatsApp - SA")

    # علاقة (Relationship)
    user = relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, text='{self.display_text}')>"

class Transfer(Base):
    __tablename__ = 'transfers' # اسم الجدول

    id = Column(Integer, primary_key=True, index=True) # معرف التحويل (يزيد تلقائياً)
    from_user_id = Column(Integer, ForeignKey('users.id')) # مفتاح خارجي: معرف المستخدم المرسل
    to_user_id = Column(Integer, ForeignKey('users.id')) # مفتاح خارجي: معرف المستخدم المستلم
    amount = Column(Float) # المبلغ المحول
    fee = Column(Float) # رسوم التحويل
    timestamp = Column(DateTime, default=datetime.now) # تاريخ ووقت التحويل

    # علاقات (Relationships)
    sender = relationship("User", foreign_keys=[from_user_id], back_populates="transfers_sent")
    receiver = relationship("User", foreign_keys=[to_user_id], back_populates="transfers_received")

    def __repr__(self):
        return f"<Transfer(from={self.from_user_id}, to={self.to_user_id}, amount={self.amount})>"