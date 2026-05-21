from __future__ import annotations

from typing import Any, Dict, List


def preserve_epistemic_boundaries(
    evidence: List[str],
    noninferable_regions: List[str],
    unstable_regions: List[str],
) -> Dict[str, Any]:
    return {
        "visible": True,
        "where_inference_stops": noninferable_regions,
        "where_cognition_stops": unstable_regions,
        "where_reconstruction_stops": unstable_regions,
        "suppress_stabilization": bool(unstable_regions),
        "suppress_coherence": len(evidence) < 2,
    }
