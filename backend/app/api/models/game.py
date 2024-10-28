from sqlalchemy import Integer, Column, String, JSON
from sqlalchemy.orm import relationship

from app.api.db import Base


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)
    participant_count = Column(JSON, nullable=False)


    # Зв'язок One-to-Many з Match
    matches = relationship('Match', back_populates='game')

    # Many-to-Many зв'язок з User через user_game
    user_games = relationship('UserGame', back_populates='game', cascade="all, delete-orphan")
