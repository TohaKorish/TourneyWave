from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models.user import user_team


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


    # Зовнішній ключ для зв'язку з Match
    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match', back_populates='teams', foreign_keys=[match_id])

    # Many-to-Many зв'язок з User
    members = relationship('User', secondary=user_team, back_populates='teams', lazy='selectin')
