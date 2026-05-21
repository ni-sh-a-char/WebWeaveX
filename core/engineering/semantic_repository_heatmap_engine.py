from __future__ import annotations

from typing import Any, Dict, List


MAX_HEATMAP = 10000


def build_repository_heatmap(
    repository_ir: Dict[str, Any],
) -> Dict[str, Any]:
    files = list(repository_ir.get("files", []))[:MAX_HEATMAP]
    heatmap = [
        {
            "path": path,
            "intensity": 1,
        }
        for path in sorted(str(f) for f in files if f)
    ]
    return {
        "heatmap": heatmap,
        "count": len(heatmap),
        "bounded": True,
    }
