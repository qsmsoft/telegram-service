from pydantic import BaseModel


class UserbotInfoBase(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str


class UserBotInfoCreate(UserbotInfoBase):
    pass


class UserBotInfo(UserbotInfoBase):
    id: int
    organization_id: int
