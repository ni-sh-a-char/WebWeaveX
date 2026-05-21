from __future__ import annotations

from typing import Any, Dict, List


def stamp_ontology_lineage(edge: Dict[str, Any], stage: str = "ontology") -> Dict[str, Any]:
    lineage = edge.get("lineage", {}) or {}
    stages = list(lineage.get("stages", [])) if isinstance(lineage.get("stages"), list) else []
    stages.append({"stage": stage, "from": edge.get("from"), "to": edge.get("to")})
    return {**edge, "lineage": {**lineage, "stages": stages, "depth": len(stages)}}
