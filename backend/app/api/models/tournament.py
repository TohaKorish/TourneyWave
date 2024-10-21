from sqlalchemy import Integer, Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models.enums import TournamentStatusEnum


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False)
    role = Column(Enum(TournamentStatusEnum), default=TournamentStatusEnum.CREATED, nullable=False)
    connection_key = Column(String(255), nullable=False)
    connection_description = Column(Text, nullable=False)
    password = Column(String(30), nullable=True)

    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates='tournaments')

    stream_url = Column(String(255), nullable=True)

    teams = relationship('Team', back_populates='tournament')
    # winner_team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)

    # winner_team = relationship('Team', back_populates='winner_team_id')
