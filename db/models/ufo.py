from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from utils.custom_types import EncryptedType

class Ufo(Base):
    __tablename__ = 'ufos'
    __table_args__ = {'schema': 'ufo'}
    
    id            = Column(Integer, primary_key=True, index=True)
    tax_number    = Column(EncryptedType(), nullable=True)
    Shaba_number  = Column(EncryptedType(), nullable=True)
    national_code = Column(EncryptedType(), nullable=True)

    user_id       = Column(Integer, ForeignKey('account.users.id'))

    user = relationship('User', back_populates='ufos')
