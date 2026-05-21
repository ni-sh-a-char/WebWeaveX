from __future__ import annotations

from typing import Any, Dict, List


def track_divergence(views: List[Dict[str, Any]]) -> Dict[str, Any]:
    keys: Dict[str, set] = {}
    for view in views or []:
        if not isinstance(view, dict):
            continue
        for k, v in sorted(view.items()):
            keys.setdefault(k, set()).add(str(v))
    divergent = sorted(k for k, vals in keys.items() if len(vals) > 1)
    return {
        "divergent_keys": divergent,
        "preserved": divergent,
        "evidence": ["semantic_divergence"],
        "lineage": {"views": len(views or [])},
    }
