from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    name: str
    image: str
    participant_count: list[int]

    class Config:
        from_attributes = True
