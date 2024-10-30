from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.api.db import Base


class UserGame(Base):
    __tablename__ = 'user_game'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    rating = Column(Integer, nullable=False, default=100)

    user = relationship('User', back_populates='user_games')
    game = relationship('Game', back_populates='user_games')
