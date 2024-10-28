from pydantic import BaseModel, EmailStr
from app.api.models.enums import RoleEnum
from app.api.schema.user_game.user_game_response import UserGameResponse


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum
    user_games: list[UserGameResponse]

    class Config:
        from_attributes = True
