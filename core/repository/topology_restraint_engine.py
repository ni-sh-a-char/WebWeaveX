from __future__ import annotations

from typing import Any, Dict, List

from core.repository.speculative_topology_engine import suppress_speculative_topology_edge


def restrain_topology_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    humbled = suppress_speculative_topology_edge(edge)
    suppressed = humbled.get("unsupported", {}).get("edge", False)
    return {
        **humbled,
        "observed": edge.get("observed", {}),
        "inferred": edge.get("inferred", {}),
        "restraint": {"conservative": True, "propagation_allowed": not suppressed},
    }
