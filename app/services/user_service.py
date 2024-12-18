from typing import List, Optional

from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse, UserCreate, UserFilter, UserUpdate
from app.utils.exceptions.user import UserAlreadyExistsException, UserNotFoundException


class UserService:
    def __init__(self, repository: UserRepository):
        self.user_repo = repository

    async def create_user(self, user: UserCreate) -> UserResponse:
        if await self.user_repo.get_by_username(user.username):
            raise UserAlreadyExistsException("Username already exists")
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        created_user = await self.user_repo.create(user)

        return UserResponse.model_validate(created_user)

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        return UserResponse.model_validate(user)

    async def get_users(self, filter: UserFilter = None, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = await self.user_repo.list(filter, skip, limit)

        return [UserResponse.model_validate(user) for user in users if user]



    async def update_user(self, user_id: int, user: UserUpdate) -> Optional[UserResponse]:
        updated_user = await self.user_repo.update(user_id, user)
        if not updated_user:
            raise UserNotFoundException("User not found")

        return UserResponse.model_validate(updated_user)


    async def delete_user(self, user_id: int) -> bool:
        if not await self.user_repo.get(user_id):
            raise UserNotFoundException("User not found")

        return await self.user_repo.delete(user_id)

    async def get_by_username(self, username: str) -> Optional[UserResponse]:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User not found")

        return UserResponse.model_validate(user)
