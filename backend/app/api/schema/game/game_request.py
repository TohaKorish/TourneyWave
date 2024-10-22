from typing import Dict, Any

from pydantic import BaseModel


class GameRequest(BaseModel):
    name: str
    image: str
    participant_count: Dict[str, Any]
