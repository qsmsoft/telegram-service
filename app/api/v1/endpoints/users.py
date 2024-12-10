from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud_user
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user_schema import UserRead, UserCreate

router = APIRouter()


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user_by_username(session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud_user.create_user(user=user)


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user(user_id=user_id, session=session)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[UserRead])
async def read_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_db)):
    users = await crud_user.get_users(session=session, skip=skip, limit=limit)
    return users
