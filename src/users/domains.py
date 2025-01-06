from passlib.context import CryptContext
from src.config import settings
import jwt
import datetime
import uuid
import logging


class UserDomain:
    myctx = CryptContext(schemes=["sha256_crypt"])
    JWT_ALGORITHM = "HS256"

    def __init__(self, username, email, password, first_name=None, last_name=None):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def hash_password(self):
        password_hash = UserDomain.myctx.hash(self.password)
        return password_hash

    def verify_password(self, password_hash: str):
        return UserDomain.myctx.verify(self.password, password_hash)

    def create_token(self, expiry: datetime.timedelta = 3600, refresh: bool = False):
        payload = {
            "user": {"email": self.email},
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry),
            "jti": str(uuid.uuid4),
            "refresh": refresh,
        }

        token = jwt.encode(
            payload=payload, key=settings.JWT_SECRET, algorithm=UserDomain.JWT_ALGORITHM
        )

        return token

    def decode_token(self, token: str) -> dict:
        try:
            token_data = jwt.decode(
                jwt=token, key=settings.JWT_SECRET, algorithm=[UserDomain.JWT_ALGORITHM]
            )

            return token_data

        except jwt.PyJWTError as ex:
            logging.exception(ex)

            return None
