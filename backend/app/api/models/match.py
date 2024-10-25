from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models import Team
from app.api.models.enums import MatchStatusEnum


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    # status = Column(Enum(MatchStatusEnum), default=MatchStatusEnum.CREATED, nullable=False)
    connection_key = Column(String(255), nullable=False)
    connection_description = Column(Text, nullable=False)
    stream_url = Column(String(255), nullable=True)
    password = Column(String(30), nullable=True)

    @property
    def status(self) -> MatchStatusEnum:
        if self.datetime > datetime.now():
            if self.winner_team_id:
                return MatchStatusEnum.COMPLETED
            else:
                return MatchStatusEnum.IN_PROGRESS
        return MatchStatusEnum.OPEN

    # Зв'язок Many-to-One з Game
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship('Game', back_populates='matches')

    # One-to-Many зв'язок з Team
    teams = relationship(
        'Team',
        back_populates='match',
        foreign_keys=[Team.match_id],
        cascade="all, delete-orphan"
    )

    # Зв'язок One-to-One з переможною командою
    winner_team_id = Column(Integer, ForeignKey('teams.id'))
    winner_team = relationship('Team', uselist=False, foreign_keys=[winner_team_id])
