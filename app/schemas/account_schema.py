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


class AccountUpdate(AccountBase):
    api_id: Optional[int] = None
    api_hash: Optional[str] = None
    phone_number: Optional[str] = None


class AccountResponse(AccountBase):
    id: int
    user_id: int
    is_active: bool


class AccountInfo(AccountBase):
    session_name: str
    class Config:
        from_attributes = True


class AccountFilter(BaseModel):
    user_id: Optional[int] = None
    session_name: Optional[str] = None