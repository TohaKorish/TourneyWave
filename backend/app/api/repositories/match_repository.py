from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Match, Team, User


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
        stmt = select(Match).options(selectinload(Match.teams).selectinload(Team.members).selectinload(User.user_games)).where(Match.id == match_id)
        match = await self._db.scalar(stmt)

        if not match:
            raise ModelNotFoundError(Match.__tablename__)

        for team in match.teams:
            for member in team.members:
                member.user_games = [ug for ug in member.user_games if ug.game_id == match.game_id]

        return match

    async def get_by_game_id(self, game_id: int) -> list[Match]:
        stmt = select(Match).where(Match.game_id == game_id)
        matches = await self._db.scalars(stmt)

        return matches.all()

    async def get_by_status(self, status: str) -> list[Match]:
        stmt = select(Match)
        matches = await self._db.scalars(stmt)

        return [match for match in matches if match.status.value == status]

    async def get_by_game_id_and_status(self, game_id: int, status: str) -> list[Match]:
        stmt = select(Match).where(Match.game_id == game_id)
        matches = await self._db.scalars(stmt)

        return [match for match in matches if match.status.value == status]

    async def get_all_matches(self) -> list[Match]:
        stmt = select(Match)
        matches = await self._db.scalars(stmt)

        return matches.all()

    async def delete_match(self, match_id: int) -> bool:
        match = await self.get_by_id(match_id)
        await self._db.delete(match)
        return True
