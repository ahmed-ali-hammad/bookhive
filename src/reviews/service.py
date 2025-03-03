import logging
from uuid import UUID

from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.reviews.exceptions import (
    BookNotFoundException,
    UserNotFoundException,
)
from src.reviews.models import Review
from src.reviews.schemas import ReviewCreateModel
from src.users.service import UserService

book_service = BookService()
user_service = UserService()

logger = logging.getLogger(__name__)


class ReviewService:
    async def add_new_review(
        self,
        user_email: EmailStr,
        book_id: UUID,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        user = await user_service.get_user(email=user_email, session=session)
        book = await book_service.get_book(book_id=book_id, session=session)

        if book is None:
            raise BookNotFoundException(f"Book {book_id} doesn't exist")
        if user is None:
            raise UserNotFoundException(f"User {user_email} doesn't exist")

        review = Review(**review_data.model_dump())
        review.user_id = user.id
        review.book_id = book_id

        session.add(review)
        await session.commit()

        return review
