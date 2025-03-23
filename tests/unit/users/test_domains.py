import datetime

import jwt
import passlib
import pytest

from src.users.domains import UserProfile


class TestUserProfile:
    @pytest.mark.asyncio
    async def test_hash_password_success(self):
        password = "PineappleOnPizza!"
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert isinstance(password_hash, str)
        assert password != password_hash
        assert password_hash.startswith("$5$")  # sha256_crypt prefix
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_empty_password(self):
        password = ""
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert password_hash.startswith("$5$")
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_short_password(self):
        password = "A"
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert password_hash.startswith("$5$")
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_long_password(self):
        password = "A" * 1000 + "B" * 1000
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert password_hash.startswith("$5$")
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_password_special_chars(self):
        password = "!@#$%^&*()_+-=[]{};':\",.<>?/\\|"
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_password_unicode(self):
        password = "密码🔒安全"
        password_hash = UserProfile.hash_password(password)

        assert password_hash is not None
        assert UserProfile.myctx.verify(password, password_hash)

    @pytest.mark.asyncio
    async def test_hash_password_different_hashes(self):
        password = "SamePassword"
        hash1 = UserProfile.hash_password(password)
        hash2 = UserProfile.hash_password(password)

        assert hash1 != hash2  # Hashes should not be identical due to salting

    @pytest.mark.asyncio
    async def test_verify_password_success(self):
        password = "PineappleOnPizza!"
        password_hash = "$5$rounds=535000$VQoaVTVn3DuHQYTC$APDkEnrQm.hdgILd4rlRVNIZskJuNDOC/ONSQm7iTm7"

        results = UserProfile.verify_password(password, password_hash)

        assert results is True

    @pytest.mark.asyncio
    async def test_verify_password_failure(self):
        password = "WrongPassword!"
        password_hash = "$5$rounds=535000$VQoaVTVn3DuHQYTC$APDkEnrQm.hdgILd4rlRVNIZskJuNDOC/ONSQm7iTm7"

        results = UserProfile.verify_password(password, password_hash)

        assert results is False

    @pytest.mark.asyncio
    async def test_verify_password_empty_hash(self):
        password = "PineappleOnPizza!"
        password_hash = ""

        with pytest.raises(passlib.exc.UnknownHashError):
            _ = UserProfile.verify_password(password, password_hash)

    @pytest.mark.asyncio
    async def test_verify_password_special_chars(self):
        password = "!@#$%^&*()_+-=[]{};':\",.<>?/\\|"
        password_hash = "$5$rounds=535000$sCIzlzJgVsGWtFoX$COt7DU3nqmgpozw7Sy72WqSu/3zMHoXfl4btrhGkxCD"

        results = UserProfile.verify_password(password, password_hash)

        assert results is True

    @pytest.mark.asyncio
    async def test_verify_password_unicode(self):
        password = "🔒安全密码"
        password_hash = "$5$rounds=535000$L9z5fK7hLSJRoaKZ$ZyM.a3kn4v49rZX.AY7QxaPTpNLzkKavo4biOY4y1UD"

        results = UserProfile.verify_password(password, password_hash)

        assert results is True

    @pytest.mark.asyncio
    async def test_generate_jwt_token_success(self, dummy_user_data, dummy_JWT_secret):
        token = UserProfile.generate_jwt_token(
            user_data=dummy_user_data, secret_key=dummy_JWT_secret
        )

        assert token is not None
        assert isinstance(token, str)
        assert "." in token  # JWT should have three parts separated by dots

    @pytest.mark.asyncio
    async def test_generate_jwt_token_payload(self, dummy_user_data, dummy_JWT_secret):
        token = UserProfile.generate_jwt_token(
            user_data=dummy_user_data, secret_key=dummy_JWT_secret
        )
        decoded = jwt.decode(
            token, key=dummy_JWT_secret, algorithms=[UserProfile.JWT_ALGORITHM]
        )

        assert decoded["user"] == dummy_user_data
        assert "exp" in decoded
        assert "jti" in decoded
        assert "refresh" in decoded
        assert decoded["refresh"] is False

    @pytest.mark.asyncio
    async def test_generate_jwt_token_expiry(self, dummy_user_data, dummy_JWT_secret):
        expiry_seconds = 600  # 10 minutes

        token = UserProfile.generate_jwt_token(
            user_data=dummy_user_data,
            expiry=expiry_seconds,
            secret_key=dummy_JWT_secret,
        )

        decoded = jwt.decode(
            token, key=dummy_JWT_secret, algorithms=[UserProfile.JWT_ALGORITHM]
        )

        expected_expiry = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(seconds=expiry_seconds)

        assert (
            abs(decoded["exp"] - expected_expiry.timestamp()) < 1
        )  # Allow a small time drift

    @pytest.mark.asyncio
    async def test_generate_refresh_token(self, dummy_user_data, dummy_JWT_secret):
        token = UserProfile.generate_jwt_token(
            user_data=dummy_user_data, refresh=True, secret_key=dummy_JWT_secret
        )
        decoded = jwt.decode(
            token, key=dummy_JWT_secret, algorithms=[UserProfile.JWT_ALGORITHM]
        )

        assert decoded["user"] == dummy_user_data
        assert "exp" in decoded
        assert "jti" in decoded
        assert "refresh" in decoded
        assert decoded["refresh"] is True

    @pytest.mark.asyncio
    async def test_generate_jwt_token_different_users(self, dummy_JWT_secret):
        user1 = {"id": 7, "email": "unit.test.unicorn@example.com", "role": "admin"}
        user2 = {"id": 8, "email": "test.user.zombie@example.com", "role": "user"}

        token1 = UserProfile.generate_jwt_token(
            user_data=user1, secret_key=dummy_JWT_secret
        )
        token2 = UserProfile.generate_jwt_token(
            user_data=user2, secret_key=dummy_JWT_secret
        )

        assert token1 != token2  # Different users should have different tokens

    @pytest.mark.asyncio
    async def test_generate_jwt_token_different_instances(
        self, dummy_user_data, dummy_JWT_secret
    ):
        token1 = UserProfile.generate_jwt_token(
            user_data=dummy_user_data, secret_key=dummy_JWT_secret
        )
        token2 = UserProfile.generate_jwt_token(
            user_data=dummy_user_data, secret_key=dummy_JWT_secret
        )

        assert token1 != token2  # Different tokens should be generated
