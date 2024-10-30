from datetime import datetime
from pydantic import BaseModel, Field

from app.api.models.enums import MatchStatusEnum
from app.api.schema.game.game_response import GameResponse


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
    game: GameResponse
    players_number: int = Field(..., serialization_alias="playersNumber")
    total_teams_members: int = Field(..., serialization_alias="totalTeamsMembers")
    total_players: int = Field(..., serialization_alias="totalPlayers")

    class Config:
        from_attributes = True
