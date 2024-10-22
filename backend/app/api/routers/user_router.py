from fastapi import APIRouter

from app.api.depenencies import UserServiceIoC, ValidateTokenIoC
from app.api.schema.user.user_request import UserRequest
from app.api.schema.user.user_response import UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post('/')
async def create_user(body: UserRequest, service: UserServiceIoC) -> UserResponse:
    user = await service.create(body)

    return UserResponse.model_validate(user)


@router.get('/me')
async def get_me(user_id: ValidateTokenIoC, user_service: UserServiceIoC):
    user = await user_service.get(user_id)

    return UserResponse.model_validate(user)
