import time
from collections.abc import Generator
from functools import wraps

    
log_buffer = list()
need_logging = False

# Change default args if needed functions logging
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log_info = f"Calling {func.__name__}() with args={args}, kwargs={kwargs}\n"
        result = func(*args, **kwargs)
        log_info += f"{func.__name__}() returned {result}"
        if need_logging:
            log_buffer.append(log_info)
        return result
    return wrapper


execution_stats = {"<SCAN_TIME>": 0.0, "<REPORT_TIME>": 0.0}

def measure_time(category: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            
            if isinstance(result, Generator):
                result = list(result)
                
            elapsed = (time.perf_counter() - start) * 1000
            execution_stats[category] += elapsed
            return result
        return wrapper
    return decorator