from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from telethon import TelegramClient

from app.db.session import telegram_client_connection, get_db
from app.models.telegram_client import TelegramClient as Client
from app.schemas.telegram_client import TelegramClientInfo, TelegramClientCreate
from app.utils.utils import generate_random_string


# database dan client information larini oladigan yordamchi funksiya
async def get_client_info(session_name: str) -> TelegramClientInfo:
    async with get_db() as session:
        result = await session.execute(select(Client).filter_by(session_name=session_name))
        client_info = result.scalar_one_or_none()

    if not client_info:
        raise HTTPException(status_code=404, detail="Client not found")

    return TelegramClientInfo.model_validate(client_info)


# dinamik TelegramClient funksiyasi
async def get_telegram_client(client_info: TelegramClientInfo) -> TelegramClient:
    client = telegram_client_connection(client_info.api_id, client_info.api_hash)
    await client.connect()
    return client


async def create_client(client_info: TelegramClientCreate):
    name = generate_random_string()
    async with get_db() as db_session:
        async with db_session.begin():
            db_client = Client(
                api_id=client_info.api_id,
                api_hash=client_info.api_hash,
                phone_number=client_info.phone_number,
                session_name=name,
                user_id=client_info.user_id,
            )
            db_session.add(db_client)
        await db_session.commit()
        await db_session.refresh(db_client)

    return db_client


async def get_client_by_phone(session: AsyncSession, phone_number: str):
    async with session as db_session:
        result = await db_session.execute(select(Client).filter_by(phone_number=phone_number))
        client = result.scalar_one_or_none()

    return client
