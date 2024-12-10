from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from app.core.security import hashed_password as hashed_pass
from app.db.session import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate


async def get_user(user_id: int, session: AsyncSession):
    async with session as db_session:
        result = await db_session.execute(select(User).options(joinedload(User.accounts)).filter_by(id=user_id))
        user = result.unique().scalar_one_or_none()
    return user


async def get_user_by_username(session: AsyncSession, username: str):
    async with session as db_session:
        result = await db_session.execute(select(User).filter_by(username=username))
        user = result.scalar_one_or_none()
    return user


async def get_users(session: AsyncSession, skip: int = 0, limit: int = 10):
    async with session as db_session:
        result = await db_session.execute(select(User).options(selectinload(User.accounts)).offset(skip).limit(limit))
        users = result.scalars().all()
    return users


async def create_user(user: UserCreate):
    hashed_password = hashed_pass(user.password)
    async with get_db() as db_session:
        async with db_session.begin():
            db_user = User(
                username=user.username,
                name=user.name,
                password=hashed_password,
            )
            db_session.add(db_user)
        await db_session.commit()
        await db_session.refresh(db_user)

        result = await db_session.execute(
            select(User).options(joinedload(User.accounts)).filter_by(username=user.username))
        user = result.unique().scalar_one_or_none()
    return user
