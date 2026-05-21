from __future__ import annotations

from typing import Any, Dict, List


def append_runtime_history(
    history: List[Dict[str, Any]],
    entry: Dict[str, Any],
) -> List[Dict[str, Any]]:
    updated = list(history)
    updated.append(entry)
    return sorted(updated, key=lambda item: int(item.get("tick", 0)))[:100000]
