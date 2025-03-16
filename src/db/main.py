from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app_logging import LoggingConfig
from src.config import settings

logger = LoggingConfig.get_logger(__name__)

async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=False))


async def get_session() -> AsyncGenerator[AsyncSession]:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session


async def check_db_connection(session: AsyncSession) -> bool:
    """
    Simple check for database connection using a SELECT query.

    Args:
        db_sess (AsyncSession): The database session.

    Returns:
        bool: True if the DB is reachable, False otherwise.
    """
    try:
        await session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return False
