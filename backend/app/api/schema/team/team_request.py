from typing import Dict, Any, List

from pydantic import BaseModel


class TeamRequest(BaseModel):
    name: str
    members: List[str]
    match_id: int
