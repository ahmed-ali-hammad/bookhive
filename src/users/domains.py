import datetime
import uuid

import jwt
from passlib.context import CryptContext

from src.app_logging import LoggingConfig
from src.config import settings

logger = LoggingConfig.get_logger(__name__)


class UserProfile:
    """
    A class for handling user authentication-related operations, including password hashing,
    verification, and JWT token creation/decoding.

    Attributes:
        myctx (CryptContext): A cryptographic context for password hashing and verification.
        JWT_ALGORITHM (str): The algorithm used for JWT token encoding and decoding.
    """

    myctx = CryptContext(schemes=["sha256_crypt"])
    JWT_ALGORITHM = "HS256"

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a given password using sha256_crypt.

        Args:
            password (str): The plain text password.

        Returns:
            str: The hashed password.
        """
        password_hash = UserProfile.myctx.hash(password)
        return password_hash

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verifies a password against its hashed version.

        Args:
            password (str): The plain text password.
            password_hash (str): The hashed password to verify against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return UserProfile.myctx.verify(password, password_hash)

    @staticmethod
    def generate_jwt_token(
        user_data: dict,
        expiry: datetime.timedelta = 3600,
        refresh: bool = False,
        secret_key: str = settings.JWT_SECRET,
    ) -> str:
        """
        Creates a JWT token for authentication.

        Args:
            user_data (dict): The user-related data to be included in the token.
            expiry (datetime.timedelta, optional): Token expiry time in seconds. Defaults to 3600 seconds (1 hour).
            refresh (bool, optional): Indicates if the token is a refresh token. Defaults to False.

        Returns:
            str: The generated JWT token.
        """
        payload = {
            "user": user_data,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=expiry),
            "jti": str(uuid.uuid4()),
            "refresh": refresh,
        }

        token = jwt.encode(
            payload=payload,
            key=secret_key,
            algorithm=UserProfile.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode_token(token: str, secret_key: str = settings.JWT_SECRET) -> dict | None:
        """
        Decodes and validates a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token data if valid.
            None: If the token is expired or invalid.

        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.PyJWTError: If the token is invalid.
        """
        try:
            token_data = jwt.decode(
                jwt=token,
                key=secret_key,
                algorithms=[UserProfile.JWT_ALGORITHM],
            )
            return token_data
        except jwt.exceptions.ExpiredSignatureError:
            logger.warning(f"Token is Expired: {token}")
        except jwt.PyJWTError as ex:
            logger.error(f"Failed to decode JWT token due to an error. Exception: {ex}")
            return None
        except Exception:
            logger.exception("Unexpected error while decoding JWT token")
            return None
