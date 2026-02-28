import logging
import time
from collections.abc import Generator
from functools import wraps


logging.basicConfig(level=logging.INFO)


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}() with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__}() returned {result}")
        return result
    return wrapper


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        if isinstance(result, Generator):
            result = list(result)
        end = time.perf_counter()
        elapsed = end - start
        return result, elapsed
    return wrapper