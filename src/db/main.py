from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from src.books.models import Book

from src.config import Settings

settings = Settings()


engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
