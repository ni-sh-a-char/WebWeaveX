from __future__ import annotations

from typing import Any, Dict, List


def track_recursive_evidence_ancestry(evidence: List[str], depth: int) -> Dict[str, Any]:
    detached = depth > 3 and len(evidence) < 2
    return {"ancestry": list(evidence), "depth": depth, "detached": detached, "suppress_stabilization": detached}
