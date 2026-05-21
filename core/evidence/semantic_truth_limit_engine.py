from __future__ import annotations

from typing import Any, Dict


def semantic_truth_limits(entropy: Dict[str, Any], instability: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "stabilization_allowed": not entropy.get("suppress_stabilization", False),
        "coherence_allowed": not entropy.get("suppress_coherence", False),
        "instability_preserved": instability.get("preserved", True),
    }
