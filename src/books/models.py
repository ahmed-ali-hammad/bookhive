from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "book"

    id: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"Book {self.title}"
