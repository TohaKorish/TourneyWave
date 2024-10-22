from fastapi import APIRouter

from app.api.depenencies import GameServiceIoC
from app.api.schema.game.game_request import GameRequest
from app.api.schema.game.game_response import GameResponse

router = APIRouter(prefix="/api/games", tags=["games"])

@router.post('/')
async def create_game(body: GameRequest, service: GameServiceIoC) -> GameResponse:
    game = await service.create(body)
    return GameResponse.model_validate(game)

@router.get('/{game_id}')
async def get_game(game_id: int, game_service: GameServiceIoC) -> GameResponse:
    game = await game_service.get(game_id)
    return GameResponse.model_validate(game)

@router.put('/')
async def update_game(body: GameRequest, game_service: GameServiceIoC) -> GameResponse:
    game = await game_service.update(body)
    return GameResponse.model_validate(game)

@router.delete('/{game_id}')
async def delete_game(game_id: int, game_service: GameServiceIoC) -> bool:
    return await game_service.delete(game_id)
