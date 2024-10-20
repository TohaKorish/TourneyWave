from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
