from datetime import timedelta
import os
from typing import Any, TypeVar
from cache.manager import CacheSessionManager

T = TypeVar("T")
__CACHE_URL = os.getenv("CACHE_URL") or "redis://localhost:6379/0"
CACHE = CacheSessionManager(__CACHE_URL)

async def aget_cache(key: str, klass: type[T] | None = None):
    """
        Get object from cache
        :param key: key used to store object
        :param model: type of object
        :return: deserialized object
    """
    return await CACHE.aget(key=key, klass=klass)

async def aset_cache(key: str, value: Any, expire: int | timedelta | None = None):
    """
        Store object in cache
        :param key: key used to store
        :param value: object to store
        :param expire: object expired after ``expire`` seconds
    """
    await CACHE.aset(key=key, value=value, expire=expire)