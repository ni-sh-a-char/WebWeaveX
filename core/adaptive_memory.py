def _pattern_key(pattern_item):
    if isinstance(pattern_item, dict):
        path = pattern_item.get("path", [])
        if isinstance(path, list):
            return " -> ".join([str(p) for p in sorted(path)])
        return str(path)
    return str(pattern_item)


def update_memory(context):
    patterns = context["intelligence"]["patterns"]
    success = context["learning"]["success_paths"]
    failure = context["learning"]["failed_paths"]

    for pattern in patterns.get("high_value_patterns", []):
        key = _pattern_key(pattern)
        success[key] = success.get(key, 0) + 1

    for pattern in patterns.get("dead_patterns", []):
        key = _pattern_key(pattern)
        failure[key] = failure.get(key, 0) + 1
