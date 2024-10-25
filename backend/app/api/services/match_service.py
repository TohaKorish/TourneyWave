from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Match, Team
from app.api.repositories.match_repository import MatchRepository
from app.api.repositories.team_repository import TeamRepository
from app.api.schema.match.match_request import MatchRequest


class MatchService:
    def __init__(self, db: AsyncSession, repository: MatchRepository, team_repository: TeamRepository):
        self._db = db
        self._repository = repository
        self._team_repository = team_repository

    async def create(self, body: MatchRequest, user_id: int) -> Match:
        match = Match(
            datetime=body.datetime,
            connection_key=body.connection_key,
            connection_description=body.connection_description,
            stream_url=body.stream_url,
            password=body.password,
            game_id=body.game_id,
            owner_id=user_id,
            teams=[
                Team(name="Team 1", members=[]),
                Team(name="Team 2", members=[]),
            ]
        )

        await self._repository.store_match(match)
        await self._db.commit()


        return match

    async def get(self, match_id: int) -> Match:
        match = await self._repository.get_by_id(match_id)
        return match

    async def get_all_matches(self) -> list[Match]:
        matches = await self._repository.get_all_matches()

        return matches

    async def get_by_game_id(self, game_id: int) -> list[Match]:
        matches = await self._repository.get_by_game_id(game_id)

        return matches

    async def get_by_status(self, status: str) -> list[Match]:
        matches = await self._repository.get_by_status(status)

        return matches

    async def get_by_game_id_and_status(self, game_id: int, status: str) -> list[Match]:
        matches = await self._repository.get_by_game_id_and_status(game_id, status)

        return matches

    async def update(self, body: MatchRequest) -> Match:
        match = await self._repository.get_by_id(body.id)
        match.datetime = body.datetime
        match.connection_key = body.connection_key
        match.connection_description = body.connection_description
        match.stream_url = body.stream_url
        match.password = body.password

        match = await self._repository.update_match(match)
        await self._db.commit()

        return match

    async def delete(self, match_id: int) -> bool:
        is_deleted = await self._repository.delete_match(match_id)
        await self._db.commit()
        return is_deleted

