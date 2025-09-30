"""Redis caching system with in-memory fallback"""
import redis
import json
import hashlib
import os
import time
from typing import Optional, Any, Dict
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_stats = {"hits": 0, "misses": 0, "sets": 0}

        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            self.redis_client = redis.from_url(
                redis_url,
                socket_connect_timeout=2,
                socket_timeout=2,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            print("[OK] Redis connected successfully")
        except Exception as e:
            print(f"[WARN] Redis not available: {e}")
            print("[INFO] Using in-memory cache fallback")
            self.redis_client = None

    def get_cache_key(self, prompt: str, operation: str = "generate") -> str:
        """Generate cache key from prompt"""
        key_data = f"{operation}:{prompt}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]

    def get(self, key: str) -> Optional[Any]:
        """Get cached result"""
        if self.redis_client:
            try:
                cached = self.redis_client.get(f"prompt:{key}")
                if cached:
                    self._cache_stats["hits"] += 1
                    return json.loads(cached)
            except Exception:
                pass

        # Check memory cache with TTL
        if key in self._memory_cache:
            cache_entry = self._memory_cache[key]
            if cache_entry["expires"] > time.time():
                self._cache_stats["hits"] += 1
                return cache_entry["value"]
            else:
                # Expired, remove it
                del self._memory_cache[key]

        self._cache_stats["misses"] += 1
        return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Cache result with TTL (default 1 hour)"""
        self._cache_stats["sets"] += 1

        if self.redis_client:
            try:
                self.redis_client.setex(
                    f"prompt:{key}",
                    ttl,
                    json.dumps(value, default=str)
                )
                return True
            except Exception:
                pass

        # Memory cache with TTL
        self._memory_cache[key] = {
            "value": value,
            "expires": time.time() + ttl
        }

        # Clean up expired entries periodically
        if len(self._memory_cache) % 100 == 0:
            self._cleanup_expired()

        return True

    def cached_generate(self, prompt: str, generator_func):
        """Cache wrapper for generate operations"""
        cache_key = self.get_cache_key(prompt, "generate")

        # Try cache first
        cached_result = self.get(cache_key)
        if cached_result:
            return cached_result

        # Generate and cache
        result = generator_func(prompt)
        self.set(cache_key, result)
        return result

    def _cleanup_expired(self):
        """Remove expired entries from memory cache"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._memory_cache.items()
            if entry["expires"] <= current_time
        ]
        for key in expired_keys:
            del self._memory_cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self._cache_stats["hits"] + self._cache_stats["misses"]
        hit_rate = (self._cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "cache_type": "Redis" if self.redis_client else "Memory",
            "hits": self._cache_stats["hits"],
            "misses": self._cache_stats["misses"],
            "sets": self._cache_stats["sets"],
            "hit_rate_percent": round(hit_rate, 2),
            "memory_cache_size": len(self._memory_cache),
            "redis_connected": self.redis_client is not None
        }

    def clear_cache(self) -> bool:
        """Clear all cached data"""
        try:
            if self.redis_client:
                # Clear Redis cache
                for key in self.redis_client.scan_iter(match="prompt:*"):
                    self.redis_client.delete(key)

            # Clear memory cache
            self._memory_cache.clear()

            # Reset stats
            self._cache_stats = {"hits": 0, "misses": 0, "sets": 0}

            return True
        except Exception:
            return False

# Global cache instance
cache = CacheManager()
