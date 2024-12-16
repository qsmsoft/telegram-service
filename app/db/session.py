from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from teleredis import RedisSession
from telethon import TelegramClient

from app.core.settings import Settings

DATABASE_URL = Settings.database_url()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def account_connection(session_name: str, api_id: int, api_hash: str) -> TelegramClient:
    redis_connector = Settings.redis_connector()
    session = RedisSession(session_name, redis_connector)
    client = TelegramClient(session, api_id, api_hash)

    return client
