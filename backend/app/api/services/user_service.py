from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models.enums import RoleEnum
from app.api.models.user import User
from app.api.repositories.user_repository import UserRepository
from app.api.schema.user.user_request import UserRequest
from passlib.context import CryptContext


class UserService:
    def __init__(self, db: AsyncSession, repository: UserRepository, context: CryptContext):
        self._db = db
        self._repository = repository
        self._cryp_context = context


    async def create(self, body: UserRequest) -> User:
        hashed = self._cryp_context.hash(body.password)
        try:
            # Check if the email is already taken
            await self._repository.get_by_email(body.email)
            raise ValueError("Email already taken")
        except ModelNotFoundError:
            # Email is not taken, proceed with user creation
            pass

        user = User(username=body.username, email=body.email, hashed_password=hashed, role=RoleEnum.ADMIN if body.email == "admin@gmail.com" else RoleEnum.USER)

        await self._repository.store_user(user)

        await self._db.commit()

        return user




    async def get(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)

        return user

    async def get_by_email(self, email: str) -> User:
        user = await self._repository.get_by_email(email)

        return user

    async def ban_user(self, user_id: int) -> bool:
        try:
            result = await self._repository.ban_user(user_id)
            await self._db.commit()
            return result
        except ModelNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def unban_user(self, user_id: int) -> bool:
        try:
            result = await self._repository.unban_user(user_id)
            await self._db.commit()
            return result
        except ModelNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

