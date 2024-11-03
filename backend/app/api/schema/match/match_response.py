from datetime import datetime
from pydantic import BaseModel, Field

from app.api.models.enums import MatchStatusEnum
from app.api.schema.game.game_response import GameResponse


class MatchResponse(BaseModel):
    id: int
    datetime: datetime
    status: MatchStatusEnum
    connection_key: str = Field(..., serialization_alias="connectionKey")
    connection_description: str = Field(..., serialization_alias="connectionDescription")
    stream_url: str | None = Field(None, serialization_alias="streamUrl")
    password: str | None
    game_id: int
    owner_id: int = Field(..., serialization_alias="ownerId")
    winner_team_id: int | None = Field(..., serialization_alias="winnerTeamId")
    game: GameResponse
    players_number: int = Field(..., serialization_alias="playersNumber")
    total_teams_members: int = Field(..., serialization_alias="totalTeamsMembers")
    total_players: int = Field(..., serialization_alias="totalPlayers")

    class Config:
        from_attributes = True
