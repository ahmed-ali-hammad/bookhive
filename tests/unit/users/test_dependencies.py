import pytest
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException

from src.users.domains import UserProfile
from src.users.service import UserService
from src.users.dependencies import (
    TokenBearer,
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user,
)


class TestTokenBearer:
    @pytest.fixture
    def setup(self):
        user_email = "example@example.de"
        role = "user"
        return {
            "token_bearer": TokenBearer(),
            "user_email": user_email,
            "role": role,
            "token": UserProfile.create_token({"email": user_email, "role": role}),
            "expired_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoidGVzdF9yb2xlX2FnYWluQGJvb2toaXZlLmRlIiwicm9sZSI6InVzZXIifSwiZXhwIjoxNzM3MTIwODU2LCJqdGkiOiIyZDhmMzVjNy00OTVlLTQyOWMtYTQ5Ny1mNGFhNDZlNDU2NWMiLCJyZWZyZXNoIjpmYWxzZX0.g13YNuxRM3X41zlHcSQDCu1huKGZuKMau8MfM00r3xc",
            "invalid_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoidGVzdF9yb2xlX2FnYWluQGJvb2toaXZlLmRlIiwicm9sZSI6InVzZXIifSwiZXhwIjoxNzM3MTIwODU2LCJqdGkiOiIyZDhmMzVjNy00OTVlLTQyOWMtYTQ5Ny1mNGFhNDZlNDU2NWMiLCJyZWZyZXNoIjpmYWxzZX0.g13YNuxRM3X41zlHcSQDCu1huKGZuKMau8MfM00r3ga",
        }

    @pytest.mark.asyncio
    async def test_verify_token_type(self, setup):
        with pytest.raises(NotImplementedError):
            await setup["token_bearer"].verify_token_type()

    @pytest.mark.asyncio
    async def test_get_token_data_success(self, setup):
        token = setup["token"]
        token_data = await setup["token_bearer"].get_token_data(token)

        assert token_data is not None
        assert isinstance(token_data, dict)
        assert token_data["user"]["email"] == setup["user_email"]
        assert token_data["user"]["role"] == setup["role"]

    @pytest.mark.asyncio
    async def test_get_token_data_expired_token(self, setup):
        expired_token = setup["expired_token"]
        token_data = await setup["token_bearer"].get_token_data(expired_token)
        assert token_data is None

    @pytest.mark.asyncio
    async def test_get_token_data_invalid_token(self, setup):
        invalid_token = setup["invalid_token"]
        token_data = await setup["token_bearer"].get_token_data(invalid_token)
        assert token_data is None

    @pytest.mark.asyncio
    async def test_validate_token_success(self, setup):
        token = setup["token"]

        is_token_valid = await setup["token_bearer"].validate_token(token)
        assert is_token_valid is True

    @pytest.mark.asyncio
    async def test_validate_token_failure_expired_token(self, setup):
        expired_token = setup["expired_token"]

        is_token_valid = await setup["token_bearer"].validate_token(expired_token)
        assert is_token_valid is False

    @pytest.mark.asyncio
    async def test_validate_token_failure_invalid_token(self, setup):
        invalid_token = setup["invalid_token"]

        is_token_valid = await setup["token_bearer"].validate_token(invalid_token)
        assert is_token_valid is False

    @pytest.mark.asyncio
    async def test_token_bearer_valid_token(self, setup, monkeypatch):
        token_bearer = setup["token_bearer"]

        async def mock_super_call(self, request):
            class creds:
                credentials = setup["token"]

            return creds

        async def mock_is_jti_in_blocklist(jti):
            return False

        async def mock_verify_token_type(token_data):
            pass

        monkeypatch.setattr(HTTPBearer, "__call__", mock_super_call)
        monkeypatch.setattr(
            "src.users.dependencies.is_jti_in_blocklist", mock_is_jti_in_blocklist
        )
        monkeypatch.setattr(token_bearer, "verify_token_type", mock_verify_token_type)

        token_data = await token_bearer.__call__(None)

        assert isinstance(token_data, dict)
        assert list(token_data.keys()) == ["user", "exp", "jti", "refresh"]
        assert token_data["user"]["email"] == setup["user_email"]
        assert token_data["user"]["role"] == "user"

    @pytest.mark.asyncio
    async def test_token_bearer_invalid_token(self, setup, monkeypatch):
        token_bearer = setup["token_bearer"]

        async def mock_super_call(self, request):
            class creds:
                credentials = setup["invalid_token"]

            return creds

        async def mock_is_jti_in_blocklist(jti):
            return False

        async def mock_verify_token_type(token_data):
            pass

        monkeypatch.setattr(HTTPBearer, "__call__", mock_super_call)
        monkeypatch.setattr(
            "src.users.dependencies.is_jti_in_blocklist", mock_is_jti_in_blocklist
        )
        monkeypatch.setattr(token_bearer, "verify_token_type", mock_verify_token_type)

        with pytest.raises(HTTPException) as exc_info:
            await token_bearer.__call__(None)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Token is invalid or has expired."

    @pytest.mark.asyncio
    async def test_token_bearer_expired_token(self, setup, monkeypatch):
        token_bearer = setup["token_bearer"]

        async def mock_super_call(self, request):
            class creds:
                credentials = setup["expired_token"]

            return creds

        async def mock_is_jti_in_blocklist(jti):
            return False

        async def mock_verify_token_type(token_data):
            pass

        monkeypatch.setattr(HTTPBearer, "__call__", mock_super_call)
        monkeypatch.setattr(
            "src.users.dependencies.is_jti_in_blocklist", mock_is_jti_in_blocklist
        )
        monkeypatch.setattr(token_bearer, "verify_token_type", mock_verify_token_type)

        with pytest.raises(HTTPException) as exc_info:
            await token_bearer.__call__(None)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Token is invalid or has expired."

    @pytest.mark.asyncio
    async def test_token_bearer_in_block_list_token(self, setup, monkeypatch):
        token_bearer = setup["token_bearer"]

        async def mock_super_call(self, request):
            class creds:
                credentials = setup["token"]

            return creds

        async def mock_is_jti_in_blocklist(jti):
            return True

        async def mock_verify_token_type(token_data):
            pass

        monkeypatch.setattr(HTTPBearer, "__call__", mock_super_call)
        monkeypatch.setattr(
            "src.users.dependencies.is_jti_in_blocklist", mock_is_jti_in_blocklist
        )
        monkeypatch.setattr(token_bearer, "verify_token_type", mock_verify_token_type)

        with pytest.raises(HTTPException) as exc_info:
            await token_bearer.__call__(None)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == {
            "error": "This token has been revoked",
            "resolution": "Please get a new token",
        }


