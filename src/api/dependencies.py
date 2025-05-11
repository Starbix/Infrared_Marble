import os
from concurrent.futures import ProcessPoolExecutor

# Create shared resources, then define dependencies to get access to them. This avoids having e.g. a Redis client per
# active connection. This is especially crucial for the ProcessPoolExecutor, that needs to share workers across threads.

# Single shared executor. Leave two cores free for performance. Assign a minimum of two workers.
max_workers = max((os.cpu_count() or 4) - 2, 2)
executor = ProcessPoolExecutor(max_workers=max_workers)


def get_executor():
    try:
        yield executor
    finally:
        pass
