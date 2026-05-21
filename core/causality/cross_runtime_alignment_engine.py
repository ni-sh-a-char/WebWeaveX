from __future__ import annotations

from typing import Any, Dict, List


RUNTIME_ORDER = (
    "browser",
    "application",
    "electron",
    "desktop",
    "terminal",
    "vm",
    "remote",
    "distributed",
)


def align_cross_runtime_events(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    buckets: Dict[str, List[Dict[str, Any]]] = {
        runtime: [] for runtime in RUNTIME_ORDER
    }

    for event in events[:20000]:
        runtime = str(event.get("runtime", "browser")).lower()
        if runtime not in buckets:
            buckets[runtime] = []
        buckets[runtime].append(event)

    aligned: List[Dict[str, Any]] = []
    step = 0
    for runtime in RUNTIME_ORDER:
        for event in sorted(
            buckets.get(runtime, []),
            key=lambda item: int(item.get("step", 0)),
        ):
            aligned.append({
                **event,
                "aligned_step": step,
                "aligned_runtime": runtime,
            })
            step += 1

    correlations = []
    for index in range(1, len(aligned)):
        prev = aligned[index - 1]
        curr = aligned[index]
        correlations.append({
            "from_runtime": prev.get("runtime", ""),
            "to_runtime": curr.get("runtime", ""),
            "from_event": prev.get("id", ""),
            "to_event": curr.get("id", ""),
            "correlation_id": f"corr:{index}",
        })

    return {
        "aligned_events": aligned,
        "correlations": correlations,
        "runtime_count": len({e.get("runtime") for e in aligned}),
        "bounded": True,
    }
