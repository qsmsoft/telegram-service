from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import secret_key, algorithm, access_token_expire_minutes
from app.core.security import verify_password
from app.crud.user import get_user_by_username

# to get a string like this run:
# openssl rand -hex 32
# Secret key to encode JWT tokens (keep this secret in production)
SECRET_KEY = secret_key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minutes)

# OAuth2PasswordBearer instance to handle OAuth2 token requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
