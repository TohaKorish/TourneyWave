from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Match


class MatchRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def store_match(self, match: Match) -> Match:
        self._db.add(match)
        await self._db.flush()
        return match

    async def update_match(self, match: Match) -> Match:
        await self._db.flush()
        return match

    async def get_by_id(self, match_id: int) -> Match:
        stmt = select(Match).where(Match.id == match_id)
        match = await self._db.scalar(stmt)

        if not match:
            raise ModelNotFoundError(Match.__tablename__)

        return match

    async def get_by_name(self, name: str) -> Match:
        stmt = select(Match).where(Match.name == name)
        match = await self._db.scalar(stmt)

        if not match:
            raise ModelNotFoundError(Match.__tablename__)

        return match

    async def delete_match(self, match_id: int) -> bool:
        match = await self.get_by_id(match_id)
        await self._db.delete(match)
        return True
