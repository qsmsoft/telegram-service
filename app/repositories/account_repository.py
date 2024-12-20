from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.account_model import Account
from app.schemas.account_schema import AccountCreate, AccountFilter, AccountUpdate


class AccountRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, account: AccountCreate) -> Account:
        new_account = Account(**account.model_dump())
        self.db.add(new_account)
        try:
            await self.db.commit()
            await self.db.refresh(new_account)
            return new_account
        except IntegrityError:
            await self.db.rollback()
            raise


    async def get(self, account_id: int) -> Account:
        query = select(Account).where(Account.id == account_id)
        result = await self.db.execute(query)
        account = result.scalar_one_or_none()

        return account

    async def get_by_phone_number(self, phone_number: str) -> Account:
        query = select(Account).where(Account.phone_number == phone_number)
        result = await self.db.execute(query)
        account = result.scalar_one_or_none()

        return account


    async def list(self, filter:Optional[AccountFilter] = None, skip: int = 0, limit: int = 100) -> List[Account]:
        query = select(Account)
        if filter:
            if filter.user_id:
                query = query.where(Account.user_id == filter.user_id)
            if filter.session_name:
                query = query.where(Account.session_name == filter.session_name)

        result = await self.db.execute(query.offset(skip).limit(limit))
        accounts = list(result.scalars())

        return accounts


    async def update(self, account_id: int, account: AccountUpdate) -> Optional[Account]:
        query = update(Account).where(Account.id == account_id).values(**account.model_dump(exclude_unset=True))
        try:
            await self.db.execute(query)
            await self.db.commit()
            return await self.get(account_id)
        except IntegrityError:
            await self.db.rollback()
            raise


    async def delete(self, account_id: int) -> bool:
        delete_query = delete(Account).where(Account.id == account_id)
        deleted_rows = await self.db.execute(delete_query)
        await self.db.commit()

        return deleted_rows.rowcount > 0