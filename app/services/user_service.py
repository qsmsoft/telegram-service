from typing import List, Optional

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse, UserCreate, UserFilter


class UserService:
    def __init__(self, repository: UserRepository):
        self.user_repo = repository

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = await self.user_repo.get_user_by_id(user_id)
        if user:
            return UserResponse.model_validate(user)
        return None

    async def get_users(self, filter: UserFilter = None, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = await self.user_repo.get_users(filter, skip, limit)
        return [UserResponse.model_validate(user) for user in users if user]

    async def create_user(self, user: UserCreate) -> UserResponse:
        created_user = await self.user_repo.create_user(user)
        return UserResponse.model_validate(created_user)

    async def update_user(self, user_id: int, user: UserResponse) -> Optional[UserResponse]:
        updated_user = await self.user_repo.update_user(user_id, user)
        if updated_user:
            return UserResponse.model_validate(updated_user)
        return None

    async def delete_user(self, user_id: int) -> Optional[UserResponse]:
        deleted_user = await self.user_repo.delete_user(user_id)
        if deleted_user:
            return UserResponse.model_validate(deleted_user)
        return None

    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        user = await self.user_repo.get_user_by_username(username)
        if user:
            return UserResponse.model_validate(user)
        return None
