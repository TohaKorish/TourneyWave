from sqlalchemy import Integer, Column, String, Enum
from app.api.db import Base
from app.api.models.enums import RoleEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    hashed_password = Column(String(255), nullable=False)
