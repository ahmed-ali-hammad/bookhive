from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routes import book_router
from src.middleware import register_middleware
from src.reviews.routes import review_router
from src.users.routes import user_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting")
    yield
    print("Server has stopped")


app = FastAPI(
    title="BookHive", description="Rest API for a book service", lifespan=life_span
)

register_middleware(app)

app.include_router(book_router, prefix="/api/books", tags=["Books"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(review_router, prefix="/api/reviews", tags=["Reviews"])


@app.get("/health", status_code=200)
async def health():
    return {"message": "App is healthy"}
