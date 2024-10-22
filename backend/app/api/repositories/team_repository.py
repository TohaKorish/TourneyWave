from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Team


class TeamRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def store_team(self, team: Team) -> Team:
        self._db.add(team)
        await self._db.flush()
        return team

    async def update_team(self, team: Team) -> Team:
        await self._db.flush()
        return team

    async def get_by_id(self, team_id: int) -> Team:
        stmt = select(Team).where(Team.id == team_id)
        team = await self._db.scalar(stmt)

        if not team:
            raise ModelNotFoundError(Team.__tablename__)

        return team

    async def get_by_name(self, name: str) -> Team:
        stmt = select(Team).where(Team.name == name)
        team = await self._db.scalar(stmt)

        if not team:
            raise ModelNotFoundError(Team.__tablename__)

        return team

    async def get_team_with_members(self, team_id: int) -> Team:
        stmt = select(Team).options(selectinload(Team.members)).where(Team.id == team_id)
        team = await self._db.scalar(stmt)

        if not team:
            raise ModelNotFoundError(Team.__tablename__)

        return team

    async def delete_team(self, team_id: int) -> bool:
        team = await self.get_by_id(team_id)
        await self._db.delete(team)
        return True
