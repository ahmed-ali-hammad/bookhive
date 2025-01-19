import pytest

from src.users.domains import UserProfile
from src.users.dependencies import TokenBearer


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
