from typing import Optional, Any
import aioredis
import json
from datetime import datetime
from config.settings.base import Settings

settings = Settings()

class CacheManager:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.default_ttl = 3600  # 1 hour

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, datetime):
            value = value.isoformat()
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl or self.default_ttl
        )

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def clear_pattern(self, pattern: str):
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)