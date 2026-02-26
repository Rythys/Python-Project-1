import logging
import time
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
        end = time.perf_counter()
        print(f"{func.__name__}() took {end - start:.4f} seconds")
        return result
    return wrapper