from sqlalchemy import Integer, Column, String, Enum, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models.enums import RoleEnum

user_team = Table(
    'user_team', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

user_game = Table(
    'user_game',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('rating', Integer, nullable=False, default=0)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String(255), nullable=False)


    # Many-to-Many зв'язок з Team
    teams = relationship('Team', secondary=user_team, back_populates='members')

    # Зв'язок One-to-Many з Match
    matches = relationship('Match', back_populates='owner')

    # Many-to-Many зв'язок з Game через user_game
    games = relationship('Game', secondary=user_game, back_populates='users')
