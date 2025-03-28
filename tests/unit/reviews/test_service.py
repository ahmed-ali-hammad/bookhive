import pytest

from src.exceptions import BookNotFoundException, UserNotFoundException
from src.reviews.service import ReviewService

review_service = ReviewService()


class TestReviewService:
    @pytest.mark.asyncio
    async def test_add_new_review_success(
        self, mocker, dummy_user, dummy_book, dummy_review_data, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=dummy_user,
        )

        mocker.patch("src.books.service.BookService.get_book", return_value=dummy_book)

        review = await review_service.add_new_review(
            "email@google.de", dummy_book.id, dummy_review_data, mock_async_db_session
        )

        assert review is not None
        assert review.text == "Great book! Would’ve been 5 stars if it had pictures."
        assert review.rating == 4
        assert review.user_id == dummy_user.id
        assert review.book_id == dummy_book.id
        mock_async_db_session.add.assert_called_once()
        mock_async_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_new_review_user_not_found(
        self, mocker, dummy_book, dummy_review_data, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=None,
        )

        with pytest.raises(UserNotFoundException):
            await review_service.add_new_review(
                "email@google.de",
                dummy_book.id,
                dummy_review_data,
                mock_async_db_session,
            )

        mock_async_db_session.add.assert_not_called()
        mock_async_db_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_new_review_book_not_found(
        self, mocker, dummy_user, dummy_book, dummy_review_data, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email",
            return_value=dummy_user,
        )

        mocker.patch("src.books.service.BookService.get_book", return_value=None)

        with pytest.raises(BookNotFoundException):
            await review_service.add_new_review(
                "email@google.de",
                dummy_book.id,
                dummy_review_data,
                mock_async_db_session,
            )

        mock_async_db_session.add.assert_not_called()
        mock_async_db_session.commit.assert_not_called()
