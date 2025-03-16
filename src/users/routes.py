from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app_logging import LoggingConfig
from src.db.main import get_session
from src.exceptions import InvalidCredentials, UserAlreadyExists, UserNotFoundException
from src.redis import add_jti_to_blocklist
from src.users.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
)
from src.users.schemas import UserAuthModel, UserBookModel, UserCreateModel, UserModel
from src.users.service import UserService

user_router = APIRouter()
role_checker = RoleChecker(["admin", "user"])
logger = LoggingConfig.get_logger(__name__)


@user_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
        404: {"description": "User not found"},
    },
)
async def get_current_logged_in_user(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(AccessTokenBearer()),
    user_service: UserService = Depends(UserService),
    _: Union[bool, Exception] = Depends(role_checker),
) -> UserBookModel:
    """
    Retrieve the currently authenticated user's profile.

    This endpoint returns the details of the user associated with the provided authentication token.
    If the user does not exist, an HTTP 404 error is returned.

    Args:
        session (AsyncSession): Database session dependency.
        token_details (dict): Token details extracted from the request.
        user_service (UserService): Service for handling user-related operations.
        _ (Union[bool, Exception]): Role checker dependency to ensure the user has the required role.

    Returns:
        UserBookModel: The authenticated user's profile data.

    Raises:
        HTTPException:
            - 403: If the user is not authenticated.
            - 400: If the request is invalid.
            - 404: If the user is not found.
            - 500: If an unexpected error occurs.
    """
    try:
        user = await user_service.get_user(token_details["user"]["email"], session)
        if user is None:
            raise HTTPException(status_code=404, detail="User doesn't exists")
        return user
    except HTTPException as http_ex:
        # Not the best approach—needs improvement.
        raise http_ex
    except Exception as ex:
        logger.error(
            f"Error occurred while retrieving the current logged-in user. Exception: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@user_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel,
    responses={
        409: {"description": "User already exists"},
    },
)
async def create_user(
    user_data: UserCreateModel,
    user_service: UserService = Depends(UserService),
    session: AsyncSession = Depends(get_session),
):
    """
    Creates a new user.

    It returns the created user model upon success.
    If the user already exists, a 409 Conflict response is returned.
    In case of any other error, a 500 Internal Server Error response is returned.

    Args:
        user_data (UserCreateModel): The data required to create a new user.
        user_service (UserService): The service responsible for handling user creation logic.
        session (AsyncSession): The database session used to interact with the database.

    Returns:
        UserModel: The created user model.

    Responses:
        201: User successfully created.
        409: The user already exists.
        500: An internal server error occurred.
    """
    logger.info(f"Attempting to create user: '{user_data.email}'")
    try:
        user = await user_service.create_new_user(user_data, session)
        logger.info(f"User '{user.email}' was successfully created.")
        return user
    except UserAlreadyExists:
        logger.warning(
            f"User creation failed: user '{user_data.email}' already exists."
        )
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as ex:
        logger.error(
            f"An error occurred while creating a new user. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, user is not created",
        )


@user_router.post(
    "/auth/token",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User not found"},
        401: {"description": "Incorrect password"},
        400: {"description": "Bad Request"},
    },
)
async def generate_token(
    auth_data: UserAuthModel,
    user_service: UserService = Depends(UserService),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Generates an authentication token for a user.

    This endpoint authenticates a user by verifying their email and password.
    If successful, it returns an authentication token.
    If the user is not found or the credentials are incorrect, appropriate HTTP errors are returned.

    Args:
        auth_data (UserAuthModel): The email and password required for authentication.
        user_service (UserService): The service responsible for generating the authentication token.
        session (AsyncSession): The database session used to interact with the database.

    Returns:
        dict: A dictionary containing the generated authentication token.

    Responses:
        200: Token successfully generated.
        401: Incorrect password provided.
        404: User not found.
        500: Internal server error occurred.
    """
    try:
        token = await user_service.generate_token(
            email=auth_data.email, password=auth_data.password, session=session
        )
        return token
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while generating a token for user '{auth_data.email}'. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@user_router.post(
    "/auth/refresh-token",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def refresh_token(
    token_data: dict = Depends(RefreshTokenBearer()),
    user_service: UserService = Depends(UserService),
) -> dict:
    """
    Refresh the authentication token.

    This endpoint validates the provided refresh token and issues a new access token.

    Parameters:
    - token_data (dict): The decoded refresh token data, containing user information.
    - user_service (UserService): A dependency for handling user authentication services.

    Returns:
    - dict: A dictionary containing the new access token.

    Raises:
    - HTTPException (403): If the refresh token is invalid.
    - HTTPException (400): If the request is invalid.
    - HTTPException (500): If an unexpected error occurs.
    """
    try:
        user_data = token_data["user"]
        new_token = await user_service.refresh_token(user_data=user_data)

        return {"access_token": new_token}
    except Exception as ex:
        logger.error(
            f"An error occurred while refreshing a token for user '{token_data['user']['email']}'. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, couldn't generate a new access token",
        )


@user_router.get(
    "/auth/token/revoke",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def revoke_token(token_data: dict = Depends(AccessTokenBearer())) -> dict:
    """
    Revoke access token to log out a user.

    This endpoint invalidates the provided access token by adding its unique identifier (JTI)
    to the blocklist, effectively logging the user out.

    Parameters:
    - token_data (dict): The decoded access token data, containing the JTI (unique token identifier).

    Returns:
    - dict: A message indicating successful logout.

    Raises:
    - HTTPException (403): If the user is not authenticated.
    - HTTPException (400): If the request is invalid.
    - HTTPException (500): If an unexpected error occurs while revoking the token.
    """
    try:
        jti = token_data["jti"]
        await add_jti_to_blocklist(jti)
        return {"Message": "Logged out successfuly"}
    except Exception as ex:
        logger.error(
            f"An error occurred while revoking a token for user '{token_data['user']['email']}'. Exception details: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, couldn't revoke token",
        )
