from multiprocessing.managers import Value

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.user_banned_error import UserBannedError
from app.api.models import Match, Team
from app.api.models.user_game import UserGame
from app.api.repositories.match_repository import MatchRepository
from app.api.repositories.team_repository import TeamRepository
from app.api.repositories.user_game_repository import UserGameRepository
from app.api.repositories.user_repository import UserRepository
from app.api.schema.match.join_team_request import JoinTeamRequest
from app.api.schema.match.match_request import MatchRequest
from app.api.services.rating_service import RatingService


class MatchService:
    def __init__(self, db: AsyncSession, repository: MatchRepository, team_repository: TeamRepository, user_repository: UserRepository, user_game_repository: UserGameRepository, rating_service: RatingService):
        self._db = db
        self._repository = repository
        self._team_repository = team_repository
        self._user_repository = user_repository
        self._user_game_repository = user_game_repository
        self._rating_service = rating_service

    async def create(self, body: MatchRequest, user_id: int) -> Match:
        user = await self._user_repository.get_by_id(user_id)
        if user.is_banned:
            raise UserBannedError("create a match")

        match = Match(
            datetime=body.datetime,
            connection_key=body.connection_key,
            connection_description=body.connection_description,
            stream_url=body.stream_url,
            password=body.password,
            game_id=body.game_id,
            owner_id=user_id,
            players_number=body.players_number,
            teams=[
                Team(name="Team 1", members=[]),
                Team(name="Team 2", members=[]),
            ]
        )

        await self._repository.store_match(match)
        await self._db.commit()


        match = await self._repository.get_by_id(match.id)

        return match

    async def get(self, match_id: int) -> Match:
        match = await self._repository.get_by_id(match_id)
        return match

    async def get_all_matches(self) -> list[Match]:
        matches = await self._repository.get_all_matches()

        return matches

    async def get_by_game_id(self, game_id: int) -> list[Match]:
        matches = await self._repository.get_by_game_id(game_id)

        return matches

    async def get_by_status(self, status: str) -> list[Match]:
        matches = await self._repository.get_by_status(status)

        return matches

    async def get_by_game_id_and_status(self, game_id: int, status: str) -> list[Match]:
        matches = await self._repository.get_by_game_id_and_status(game_id, status)

        return matches

    async def update(self, match_id: int, body: MatchRequest) -> Match:
        match = await self._repository.get_by_id(match_id)
        match.datetime = body.datetime
        match.connection_key = body.connection_key
        match.connection_description = body.connection_description
        match.stream_url = body.stream_url
        match.password = body.password

        match = await self._repository.update_match(match)
        await self._db.commit()

        return match

    async def delete(self, match_id: int) -> bool:
        is_deleted = await self._repository.delete_match(match_id)
        await self._db.commit()
        return is_deleted

    async def join_team(self, body: JoinTeamRequest) -> Match:
        user = await self._user_repository.get_by_id(body.user_id)
        if user.is_banned:
            raise UserBannedError("join a team")

        match = await self._repository.get_by_id(body.match_id)
        max_team_size = match.players_number

        for team in match.teams:
            if team.id != body.team_id:
                team.members = [member for member in team.members if member.id != body.user_id]
            else:
                user_in_team = any(member.id == body.user_id for member in team.members)
                if not user_in_team:
                    if len(team.members) == max_team_size:
                        raise ValueError("too many team members")

                    team.members.append(user)

        user_game = await self._user_game_repository.get_by_user_id_and_game_id(body.user_id, match.game_id)

        if not user_game:
            user_game = UserGame(
                user_id=body.user_id,
                game_id=match.game_id
            )

            await self._user_game_repository.store_user_game(user_game)

        await self._db.commit()
        return match

    async def complete_match(self, match_id: int, winner_team_id: int) -> Match:
        match = await self._repository.get_by_id(match_id)

        if match.winner_team_id:
            raise ValueError('Already has a winner');

        match.winner_team_id = winner_team_id

        await self._rating_service.update_game_points(match_id, winner_team_id)

        await self._repository.update_match(match)
        await self._db.commit()

        return match
