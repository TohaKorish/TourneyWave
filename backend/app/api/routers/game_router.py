from fastapi import APIRouter, Query
from fastapi_pagination import Page, paginate
from pydantic import TypeAdapter

from app.api.depenencies import GameServiceIoC
from app.api.schema.game.game_request import GameRequest
from app.api.schema.game.game_response import GameResponse

router = APIRouter(prefix="/api/games", tags=["games"])
# TODO: get all route with search and pagination
@router.post('/')
async def create_game(body: GameRequest, service: GameServiceIoC) -> GameResponse:
    game = await service.create(body)
    return GameResponse.model_validate(game)

@router.get('/')
async def get_all_games(game_service: GameServiceIoC,
                        search: str | None = Query(default=None, description="Search by game name")
                        ) -> Page[GameResponse]:
    if search:
        games = await game_service.search_by_part_of_name(search)
    else:
        games = await game_service.get_all_games()

    return paginate(TypeAdapter(list[GameResponse]).validate_python(
        games, from_attributes=True
    ))

@router.get('/{game_id}')
async def get_game(game_id: int, game_service: GameServiceIoC) -> GameResponse:
    game = await game_service.get(game_id)
    return GameResponse.model_validate(game)

@router.put('/{game_id}')
async def update_game(body: GameRequest, game_service: GameServiceIoC, game_id: int) -> GameResponse:
    game = await game_service.update(game_id, body)
    return GameResponse.model_validate(game)

@router.delete('/{game_id}')
async def delete_game(game_id: int, game_service: GameServiceIoC) -> bool:
    return await game_service.delete(game_id)
