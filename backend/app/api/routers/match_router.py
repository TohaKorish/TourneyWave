from fastapi import APIRouter, Query
from pydantic import TypeAdapter
from fastapi_pagination import Page, paginate

from app.api.depenencies import MatchServiceIoC, AuthenticateTokenIoC
from app.api.schema.match.join_team_request import JoinTeamRequest
from app.api.schema.match.match_request import MatchRequest
from app.api.schema.match.match_response import MatchResponse
from app.api.schema.match.match_response_with_teams import MatchResponseWithTeams

router = APIRouter(prefix="/api/matches", tags=["matches"])

# TODO: get all route with search and pagination (FILTER IN PROCESS GAMES)

@router.post('/')
async def create_match(body: MatchRequest, service: MatchServiceIoC, user_id: AuthenticateTokenIoC) -> MatchResponse:
    match = await service.create(body, user_id)
    return MatchResponse.model_validate(match)

@router.get('/')
async def get_all_matches(match_service: MatchServiceIoC,
                          game_id: int | None = Query(default=None, description="Filter by game id"),
                          status: str | None = Query(default=None, description="Filter by match status")
                          ) -> Page[MatchResponse]:
    if game_id and status:
        matches = await match_service.get_by_game_id_and_status(game_id, status)
    elif game_id:
        matches = await match_service.get_by_game_id(game_id)
    elif status:
        matches = await match_service.get_by_status(status)
    else:
        matches = await match_service.get_all_matches()

    return paginate(TypeAdapter(list[MatchResponse]).validate_python(
        matches, from_attributes=True
    ))

@router.get('/{match_id}')
async def get_match(match_id: int, match_service: MatchServiceIoC) -> MatchResponseWithTeams:
    match = await match_service.get(match_id)
    return MatchResponseWithTeams.model_validate(match)

@router.put('/{match_id}')
async def update_match(body: MatchRequest, match_service: MatchServiceIoC, match_id: int) -> MatchResponseWithTeams:
    match = await match_service.update(match_id, body)
    return MatchResponseWithTeams.model_validate(match)

@router.delete('/{match_id}')
async def delete_match(match_id: int, match_service: MatchServiceIoC) -> bool:
    return await match_service.delete(match_id)

@router.patch('/join-team/{match_id}')
async def join_team(body: JoinTeamRequest, match_service: MatchServiceIoC) -> MatchResponseWithTeams:
    match = await match_service.join_team(body)
    return MatchResponseWithTeams.model_validate(match)