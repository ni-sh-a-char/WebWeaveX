from __future__ import annotations

def compute_freshness(version_map: dict):
    ordered = sorted((version_map or {}).items())
    return {"ordered_versions": ordered, "count": len(ordered)}
