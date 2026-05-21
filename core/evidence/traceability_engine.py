from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_traceability(
    evidence: Optional[List[str]] = None,
    lineage: Optional[Dict[str, Any]] = None,
    stages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in (evidence or []) if e))
    chain = sorted(set(stages or []))
    return {
        "evidence_chain": ev,
        "lineage_ref": lineage or {},
        "stages": chain,
        "deterministic": True,
        "reconstructible": bool(ev),
    }
