from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from src.users.domains import UserProfile
from fastapi.exceptions import HTTPException


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def verify_token_type(self, token_data: dict) -> None:
        raise NotImplementedError("Please Implement in Child Classes")

    async def get_token_data(self, token):
        return UserProfile.decode_token(token)

    async def validate_token(self, token: str) -> bool:
        token_data = await self.get_token_data(token)

        if token_data is not None:
            return True
        else:
            return False

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not await self.validate_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or has expired.",
            )

        token_data = await self.get_token_data(token)

        await self.verify_token_type(token_data)

        return token_data


class AccessTokenBearer(TokenBearer):
    async def verify_token_type(self, token_data: dict) -> None:
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: Please provide an access token instead of a refresh token.",
            )


class RefreshTokenBearer(TokenBearer):
    async def verify_token_type(self, token_data: dict) -> None:
        if not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: Please provide a refresh token instead of an access token.",
            )
