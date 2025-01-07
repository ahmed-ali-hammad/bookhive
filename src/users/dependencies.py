from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from src.users.domains import UserProfile
from fastapi.exceptions import HTTPException


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def get_token_data(self, token):
        return UserProfile.decode_token(token)

    async def validate_toke(self, token: str) -> bool:
        token_data = await self.get_token_data(token)

        if token_data is not None:
            return True
        else:
            return False

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not await self.validate_toke(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or has expired.",
            )

        token_data = await self.get_token_data(token)

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: Please provide an access token instead of a refresh token.",
            )

        return token_data["user"]
