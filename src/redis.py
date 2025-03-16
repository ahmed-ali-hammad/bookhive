import redis.asyncio as redis
from src.config import settings

JTI_EXPIRY = 3600

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


async def add_jti_to_blocklist(jti: str) -> None:
    """
    Adds a JWT ID (JTI) to the blocklist in Redis.

    This function stores the JWT ID (JTI) in Redis with an expiry time to ensure that
    the token associated with the JTI is considered revoked and cannot be used again.

    Parameters:
    - jti (str): The JWT ID that uniquely identifies the token to be revoked.

    Returns:
    - None: This function does not return any value. It performs an asynchronous operation
      to store the JTI in Redis with an expiry time.

    Notes:
    - The JTI is stored with an empty value, and the expiry time is defined by the `JTI_EXPIRY` constant.
    """
    await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)


async def is_jti_in_blocklist(jti: str) -> bool:
    """
    Checks if a JWT ID (JTI) is present in the blocklist in Redis.

    This function queries Redis to determine if the given JWT ID (JTI) has been added to the
    blocklist, indicating that the associated token has been revoked.

    Parameters:
    - jti (str): The JWT ID to check in the blocklist.

    Returns:
    - bool: Returns `True` if the JTI is found in the blocklist (indicating the token is revoked),
            or `False` if the JTI is not present.
    """
    jti = await redis_client.get(jti)
    return jti is not None
