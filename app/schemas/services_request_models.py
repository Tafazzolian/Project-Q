
from typing import List, Optional

from pydantic import BaseModel, validator

from utils.validations import BankAccountNumberValidator, PhoneNumberValidator

class Otp(BaseModel):
    mobile: str

    @validator('mobile')
    def mobile_check(cls, v):
        try:
            PhoneNumberValidator("body.mobile", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v


class BankAccountNumber(BaseModel):
    acc_number: str
    bank:Optional[str] = None

    @validator('acc_number')
    def account_number_check(cls, v):
        try:
            BankAccountNumberValidator("body.acc_number", v).validate()
        except ValueError as e:
            raise ValueError(str(e))
        return v