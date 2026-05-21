from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.speculative_inference_engine import collect_suppressed_speculation


def detect_semantic_speculation(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> Dict[str, Any]:
    suppressed = collect_suppressed_speculation(evidence, inferred, reconciled)
    return {
        "speculative": len(suppressed) > 0,
        "suppressed_speculation": suppressed,
        "density": round(len(suppressed) / max(1, len(inferred) + 1), 3),
    }
