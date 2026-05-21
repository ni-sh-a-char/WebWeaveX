from __future__ import annotations

from typing import Any, Dict, List

_ALLOWED = frozenset({
    "EXTRACT", "SYNC", "REPLAY", "EXECUTE", "FEDERATE", "RECONSTRUCT", "MEMORY",
})


def validate_wwx(parsed: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    for stmt in parsed.get("statements", []):
        if stmt.get("verb") not in _ALLOWED:
            errors.append(f"forbidden verb: {stmt.get('verb')}")
    return {
        "valid": not errors,
        "errors": sorted(errors),
        "bounded": True,
    }
