from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routes import book_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting")
    yield
    print("Server has stopped")


app = FastAPI(
    title="Book API", description="Rest API for a book service", lifespan=life_span
)

app.include_router(book_router, prefix="/api")
