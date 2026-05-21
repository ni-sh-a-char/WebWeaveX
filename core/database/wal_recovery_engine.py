from __future__ import annotations

from typing import Any, Dict, List


def replay_wal(
    entries: List[Dict[str, Any]],
) -> Dict[str, Any]:

    recovered = []

    for entry in entries:
        recovered.append(entry)

    return {
        "recovered": recovered,
        "count": len(recovered),
    }
