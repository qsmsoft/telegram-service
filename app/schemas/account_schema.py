from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str
    phone_code_hash: Optional[str] = None



class AccountCreate(AccountBase):
    user_id: int
    session_name: str = None


class AccountRead(AccountBase):
    id: int
    user_id: int
    is_active: bool


class AccountInfo(AccountBase):
    session_name: str
    class Config:
        from_attributes = True