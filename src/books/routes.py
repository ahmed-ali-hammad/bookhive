from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import (
    BookCreateModel,
    BookDetailModel,
    BookModel,
    BookUpdateModel,
)
from src.app_logging import LoggingConfig
from src.books.service import BookService
from src.db.main import get_session
from src.users.dependencies import AccessTokenBearer, RoleChecker, get_current_user

book_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])
logger = LoggingConfig.get_logger(__name__)


@book_router.get(
    "/",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def get_all_books(
    book_service: BookService = Depends(BookService),
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> list[BookModel]:
    """
    Fetch all available books.

    This endpoint retrieves a list of all books from the database.
    Authentication is required, and only authorized users can access this resource.

    Args:
        book_service (BookService): The service handling book-related operations.
        session (AsyncSession): The database session dependency.
        _ (dict): The access token extracted from the request (for authentication).

    Returns:
        list[BookModel]: A list of books

    Raises:
        HTTPException: If an internal server error occurs.
    """
    try:
        books = await book_service.get_all_books(session)
        return books
    except Exception as ex:
        logger.error(
            f"An error occurred while retrieving the list of books. Exception is: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@book_router.get(
    "/user/{user_id}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def get_user_books(
    user_id: int,
    book_service: BookService = Depends(BookService),
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> list[BookModel]:
    try:
        books = await book_service.get_user_books(user_id, session)
        return books
    except Exception as ex:
        logger.error(
            f"An error occurred while retrieving the list of books for user: {user_id}. Exception is: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@book_router.get(
    "/current-user",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def get_current_user_books(
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(BookService),
    token_details: dict = Depends(access_token_bearer),
) -> list[BookModel]:
    """Returns a list of books for the current logged in user"""
    user = await get_current_user(token_details, session)

    books = await book_service.get_user_books(user.id, session)
    return books


@book_router.get(
    "/get-book/{book_id}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def get_book(
    book_id: UUID,
    book_service: BookService = Depends(BookService),
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> BookDetailModel:
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
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def create_book(
    book_data: BookCreateModel,
    book_service: BookService = Depends(BookService),
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> BookModel:
    """Create a new book"""

    user = await get_current_user(token_details, session)

    book = await book_service.create_book(book_data, user.id, session)

    if book is not None:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book not added"
        )


@book_router.put(
    "/update-book/{book_id}",
    dependencies=[Depends(role_checker)],
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def update_book(
    book_id: UUID,
    book_data: BookUpdateModel,
    book_service: BookService = Depends(BookService),
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


@book_router.delete(
    "/delete-book/{book_id}",
    dependencies=[Depends(role_checker)],
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def delete_book(
    book_id: UUID,
    book_service: BookService = Depends(BookService),
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
