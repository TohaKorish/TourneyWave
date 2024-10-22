from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models import Team
from app.api.repositories.team_repository import TeamRepository

from app.api.schema.team.team_request import TeamRequest
from app.api.schema.team.team_response import TeamResponse


class TeamService:
    def __init__(self, db: AsyncSession, repository: TeamRepository):
        self._db = db
        self._repository = repository

    async def create(self, body: TeamRequest) -> Team:
        try:
            await self._repository.get_by_name(body.name)
            raise ValueError("Team with this name already exists")
        except ModelNotFoundError:
            pass

        team = Team(name=body.name)
        await self._repository.store_team(team)
        await self._db.commit()

        return team

    async def get(self, team_id: int) -> TeamResponse:
        team = await self._repository.get_team_with_members(team_id)
        return TeamResponse(id=team.id, name=team.name, members=team.members)

    async def get_by_name(self, name: str) -> Team:
        team = await self._repository.get_by_name(name)
        return team

    async def update(self, body: TeamRequest) -> Team:
        team = await self._repository.get_by_id(body.id)
        team.name = body.name

        team = await self._repository.update_team(team)
        await self._db.commit()

        return team

    async def delete(self, team_id: int) -> bool:
        is_deleted = await self._repository.delete_team(team_id)
        await self._db.commit()
        return is_deleted
