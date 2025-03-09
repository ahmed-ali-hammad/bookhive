from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.exceptions import InvalidCredentials, UserNotFoundException
from src.redis import add_jti_to_blocklist
from src.users.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from src.users.models import User
from src.users.schemas import UserAuthModel, UserBookModel, UserCreateModel, UserModel
from src.users.service import UserService

user_router = APIRouter()
role_checker = RoleChecker(["admin", "user"])


@user_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def get_current_user(
    user: User = Depends(get_current_user),
    _: Union[bool, Exception] = Depends(role_checker),
) -> UserBookModel:
    return user


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
    user = await user_service.create_new_user(user_data, session)

    if not user:
        raise HTTPException(status_code=409, detail="User already exists")

    return user


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
    """Login endpoint"""
    try:
        token = await user_service.generate_token(
            email=auth_data.email, password=auth_data.password, session=session
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    return token


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
    user_data = {"email": token_data["user"]["email"]}
    new_token = await user_service.refresh_token(user_data=user_data)

    return {"access_token": new_token}


@user_router.get(
    "/auth/token/revoke",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
    },
)
async def revoke_token(token_data: dict = Depends(AccessTokenBearer())) -> dict:
    """Logout endpoint"""
    jti = token_data["jti"]

    await add_jti_to_blocklist(jti)

    return {"Message": "Logged out successfuly"}
