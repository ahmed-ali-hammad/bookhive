import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from src.reviews.schemas import ReviewModel


class BookModel(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class BookDetailModel(BookModel):
    reviews: List[ReviewModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
