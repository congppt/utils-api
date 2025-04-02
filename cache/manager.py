import json
from datetime import timedelta
from typing import Any, TypeVar

from pydantic import BaseModel
from pydantic_core import from_json, to_jsonable_python
from redis.asyncio import StrictRedis

T = TypeVar("T")


class CacheSessionManager:
    def __init__(self, url: str):
        self._redis = StrictRedis.from_url(url)

    async def aclose(self):
        """Close all connections including in-use connections."""
        await self._redis.aclose()

    async def aget(self, key: str, klass: type[T] | None = None):
        """
        Get object from cache
        :param key: key used to store object
        :param model: type of object
        :return: deserialized object
        """
        value = await self._redis.get(name=key)
        if value:
            obj = from_json(data=value)
            if not klass:
                return obj
            if issubclass(klass, BaseModel):
                return klass.model_validate(obj)
            return klass.__init__(obj)
        return None

    async def aset(self, key: str, value: Any, expire: int | timedelta | None = None):
        """
        Store object in cache
        :param key: key used to store
        :param value: object to store
        :param expire: object expired after ``expire`` seconds
        """
        value = json.dumps(to_jsonable_python(value))
        await self._redis.set(name=key, value=value, ex=expire)
