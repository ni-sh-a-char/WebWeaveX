from __future__ import annotations

from typing import Any, Dict, List


def build_event_chain(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(events, key=lambda item: int(item.get("step", 0)))
    chain: List[Dict[str, Any]] = []

    for index, event in enumerate(ordered[:10000]):
        chain.append({
            "id": str(event.get("id", f"evt:{index}")),
            "runtime": str(event.get("runtime", "unknown")),
            "type": str(event.get("type", "mutation")),
            "step": index,
            "depth": index,
        })

    return {
        "chain": chain,
        "length": len(chain),
        "max_depth": len(chain) - 1 if chain else 0,
        "synchronized": [
            item["id"]
            for item in chain
            if chain and item.get("runtime") != chain[0]["runtime"]
        ],
        "bounded": True,
    }
