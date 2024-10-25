from functools import lru_cache
from typing import Annotated, Any

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.models.enums import RoleEnum
from app.api.repositories.game_repository import GameRepository
from app.api.repositories.match_repository import MatchRepository
from app.api.repositories.team_repository import TeamRepository
from app.api.repositories.user_repository import UserRepository
from app.api.services.auth_service import AuthService
from app.api.services.game_service import GameService
from app.api.services.match_service import MatchService
from app.api.services.team_service import TeamService
from app.api.services.token_service import TokenService
from app.api.services.user_service import UserService
from fastapi import Request, Depends, HTTPException
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


def get_game_repository(session: AsyncSession = Depends(get_sa_session)) -> GameRepository:
    return GameRepository(session)


def get_team_repository(session: AsyncSession = Depends(get_sa_session)) -> TeamRepository:
    return TeamRepository(session)


def get_match_repository(session: AsyncSession = Depends(get_sa_session)) -> MatchRepository:
    return MatchRepository(session)


def get_user_service(session: AsyncSession = Depends(get_sa_session),
                     repo: UserRepository = Depends(get_user_repository),
                     crypt: CryptContext = Depends(get_crypt_context)) -> UserService:
    return UserService(session, repo, crypt)


def get_team_service(session: AsyncSession = Depends(get_sa_session),
                     repo: TeamRepository = Depends(get_team_repository),
                     user_repo: UserRepository = Depends(get_user_repository)) -> TeamService:
    return TeamService(session, repo, user_repo)


def get_game_service(session: AsyncSession = Depends(get_sa_session),
                     repo: GameRepository = Depends(get_game_repository)) -> GameService:
    return GameService(session, repo)

def get_match_service(session: AsyncSession = Depends(get_sa_session),
                     repo: MatchRepository = Depends(get_match_repository),
                      team_repo: TeamRepository = Depends(get_team_repository)) -> MatchService:
    return MatchService(session, repo, team_repo)


def get_auth_service(
        context: CryptContext = Depends(get_crypt_context),
        user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(context, user_service)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_by_token(token: Annotated[str, Depends(oauth2_scheme)],
                          token_service: TokenService = Depends(get_token_service)) -> int:
    return token_service.validate_token(token)['user_id']


def authorize_by_token(token: Annotated[str, Depends(oauth2_scheme)],
                       token_service: TokenService = Depends(get_token_service)) -> RoleEnum:
    role = token_service.validate_token(token)['role']

    if role == RoleEnum.USER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return role


DBSessionIoC = Annotated[AsyncSession, Depends(get_sa_session)]
UserServiceIoC = Annotated[UserService, Depends(get_user_service)]
GameServiceIoC = Annotated[GameService, Depends(get_game_service)]
TeamServiceIoC = Annotated[TeamService, Depends(get_team_service)]
MatchServiceIoC = Annotated[MatchService, Depends(get_match_service)]
TokenServiceIoC = Annotated[TokenService, Depends(get_token_service)]
AuthServiceIoC = Annotated[AuthService, Depends(get_auth_service)]
AuthenticateTokenIoC = Annotated[int, Depends(authenticate_by_token)]
AuthorizeTokenIoC = Annotated[RoleEnum, Depends(authorize_by_token)]
