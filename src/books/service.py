from uuid import UUID

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book
from src.books.schemas import BookCreateModel, BookModel, BookUpdateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        results = await session.exec(statement)

        return results.all()

    async def get_book(self, book_id: int, session: AsyncSession) -> BookModel:
        statement = select(Book).where(Book.id == book_id)

        results = await session.exec(statement)

        return results.first()

    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
    ) -> BookModel:
        book = Book(**book_data.model_dump())

        session.add(book)
        await session.commit()

        return book

    async def update_book(
        self, book_id: UUID, book_data: BookUpdateModel, session: AsyncSession
    ) -> Book:
        book_to_update = await self.get_book(book_id, session)

        if book_to_update:
            for key, value in book_data.model_dump().items():
                setattr(book_to_update, key, value)

            session.add(book_to_update)
            await session.commit()

            return book_to_update
        else:
            return None

    async def delete_book(self, book_id: UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_id, session)

        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return False
