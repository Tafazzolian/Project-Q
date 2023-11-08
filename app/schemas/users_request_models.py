from typing import List, Optional

from pydantic import BaseModel, validator

from utils.validations import PhoneNumberValidator, PasswordStrentghCheck, EmailValidator, PostalCodeValidator


class SendOtpRequestModel(BaseModel):
    mobile: str
    postal_code: str

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v
    
    @validator('postal_code', pre=True, always=True)
    def postal_code_check(cls, v):
        try:
            PostalCodeValidator("body.postal_code", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v


class LoginUser(BaseModel):
    mobile: str
    email: Optional[str] = None
    password: str

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v
    
    @validator('email', pre=True, always=True)
    def email_check(cls, v):
        if v is not None:
            try:
                EmailValidator("body.email", v).validate()
            except ValueError as e:
                raise ValueError(str(e))
        return v

class GetUser(BaseModel):
    user_id: Optional[int] = None
    mobile: Optional[str] = None
    last_name: Optional[str] = None

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v


class Otp(BaseModel):
    mobile: str

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    password: str
    code: str
    
    @validator('password')
    def password_strength_check(cls, v):
        try:
            PasswordStrentghCheck("body.password", v).validate()
        except ValueError as e:
            raise ValueError(f"Password is too weak: {', '.join(e.args[0])}")
        return v

class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    two_factor_authentication: Optional[bool] = False
    is_admin: Optional[bool] = False

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v
