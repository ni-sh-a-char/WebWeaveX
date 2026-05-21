from __future__ import annotations

from typing import Any, Dict, List


def model_topology_boundaries(evidence: List[str], parser_grounded: bool = False) -> Dict[str, Any]:
    return {
        "propagation_allowed": len(evidence) >= 2 and parser_grounded,
        "service_links_allowed": parser_grounded and len(evidence) >= 1,
        "deployment_inference_allowed": False,
        "orchestration_inference_allowed": len(evidence) >= 2,
    }
