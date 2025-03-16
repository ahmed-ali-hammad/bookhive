from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import InvalidCredentials, UserAlreadyExists, UserNotFoundException
from src.users.domains import UserProfile
from src.users.models import User
from src.users.schemas import UserCreateModel


class UserService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    async def get_user(self, email: EmailStr, session: AsyncSession) -> User:
        statement = select(User).where(User.email == email)

        results = await session.exec(statement)

        return results.first()

    async def get_user_by_id(self, id: int, session: AsyncSession) -> User:
        statement = select(User).where(User.id == id)

        results = await session.exec(statement)

        return results.first()

    async def create_new_user(self, user_data: UserCreateModel, session: AsyncSession):
        # Check if user exists
        if await self.get_user(user_data.email, session) is not None:
            raise UserAlreadyExists

        # Hash the password and prepare user data
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = UserProfile.hash_password(user_dict["password"])

        # Remove password field and create User object
        user_dict.pop("password")
        user = User(**user_dict)
        session.add(user)
        await session.commit()

        return user

    async def create_token(self, user_data: dict) -> dict:
        access_token = UserProfile.create_token(user_data, 120 * 60)
        refresh_token = UserProfile.create_token(user_data, 24 * 60 * 60, True)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def generate_token(self, email, password, session):
        user = await self.get_user(email, session)
        if not user:
            raise UserNotFoundException

        is_password_verified = UserProfile.verify_password(password, user.password_hash)

        if not is_password_verified:
            raise InvalidCredentials

        user_data = {"id": user.id, "email": email, "role": user.role}

        token = await self.create_token(user_data)

        return token

    async def refresh_token(self, user_data: dict) -> str:
        new_token = UserProfile.create_token(user_data=user_data, expiry=10 * 60)

        return new_token
