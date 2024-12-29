from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting")

    await init_db()
    yield

    print("Server has stopped")


app = FastAPI(
    title="Book API", description="Rest API for a book service", lifespan=life_span
)

app.include_router(book_router, prefix="/api")
