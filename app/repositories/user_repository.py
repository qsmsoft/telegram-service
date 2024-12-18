from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user_model import User
from app.schemas.user_schema import UserFilter, UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get(self, user_id: int) -> Optional[User]:
        query = select(User).options(selectinload(User.accounts)).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        return user

    async def get_by_username(self, username: str) -> User:
        query = select(User).options(selectinload(User.accounts)).where(User.username == username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        return user

    async def list(self, filter: Optional[UserFilter] = None, skip: int = 0, limit: int = 100) -> List[User]:
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

    async def update(self, user_id: int, user: UserUpdate) -> Optional[User]:
        query = update(User).where(User.id == user_id).values(**user.model_dump(exclude_unset=True))
        try:
            await self.db.execute(query)
            await self.db.commit()
            return await self.get(user_id)
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete(self, user_id: int) -> bool:
        delete_query = delete(User).where(User.id == user_id)
        deleted_rows = await self.db.execute(delete_query)
        await self.db.commit()

        return deleted_rows.rowcount > 0
