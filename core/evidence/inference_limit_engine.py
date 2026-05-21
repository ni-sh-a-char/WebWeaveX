from __future__ import annotations

from typing import Any, Dict

from core.evidence.semantic_boundary_engine import model_semantic_boundaries


def model_inference_limits(inferred: Dict[str, Any], evidence_count: int) -> Dict[str, Any]:
    allowed = evidence_count >= 2
    boundaries = model_semantic_boundaries(inferred, allowed)
    return {
        **boundaries,
        "max_inferred_keys": len(inferred) if allowed else 0,
        "evidence_required": 2,
    }
