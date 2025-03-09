from typing import Union

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.exceptions import UserNotFoundException
from src.redis import is_jti_in_blocklist
from src.users.domains import UserProfile
from src.users.models import User
from src.users.service import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def verify_token_type(self) -> None:
        raise NotImplementedError("Please Implement in Child Classes")

    async def get_token_data(self, token: str) -> dict | None:
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
        token_data = await self.get_token_data(token)

        if not await self.validate_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or has expired.",
            )

        if await is_jti_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token has been revoked",
                    "resolution": "Please get a new token",
                },
            )

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


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> User:
    user_email = token_details["user"]["email"]

    user = await user_service.get_user(user_email, session)

    if user is None:
        raise UserNotFoundException

    return user


class RoleChecker:
    def __init__(self, allowed_roles: list) -> None:
        self.allowed_roles = allowed_roles

    def __call__(
        self, current_user: User = Depends(get_current_user)
    ) -> Union[bool, Exception]:
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access. You lack the necessary role to access this resource.",
        )
