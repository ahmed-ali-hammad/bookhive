import redis.asyncio as redis
from src.config import settings

JTI_EXPIRY = 3600

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


async def add_jti_to_blocklist(jti: str) -> None:
    await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)


async def is_jti_in_blocklist(jti: str) -> bool:
    jti = await redis_client.get(jti)
    return jti is not None
