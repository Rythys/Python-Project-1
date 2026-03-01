from decorators import *

@measure_time("<SCAN_TIME>")
@log_calls
def is_filtered_by_extension(file, ext):
    if not ext:
        return True
    return file.suffix == ext


@measure_time("<SCAN_TIME>")
@log_calls
def is_filtered_by_min_size(file, min_size):
    if not min_size:
        return True
    return file.stat().st_size >= min_size


@measure_time("<SCAN_TIME>")
@log_calls
def is_filtered_by_max_size(file, max_size):
    if not max_size:
        return True
    return file.stat().st_size <= max_size


@measure_time("<SCAN_TIME>")
@log_calls
def is_filtered_by_name(file, name):
    if not name:
        return True
    return name in file
 

