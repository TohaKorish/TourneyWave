from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.user_game import UserGame


class UserGameRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def store_user_game(self, user_game: UserGame) -> UserGame:
        self._db.add(user_game)
        await self._db.flush()

        return user_game

    async def get_by_user_id_and_game_id(self, user_id: int, game_id: int,) -> UserGame:
        stmt = select(UserGame).where(UserGame.user_id == user_id, UserGame.game_id == game_id)
        user_game = await self._db.scalar(stmt)

        return user_game
