from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship

class Shop(Base):
    __tablename__ = 'shops'
    __table_args__ = {'schema': 'shop'}

    id         = Column(Integer,  primary_key=True)
    shop_name  = Column(String(200), nullable=True)
    address    = Column(String(500), nullable=True)
    postal_code= Column(String(20) , nullable=True)
    email      = Column(String(100), nullable=True)
    phone      = Column(String(11) , nullable=True)

    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())

    user_id = Column(Integer, ForeignKey('account.users.id'))
    
    files = relationship('File', back_populates='shops')
    users = relationship('User', back_populates='shops')

