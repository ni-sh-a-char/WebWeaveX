from __future__ import annotations

from typing import Any, Dict, List


def terminate_inference_chain(
    refused_inferences: List[str],
    suppressed_speculation: List[Dict[str, Any]],
) -> Dict[str, Any]:
    terminated = list(refused_inferences) + [
        s.get("reason", "speculative") for s in suppressed_speculation if isinstance(s, dict)
    ]
    return {
        "terminated_inferences": sorted(set(terminated)),
        "chain_stopped": bool(terminated),
        "stop_at": terminated[0] if terminated else None,
    }
