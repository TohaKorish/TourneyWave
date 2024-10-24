from pydantic import BaseModel

from app.api.schema.user.user_response import UserResponse


class TeamResponse(BaseModel):
    id: int
    name: str
    members: list[UserResponse]

    class Config:
        from_attributes = True
