from typing import Optional
from pydantic import BaseModel


class GetUfo(BaseModel):
    user_id: Optional[int] = None
    national_code: Optional[str] = None


class CreateUfo(BaseModel):
    tax_number: Optional[str] = None
    Shaba_number:Optional[str] = None
    national_code:str