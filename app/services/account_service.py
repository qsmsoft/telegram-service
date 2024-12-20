from typing import Optional, List

from sqlalchemy.future import select

from app.db.config import get_async_session
from app.models.account_model import Account
from app.repositories.account_repository import AccountRepository
from app.schemas.account_schema import AccountResponse, AccountCreate, AccountFilter
from app.utils.exceptions.account import AccountAlreadyExistsException, AccountNotFoundException


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.account_repo = repository

    async def create(self, account: AccountCreate) -> AccountResponse:
        if self.account_repo.get_by_phone_number(account.phone_number):
            raise AccountAlreadyExistsException("Account already exists")
        created_account = await self.account_repo.create(account)

        return AccountResponse.model_validate(created_account)

    async def get_account(self, account_id: int) -> Optional[AccountResponse]:
        account = await self.account_repo.get(account_id)
        if not account:
            raise AccountNotFoundException("Account not found")

        return AccountResponse.model_validate(account)

    async def get_users(self, filter: Optional[AccountFilter] = None, skip: int = 0, limit: int = 100) -> List[
        AccountResponse]:
        accounts = await self.account_repo.list(filter, skip, limit)

        return [AccountResponse.model_validate(account) for account in accounts if account]


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
