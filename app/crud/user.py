from sqlalchemy.orm import Session

from app.core.security import hashed_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    h_password = hashed_password(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        hashed_password=h_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
