from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Game
from app.api.repositories.game_repository import GameRepository
from app.api.schema.game.game_request import GameRequest


class GameService:
    def __init__(self, db: AsyncSession, repository: GameRepository):
        self._db = db
        self._repository = repository


    async def create(self, body: GameRequest) -> Game:
        try:
            await self._repository.get_by_name(body.name)
            raise ValueError("Game with this name already exists")
        except ModelNotFoundError:
            # Email is not taken, proceed with user creation
            pass

        game = Game(name=body.name, image=body.image, participant_count=body.participant_count)

        await self._repository.store_game(game)

        await self._db.commit()

        return game


    async def get(self, game_id: int) -> Game:
        game = await self._repository.get_by_id(game_id)

        return game

    async def get_all_games(self) -> list[Game]:
        games = await self._repository.get_all_games()

        return games

    async def get_by_name(self, name: str) -> Game:
        game = await self._repository.get_by_name(name)

        return game

    async def search_by_part_of_name(self, name: str) -> list[Game]:
        games = await self._repository.search_by_part_of_name(name)

        return games

    async def update(self, body: GameRequest) -> Game:
        game = Game(name=body.name, image=body.image, participant_count=body.participant_count)
        game = await self._repository.update_game(game)
        await self._db.commit()

        return game

    async def delete(self, game_id: int) -> bool:
        game = await self._repository.get_by_id_with_matches(game_id)

        if len(game.matches) > 0:
            raise ValueError("Can not delete a game with matches")

        is_deleted = await self._repository.delete_game(game_id)
        await self._db.commit()

        return is_deleted
