from typing import Dict, Any, List

from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    name: str
    image: str
    participant_count: List[int]

    class Config:
        from_attributes = True
