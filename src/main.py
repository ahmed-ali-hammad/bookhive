from fastapi import FastAPI
from src.books.routes import book_router

app = FastAPI(title="Book API", description="Rest API for a book service")

app.include_router(book_router, prefix="/api")
