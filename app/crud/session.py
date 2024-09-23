from sqlalchemy.orm import Session

from app.models.session import Session as Telegram_session


async def get_session(db: Session, session_id: int):
    return db.query(Telegram_session).filter(Telegram_session.id == session_id).first()


async def get_sessions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Telegram_session).offset(skip).limit(limit).all()


async def get_session_by_name(db: Session, name: str):
    return db.query(Telegram_session).filter(Telegram_session.session_name == name).first()


async def create_session(db: Session, session: Telegram_session):
    db_session = Telegram_session(
        account_id=session.account_id,
        code=session.code,
        session_name=session.session_name,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
