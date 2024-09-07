from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import userbotinfo as crud_userbotinfo
from app.db.session import get_db
from app.schemas.userbotinfo import UserBotInfoRead, UserBotInfoCreate

router = APIRouter()


@router.post("/", response_model=UserBotInfoRead)
async def create_userbotinfo(userbotinfo: UserBotInfoCreate, db: Session = Depends(get_db)):
    db_userbotinfo = crud_userbotinfo.get_userbotinfo_by_phone(db, phone=userbotinfo.phone)
    if db_userbotinfo:
        raise HTTPException(status_code=400, detail="Telegram account already registered")
    return crud_userbotinfo.create_userbotinfo(db=db, userbotinfo=userbotinfo)


@router.get("/{userbotinfo_id}", response_model=UserBotInfoRead)
async def read_userbotinfo(userbotinfo_id: int, db: Session = Depends(get_db)):
    db_userbotinfo = crud_userbotinfo.get_userbotinfo(db, userbotinfo_id=userbotinfo_id)
    if db_userbotinfo is None:
        raise HTTPException(status_code=404, detail="Telegram Account not found")
    return db_userbotinfo


@router.get("/", response_model=list[UserBotInfoRead])
async def read_userbotinfos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    userbotinfos = crud_userbotinfo.get_userbotinfos(db, skip=skip, limit=limit)
    return userbotinfos
