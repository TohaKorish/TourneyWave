from pydantic import BaseModel, Field


class GameResponse(BaseModel):
    id: int
    name: str
    image: str
    participant_count: list[int] = Field(serialization_alias='participantCount')

    class Config:
        from_attributes = True
