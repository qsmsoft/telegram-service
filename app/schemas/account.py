from pydantic import BaseModel


class AccountBase(BaseModel):
    api_id: int
    api_hash: str
    phone: str


class AccountCreate(AccountBase):
    user_id: int


class AccountRead(AccountBase):
    id: int
    user_id: int