class TestAccessTokenBearer:
    @pytest.mark.asyncio
    async def test_verify_token_type_success(self):
        token_data = {
            "user": {"email": "example@example.de", "role": "user"},
            "exp": 1737573128,
            "jti": "73854d44-7cbe-4bdd-894b-e3f28366d9ca",
            "refresh": False,
        }

        # Call the method; the test will pass if no exception is raised.
        await AccessTokenBearer().verify_token_type(token_data)

    @pytest.mark.asyncio
    async def test_verify_token_type_failure(self):
        token_data = {
            "user": {"email": "example@example.de", "role": "user"},
            "exp": 1737573128,
            "jti": "73854d44-7cbe-4bdd-894b-e3f28366d9ca",
            "refresh": True,
        }

        with pytest.raises(HTTPException) as exc_info:
            await AccessTokenBearer().verify_token_type(token_data)

        assert exc_info.value.status_code == 403
        assert (
            exc_info.value.detail
            == "Invalid token: Please provide an access token instead of a refresh token."
        )


class TestRefreshTokenBearer:
    @pytest.mark.asyncio
    async def test_verify_token_type_success(self):
        token_data = {
            "user": {"email": "example@example.de", "role": "user"},
            "exp": 1737573128,
            "jti": "73854d44-7cbe-4bdd-894b-e3f28366d9ca",
            "refresh": True,
        }

        # Call the method; the test will pass if no exception is raised.
        await RefreshTokenBearer().verify_token_type(token_data)

    @pytest.mark.asyncio
    async def test_verify_token_type_failure(self):
        token_data = {
            "user": {"email": "example@example.de", "role": "user"},
            "exp": 1737573128,
            "jti": "73854d44-7cbe-4bdd-894b-e3f28366d9ca",
            "refresh": False,
        }

        with pytest.raises(HTTPException) as exc_info:
            await RefreshTokenBearer().verify_token_type(token_data)

        assert exc_info.value.status_code == 403
        assert (
            exc_info.value.detail
            == "Invalid token: Please provide a refresh token instead of an access token."
        )


class TestGetCurrentUser:
    @pytest.mark.asyncio
    async def test_get_current_user_user_found(self, monkeypatch):
        token_detail = {
            "user": {"email": "example@example.de", "role": "user"},
            "exp": 1737800948,
            "jti": "b0478698-5b8a-42db-86bc-4102f07d79ef",
            "refresh": False,
        }
        session = None

        async def mock_get_user(self, user_email, session):
            class MockUser:
                email = token_detail["user"]["email"]
                role = token_detail["user"]["role"]

            return MockUser()

        monkeypatch.setattr(UserService, "get_user", mock_get_user)

        user = await get_current_user(token_detail, session)

        assert user.email == "example@example.de"
        assert user.role == "user"

    @pytest.mark.asyncio
    async def test_get_current_user_user_not_found(self, monkeypatch):
        token_detail = {
            "user": {"email": "valid@example.com", "role": "user"},
            "exp": 1737800948,
            "jti": "b0478698-5b8a-42db-86bc-4102f07d79ef",
            "refresh": False,
        }
        session = None

        async def mock_get_user(self, user_email, session):
            return None

        monkeypatch.setattr(UserService, "get_user", mock_get_user)

        user = await get_current_user(token_detail, session)

        assert user is None

    @pytest.mark.asyncio
    async def test_get_current_user_missing_email(self):
        token_detail = {
            "user": {"role": "user"},
            "exp": 1737800948,
            "jti": "b0478698-5b8a-42db-86bc-4102f07d79ef",
            "refresh": False,
        }
        session = None

        with pytest.raises(KeyError):
            await get_current_user(token_detail, session)

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token_format(self):
        token_detail = "invalid_token_details"
        session = None

        with pytest.raises(TypeError):
            await get_current_user(token_detail, session)

    @pytest.mark.asyncio
    async def test_get_current_user_db_access_failure(self, monkeypatch):
        token_detail = {
            "user": {"email": "example@example.com", "role": "user"},
            "exp": 1737800948,
            "jti": "b0478698-5b8a-42db-86bc-4102f07d79ef",
            "refresh": False,
        }
        session = None

        async def mock_get_user(self, user_email, session):
            raise Exception("Database access error")

        monkeypatch.setattr(UserService, "get_user", mock_get_user)

        with pytest.raises(Exception) as exc_info:
            await get_current_user(token_detail, session)

        assert str(exc_info.value) == "Database access error"
