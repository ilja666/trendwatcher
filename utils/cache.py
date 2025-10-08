"""
Simple in-memory cache with TTL support for API responses.
Helps avoid rate limits by caching API responses for a specified duration.
"""

from datetime import datetime, timedelta
from typing import Any, Optional
import json

# In-memory cache storage
_CACHE = {}

def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve cached data by key if it exists and hasn't expired.

    Args:
        key: Cache key (e.g., "crypto_trending", "stocks_news")

    Returns:
        Cached data if valid, None if expired or not found
    """
    if key not in _CACHE:
        return None

    entry = _CACHE[key]
    now = datetime.now()

    # Check if cache has expired
    if entry["expires"] < now:
        # Clean up expired entry
        del _CACHE[key]
        return None

    print(f"[CACHE HIT] {key} (expires in {(entry['expires'] - now).seconds}s)")
    return entry["data"]


def set_cache(key: str, data: Any, ttl: int = 900) -> None:
    """
    Store data in cache with TTL (time-to-live).

    Args:
        key: Cache key (e.g., "crypto_trending", "stocks_news")
        data: Data to cache (must be JSON-serializable)
        ttl: Time-to-live in seconds (default: 900 = 15 minutes)
    """
    now = datetime.now()
    expires = now + timedelta(seconds=ttl)

    _CACHE[key] = {
        "data": data,
        "expires": expires,
        "cached_at": now
    }

    print(f"[CACHE SET] {key} (TTL: {ttl}s)")


def clear_cache(key: Optional[str] = None) -> None:
    """
    Clear cache entry by key, or entire cache if no key provided.

    Args:
        key: Specific cache key to clear, or None to clear all
    """
    if key:
        if key in _CACHE:
            del _CACHE[key]
            print(f"[CACHE CLEAR] {key}")
    else:
        _CACHE.clear()
        print("[CACHE CLEAR] All entries cleared")


def get_cache_stats() -> dict:
    """
    Get statistics about current cache state.

    Returns:
        Dictionary with cache statistics
    """
    now = datetime.now()
    stats = {
        "total_entries": len(_CACHE),
        "active_entries": 0,
        "expired_entries": 0,
        "entries": []
    }

    for key, entry in _CACHE.items():
        is_expired = entry["expires"] < now
        if is_expired:
            stats["expired_entries"] += 1
        else:
            stats["active_entries"] += 1

        stats["entries"].append({
            "key": key,
            "cached_at": entry["cached_at"].isoformat(),
            "expires": entry["expires"].isoformat(),
            "expired": is_expired,
            "ttl_remaining": max(0, (entry["expires"] - now).seconds)
        })

    return stats
