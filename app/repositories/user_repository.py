from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.security import hashed_password
from app.models.user_model import User
from app.schemas.user_schema import UserFilter, UserCreate, UserBase


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).options(selectinload(User.accounts)).where(User.id == user_id)

        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def get_users(self, filter: UserFilter = None, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).options(selectinload(User.accounts))

        if filter:
            if filter.name:
                query = query.where(User.name.ilike(f"%{filter.name}%"))
            if filter.username:
                query = query.where(User.username.ilike(f"%{filter.username}%"))
            if filter.created_at_start:
                query = query.where(User.created_at >= filter.created_at_start)
            if filter.created_at_end:
                query = query.where(User.created_at <= filter.created_at_end)

        result = await self.db.execute(query.offset(skip).limit(limit))

        return list(result.scalars())

    async def create_user(self, user: UserCreate) -> User:
        user.password = hashed_password(user.password)
        db_user = User(**user.model_dump())

        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)

        except Exception as e:
            await self.db.rollback()
            raise e

        return db_user

    async def update_user(self, user_id: int, user: UserBase) -> Optional[User]:
        result = await self.db.execute(select(User).options(selectinload(User.accounts)).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if db_user:
            return None

        for key, value in user.model_dump().items():
            if value is not None:
                setattr(db_user, key, value)

        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def delete_user(self, user_id: int) -> Optional[User]:
        query = select(User).options(selectinload(User.accounts)).where(User.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return None

        await self.db.delete(db_user)
        await self.db.commit()

        return db_user

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).options(selectinload(User.accounts)).where(User.username == username)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()
