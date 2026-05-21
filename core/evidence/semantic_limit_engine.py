from __future__ import annotations

from typing import Any, Dict, List


def semantic_limits(
    evidence_count: int,
    noninferable_regions: List[str],
    self_limitation: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "max_confidence_without_evidence": 0.45,
        "min_evidence_for_inference": 2,
        "noninferable_count": len(noninferable_regions),
        "expansion_allowed": self_limitation.get("expansion_allowed", False),
        "reconciliation_allowed": self_limitation.get("reconciliation_allowed", False),
    }
