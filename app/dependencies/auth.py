from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.crud import user as crud_user
from app.db.session import get_db
from app.schemas.token_schema import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
config = Settings.jwt_config()


# Dependency to get current user from JWT
async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config['secret_key'], algorithms=[config['algorithm']])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
