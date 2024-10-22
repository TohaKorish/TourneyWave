from fastapi import APIRouter

from app.api.depenencies import TeamServiceIoC
from app.api.schema.team.team_request import TeamRequest
from app.api.schema.team.team_response import TeamResponse

router = APIRouter(prefix="/api/teams", tags=["teams"])

@router.post('/')
async def create_team(body: TeamRequest, service: TeamServiceIoC) -> TeamResponse:
    team = await service.create(body)
    return TeamResponse.model_validate(team)

@router.get('/{team_id}')
async def get_team(team_id: int, team_service: TeamServiceIoC) -> TeamResponse:
    team = await team_service.get(team_id)
    return TeamResponse.model_validate(team)

@router.put('/')
async def update_team(body: TeamRequest, team_service: TeamServiceIoC) -> TeamResponse:
    team = await team_service.update(body)
    return TeamResponse.model_validate(team)

@router.delete('/{team_id}')
async def delete_team(team_id: int, team_service: TeamServiceIoC) -> bool:
    return await team_service.delete(team_id)
