from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AnyncEngine

from src.config import Settings

settings = Settings()


engine = AnyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))
