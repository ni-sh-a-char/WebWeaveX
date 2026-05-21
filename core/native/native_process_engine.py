from __future__ import annotations

from typing import Any, Dict, List, Optional


def enumerate_native_processes(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    processes = list(snap.get("processes", []))[:10000]

    return {
        "processes": sorted(
            processes,
            key=lambda item: str(item.get("name", item.get("pid", ""))),
        ),
        "count": len(processes),
        "bounded": True,
    }
