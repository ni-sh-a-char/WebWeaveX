from __future__ import annotations

from typing import Any, Dict, List


def trace_semantic_path(events: List[str]) -> Dict[str, Any]:
    path = sorted(set(str(e) for e in (events or []) if e))
    return {"trace": path, "length": len(path), "deterministic": True}
