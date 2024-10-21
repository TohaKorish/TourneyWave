from sqlalchemy import Integer, Column, String, JSON
from sqlalchemy.orm import relationship

from app.api.db import Base

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)
    participant_count = Column(JSON, nullable=False)

    matches = relationship('Match', back_populates='game')
