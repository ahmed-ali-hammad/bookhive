from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: int = Field(default=None, primary_key=True, nullable=False)
    text: str
    rating: int = Field(ge=0, lt=5)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_id: int | None = Field(default=None, foreign_key="user.id")
    book_id: UUID | None = Field(default=None, foreign_key="book.id")
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"Review: {self.text}"
