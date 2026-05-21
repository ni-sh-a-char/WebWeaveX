from __future__ import annotations

from typing import Any, Dict, List


def bridge_browser_native_runtime(
    browser_events: List[Dict[str, Any]],
    native_events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bridges: List[Dict[str, Any]] = []
    step = len(browser_events)

    for index, native_event in enumerate(native_events[:5000]):
        source = browser_events[-1] if browser_events else {"id": "browser:root"}
        bridges.append({
            "from_runtime": "browser",
            "to_runtime": str(native_event.get("runtime", "desktop")),
            "from_event": str(source.get("id", "")),
            "to_event": str(native_event.get("id", f"native:{index}")),
            "relation": "propagates",
            "step": step + index,
        })

    return {
        "bridges": bridges,
        "chain_length": len(bridges),
        "bounded": True,
    }
