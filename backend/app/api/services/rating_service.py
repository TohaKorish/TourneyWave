from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Team
from app.api.repositories.match_repository import MatchRepository
from app.api.repositories.user_repository import UserRepository


class RatingService:
    def __init__(self, db: AsyncSession, match_repository: MatchRepository, user_repository: UserRepository):
        self._db = db
        self._match_repository = match_repository
        self._user_repository = user_repository


    async def update_game_points(self, match_id: int, winner_team_id: int) -> None:
        match = await self._match_repository.get_by_id(match_id)

        winning_team = next(team for team in match.teams if team.id == winner_team_id)
        losing_team = next(team for team in match.teams if team.id != winner_team_id)


        avg_winner_rating = self.calculate_average_rating(winning_team)
        avg_loser_rating = self.calculate_average_rating(losing_team)


        coefficient = min(20, 10 * (avg_loser_rating / avg_winner_rating))

        for team in match.teams:
            for member in team.members:
                points_change = coefficient if team.id == winner_team_id else -coefficient
                member.user_games[0].rating += int(points_change)

        await self._db.flush()
        await self._db.commit()

        return None

    def calculate_average_rating(self, team: Team) -> float:

        ratings = [
            member.user_games[0].rating
            for member in team.members
        ]

        return sum(ratings) / len(ratings)

