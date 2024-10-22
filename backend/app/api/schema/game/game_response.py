from typing import Dict, Any

from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    name: str
    image: str
    participant_count: Dict[str, Any]

    class Config:
        from_attributes = True
