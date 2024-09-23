from pydantic import BaseModel


class SessionBase(BaseModel):
    code: int


class SessionCreate(SessionBase):
    account_id: int
    session_name: str


class SessionRead(SessionBase):
    id: int
    account_id: int
