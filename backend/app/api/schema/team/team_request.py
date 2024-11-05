from pydantic import BaseModel


class TeamRequest(BaseModel):
    name: str
    members: list[str]
    match_id: int
