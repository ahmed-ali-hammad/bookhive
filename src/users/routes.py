from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.schemas import UserCreateModel, UserModel

from src.db.main import get_session
from src.users.service import UserService

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
