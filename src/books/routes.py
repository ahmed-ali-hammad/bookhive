from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
import json
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.books.schemas import Book, BookUpdate, BookCreate
from src.books.service import BookService

from src.db.main import get_session

book_router = APIRouter()
book_service = BookService()


@book_router.get("/health", status_code=200)
async def health():
    return {"message": "App is healthy"}


@book_router.get("/books", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> list[Book]:
    """Returns a list of all available books"""
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/books/get-book/{book_id}")
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)) -> Book:
    """Retrieve a book from the db"""
    book = await book_service.get_book(book_id, session)
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate, session: AsyncSession = Depends(get_session)
) -> Book:
    """Create a new book"""
    book = await book_service.create_book(book_data, session)

    if book is not None:
        return book
    else:
        raise HTTPException(status_code=400, detail="Book not added")


@book_router.put("/books/update-book/{book_id}")
async def update_book(
    book_id: UUID, book_data: BookUpdate, session: AsyncSession = Depends(get_session)
) -> Book:
    """Update a book"""
    book = await book_service.update_book(book_id, book_data, session)

    if book is not None:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/books/delete-book/{book_id}")
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    """delete a book"""

    result = await book_service.delete_book(book_id, session)

    if result:
        return {"Message": f"book #{book_id} is deleted"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
