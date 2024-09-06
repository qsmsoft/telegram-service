from sqlalchemy.orm import Session

from app.models.userbotinfo import UserbotInfo


def get_userbotinfo(db: Session, userbotinfo_id: int):
    return db.query(UserbotInfo).filter(UserbotInfo.id == userbotinfo_id).first()

def get_userbotinfo_by_phone(db: Session, phone: str):
    return db.query(UserbotInfo).filter(UserbotInfo.phone == phone).first()


def get_userbotinfos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserbotInfo).offset(skip).limit(limit).all()


def create_userbotinfo(db: Session, userbotinfo: UserbotInfo):
    db_userbotinfo = UserbotInfo(
        api_id=userbotinfo.api_id,
        api_hash=userbotinfo.api_hash,
        phone=userbotinfo.phone,
        user_id=userbotinfo.user_id
    )

    db.add(db_userbotinfo)
    db.commit()
    db.refresh(db_userbotinfo)
    return db_userbotinfo
