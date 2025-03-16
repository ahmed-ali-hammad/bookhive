from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app_logging import LoggingConfig
from src.books.routes import book_router
from src.db.main import check_db_connection, get_session
from src.middleware import register_middleware
from src.reviews.routes import review_router
from src.users.routes import user_router

logger = LoggingConfig.get_logger(__name__)


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Server is starting")
    yield
    logger.info("Server has stopped")


app = FastAPI(
    title="BookHive", description="Rest API for a book service", lifespan=life_span
)

register_middleware(app)

app.include_router(book_router, prefix="/api/books", tags=["Books"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(review_router, prefix="/api/reviews", tags=["Reviews"])


@app.get("/health")
async def health(session: AsyncSession = Depends(get_session)):
    """
    Health check endpoint that checks if the app and database are functioning.

    Args:
        db_sess (AsyncSession): The database session.

    Returns:
        dict: Health status of the application and database.
    """

    db_connection_status = await check_db_connection(session)

    if not db_connection_status:
        raise HTTPException(status_code=500, detail="Database connection failed")

    return {"status": "OK"}
