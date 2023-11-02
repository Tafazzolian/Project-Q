from sqlalchemy import Column, DateTime, Integer, ForeignKey, func, String
from sqlalchemy.orm import relationship

from utils.tools import Tools
from .base import Base
from utils.custom_types import EncryptedType

class Ufo(Base):
    __tablename__ = 'ufos'
    __table_args__ = {'schema': 'ufo'}
    
    id            = Column(Integer, primary_key=True, index=True)
    tax_number    = Column(EncryptedType(), nullable=True)
    Shaba_number  = Column(EncryptedType(), nullable=True)
    national_code = Column(EncryptedType(), nullable=True)
    mamad = Column(String)

    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=None)

    user_id       = Column(Integer, ForeignKey('account.users.id'))

    users = relationship('User', back_populates='ufo')

