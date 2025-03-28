import pytest

from src.exceptions import UserNotFoundException, BookNotFoundException
from src.reviews.schemas import ReviewCreateModel
from src.reviews.service import ReviewService

review_service = ReviewService()


class TestReviewService:
    @pytest.mark.asyncio
    async def test_add_new_review_success(
        self, mocker, dummy_user, dummy_book, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=dummy_user,
        )

        mocker.patch("src.books.service.BookService.get_book", return_value=dummy_book)

        review_data = ReviewCreateModel(text="review text", rating=4)

        review = await review_service.add_new_review(
            "email@google.de", dummy_book.id, review_data, mock_async_db_session
        )

        assert review is not None
        assert review.text == "review text"
        assert review.rating == 4
        assert review.user_id == dummy_user.id
        assert review.book_id == dummy_book.id

    @pytest.mark.asyncio
    async def test_add_new_review_user_not_found(
        self, mocker, dummy_book, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=None,
        )

        review_data = ReviewCreateModel(text="review text", rating=4)

        with pytest.raises(UserNotFoundException):
            await review_service.add_new_review(
                "email@google.de", dummy_book.id, review_data, mock_async_db_session
            )

    @pytest.mark.asyncio
    async def test_add_new_review_book_not_found(
        self, mocker, dummy_user, dummy_book, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=dummy_user,
        )

        mocker.patch("src.books.service.BookService.get_book", return_value=None)

        review_data = ReviewCreateModel(text="review text", rating=4)

        with pytest.raises(BookNotFoundException):
            await review_service.add_new_review(
                "email@google.de", dummy_book.id, review_data, mock_async_db_session
            )
