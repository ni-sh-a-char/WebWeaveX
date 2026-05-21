from __future__ import annotations

from typing import Any, Dict


def diff_runtime_memory(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    prev_ids = {str(item.get("id", "")) for item in previous.get("lineage", [])}
    curr_ids = {str(item.get("id", "")) for item in current.get("lineage", [])}

    return {
        "memory_changed": previous.get("memory_id") != current.get("memory_id"),
        "lineage_added": sorted(curr_ids - prev_ids),
        "lineage_removed": sorted(prev_ids - curr_ids),
        "history_delta": len(current.get("runtime_history", [])) - len(
            previous.get("runtime_history", [])
        ),
        "revertible": True,
        "bounded": True,
    }
