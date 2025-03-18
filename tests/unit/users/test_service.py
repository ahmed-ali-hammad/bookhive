import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.models import User
from src.users.service import UserService


@pytest_asyncio.fixture
def get_mock_session(mocker):
    session = mocker.AsyncMock(spec=AsyncSession)
    yield session


@pytest_asyncio.fixture
async def mocked_user():
    return User(
        id=1,
        username="user.name",
        email="unit.test.dummy@mockdata.com",
        password_hash="b1458db3556bf74b02c31f2de5bbb65e32d747e5338156bbf559d2d1e6f71e3f",
    )


class TestUserService:
    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self, mocker, mocked_user, get_mock_session
    ):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = mocked_user
        get_mock_session.exec.return_value = mock_query

        email = "unit.test.dummy@mockdata.com"
        result = await UserService().get_user_by_email(email, get_mock_session)

        assert result is not None
        assert result.email == "unit.test.dummy@mockdata.com"
