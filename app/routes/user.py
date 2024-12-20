from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import get_async_session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse, UserCreate, UserFilter, UserUpdate
from app.services.user_service import UserService
from app.utils.exceptions.user import UserAlreadyExistsException, UserNotFoundException

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            return await user_service.create_user(user)
        except UserAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            return await user_service.get_user(user_id)
        except UserNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{username}", response_model=UserResponse)
async def get_by_username(username: str, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            return await user_service.get_by_username(username)
        except UserNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[UserResponse])
async def get_users(filter_name: Optional[str] = Query(None, description="Filter by user name"),
                    filter_username: Optional[str] = Query(None, description="Filter by username"),
                    created_at_start: Optional[datetime] = Query(None, description="Filter by creation date start"),
                    created_at_end: Optional[datetime] = Query(None, description="Filter by creation date end"),
                    skip: int = Query(0, description="Offset for pagination"),
                    limit: int = Query(100, description="Limit for pagination"),
                    db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        filter = UserFilter(
            name=filter_name,
            username=filter_username,
            created_at_start=created_at_start,
            created_at_end=created_at_end
        )

        return await user_service.get_users(filter, skip, limit)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            return await user_service.update_user(user_id, user)
        except UserNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            return await user_service.delete_user(user_id)
        except UserNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
