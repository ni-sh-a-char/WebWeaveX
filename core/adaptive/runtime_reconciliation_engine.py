from __future__ import annotations

from typing import Any, Dict


def reconcile_runtime_state(
    browser_runtime: Dict[str, Any],
    stream_runtime: Dict[str, Any],
    interaction_runtime: Dict[str, Any],
    extraction_runtime: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "browser": {
            "available": browser_runtime.get("available", False),
            "url": browser_runtime.get("url", ""),
        },
        "stream": {
            "event_count": len(stream_runtime.get("events", [])),
        },
        "interaction": {
            "count": len(interaction_runtime.get("interactions", [])),
        },
        "extraction": {
            "field_count": len(extraction_runtime.get("fields", [])),
        },
        "consistent": True,
        "bounded": True,
    }
