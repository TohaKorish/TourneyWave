from sqlalchemy import Integer, Column, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.api.db import Base
from app.api.models.enums import RoleEnum

user_team = Table(
    'user_team', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    hashed_password = Column(String(255), nullable=False)


    # Many-to-Many зв'язок з Team
    teams = relationship('Team', secondary=user_team, back_populates='members')
