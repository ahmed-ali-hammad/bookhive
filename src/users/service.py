from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.exceptions import InvalidCredentials, UserAlreadyExists, UserNotFoundException
from src.users.domains import UserProfile
from src.users.models import User
from src.users.schemas import UserCreateModel


class UserService:
    """
    A service class for managing user-related operations, including authentication,
    user retrieval, and token management.
    """

    async def get_user_by_email(self, email: EmailStr, session: AsyncSession) -> User:
        """
        Retrieve a user by their email address.

        Parameters:
        - email (EmailStr): The email of the user to fetch.
        - session (AsyncSession): The database session.

        Returns:
        - User: The user object if found, otherwise None.
        """
        statement = select(User).where(User.email == email)
        results = await session.exec(statement)
        return results.first()

    async def get_user_by_id(self, id: int, session: AsyncSession) -> User:
        """
        Retrieve a user by their unique ID.

        Parameters:
        - id (int): The ID of the user.
        - session (AsyncSession): The database session.

        Returns:
        - User: The user object if found, otherwise None.
        """
        statement = select(User).where(User.id == id)
        results = await session.exec(statement)
        return results.first()

    async def create_new_user(
        self, user_data: UserCreateModel, session: AsyncSession
    ) -> User:
        """
        Create a new user in the system.

        This method first checks if a user with the given email already exists.
        If not, it hashes the password, removes it from the stored data, and creates a new user.

        Parameters:
        - user_data (UserCreateModel): The data required to create a new user.
        - session (AsyncSession): The database session.

        Returns:
        - User: The newly created user object.

        Raises:
        - UserAlreadyExists: If a user with the given email already exists.
        """
        # Check if user exists
        if await self.get_user_by_email(user_data.email, session) is not None:
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
        """
        Creates an access token and refresh token for a user.

        Parameters:
        - user_data (dict): User information to encode into the tokens.

        Returns:
        - dict: A dictionary containing both access and refresh tokens.
        """
        access_token = UserProfile.create_token(user_data, 120 * 60)
        refresh_token = UserProfile.create_token(user_data, 24 * 60 * 60, True)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def authenticate_and_generate_token(self, email, password, session) -> dict:
        """
        Authenticate a user and generate a token if credentials are valid.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.
        - session (AsyncSession): The database session.

        Returns:
        - dict: A dictionary containing the access and refresh tokens.

        Raises:
        - UserNotFoundException: If no user is found with the given email.
        - InvalidCredentials: If the provided password is incorrect.
        """
        user = await self.get_user_by_email(email, session)
        if not user:
            raise UserNotFoundException

        is_password_verified = UserProfile.verify_password(password, user.password_hash)
        if not is_password_verified:
            raise InvalidCredentials

        user_data = {"id": user.id, "email": email, "role": user.role}
        token = await self.create_token(user_data)

        return token

    async def refresh_token(self, user_data: dict) -> str:
        """
        Generate a new access token using existing user data.

        Parameters:
        - user_data (dict): The user's existing authentication data.

        Returns:
        - str: The newly generated access token.
        """
        new_token = UserProfile.create_token(user_data=user_data, expiry=10 * 60)
        return new_token
