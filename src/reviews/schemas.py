from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    text: str
    rating: int = Field(ge=0, lt=5)
    created_at: datetime
    user_id: int
    book_id: UUID


class ReviewCreateModel(BaseModel):
    text: str
    rating: int = Field(ge=0, lt=5)
