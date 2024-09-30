from contextlib import asynccontextmanager

from dotenv import load_dotenv
from mongoengine import connect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from telemongo import MongoSession
from telethon import TelegramClient

from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, SESSION_DB_HOST, SESSION_DB_PORT, \
    SESSION_DB_NAME

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


SESSION_DB_URL = f'mongodb://{SESSION_DB_HOST}:{SESSION_DB_PORT}/{SESSION_DB_NAME}'


def telegram_client_connection(api_id: int, api_hash: str) -> TelegramClient:
    connect(db=SESSION_DB_NAME, host=SESSION_DB_URL)
    session = MongoSession(database=SESSION_DB_NAME, host=SESSION_DB_URL)
    client = TelegramClient(session, api_id, api_hash)
    return client
