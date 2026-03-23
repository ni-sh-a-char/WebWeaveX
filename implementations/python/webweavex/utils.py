"""WebWeaveX Utilities."""

import json
from typing import Any, Dict, List


def deterministic_sort(items: List[Any]) -> List[Any]:
    """Sort items deterministically."""
    if isinstance(items, list) and items:
        if hasattr(items[0], 'to_dict'):
            return sorted(items, key=lambda x: json.dumps(x.to_dict(), sort_keys=True))
        return sorted(items, key=lambda x: json.dumps(x, sort_keys=True))
    return items


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    import re
    return re.sub(r'\s+', ' ', text).strip()


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def safe_json_dumps(obj: Any, **kwargs) -> str:
    """Safely dump object to JSON with deterministic sorting."""
    kwargs.setdefault("sort_keys", True)
    return json.dumps(obj, **kwargs)
