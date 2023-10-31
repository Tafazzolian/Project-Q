from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, UniqueConstraint, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship
import bcrypt
from utils.tools import Tools

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('mobile', name='uq_mobile'),
        UniqueConstraint('email', name='uq_email'),
        UniqueConstraint('first_name', name='first_name'),
        UniqueConstraint('last_name', name='last_name'),
    )
    id         = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name  = Column(String(30))
    email      = Column(String(100), unique=True ,nullable=True)
    mobile     = Column(String(11), unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=None)
    
    hashed_password = Column(String)
    is_admin        = Column(Boolean, default=False)
    membership      = Column(String(5), default="Free")
    two_factor_authentication = Column(Boolean, nullable=True, default=False)

    shops   = relationship('Shop', back_populates='users')
    files   = relationship('File', back_populates='users')
    ufo     = relationship('Ufo' , back_populates='users', uselist=False)

    __table_args__ = {'schema': 'account'}

    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        # Convert the hashed password back to a string for storage
        return hashed_password.decode('utf-8')

    def check_password(stored_password: str, provided_password: str) -> bool:
        password_match = bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
        return password_match