from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.exceptions import (
    BookNotFoundException,
    UserNotFoundException,
)
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from src.reviews.service import ReviewService
from src.users.dependencies import AccessTokenBearer, RoleChecker, get_current_user

review_router = APIRouter()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@review_router.post(
    "/create-review/{book_id}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    book_id: UUID,
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> ReviewModel:
    """Create a new review for a book"""

    try:
        user = await get_current_user(token_details, session)

        review = await review_service.add_new_review(
            user.email, book_id, review_data, session
        )
        return review

    except UserNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist"
        )
    except BookNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book doesn't exist"
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
