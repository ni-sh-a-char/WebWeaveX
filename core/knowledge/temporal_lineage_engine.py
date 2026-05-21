from __future__ import annotations

from typing import Any, Dict, List


def stamp_temporal_lineage(edge: Dict[str, Any], tick: int) -> Dict[str, Any]:
    lineage = edge.get("lineage", {}) or {}
    stages = list(lineage.get("stages", [])) if isinstance(lineage.get("stages"), list) else []
    stages.append({"stage": "temporal", "tick": tick})
    return {**edge, "lineage": {**lineage, "stages": stages, "tick": tick}}
