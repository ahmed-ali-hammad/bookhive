from uuid import UUID

from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.exceptions import (
    BookNotFoundException,
    UserNotFoundException,
)
from src.reviews.models import Review
from src.reviews.schemas import ReviewCreateModel
from src.users.service import UserService

book_service = BookService()
user_service = UserService()


class ReviewService:
    """
    A service class for managing reviews in the application.

    This class provides methods to interact with reviews, such as adding new reviews
    for books.
    """

    async def add_new_review(
        self,
        user_email: EmailStr,
        book_id: UUID,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        """
        Adds a new review for a book by a user.

        Args:
            user_email (EmailStr): The email of the user submitting the review.
            book_id (UUID): The unique identifier of the book being reviewed.
            review_data (ReviewCreateModel): The data for the new review.
            session (AsyncSession): The database session for executing queries.

        Returns:
            Review: The newly created review object.

        Raises:
            BookNotFoundException: If the specified book does not exist in the database.
            UserNotFoundException: If the specified user does not exist in the database.
        """
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


review_service = ReviewService()


def get_review_service():
    return review_service
