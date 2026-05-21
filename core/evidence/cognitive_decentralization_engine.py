from __future__ import annotations

from typing import Any, Dict, List


def model_cognitive_decentralization(cluster_count: int, evidence_count: int) -> Dict[str, Any]:
    dominated = cluster_count <= 1 and evidence_count < 3
    return {
        "decentralized": not dominated,
        "cluster_count": cluster_count,
        "dominance_without_evidence": dominated,
        "empire_blocked": True,
    }
