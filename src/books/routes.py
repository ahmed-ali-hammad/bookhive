from fastapi import APIRouter, status
from fastapi import HTTPException
from typing import List
import json

from src.books.schemas import Book, BookUpdate

book_router = APIRouter()


def rewrite_data_file(f, book_list, indent=4):
    f.seek(0)
    f.write(json.dumps(book_list, indent=indent))
    f.truncate()


@book_router.get("/health", status_code=200)
async def health():
    return {"message": "App is healthy"}


@book_router.get("/books", response_model=List[Book])
async def get_all_books() -> list[Book]:
    """Returns a list of all available books"""
    with open("src/books/books.json", "r") as f:
        books = json.load(f)
    return books


@book_router.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    """Create a new book"""
    with open("src/books/books.json", "r+") as f:
        books = json.load(f)
        books.append(book_data.model_dump())

        rewrite_data_file(f, books)
        return {"Message": "Book is added"}


@book_router.get("/books/get-book/{book_id}")
async def get_book(book_id: int) -> Book:
    """Retrieve a book from the db"""
    with open("src/books/books.json", "r") as f:
        books = json.load(f)
        for book in books:
            if book_id == book["id"]:
                return book
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.put("/books/update-book/{book_id}")
async def update_book(book_id: int, book_data: BookUpdate) -> Book:
    with open("src/books/books.json", "r+") as f:
        books = json.load(f)
        print(book_data)
        for i in range(len(books)):
            if book_id == books[i]["id"]:
                books[i] = book_data.model_dump()

                rewrite_data_file(f, books)
                return books[i]
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/books/delete-book/{book_id}")
async def delete_book(book_id: int):
    """delete a book"""

    with open("src/books/books.json", "r+") as f:
        books = json.load(f)

        for i in range(len(books)):
            if book_id == books[i]["id"]:
                books.pop(i)
                rewrite_data_file(f, books)
                return {"Message": f"book #{book_id} is deleted"}

    raise HTTPException(status_code=404, detail="Book not found")
