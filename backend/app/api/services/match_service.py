from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Match
from app.api.repositories.match_repository import MatchRepository
from app.api.schema.match.match_request import MatchRequest


class MatchService:
    def __init__(self, db: AsyncSession, repository: MatchRepository):
        self._db = db
        self._repository = repository

    async def create(self, body: MatchRequest) -> Match:
        match = Match(
            datetime=body.datetime,
            connection_key=body.connection_key,
            connection_description=body.connection_description,
            stream_url=body.stream_url,
            password=body.password,
            game_id=body.game_id
        )

        await self._repository.store_match(match)
        await self._db.commit()

        return match

    async def get(self, match_id: int) -> Match:
        match = await self._repository.get_by_id(match_id)
        return match

    async def get_by_name(self, connection_key: str) -> Match:
        match = await self._repository.get_by_name(connection_key)
        return match

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

