from datetime import date, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book
from src.reviews.schemas import ReviewCreateModel
from src.users.models import User


@pytest_asyncio.fixture
async def mock_async_db_session():
    yield AsyncMock(spec=AsyncSession)


@pytest_asyncio.fixture
async def dummy_user():
    return User(
        id=1,
        username="user.name",
        email="captain.unit.test@example.com",
        password_hash="b1458db3556bf74b02c31f2de5bbb65e32d747e5338156bbf559d2d1e6f71e3f",
        role="admin",
    )


@pytest_asyncio.fixture
async def dummy_book():
    return Book(
        id=uuid4(),
        title="The Dummy Book",
        author="John Doe",
        publisher="Fictional Press",
        published_date=date(2023, 5, 15),
        page_count=250,
        language="English",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=10,
    )


@pytest_asyncio.fixture
async def dummy_user_data():
    return {"id": 10, "email": "fake.user.potato@example.com", "role": "admin"}


@pytest_asyncio.fixture
async def dummy_review_data():
    return ReviewCreateModel(
        text="Great book! Would’ve been 5 stars if it had pictures.", rating=4
    )


@pytest_asyncio.fixture
async def dummy_JWT_secret():
    return "TacoTuesdayJWTSecret"
