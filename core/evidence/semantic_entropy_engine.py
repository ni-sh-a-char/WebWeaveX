from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_entropy(
    ambiguities: List[str],
    uncertainties: List[str],
    contradicted: Dict[str, Any],
) -> Dict[str, Any]:
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    entropy = round(min(1.0, len(ambiguities) * 0.1 + len(uncertainties) * 0.08 + len(pairs) * 0.15), 3)
    return {
        "entropy": entropy,
        "visible": entropy > 0,
        "suppress_stabilization": entropy >= 0.2,
        "suppress_coherence": entropy >= 0.15,
        "preserved": True,
    }
