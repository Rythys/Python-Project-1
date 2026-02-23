

def statistic_by_extensions(data) -> dict[str, dict[str, int]]:
    """
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

<<<<<<< HEAD
    return result
=======
    return result
>>>>>>> 5603267e65736c5c6b51f094cb8ca4eed4b6f877
