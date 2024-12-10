from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telethon import TelegramClient

from app.db.session import get_db, account_connection
from app.models.account_model import Account
from app.schemas.account_schema import AccountInfo, AccountCreate
from app.utils.utils import generate_random_string


async def get_account_info(session_name: str) -> AccountInfo:
    async with get_db() as session:
        result = await session.execute(select(Account).filter_by(session_name=session_name))
        account_info = result.scalar_one_or_none()

    if not account_info:
        raise HTTPException(status_code=404, detail="Client not found")

    return AccountInfo.model_validate(account_info)


async def get_account(account_info: AccountInfo) -> TelegramClient:
    account = account_connection(account_info.session_name, account_info.api_id, account_info.api_hash)
    await account.connect()
    return account


async def create_account(account_info: AccountCreate):
    name = generate_random_string()
    async with get_db() as db_session:
        async with db_session.begin():
            db_account = Account(
                api_id=account_info.api_id,
                api_hash=account_info.api_hash,
                phone_number=account_info.phone_number,
                session_name=name,
                user_id=account_info.user_id,
            )
            db_session.add(db_account)
        await db_session.commit()
        await db_session.refresh(db_account)

    return db_account


async def get_account_by_phone(session: AsyncSession, phone_number: str):
    async with session as db_session:
        result = await db_session.execute(select(Account).filter_by(phone_number=phone_number))
        account = result.scalar_one_or_none()

    return account
