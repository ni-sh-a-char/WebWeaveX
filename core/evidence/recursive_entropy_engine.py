from __future__ import annotations

from typing import Any, Dict, List


def model_recursive_entropy(
    ambiguities: List[str],
    uncertainties: List[str],
    contradicted: Dict[str, Any],
    depth: int,
) -> Dict[str, Any]:
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    base = len(ambiguities) * 0.1 + len(uncertainties) * 0.08 + len(pairs) * 0.15
    entropy = round(min(1.0, base + depth * 0.05), 3)
    return {
        "entropy": entropy,
        "depth": depth,
        "preserved": True,
        "suppress_recursive_stabilization": entropy >= 0.15,
        "suppress_recursive_closure": entropy >= 0.2,
    }
