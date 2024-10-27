from app.api.schema.match.match_response import MatchResponse
from app.api.schema.team.team_response import TeamResponse


class MatchResponseWithTeams(MatchResponse):
    teams: list[TeamResponse]

    class Config:
        from_attributes = True
