from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.lineage_engine import build_lineage


def reconstruct_source_lineage(sources: List[str]) -> Dict[str, Any]:
    ordered = sorted(set(str(s) for s in (sources or []) if s))
    lineage = build_lineage([{"stage": "source_lineage", "inputs": [], "outputs": ordered}])
    return {"sources": ordered, "lineage": lineage, "evidence": ["source_lineage"]}
