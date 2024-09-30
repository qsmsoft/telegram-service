from typing import Optional

from pydantic import BaseModel


class TelegramClientBase(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str
    phone_code_hash: Optional[str] = None



class TelegramClientCreate(TelegramClientBase):
    user_id: int
    session_name: str = None


class TelegramClientRead(TelegramClientBase):
    id: int
    user_id: int
    is_active: bool


class TelegramClientInfo(TelegramClientBase):
    session_name: str
    class Config:
        from_attributes = True