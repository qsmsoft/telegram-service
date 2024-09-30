from fastapi import HTTPException
from sqlalchemy import select
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


async def create_client(client_info: TelegramClientCreate, session: Session):
    name = generate_random_string()
    db_client = Client(
        api_id=client_info.api_id,
        api_hash=client_info.api_hash,
        phone_number=client_info.phone_number,
        session_name=name,
        user_id=client_info.user_id,
    )

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


async def get_client_by_phone(session: Session, phone: str):
    return session.query(Client).filter_by(phone=phone).first()
