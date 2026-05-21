from __future__ import annotations

from typing import Any, Dict, List


def assess_semantic_honesty(
    evidence: List[str],
    supported: Dict[str, Any],
    unsupported: Dict[str, Any],
    fragile: Dict[str, Any],
) -> Dict[str, Any]:
    honest = not unsupported.get("claims") and fragile.get("level") != "high"
    return {
        "honest": honest,
        "prefers_insufficient_over_certainty": True,
        "supported_claims": len(supported.get("keys", []) or []),
        "unsupported_claims": len(unsupported.get("claims", []) or []),
        "message": "sufficient_honesty" if honest else "semantic_honesty_warning",
        "deterministic_inputs": [f"evidence={len(evidence)}", f"fragility={fragile.get('level', 'unknown')}"],
    }
