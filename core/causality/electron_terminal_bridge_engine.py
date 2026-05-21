from __future__ import annotations

from typing import Any, Dict, List


def bridge_electron_terminal_runtime(
    electron_events: List[Dict[str, Any]],
    terminal_events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bridges: List[Dict[str, Any]] = []

    electron_ref = electron_events[-1] if electron_events else {"id": "electron:root"}

    for index, terminal_event in enumerate(terminal_events[:5000]):
        bridges.append({
            "from_runtime": "electron",
            "to_runtime": "terminal",
            "from_event": str(electron_ref.get("id", "")),
            "to_event": str(terminal_event.get("id", f"terminal:{index}")),
            "relation": "triggers",
            "step": index,
        })

    return {
        "bridges": bridges,
        "synchronization_chain": [b["to_event"] for b in bridges],
        "bounded": True,
    }
