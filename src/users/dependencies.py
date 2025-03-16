from typing import Union

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.redis import is_jti_in_blocklist
from src.users.domains import UserProfile
from src.users.models import User
from src.users.service import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    """
    A custom authentication class for handling token-based authentication.
    """

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def verify_token_type(self) -> None:
        """
        Verify the type of the token.

        This method must be implemented in child classes to enforce specific token types.
        Raises:
        - NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("Please Implement in Child Classes")

    async def get_token_data(self, token: str) -> dict | None:
        """
        Decode the token and extract its payload.

        Parameters:
        - token (str): The encoded JWT token.

        Returns:
        - dict | None: The decoded token data if valid, otherwise None.
        """
        return UserProfile.decode_token(token)

    async def validate_token(self, token: str) -> bool:
        """
        Validate the token's authenticity.

        Parameters:
        - token (str): The encoded JWT token.

        Returns:
        - bool: True if the token is valid, otherwise False.
        """
        token_data = await self.get_token_data(token)

        if token_data is not None:
            return True
        else:
            return False

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        """
        Process authentication for incoming requests.

        Extracts and validates the token, checks if it has been revoked, and ensures
        it meets the required type.

        Parameters:
        - request (Request): The incoming request.

        Returns:
        - dict: The decoded token data if authentication is successful.

        Raises:
        - HTTPException (403): If the token is invalid, expired, or revoked.
        """
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
    """
    A subclass of TokenBearer specifically for handling access tokens.

    This class ensures that only access tokens (not refresh tokens) are used
    for authentication."
    """

    async def verify_token_type(self, token_data: dict) -> None:
        """
        Verify that the provided token is an access token.

        This method checks if the token is mistakenly a refresh token and raises
        an exception if so.

        Parameters:
        - token_data (dict): The decoded token payload.

        Raises:
        - HTTPException (403): If the token is a refresh token instead of an access token.
        """
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: Please provide an access token instead of a refresh token.",
            )


class RefreshTokenBearer(TokenBearer):
    """
    A subclass of TokenBearer specifically for handling refresh tokens.

    This class ensures that only refresh tokens are used for generating/refreshing acess tokens.
    """

    async def verify_token_type(self, token_data: dict) -> None:
        """
        Verify that the provided token is a refresh token.

        This method checks if the token is mistakenly an access token and raises
        an exception if so.

        Parameters:
        - token_data (dict): The decoded token payload.

        Raises:
        - HTTPException (403): If the token is an access token instead of a refresh token.
        """
        if not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: Please provide a refresh token instead of an access token.",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Retrieve the current authenticated user based on the provided access token.

    This function extracts the user's email from the token details and fetches
    the corresponding user from the database. If the user does not exist, an
    HTTPException is raised.

    Parameters:
    - token_details (dict): The details extracted from the access token, which includes user information.
    - session (AsyncSession): The database session to query for the user.

    Returns:
    - User: The user object corresponding to the email provided in the token.

    Raises:
    - HTTPException (404): If the user does not exist in the database.
    """
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)

    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exists")
    return user


class RoleChecker:
    """
    A class to check if the current user has one of the allowed roles.

    This class is used to enforce role-based access control (RBAC) by verifying
    that the user’s role is included in a predefined list of allowed roles.
    """

    def __init__(self, allowed_roles: list) -> None:
        self.allowed_roles = allowed_roles

    def __call__(
        self, current_user: User = Depends(get_current_user)
    ) -> Union[bool, Exception]:
        """
        Check if the current user has one of the allowed roles.

        This method is invoked to verify if the current user's role is in the
        list of allowed roles. If the user’s role is found in the allowed roles,
        the method returns True, indicating that the user has the necessary role
        to access the resource. Otherwise, an HTTPException is raised.

        Parameters:
        - current_user (User): The current authenticated user.

        Returns:
        - bool: True if the current user has a valid role.

        Raises:
        - HTTPException (403): If the current user does not have one of the allowed roles.
        """
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access. You lack the necessary role to access this resource.",
        )
