from fastapi import APIRouter

from app.api.depenencies import MatchServiceIoC
from app.api.schema.match.match_request import MatchRequest
from app.api.schema.match.match_response import MatchResponse

router = APIRouter(prefix="/api/matches", tags=["matches"])

# TODO: get all route with search and pagination (FILTER IN PROCESS GAMES)

@router.post('/')
async def create_match(body: MatchRequest, service: MatchServiceIoC) -> MatchResponse:
    match = await service.create(body)
    return MatchResponse.model_validate(match)

@router.get('/{match_id}')
async def get_match(match_id: int, match_service: MatchServiceIoC) -> MatchResponse:
    match = await match_service.get(match_id)
    return MatchResponse.model_validate(match)

@router.put('/')
async def update_match(body: MatchRequest, match_service: MatchServiceIoC) -> MatchResponse:
    match = await match_service.update(body)
    return MatchResponse.model_validate(match)

@router.delete('/{match_id}')
async def delete_match(match_id: int, match_service: MatchServiceIoC) -> bool:
    return await match_service.delete(match_id)
