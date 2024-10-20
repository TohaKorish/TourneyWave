import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()


engine = create_async_engine(os.getenv("DATABASE_URI"), echo=True)
Base = declarative_base()

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
