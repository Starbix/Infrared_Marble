import os
from concurrent.futures import ProcessPoolExecutor

import redis

# Create shared resources, then define dependencies to get access to them. This avoids having e.g. a Redis client per
# active connection. This is especially crucial for the ProcessPoolExecutor, that needs to share workers across threads.

# Single shared Redis connection pool
pool = redis.ConnectionPool.from_url(url=os.getenv("REDIS_URL", "redis://redis:6379/0"))

# Single shared executor. Leave two cores free for performance. Assign a minimum of two workers.
max_workers = max((os.cpu_count() or 4) - 2, 2)
executor = ProcessPoolExecutor(max_workers=max_workers)


def get_redis_client():
    redis_client = redis.Redis(connection_pool=pool)
    try:
        yield redis_client
    finally:
        pass


def get_executor():
    try:
        yield executor
    finally:
        pass
