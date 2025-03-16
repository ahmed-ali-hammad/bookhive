from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app_logging import LoggingConfig
from src.books.schemas import (
    BookCreateModel,
    BookDetailModel,
    BookModel,
    BookUpdateModel,
)
from src.books.service import BookService
from src.db.main import get_session
from src.exceptions import BookNotFoundException, UserNotFoundException
from src.users.dependencies import AccessTokenBearer, RoleChecker

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
    """
    Retrieves a list of books associated with a specific user.

    Args:
        user_id (int): The ID of the user whose books should be retrieved.
        book_service (BookService): The service handling book-related operations.
        session (AsyncSession): The database session dependency.
        _ (dict): The access token bearer for authentication.

    Returns:
        list[BookModel]: A list of books belonging to the specified user.

    Raises:
        HTTPException: 400 if the user does not exist.
        HTTPException: 500 if an internal server error occurs.
    """

    try:
        books = await book_service.get_user_books(user_id, session)
        return books
    except UserNotFoundException as ex:
        logger.warning(f"User {user_id} not found. Unable to retrieve book list.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist"
        )
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
    """
    Retrieves a list of books for the currently authenticated user.

    Args:
        session (AsyncSession): The database session dependency.
        book_service (BookService): The service handling book-related operations.
        token_details (dict): The authentication token containing user details.

    Returns:
        list[BookModel]: A list of books associated with the logged-in user.

    Raises:
        HTTPException: 400 if the user does not exist.
        HTTPException: 500 if an internal server error occurs.
    """

    try:
        books = await book_service.get_user_books(token_details["user"]["id"], session)
        return books
    except UserNotFoundException:
        logger.warning(
            f"User {token_details["user"]["email"]} not found. Unable to retrieve book list."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist"
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while retrieving the list of books for user: {token_details["user"]["email"]}. Exception is: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


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
    """
    Retrieve a book by its ID.

    This endpoint fetches a book's details based on the provided book ID. If the book is not found,
    a 404 error is returned. In case of other errors, a generic 500 error is raised.

    Args:
        book_id (UUID): The ID of the book to retrieve.
        book_service (BookService): The service used to interact with the book data.
        session (AsyncSession): The database session used for queries.
        _: dict: The access token for user authentication (included by the Depends).

    Returns:
        BookDetailModel: The details of the requested book if found.

    Raises:
        HTTPException: If the book is not found (404), or if an unexpected error occurs (500).
    """

    try:
        book = await book_service.get_book(book_id, session)
        if book is not None:
            return book
        else:
            raise BookNotFoundException(f"Book {book_id} doesn't exist")
    except BookNotFoundException:
        logger.warning(f"Book {book_id} doesn't exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while retrieving book: {book_id}. Exception is: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
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
    """
    Creates a new book entry in the database.

    This endpoint allows an authenticated user to create a new book record.
    The user must be logged in and have the proper role to access this endpoint.
    The book data is provided in the request body.

    Args:
        book_data (BookCreateModel): Data for the new book to be created.
        book_service (BookService): Service for handling book-related operations.
        session (AsyncSession): Database session for executing the operation.
        token_details (dict): The details of the current user's authentication token.

    Returns:
        BookModel: The newly created book.

    Raises:
        HTTPException: If the user is not found, or if an unexpected error occurs during book creation.
    """

    try:
        book = await book_service.create_book(
            book_data, token_details["user"]["email"], session
        )
        return book
    except UserNotFoundException:
        logger.warning(
            f"Cannot create a book, user {token_details['user']['email']} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create a book, user doesn't exist",
        )
    except Exception as ex:
        logger.error(f"An error occurred while creating a book. Exception is: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, book not added",
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
    """
    Update the details of an existing book.

    This endpoint allows for updating the book information in the database.
    It expects a valid book ID and the updated data. If the book doesn't exist, it raises a 404 error.
    If an internal error occurs during the update process, a 500 error is raised.

    Parameters:
    - book_id (UUID): The unique identifier of the book to be updated.
    - book_data (BookUpdateModel): The data to update the book with.

    Returns:
    - BookModel: The updated book data.

    Responses:
    - 200 OK: Book successfully updated.
    - 400 Bad Request: Invalid request or data provided.
    - 404 Not Found: Book with the specified ID not found.
    - 500 Internal Server Error: An error occurred during the update process.
    """

    try:
        book = await book_service.update_book(book_id, book_data, session)
        return book
    except BookNotFoundException:
        logger.warning(
            f"Failed to update book {book_id}. The book was not found in the database."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update book, book not found",
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while updating book {book_id}. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, book is not updated",
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
    """
    Delete a book from the database.

    Args:
        book_id (UUID): The unique identifier of the book to delete.
        book_service (BookService): The service responsible for interacting with the book data.
        session (AsyncSession): The database session for interacting with the database.
        _ (dict): The current authenticated user details from the access token.

    Returns:
        dict: A message confirming the deletion of the book.

    Raises:
        HTTPException: If the book is not found, or if any other error occurs during the deletion process.

    Responses:
        200: Successfully deleted the book.
        404: Book not found in the database.
        500: Internal Server Error.
    """

    try:
        _ = await book_service.delete_book(book_id, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except BookNotFoundException:
        logger.warning(
            f"Failed to delete book {book_id}. The book was not found in the database."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete book, book not found",
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while deleting book {book_id}. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, book is not deleted",
        )
