from pydantic import BaseModel, EmailStr
from app.api.models.enums import RoleEnum


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True
