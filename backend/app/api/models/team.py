from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.api.db import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    users = relationship('User', back_populates='team')

    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match', back_populates='teams')

    matchbywinner = relationship('Match', back_populates='winner_team')