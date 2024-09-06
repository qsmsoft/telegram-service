from pydantic import BaseModel


class UserbotInfoBase(BaseModel):
    api_id: int
    api_hash: str
    phone: str


class UserBotInfoCreate(UserbotInfoBase):
    user_id: int


class UserBotInfoRead(UserbotInfoBase):
    id: int
    user_id: int
