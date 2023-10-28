from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    mobile: str
    membership: str
    email: Optional[str] = None