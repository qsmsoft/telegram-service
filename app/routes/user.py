from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, async_session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserFilter
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: async_session = Depends(get_db)):
    try:
        repository = UserRepository(db)

        service = UserService(repository)

        if await service.get_user_by_username(user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        created_user = await service.create_user(user)

        return created_user

    except Exception as e:
        print(f"Error creating user: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            repository = UserRepository(session)

        service = UserService(repository)

        user = await service.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except Exception as e:
        print(f"Error getting user: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            repository = UserRepository(session)

        service = UserService(repository)

        user = await service.get_user_by_username(username)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except Exception as e:
        print(f"Error getting user: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=list[UserResponse])
async def get_users(
        filter_name: Optional[str] = Query(None, description="Filter by user name"),
        filter_username: Optional[str] = Query(None, description="Filter by username"),
        created_at_start: Optional[datetime] = Query(None, description="Filter by creation date start"),
        created_at_end: Optional[datetime] = Query(None, description="Filter by creation date end"),
        skip: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        db: AsyncSession = Depends(get_db),
):
    try:
        async with db as session:
            repository = UserRepository(session)

        service = UserService(repository)

        filter = UserFilter(
            name=filter_name,
            username=filter_username,
            created_at_start=created_at_start,
            created_at_end=created_at_end
        )

        users = await service.get_users(filter, skip, limit)

        return users

    except Exception as e:
        print(f"Error getting users: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            repository = UserRepository(session)

        service = UserService(repository)

        updated_user = await service.update_user(user_id, user)

        if updated_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return updated_user

    except Exception as e:
        print(f"Error updating user: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            repository = UserRepository(session)

        service = UserService(repository)

        deleted_user = await service.delete_user(user_id)

        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return deleted_user

    except Exception as e:
        print(f"Error deleting user: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
