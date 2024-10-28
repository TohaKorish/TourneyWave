from pydantic import BaseModel

class UserGameResponse(BaseModel):
    user_id: int
    game_id: int
    rating: int

    class Config:
        from_attributes = True
