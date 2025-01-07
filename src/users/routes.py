from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.schemas import UserCreateModel, UserModel, UserAuthModel

from src.db.main import get_session
from src.users.service import UserService
from src.users.exceptions import UserNotFoundException, IncorrectPasswordException
from src.users.dependencies import RefreshTokenBearer

user_router = APIRouter()

user_service = UserService()


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
) -> UserModel:
    user = await user_service.create_new_user(user_data, session)

    if not user:
        raise HTTPException(status_code=409, detail="User already exists")

    return user


@user_router.post("/auth/token", status_code=status.HTTP_200_OK)
async def generate_token(
    auth_data: UserAuthModel, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        token = await user_service.generate_token(
            email=auth_data.email, password=auth_data.password, session=session
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except IncorrectPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    return token


@user_router.post("/auth/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(
    token_data: dict = Depends(RefreshTokenBearer()),
) -> dict:
    
    user_email = token_data["user"]["email"]
    new_token = await user_service.refresh_token(email=user_email)
    
    return {"access_token": new_token}
