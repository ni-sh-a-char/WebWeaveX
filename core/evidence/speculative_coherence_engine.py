from __future__ import annotations

from typing import Any, Dict, List


def detect_speculative_coherence(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> Dict[str, Any]:
    speculative = reconciled != inferred and len(evidence) < 2 and bool(inferred)
    return {
        "speculative": speculative,
        "suppress_coherence": speculative,
        "density": round(1.0 if speculative else 0.0, 3),
    }
