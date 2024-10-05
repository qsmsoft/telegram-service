from contextlib import asynccontextmanager

import redis
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from teleredis import RedisSession
from telethon import TelegramClient

from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

load_dotenv()

Base = declarative_base()

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


def telegram_client_connection(session_name: str, api_id: int, api_hash: str) -> TelegramClient:
    redis_connector = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)
    session = RedisSession(session_name, redis_connector)
    client = TelegramClient(session, api_id, api_hash)

    return client
