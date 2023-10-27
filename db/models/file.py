from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class File(Base):
    __tablename__ = 'files'
    __table_args__ = {'schema': 'file'}

    id         = Column(Integer, primary_key=True, index=True)
    s3_key     = Column(String, unique=True, index=True)  # The key of the file in the S3 bucket
    file_name  = Column(String, index=True)  # The name of the file in the S3 bucket
    link       = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id    = Column(Integer, ForeignKey('account.users.id'))
    shop_id    = Column(Integer, ForeignKey('shop.shops.id'), nullable=True)

    users = relationship('User', back_populates='files')
    shops = relationship('Shop', back_populates='files')


    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, s3_key={self.s3_key})>"
