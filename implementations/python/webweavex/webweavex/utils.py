"""Utility functions for WebWeaveX."""

import re
import json
from typing import Any, Dict, List


def load_spec(spec_path: str = None) -> Dict[str, Any]:
    """Load the WebWeaveX specification."""
    import os
    if spec_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        spec_path = os.path.join(base_dir, "..", "..", "..", "core", "specs", "wxp_v1.yaml")
    
    with open(spec_path, "r") as f:
        import yaml
        return yaml.safe_load(f)


SPEC = None


def get_spec() -> Dict[str, Any]:
    """Get the loaded specification."""
    global SPEC
    if SPEC is None:
        SPEC = load_spec()
    return SPEC


def deterministic_sort(items: List[Any]) -> List[Any]:
    """Sort items deterministically."""
    if isinstance(items, list) and items:
        if hasattr(items[0], '__dict__'):
            return sorted(items, key=lambda x: json.dumps(x.to_dict() if hasattr(x, 'to_dict') else x, sort_keys=True))
        return sorted(items, key=lambda x: json.dumps(x, sort_keys=True))
    return items


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def strip_text(text: str) -> str:
    """Strip text."""
    return text.strip()


def remove_empty_lines(text: str) -> str:
    """Remove empty lines from text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def safe_json_dumps(obj: Any, **kwargs) -> str:
    """Safely dump object to JSON with deterministic sorting."""
    return json.dumps(obj, sort_keys=True, **kwargs)
