from decorators import *

@measure_time("<REPORT_TIME>")
@log_calls
def statistic_by_extensions(data) -> dict[str, dict[str, int]]:
    """
    Group files by extensions
    
    returns:
        {
            "extension": {"count": int, "size": int},
            ...
        }

    """
    result = dict()
    for file_stats in data:
        ext = file_stats["extension"]
        if ext not in result:
            result[ext] = {"count": 0, "size": 0}
        result[ext]["count"] += 1
        result[ext]["size"] += file_stats["size"]

    return result
