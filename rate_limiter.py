"""Rate limiter for the HR service"""

import time

import redis
from fastapi import Request

from config import settings

RATE_LIMIT = 5  # requests
WINDOW_SECONDS = 60  # per minute


# Redis client
def get_redis_client():
    """Get Redis client"""
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True,
    )


def get_client_key(request: Request) -> str:
    """Get client key"""
    ip = request.client.host
    path = request.url.path
    return f"rate:{ip}:{path}"


def is_rate_limited(request: Request) -> bool:
    """Check if the request is rate limited"""
    key = get_client_key(request)
    r = get_redis_client()
    current_count = r.incr(key)

    if current_count == 1:
        r.expire(key, WINDOW_SECONDS)

    return current_count > RATE_LIMIT
