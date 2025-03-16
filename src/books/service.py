from uuid import UUID

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel
from src.exceptions import BookNotFoundException, UserNotFoundException
from src.users.service import UserService

user_service = UserService()


class BookService:
    """
    Service class for managing book-related operations.

    This class provides methods to retrieve, create, update, and delete books
    from the database. It ensures that user-related checks are performed where necessary.
    """

    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        """
        Retrieve all books from the database.

        Args:
            session (AsyncSession): The database session.

        Returns:
            list[Book]: A list of all books, ordered by creation date.
        """
        statement = select(Book).order_by(desc(Book.created_at))
        results = await session.exec(statement)

        return results.all()

    async def get_user_books(self, user_id: int, session: AsyncSession) -> list[Book]:
        """
        Retrieve all books belonging to a specific user.

        Args:
            user_id (int): The ID of the user.
            session (AsyncSession): The database session.

        Returns:
            list[Book]: A list of books associated with the given user.

        Raises:
            UserNotFoundException: If the user does not exist.
        """
        user = await user_service.get_user_by_id(id=user_id, session=session)
        if user is None:
            raise UserNotFoundException(f"User {user_id} doesn't exist")

        statement = (
            select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        )
        results = await session.exec(statement)

        return results.all()

    async def get_book(self, book_id: int, session: AsyncSession) -> Book | None:
        """
        Retrieve a book by its ID.

        Args:
            book_id (UUID): The unique identifier of the book.
            session (AsyncSession): The database session.

        Returns:
            Book | None: The book if found, otherwise None.
        """
        statement = select(Book).where(Book.id == book_id)
        results = await session.exec(statement)
        return results.first()

    async def create_book(
        self, book_data: BookCreateModel, user_id: int, session: AsyncSession
    ) -> Book:
        """
        Create a new book associated with a user.

        Args:
            book_data (BookCreateModel): The data required to create the book.
            user_id (int): The ID of the user who owns the book.
            session (AsyncSession): The database session.

        Returns:
            Book: The created book instance.

        Raises:
            UserNotFoundException: If the user does not exist.
        """
        user = await user_service.get_user_by_id(id=user_id, session=session)
        if user is None:
            raise UserNotFoundException(f"User {user_id} doesn't exist")

        book = Book(**book_data.model_dump())
        book.user_id = user_id

        session.add(book)
        await session.commit()

        return book

    async def update_book(
        self, book_id: UUID, book_data: BookUpdateModel, session: AsyncSession
    ) -> Book:
        """
        Update an existing book's details.

        Args:
            book_id (UUID): The unique identifier of the book to update.
            book_data (BookUpdateModel): The updated book data.
            session (AsyncSession): The database session.

        Returns:
            Book: The updated book instance.

        Raises:
            BookNotFoundException: If the book does not exist.
        """
        book_to_update = await self.get_book(book_id, session)

        if book_to_update is None:
            raise BookNotFoundException(f"Book {book_id} doesn't exist")

        for key, value in book_data.model_dump().items():
            setattr(book_to_update, key, value)

        session.add(book_to_update)
        await session.commit()

        return book_to_update

    async def delete_book(self, book_id: UUID, session: AsyncSession) -> bool:
        """
        Delete a book from the database.

        Args:
            book_id (UUID): The unique identifier of the book to delete.
            session (AsyncSession): The database session.

        Returns:
            bool: True if the book was successfully deleted.

        Raises:
            BookNotFoundException: If the book does not exist.
        """
        book_to_delete = await self.get_book(book_id, session)

        if book_to_delete is None:
            raise BookNotFoundException(f"Book {book_id} doesn't exist")

        await session.delete(book_to_delete)
        await session.commit()
        return True
