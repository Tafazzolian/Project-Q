from typing import List, Optional

from pydantic import BaseModel, validator

from utils.validations import PhoneNumberValidator, PasswordStrentghCheck, EmailValidator, PostalCodeValidator


class CreateFile(BaseModel):
    file_name: Optional[str] = None
    user_id: Optional[int] = None
    link: Optional[str] = None
    s3_key: Optional[str] = None
