from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models import Team
from app.api.models.enums import MatchStatusEnum


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    connection_key = Column(String(255), nullable=False)
    connection_description = Column(Text, nullable=False)
    stream_url = Column(String(255), nullable=True)
    password = Column(String(30), nullable=True)

    players_number = Column(Integer)

    @property
    def total_players(self) -> int:
        # Hardcoded for now
        number_of_teams = 2

        return self.players_number * number_of_teams

    @property
    def total_teams_members(self) -> int:
        if not self.teams:
            return 0
        return sum(len(team.members) for team in self.teams)

    @property
    def status(self) -> MatchStatusEnum:
        if self.datetime < datetime.now():
            if len(self.teams[0].members) != self.players_number or len(self.teams[1].members) != self.players_number:
                return MatchStatusEnum.CANCELED

            if self.winner_team_id:
                return MatchStatusEnum.COMPLETED

            return MatchStatusEnum.IN_PROGRESS

        return MatchStatusEnum.OPEN

    # Зв'язок Many-to-One з Game
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship('Game', back_populates='matches', lazy='selectin')

    # One-to-Many зв'язок з Team
    teams = relationship(
        'Team',
        back_populates='match',
        foreign_keys=[Team.match_id],
        cascade="all, delete-orphan",
        lazy='selectin'
    )

    # Зв'язок One-to-One з переможною командою
    winner_team_id = Column(Integer, ForeignKey('teams.id'))
    winner_team = relationship('Team', uselist=False, foreign_keys=[winner_team_id])

    # Зв'язок Many-to-One з User
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='matches')
