from contextlib import asynccontextmanager

from fastapi_cli.cli import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from teleredis import RedisSession
from telethon import TelegramClient

from app.core.settings import Settings
from app.models.base_model import Base

DATABASE_URL = Settings.database_url()

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        logger.info("Initializing the database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")


@asynccontextmanager
async def get_async_session() -> AsyncSession:
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
