from datetime import datetime
from pydantic import BaseModel

from app.api.models.enums import MatchStatusEnum


class MatchResponse(BaseModel):
    id: int
    datetime: datetime
    status: MatchStatusEnum
    connection_key: str
    connection_description: str
    stream_url: str | None
    password: str | None
    game_id: int
    owner_id: int
    winner_team_id: int | None

    class Config:
        from_attributes = True
