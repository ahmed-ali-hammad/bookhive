from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    REDIS_HOST: str
    REDIS_PORT: int = 6379


settings = Settings()
