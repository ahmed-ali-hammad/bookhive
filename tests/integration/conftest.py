from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.main import app
from src.users.schemas import UserModel
from src.users.service import UserService


async def mock_async_db_session():
    yield AsyncMock(spec=AsyncSession)


async def fake_user_service():
    mock_service = AsyncMock(spec=UserService)

    mock_service.create_new_user = AsyncMock(
        return_value=UserModel(
            username="test.user",
            email="test.user@bookhive.de",
            is_verified=False,
            role="user",
            created_at="2025-03-09T11:52:53.184611",
            updated_at="2025-03-09T11:52:53.184615",
        )
    )
    return mock_service


@pytest.fixture
def test_client():
    app.dependency_overrides[get_session] = mock_async_db_session
    app.dependency_overrides[UserService] = fake_user_service
    return TestClient(app)
