from typing import List, Optional

from pydantic import BaseModel, validator

# from utils.validations import PhoneNumberValidator, PasswordStrentghCheck, EmailValidator, PostalCodeValidator


class GetShopRequestModel(BaseModel):
    shop_id: Optional[str | int] = None
    user_id: Optional[str | int] = None
    shop_name: Optional[str] = None
    phone: Optional[str] = None


class CreateShopRequestModel(BaseModel):
    shop_name: str
    phone: str
    email: Optional[str] = None
    address: str
    postal_code: Optional[str] = None


