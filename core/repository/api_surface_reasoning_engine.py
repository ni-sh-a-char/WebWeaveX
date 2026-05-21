from __future__ import annotations

from typing import Any, Dict, List


def reason_api_surface(spec: Dict[str, Any]) -> Dict[str, Any]:
    paths = spec.get("paths", {}) if isinstance(spec, dict) else {}
    if not isinstance(paths, dict):
        paths = {}
    endpoints: List[Dict[str, str]] = []
    for path, methods in paths.items():
        if isinstance(methods, dict):
            for method in methods:
                endpoints.append({"path": path, "method": method.upper()})
    return {
        "paths": endpoints,
        "path_count": len(endpoints),
        "evidence": ["openapi:paths"] if endpoints else [],
        "deterministic_inputs": [f"paths={len(endpoints)}"],
    }
