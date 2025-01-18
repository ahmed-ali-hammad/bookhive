from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import BookCreateModel, BookModel, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
from src.users.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@book_router.get(
    "/", dependencies=[Depends(role_checker)], status_code=status.HTTP_200_OK
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> list[BookModel]:
    """Returns a list of all available books"""
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/get-book/{book_id}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_200_OK,
)
async def get_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> BookModel:
    """Retrieve a book from the db"""
    book = await book_service.get_book(book_id, session)
    if book is not None:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.post(
    "/create-book",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> BookModel:
    """Create a new book"""
    book = await book_service.create_book(book_data, session)

    if book is not None:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book not added"
        )


@book_router.put("/update-book/{book_id}", dependencies=[Depends(role_checker)])
async def update_book(
    book_id: UUID,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> BookModel:
    """Update a book"""
    book = await book_service.update_book(book_id, book_data, session)

    if book is not None:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete("/delete-book/{book_id}", dependencies=[Depends(role_checker)])
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    """delete a book"""

    result = await book_service.delete_book(book_id, session)

    if result:
        return {"Message": f"book #{book_id} is deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
