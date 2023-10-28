from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'account'}

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name  = Column(String(30))
    email      = Column(String(100), nullable=True)
    mobile     = Column(String(11))
    

    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())
    
    hashed_password = Column(String)
    two_factor_authentication =  Column(Boolean, nullable=True, default=False)
    membership = Column(String(5),default="Free")

    shops   = relationship('Shop'  , back_populates='users')
    files   = relationship('File', back_populates='users')
    ufo     = relationship('Ufo',  back_populates='users', uselist=False)
