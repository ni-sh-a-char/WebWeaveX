from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_decentralization(interpretations: List[Dict[str, Any]], evidence_count: int) -> Dict[str, Any]:
    dominant = len(interpretations) == 1 and evidence_count < 2
    return {
        "decentralized": not dominant,
        "authority_diffused": len(interpretations) > 1 or evidence_count >= 2,
        "hierarchy_lock_in": False,
        "single_interpretation_dominance": dominant,
    }
