from pydantic import BaseModel, Field

from app.api.schema.game.game_response import GameResponse


class UserGameResponse(BaseModel):
    user_id: int
    game_id: int = Field(..., serialization_alias="gameId")
    game: GameResponse
    rating: int

    class Config:
        from_attributes = True
