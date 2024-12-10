from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from teleredis import RedisSession
from telethon import TelegramClient

from app.core.config import Settings

DATABASE_URL = Settings.database_url()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


def account_connection(session_name: str, api_id: int, api_hash: str) -> TelegramClient:
    redis_connector = Settings.redis_connector()
    session = RedisSession(session_name, redis_connector)
    client = TelegramClient(session, api_id, api_hash)

    return client
