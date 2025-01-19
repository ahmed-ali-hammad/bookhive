import datetime
import logging
import uuid

import jwt
from passlib.context import CryptContext

from src.config import settings


class UserProfile:
    myctx = CryptContext(schemes=["sha256_crypt"])
    JWT_ALGORITHM = "HS256"

    @staticmethod
    def hash_password(password):
        password_hash = UserProfile.myctx.hash(password)
        return password_hash

    @staticmethod
    def verify_password(password, password_hash: str):
        return UserProfile.myctx.verify(password, password_hash)

    @staticmethod
    def create_token(
        user_data: dict, expiry: datetime.timedelta = 3600, refresh: bool = False
    ) -> str:
        payload = {
            "user": user_data,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=expiry),
            "jti": str(uuid.uuid4()),
            "refresh": refresh,
        }

        token = jwt.encode(
            payload=payload,
            key=settings.JWT_SECRET,
            algorithm=UserProfile.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            token_data = jwt.decode(
                jwt=token,
                key=settings.JWT_SECRET,
                algorithms=[UserProfile.JWT_ALGORITHM],
            )

            return token_data

        except jwt.exceptions.ExpiredSignatureError:
            logging.warning("Expired Token")

        except jwt.PyJWTError as ex:
            logging.exception(ex)

            return None
