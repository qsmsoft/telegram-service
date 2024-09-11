from sqlalchemy.orm import Session

from app.models.account import Account


async def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


async def get_account_by_phone(db: Session, phone: str):
    return db.query(Account).filter(Account.phone == phone).first()


async def get_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Account).offset(skip).limit(limit).all()


async def create_account(db: Session, account: Account):
    db_account = Account(
        api_id=account.api_id,
        api_hash=account.api_hash,
        phone=account.phone,
        user_id=account.user_id
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
