from unittest.mock import AsyncMock

import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

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
async def dummy_user_data():
    return {"id": 10, "email": "fake.user.potato@example.com", "role": "admin"}


@pytest_asyncio.fixture
async def dummy_JWT_secret():
    return "TacoTuesdayJWTSecret"
