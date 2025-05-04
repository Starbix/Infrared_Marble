import os
import redis
from concurrent.futures import ProcessPoolExecutor


def get_redis_client():
    client = redis.from_url(os.getenv("REDIS_URL"))
    try:
        yield client
    finally:
        client.close()


def get_executor():
    max_workers = (os.cpu_count() or 4) - 2
    executor = ProcessPoolExecutor(max_workers=max_workers)
    try:
        yield executor
    finally:
        executor.shutdown(wait=False)
