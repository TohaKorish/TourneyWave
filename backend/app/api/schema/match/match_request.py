from pydantic import BaseModel
from datetime import datetime

from app.api.models.enums import MatchStatusEnum


class MatchRequest(BaseModel):
    datetime: datetime
    status: MatchStatusEnum
    connection_key: str
    connection_description: str
    stream_url: str | None
    password: str | None = None
    game_id: int
    winner_team_id: int | None = None
