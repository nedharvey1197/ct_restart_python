from typing import Optional, Any, List, Dict
import json
from datetime import datetime, timedelta
from redis.asyncio import Redis
from ..config.settings import get_settings

settings = get_settings()

class CacheService:
    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
        self.default_ttl = 3600  # 1 hour

    async def get_trial_analytics(self, company_id: str) -> Optional[dict]:
        """Get cached trial analytics."""
        key = f"trial_analytics:{company_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set_trial_analytics(self, company_id: str, analytics: dict, ttl: int = None):
        """Cache trial analytics."""
        key = f"trial_analytics:{company_id}"
        await self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(analytics)
        )

    async def get_trials(self, company_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached trials for company."""
        key = f"company_trials:{company_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set_trials(self, company_id: str, trials: List[Dict[str, Any]]):
        """Cache trials for company."""
        key = f"company_trials:{company_id}"
        await self.redis.setex(key, self.default_ttl, json.dumps(trials))

    async def get_analysis(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get cached analysis data."""
        key = f"analysis:{company_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set_analysis(
        self, 
        company_id: str, 
        analysis_data: Dict[str, Any],
        ttl: Optional[int] = None
    ):
        """Cache analysis data with TTL."""
        key = f"analysis:{company_id}"
        await self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(analysis_data)
        )

    async def invalidate_analysis(self, company_id: str):
        """Invalidate cached analysis."""
        key = f"analysis:{company_id}"
        await self.redis.delete(key)

    async def close(self):
        """Close Redis connection."""
        await self.redis.close() 