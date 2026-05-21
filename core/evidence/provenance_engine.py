from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_provenance(
    evidence: List[str],
    sources: Optional[List[str]] = None,
    grounding: Optional[Dict[str, Any]] = None,
    lineage: Optional[Dict[str, Any]] = None,
    confidence_basis: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in (evidence or []) if e))
    src = sorted(set(str(s) for s in (sources or evidence or []) if s))
    return {
        "evidence": ev,
        "sources": src,
        "grounding": grounding if isinstance(grounding, dict) else {},
        "lineage": lineage if isinstance(lineage, dict) else {},
        "confidence_basis": confidence_basis if isinstance(confidence_basis, dict) else {},
    }
