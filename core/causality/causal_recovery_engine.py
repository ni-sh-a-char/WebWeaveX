from __future__ import annotations

from typing import Any, Dict, List


def recover_causal_runtime(
    causality: Dict[str, Any],
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    propagation_order = list(causality.get("propagation_order", []))
    recovered_events = list(events)

    if not propagation_order and events:
        propagation_order = [str(event.get("id", "")) for event in events]

    gaps = []
    for index in range(1, len(propagation_order)):
        if not propagation_order[index]:
            gaps.append(index)

    for gap_index in gaps:
        recovered_events.append({
            "id": f"recovered:evt:{gap_index}",
            "runtime": "recovery",
            "type": "restore",
            "step": gap_index,
            "recovered": True,
        })

    recovered_order = sorted(
        recovered_events,
        key=lambda item: int(item.get("step", 0)),
    )

    return {
        "recovered_events": recovered_order,
        "propagation_order": [
            str(event.get("id", "")) for event in recovered_order
        ],
        "broken_chains_fixed": len(gaps),
        "synchronization_restored": True,
        "bounded": True,
    }
