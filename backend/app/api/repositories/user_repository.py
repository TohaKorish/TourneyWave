from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Team
from app.api.models.user import User, user_team
from app.api.models.user_game import UserGame


class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def store_user(self, user: User) -> User:
        self._db.add(user)
        await self._db.flush()

        return user

    async def update_user(self, user: User) -> User:
        await self._db.flush()

        return user

    async def get_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        user = await self._db.scalar(stmt)

        if not user:
            raise ModelNotFoundError(User.__tablename__)

        return user

    async def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        user = await self._db.scalar(stmt)

        if not user:
            raise ModelNotFoundError(User.__tablename__)

        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        await self._db.delete(user)

        return True

    async def ban_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        user.is_banned = True
        await self._db.flush()

        return True

    async def unban_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        user.is_banned = False
        await self._db.flush()

        return True
