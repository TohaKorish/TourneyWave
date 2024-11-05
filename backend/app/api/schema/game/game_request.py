from pydantic import BaseModel


class GameRequest(BaseModel):
    name: str
    # TODO: some image logic implementation
    image: str
    participant_count: list[int]
