from pydantic import Field

from app.api.schema.user.user_response import UserResponse
from app.api.schema.user_game.user_game_response import UserGameResponse


class UserResponseWithRating(UserResponse):
    user_games: list[UserGameResponse] = Field(..., serialization_alias="userGames")

    class Config:
        from_attributes = True
