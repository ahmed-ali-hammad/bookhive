from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.domains import UserProfile
from src.users.exceptions import IncorrectPasswordException, UserNotFoundException
from src.users.models import User
from src.users.schemas import UserCreateModel


class UserService:
    async def get_user(self, email: EmailStr, session: AsyncSession) -> User:
        statement = select(User).where(User.email == email)

        results = await session.exec(statement)

        return results.first()

    async def create_new_user(self, user_data: UserCreateModel, session: AsyncSession):
        # Check if user exists
        if await self.get_user(user_data.email, session) is not None:
            return False

        # Hash the password and prepare user data
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = UserProfile.hash_password(user_dict["password"])

        # Remove password field and create User object
        user_dict.pop("password")
        user = User(**user_dict)
        session.add(user)
        await session.commit()

        return user

    async def create_token(self, email):
        access_token = UserProfile.create_token(email=email, expiry=10 * 60)
        refresh_token = UserProfile.create_token(
            email=email, expiry=24 * 60 * 60, refresh=True
        )

        token = {"access_token": access_token, "refresh_token": refresh_token}

        return token

    async def generate_token(self, email, password, session):
        user = await self.get_user(email, session)
        if not user:
            raise UserNotFoundException

        is_password_verified = UserProfile.verify_password(password, user.password_hash)

        if not is_password_verified:
            raise IncorrectPasswordException

        token = await self.create_token(email=email)

        return token

    async def refresh_token(self, email):
        new_token = UserProfile.create_token(email=email, expiry=10 * 60)

        return new_token
