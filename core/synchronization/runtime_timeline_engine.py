from __future__ import annotations

from typing import Any, Dict, List


def build_sync_timeline(
    history: Dict[str, Any],
) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []

    for delta in history.get("deltas", []):
        entries.append({
            "tick": int(delta.get("timestamp", 0)),
            "delta_id": str(delta.get("delta_id", "")),
            "change_count": len(delta.get("changes", [])),
        })

    return {
        "timeline": sorted(entries, key=lambda item: item["tick"]),
        "bounded": True,
    }
