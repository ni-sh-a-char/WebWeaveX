from __future__ import annotations

from typing import Any, Set

from .deterministic_serializer import dumps_deterministic


def dumps_cycle_safe(value: Any, _seen: Set[int] | None = None) -> str:
    seen: Set[int] = set() if _seen is None else _seen

    def _strip(obj: Any, depth: int = 0) -> Any:
        if depth > 64:
            return str(obj)
        if isinstance(obj, (dict, list, tuple)):
            oid = id(obj)
            if oid in seen:
                return "<cycle>"
            seen.add(oid)
        if isinstance(obj, dict):
            return {k: _strip(v, depth + 1) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_strip(v, depth + 1) for v in obj]
        if isinstance(obj, tuple):
            return [_strip(v, depth + 1) for v in obj]
        return obj

    return dumps_deterministic(_strip(value))
