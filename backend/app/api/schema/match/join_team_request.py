from pydantic import BaseModel
class JoinTeamRequest(BaseModel):
    match_id: int
    team_id: int
    user_id: int