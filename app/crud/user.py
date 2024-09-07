from sqlalchemy.orm import Session

from app.core.security import hashed_password as hashed_pass
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: UserCreate):
    hashed_password = hashed_pass(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
