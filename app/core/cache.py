import json
from cachetools import TTLCache
from redis.asyncio.client import Redis
from redis.asyncio.utils import from_url
from redis.exceptions import RedisError
from typing import Callable, Any, TypeVar, Coroutine
from pydantic import BaseModel, ValidationError
from functools import wraps
from .config import settings
from .logger import logger

T = TypeVar("T", bound=BaseModel)

# Local cache
local_cache: TTLCache[str, Any] = TTLCache(maxsize=1000, ttl=300)

# Redis client
REDIS_URL: str = settings.REDIS_URL
redis_client: Redis | None = None
try:
    if REDIS_URL:
        redis_client = from_url(REDIS_URL, decode_responses=True)
        logger.info("Success initialize Redis client. Redis cache will be enabled.")
    else:
        logger.warning("REDIS_URL not set or missing. Redis cache will be disabled.")
except RedisError as e:
    logger.error(f"Failed to initialize Redis client: {e}. Redis cache will be disabled.")

async def redis_set(key: str, value: Any, ttl: int = 3600):
    if not redis_client:
        return False
    try:
        await redis_client.set(key, json.dumps(value), ex=ttl)
        return True
    except RedisError as e:
        logger.error(f"Could not save key '{key}' to Redis: {e}")
        return False

async def redis_get(key: str):
    if not redis_client:
        return None
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return json.loads(value)
    except RedisError as e:
        logger.error(f"Could not retrieve key '{key}' from Redis: {e}")
        return None

async def redis_delete(key: str):
    if not redis_client:
        return
    try:
        return await redis_client.delete(key)
    except RedisError as e:
        logger.error(f"Could not delete key '{key}' from Redis: {e}")
        return

def use_cachetools_hybrid(
    key_builder: Callable[..., str],
    model_cls: type[T],
    prefix: str = "cache",
    ttl: int = 3600
) -> Callable[
    [Callable[..., Coroutine[Any, Any, Any]]],
    Callable[..., Coroutine[Any, Any, T]]
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, Any]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_key = f"{prefix}:{key_builder(*args, **kwargs)}"
            if cache_key in local_cache:
                logger.debug(f"Local cache hit for key: {cache_key}")
                try:
                    return model_cls.model_validate(local_cache[cache_key])
                except ValidationError as e:
                    logger.warning(
                        f"Invalid data in local cache of key '{cache_key}': {e.errors()}"
                    )
                    del local_cache[cache_key]
            if cache := await redis_get(cache_key):
                logger.debug(f"Redis cache hit for key: {cache_key}")
                try:
                    validated_data = model_cls.model_validate(cache)
                    local_cache[cache_key] = validated_data.model_dump()
                    return validated_data
                except ValidationError as e:
                    logger.warning(
                        f"Invalid data in Redis cache of key '{cache_key}': {e.errors()}"
                    )
                    await redis_delete(cache_key)
            logger.debug(f"Cache miss for key: {cache_key}. Executing services")
            result = await func(*args, **kwargs)
            validated_result = model_cls.model_validate(result)
            local_cache[cache_key] = validated_result.model_dump()
            if await redis_set(cache_key, result, ttl):
                logger.debug(f"Saved to Redis cache: {cache_key}")
            return validated_result

        return wrapper

    return decorator
