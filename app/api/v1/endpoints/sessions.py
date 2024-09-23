from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import session as crud_session
from app.db.session import get_db
from app.schemas.session import SessionRead, SessionCreate

router = APIRouter()


@router.post("/", response_model=SessionRead)
async def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = await crud_session.get_session_by_name(db=db, name=session.session_name)
    if db_session:
        raise HTTPException(status_code=400, detail="Session already exists")
    return await crud_session.create_session(db=db, session=session)


@router.get("/{session_id}", response_model=SessionRead)
async def read_session(session_id: int, db: Session = Depends(get_db)):
    db_session = await crud_session.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session


@router.get("/", response_model=list[SessionRead])
async def read_sessions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sessions = await crud_session.get_sessions(db, skip=skip, limit=limit)
    return sessions
