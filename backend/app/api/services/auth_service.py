from passlib.context import CryptContext
from app.api.exceptions.model_not_found_error import ModelNotFoundError
from app.api.models.user import User
from app.api.services.user_service import UserService


class AuthService:
    def __init__(self, context: CryptContext, user_service: UserService):
        self._crypt_context = context
        self._user_service = user_service

    async def authenticate(self, email: str, password: str) -> bool | User:
        try:
            user = await self._user_service.get_by_email(email)
        except ModelNotFoundError:
            return False

        return self._crypt_context.verify(password, user.hashed_password) and user

