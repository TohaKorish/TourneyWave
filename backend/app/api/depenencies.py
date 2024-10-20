from functools import lru_cache
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.repositories.user_repository import UserRepository
from app.api.services.auth_service import AuthService
from app.api.services.token_service import TokenService
from app.api.services.user_service import UserService
from fastapi import Request, Depends
from passlib.context import CryptContext


async def get_sa_session(request: Request) -> AsyncSession:
    async with request.app.sa_sessionmaker() as session:
        yield session


@lru_cache
def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_token_service() -> TokenService:
    return TokenService()


def get_user_repository(session: AsyncSession = Depends(get_sa_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(session: AsyncSession = Depends(get_sa_session),
                     repo: UserRepository = Depends(get_user_repository),
                     crypt: CryptContext = Depends(get_crypt_context)) -> UserService:
    return UserService(session, repo, crypt)


def get_auth_service(
        context: CryptContext = Depends(get_crypt_context),
        user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(context, user_service)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def validate_token(token: Annotated[str, Depends(oauth2_scheme)],
                   token_service: TokenService = Depends(get_token_service)) -> int:

    return token_service.validate_token(token)


DBSessionIoC = Annotated[AsyncSession, Depends(get_sa_session)]
UserServiceIoC = Annotated[UserService, Depends(get_user_service)]
TokenServiceIoC = Annotated[TokenService, Depends(get_token_service)]
AuthServiceIoC = Annotated[AuthService, Depends(get_auth_service)]
ValidateTokenIoC = Annotated[int, Depends(validate_token)]
