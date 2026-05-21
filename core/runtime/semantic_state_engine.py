from __future__ import annotations

from typing import Any, Dict


def track_semantic_state(ir: Dict[str, Any], stage: str = "runtime") -> Dict[str, Any]:
    lineage = ir.get("lineage", {}) or {}
    stages = list(lineage.get("stages", [])) if isinstance(lineage.get("stages"), list) else []
    stages.append({"stage": stage})
    return {**ir, "lineage": {**lineage, "stages": stages, "depth": len(stages)}}
