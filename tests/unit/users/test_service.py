import pytest

from src.exceptions import InvalidCredentials, UserAlreadyExists, UserNotFoundException
from src.users.schemas import UserCreateModel
from src.users.service import UserService


class TestUserService:
    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = dummy_user
        mock_async_db_session.exec.return_value = mock_query

        result = await UserService().get_user_by_email(
            "captain.unit.test@example.com", mock_async_db_session
        )

        assert result is not None
        assert result.email == "captain.unit.test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_email_case_insensitive(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = dummy_user
        mock_async_db_session.exec.return_value = mock_query

        result = await UserService().get_user_by_email(
            "CAPTAIN.UNIT.TEST@EXAMPLE.COM", mock_async_db_session
        )

        assert result is not None
        assert result.email == "captain.unit.test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, mocker, mock_async_db_session):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = None
        mock_async_db_session.exec.return_value = mock_query

        result = await UserService().get_user_by_email(
            "captain.unit.test@example.com", mock_async_db_session
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_by_email_database_error(self, mock_async_db_session):
        mock_async_db_session.exec.side_effect = Exception("Database Error")

        with pytest.raises(Exception, match="Database Error"):
            _ = await UserService().get_user_by_email(
                "captain.unit.test@example.com", mock_async_db_session
            )

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = dummy_user
        mock_async_db_session.exec.return_value = mock_query

        result = await UserService().get_user_by_id(1, mock_async_db_session)

        assert result is not None
        assert result.email == "captain.unit.test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, mocker, mock_async_db_session):
        mock_query = mocker.MagicMock()
        mock_query.first.return_value = None
        mock_async_db_session.exec.return_value = mock_query

        result = await UserService().get_user_by_email(
            "user.never.found@example.com", mock_async_db_session
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_by_id_database_error(self, mock_async_db_session):
        mock_async_db_session.exec.side_effect = Exception("Database Error")

        with pytest.raises(Exception, match="Database Error"):
            _ = await UserService().get_user_by_email(20, mock_async_db_session)

    @pytest.mark.asyncio
    async def test_create_new_user_success(self, mocker, mock_async_db_session):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email", return_value=None
        )

        user_data = UserCreateModel(
            username="new.user", email="new.user@test.de", password="password"
        )

        new_user = await UserService().create_new_user(user_data, mock_async_db_session)

        assert new_user is not None
        assert new_user.email == user_data.email
        assert new_user.username == user_data.username
        assert new_user.password_hash is not None
        assert new_user.password_hash != user_data.password
        assert hasattr(new_user, "id")

        mock_async_db_session.commit.assert_called_once()
        mock_async_db_session.add.assert_called_once_with(new_user)

    @pytest.mark.asyncio
    async def test_create_new_user_user_already_exist(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email", return_value=dummy_user
        )

        user_data = UserCreateModel(
            username="new.user", email="new.user@test.de", password="password"
        )

        with pytest.raises(UserAlreadyExists):
            _ = await UserService().create_new_user(user_data, mock_async_db_session)

        mock_async_db_session.add.assert_not_called()
        mock_async_db_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_auth_tokens_success(self, mocker, dummy_user_data):
        mock_generate_jwt_token = mocker.patch(
            "src.users.domains.UserProfile.generate_jwt_token",
            side_effect=[
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMCwiZW1haWwiOiJ0ZXN0LnRva2VuQGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NDI1OTMwMjAsImp0aSI6ImNmZjk1YzVjLWQzZTItNGQwNi05NzE0LTViNGNlODMzMTJjYyIsInJlZnJlc2giOmZhbHNlfQ.DljmIkZc9xaYZaqtT8aCcSI5_gB2On_bzKtT5TjcvD4",
                "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMCwiZW1haWwiOiJ0ZXN0LnRva2VuQGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NDI2NzIyMjAsImp0aSI6IjM1YWM4MmE5LWZlOWUtNGY5MC04ZDkyLTQ1ZTI2ZjA0YzEyNiIsInJlZnJlc2giOnRydWV9.M9KRXfi3Yd14769yxGEjkQvMlmqsnmnbiJpofyrX-7w",
            ],
        )

        token = await UserService().create_auth_tokens(dummy_user_data)

        assert token is not None
        assert (
            token["access_token"]
            == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMCwiZW1haWwiOiJ0ZXN0LnRva2VuQGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NDI1OTMwMjAsImp0aSI6ImNmZjk1YzVjLWQzZTItNGQwNi05NzE0LTViNGNlODMzMTJjYyIsInJlZnJlc2giOmZhbHNlfQ.DljmIkZc9xaYZaqtT8aCcSI5_gB2On_bzKtT5TjcvD4"
        )
        assert (
            token["refresh_token"]
            == "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMCwiZW1haWwiOiJ0ZXN0LnRva2VuQGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NDI2NzIyMjAsImp0aSI6IjM1YWM4MmE5LWZlOWUtNGY5MC04ZDkyLTQ1ZTI2ZjA0YzEyNiIsInJlZnJlc2giOnRydWV9.M9KRXfi3Yd14769yxGEjkQvMlmqsnmnbiJpofyrX-7w"
        )
        assert isinstance(token["access_token"], str)
        assert isinstance(token["refresh_token"], str)
        assert token["access_token"] != token["refresh_token"]
        assert mock_generate_jwt_token.call_count == 2

    @pytest.mark.asyncio
    async def test_authenticate_and_generate_token_success(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email", return_value=dummy_user
        )
        mocker.patch("src.users.domains.UserProfile.verify_password", return_value=True)

        mock_create_auth_tokens = mocker.patch(
            "src.users.service.UserService.create_auth_tokens",
            return_value={
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxLCJlbWFpbCI6InVuaXQudGVzdC5kdW1teUBtb2NrZGF0YS5jb20iLCJyb2xlIjpudWxsfSwiZXhwIjoxNzQyNTk0OTk0LCJqdGkiOiI2Y2JjNzlmNy04ZDYyLTRhMGEtOGQxYi1jNDkwZTE0NTYyN2UiLCJyZWZyZXNoIjpmYWxzZX0.C265YV2cwHe8sjgOPsPhy96NtvM6hyiflDU4mi-FrdQ",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxLCJlbWFpbCI6InVuaXQudGVzdC5kdW1teUBtb2NrZGF0YS5jb20iLCJyb2xlIjpudWxsfSwiZXhwIjoxNzQyNjc0MTk0LCJqdGkiOiI5YTNiYmFiYS00MzhhLTQ3YzktYTc4Yy1kNGUxNWI0NGRkOGUiLCJyZWZyZXNoIjp0cnVlfQ.BIv9216LruFkubDFRuh89a_DmO1qa8VqgyP-_b4lFAM",
            },
        )

        token = await UserService().authenticate_and_generate_token(
            email="captain.unit.test@example.com",
            password="Bookhive1234",
            session=mock_async_db_session,
        )

        assert token is not None
        assert "access_token" in token
        assert "refresh_token" in token
        assert isinstance(token["access_token"], str)
        assert isinstance(token["refresh_token"], str)
        mock_create_auth_tokens.assert_called_once_with(
            {"id": dummy_user.id, "email": dummy_user.email, "role": dummy_user.role}
        )

    @pytest.mark.asyncio
    async def test_authenticate_and_generate_token_user_not_found(
        self, mocker, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email", return_value=None
        )

        with pytest.raises(UserNotFoundException):
            _ = await UserService().authenticate_and_generate_token(
                email="captain.unit.test@example.com",
                password="Bookhive1234",
                session=mock_async_db_session,
            )

    @pytest.mark.asyncio
    async def test_authenticate_and_generate_token_incorrect_password(
        self, mocker, dummy_user, mock_async_db_session
    ):
        mocker.patch(
            "src.users.service.UserService.get_user_by_email", return_value=dummy_user
        )

        mocker.patch(
            "src.users.domains.UserProfile.verify_password", return_value=False
        )

        with pytest.raises(InvalidCredentials):
            _ = await UserService().authenticate_and_generate_token(
                email="captain.unit.test@example.com",
                password="Bookhive1234",
                session=mock_async_db_session,
            )

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, mocker, dummy_user_data):
        mock_generate_jwt_token = mocker.patch(
            "src.users.domains.UserProfile.generate_jwt_token",
            return_value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMCwiZW1haWwiOiJ0ZXN0LnRva2VuQGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NDI2NTM2MzAsImp0aSI6Ijg3YTNjMzU4LTBjZTgtNDQ5OC05ZDZjLWU0MmRhMDNmOTVjMCIsInJlZnJlc2giOmZhbHNlfQ.uNHFq3mpLzepUsmD2VzEjFLfXjcQiYCHuvITF2lVyrQ",
        )

        new_token = await UserService().refresh_token(dummy_user_data)

        assert new_token is not None
        mock_generate_jwt_token.assert_called_once()
        assert isinstance(new_token, str)
