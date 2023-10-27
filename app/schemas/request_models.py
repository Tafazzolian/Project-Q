from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, validator

from utils.validations import PhoneNumberValidator, PasswordStrentghCheck


class SendOtpRequestModel(BaseModel):
    mobile: str

    @validator('mobile')
    def mobile_check(cls, v, values):
        PhoneNumberValidator("body.mobile", v).validate()
        return v

class LoginUser(BaseModel):
    mobile: str
    email: Optional[str]
    password: str


class GetUser(BaseModel):
    user_id: Optional[int]
    mobile: Optional[str]
    last_name: Optional[str]

    @validator('mobile')
    def mobile_check(cls, v, values):
        PhoneNumberValidator("body.mobile", v).validate()
        return v

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str]
    mobile: str
    membership: str
    password: str

    @validator('mobile')
    def mobile_check(cls, v, values):
        PhoneNumberValidator("body.mobile", v).validate()
        return v
    
    @validator('password')
    def password_strentgh_check(cls, v, values):
        PasswordStrentghCheck("body.password", v).validate()
        return v

