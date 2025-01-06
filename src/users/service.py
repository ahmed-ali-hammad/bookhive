from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.models import User
from sqlmodel import select

from src.users.schemas import UserCreateModel
from src.users.domains import UserDomain

from pydantic import EmailStr

from src.users.exceptions import UserNotFoundException, IncorrectPasswordException


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
        user_dict["password_hash"] = UserDomain(**user_dict).hash_password()

        # Remove password field and create User object
        user_dict.pop("password")
        user = User(**user_dict)
        session.add(user)
        await session.commit()

        return user

    async def get_token(self, email, password, session):
        user = await self.get_user(email, session)
        if not user:
            raise UserNotFoundException

        user_domain = UserDomain(user.username, user.email, password)

        is_user_verified = user_domain.verify_password(user.password_hash)

        if not is_user_verified:
            raise IncorrectPasswordException

        access_token = user_domain.create_token()
        refresh_token = user_domain.create_token(expiry=24 * 60 * 60, refresh=True)

        token = {"access_token": access_token, "refresh_token": refresh_token}

        return token
