from pydantic import BaseModel
import uuid
from datetime import datetime, date


class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
