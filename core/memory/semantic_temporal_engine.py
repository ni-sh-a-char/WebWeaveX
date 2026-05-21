from __future__ import annotations

from typing import Any, Dict, List


MAX_SNAPSHOTS = 100


def order_temporal_snapshots(snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(snapshots, key=lambda s: (int(s.get("version", 0)), str(s.get("fingerprint", ""))))[:MAX_SNAPSHOTS]
