import pytest

auth_prefix = f"/api/users"


class TestRoutes:
    @pytest.mark.asyncio
    async def test_user_creation_success(self, test_client):
        signup_data = {
            "username": "test.user",
            "email": "test.user@bookhive.de",
            "password": "Bookhive1234",
        }

        response = test_client.post(url=f"{auth_prefix}/signup", json=signup_data)

        assert response.status_code == 201

        assert response.json() == {
            "username": "test.user",
            "email": "test.user@bookhive.de",
            "first_name": None,
            "last_name": None,
            "is_verified": False,
            "role": "user",
            "created_at": "2025-03-09T11:52:53.184611",
            "updated_at": "2025-03-09T11:52:53.184615",
        }
