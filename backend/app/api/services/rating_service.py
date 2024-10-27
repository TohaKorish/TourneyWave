from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import Team
from app.api.repositories.game_repository import GameRepository
from app.api.repositories.match_repository import MatchRepository


def calculate_average_rating(team: Team) -> float:
    return sum(member.rating_points for member in team.members) / len(team.members)


class RatingService:
    def __init__(self, db: AsyncSession, match_repository: MatchRepository):
        self._db = db
        self._match_repository = match_repository


    async def update_game_points(self, match_id: int, winner_team_id: int) -> None:
        match = await self._match_repository.get_by_id(match_id)

        winning_team = next(team for team in match.teams if team.id == winner_team_id)
        losing_teams = [team for team in match.teams if team.id != winner_team_id]

        avg_winner_rating = calculate_average_rating(winning_team)
        avg_loser_rating = sum(calculate_average_rating(team) for team in losing_teams) / len(losing_teams)

        coefficient = min(20, 10 * (avg_loser_rating / avg_winner_rating))

        for team in match.teams:
            for member in team.members:
                points_change = coefficient if team.id == winner_team_id else -coefficient
                member.rating_points += int(points_change)

        await self._db.flush()
        await self._db.commit()

        return None
