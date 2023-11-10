from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, UniqueConstraint
from .base import Base
from sqlalchemy.orm import relationship
import bcrypt

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('mobile', name='uq_mobile'),
        UniqueConstraint('email', name='uq_email'),
        UniqueConstraint('first_name', name='first_name'),
        UniqueConstraint('last_name', name='last_name'),
    )
    id         = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30))
    last_name  = Column(String(30))
    email      = Column(String(100), unique=True ,nullable=True)
    mobile     = Column(String(11) , unique=True)
    
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
        return hashed_password.decode('utf-8')

    def check_password(stored_password: str, provided_password: str) -> bool:
        password_match = bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
        return password_match

# from pydantic import BaseModel, Field


# class UserSchema(BaseModel):
#     id: int = Field(default=None, primary_key=True, nullable=False)
#     first_name: str = Field(title="first_name")
#     last_name: str = Field(title="last_name")
#     mobile: str = Field(default="", title="Mobile")
#     email: str = Field(default="", title="Mobile")
#     membership: str = Field(default="Free", title="Mobile")
#     is_admin: bool = Field(default=False, title="Admin_status")

#     class Config:
#         orm_mode = True

    