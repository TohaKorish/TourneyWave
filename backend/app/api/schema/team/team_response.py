from pydantic import BaseModel

from app.api.schema.user.user_response import UserResponse
from app.api.schema.user.user_response_with_rating import UserResponseWithRating


class TeamResponse(BaseModel):
    id: int
    name: str
    members: list[UserResponseWithRating]

    class Config:
        from_attributes = True
