from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import account as crud_account
from app.db.session import get_db
from app.schemas.account import AccountRead, AccountCreate

router = APIRouter()


@router.post("/", response_model=AccountRead)
async def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = await crud_account.get_account_by_phone(db=db, phone=account.phone)
    if db_account:
        raise HTTPException(status_code=400, detail="Telegram account already registered")
    return await crud_account.create_account(db=db, account=account)


@router.get("/{account_id}", response_model=AccountRead)
async def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = await crud_account.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Telegram Account not found")
    return db_account


@router.get("/", response_model=list[AccountRead])
async def read_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    accounts = await crud_account.get_accounts(db, skip=skip, limit=limit)
    return accounts
