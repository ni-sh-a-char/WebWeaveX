from __future__ import annotations

from typing import Any, Dict, List


def model_recursive_semantic_decentralization(clusters: List[str], evidence_count: int) -> Dict[str, Any]:
    dominated = len(clusters) <= 1 and evidence_count < 3
    return {"decentralized": not dominated, "cluster_count": len(clusters), "dominance_blocked": dominated}
