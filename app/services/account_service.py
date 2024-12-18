from sqlalchemy.future import select

from app.db.config import get_async_session
from app.models.account_model import Account


async def status_changed(phone_number: str):
    async with get_async_session() as session:
        result = await session.execute(select(Account).filter_by(phone_number=phone_number))
        client = result.scalars().first()
        if not client.is_active:
            client.is_active = True
            await session.commit()
        else:
            client.is_active = False
            await session.commit()


async def get_all_active_accounts():
    async with get_async_session() as db:
        result = await db.execute(select(Account).filter_by(is_active=True))
        accounts = result.scalars().all()
    return accounts
