from fastapi import APIRouter

from app.api.depenencies import UserServiceIoC, AuthenticateTokenIoC, AuthorizeTokenIoC
from app.api.schema.user.user_request import UserRequest
from app.api.schema.user.user_response import UserResponse
from app.api.schema.user.user_response_with_rating import UserResponseWithRating

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post('/')
async def create_user(body: UserRequest, service: UserServiceIoC) -> UserResponse:
    user = await service.create(body)

    return UserResponse.model_validate(user)


@router.get('/me')
async def get_me(user_id: AuthenticateTokenIoC, user_service: UserServiceIoC) -> UserResponseWithRating:
    user = await user_service.get(user_id)

    return UserResponseWithRating.model_validate(user)


@router.patch('/ban/{user_id}')
async def ban_user(user_id: int, role: AuthorizeTokenIoC, user_service: UserServiceIoC) -> bool:
    return await user_service.ban_user(user_id)

@router.patch('/unban/{user_id}')
async def ban_user(user_id: int, role: AuthorizeTokenIoC, user_service: UserServiceIoC) -> bool:
    return await user_service.unban_user(user_id)