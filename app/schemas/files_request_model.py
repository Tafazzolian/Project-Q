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
