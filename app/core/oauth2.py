from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import Settings
from app.core.security import verify_password
from app.routes.user import get_user_by_username

config = Settings.jwt_config()

# OAuth2PasswordBearer instance to handle OAuth2 token requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db = db, username = username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config['access_token_expire_minutes'])
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config['secret_key'], algorithm=config['algorithm'])
