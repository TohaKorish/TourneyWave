from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Game


class GameRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def store_game(self, game: Game) -> Game:
        self._db.add(game)
        await self._db.flush()
        return game

    async def update_game(self, game: Game) -> Game:
        await self._db.flush()
        return game

    async def get_by_id(self, game_id: int) -> Game:
        stmt = select(Game).where(Game.id == game_id)
        game = await self._db.scalar(stmt)

        if not game:
            raise ModelNotFoundError(Game.__tablename__)

        return game

    async def get_by_id_with_matches(self, game_id: int) -> Game:
        stmt = select(Game).options(selectinload(Game.matches)).where(Game.id == game_id)
        game = await self._db.scalar(stmt)

        if not game:
            raise ModelNotFoundError(Game.__tablename__)

        return game

    async def get_all_games(self) -> list[Game]:
        stmt = select(Game)
        games = await self._db.scalars(stmt)

        return games.all()

    async def get_by_name(self, name: str) -> Game:
        stmt = select(Game).where(Game.name == name)
        game = await self._db.scalar(stmt)

        if not game:
            raise ModelNotFoundError(Game.__tablename__)

        return game

    async def search_by_part_of_name(self, part_of_name: str) -> list[Game]:
        stmt = select(Game).where(Game.name.icontains(f"%{part_of_name}%"))
        games = await self._db.scalars(stmt)
        return games.all()

    async def delete_game(self, game_id: int) -> bool:
        game = await self.get_by_id(game_id)
        await self._db.delete(game)
        return True
