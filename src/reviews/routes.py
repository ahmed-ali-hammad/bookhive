from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app_logging import LoggingConfig
from src.db.main import get_session
from src.exceptions import (
    BookNotFoundException,
    UserNotFoundException,
)
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from src.reviews.service import ReviewService, get_review_service
from src.users.dependencies import AccessTokenBearer, RoleChecker, get_current_user

review_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])
logger = LoggingConfig.get_logger(__name__)


@review_router.post(
    "/create-review/{book_id}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"description": "Not Authenticated"},
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"},
    },
)
async def create_review(
    book_id: UUID,
    review_data: ReviewCreateModel,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> ReviewModel:
    """
    Creates a new review for a specific book.

    This endpoint allows an authenticated user to submit a review for a book identified by `book_id`.
    The review details should be provided in the request body.

    Args:
        book_id (UUID): The unique identifier of the book being reviewed.
        review_data: The review content

    Returns:
        ReviewModel: The created review.

    Raises:
        HTTPException (400): If the user or book does not exist.
        HTTPException (403): If the user is not authenticated.
        HTTPException (500): If an unexpected error occurs.
    """
    logger.info(f"Attempting to create a review for book {book_id}")

    try:
        user = await get_current_user(token_details, session)

        review = await review_service.add_new_review(
            user.email, book_id, review_data, session
        )
        return review

    except UserNotFoundException as ex:
        logger.warning(
            f"Failed to create a review for book {book_id}: user does not exist."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist"
        )
    except BookNotFoundException as ex:
        logger.warning(
            f"Failed to create a review for book {book_id}: book does not exist."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book doesn't exist"
        )
    except Exception as ex:
        logger.error(
            f"An exception occurred while creating a review for book {book_id}. Exception is: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
