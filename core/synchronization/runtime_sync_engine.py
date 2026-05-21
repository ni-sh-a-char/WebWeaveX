from __future__ import annotations

from typing import Any, Dict, List


RUNTIME_SYNC_HANDLERS = (
    "browser",
    "electron",
    "terminal",
    "vm",
    "remote",
)


def synchronize_runtime(
    snapshots: List[Dict[str, Any]],
    tick: int = 0,
) -> Dict[str, Any]:
    synchronized: List[Dict[str, Any]] = []

    for runtime in RUNTIME_SYNC_HANDLERS:
        payload = {}
        for snapshot in snapshots:
            key = f"{runtime}_runtime" if runtime != "browser" else "browser_runtime"
            if runtime == "electron":
                key = "native_runtime"
            value = snapshot.get(key, snapshot.get("native_runtime", {}))
            if value:
                payload = {**payload, **(value if isinstance(value, dict) else {"data": value})}

        synchronized.append({
            "runtime": runtime,
            "synced": bool(payload),
            "tick": tick,
            "handler": f"sync_{runtime}",
        })

    return {
        "synchronized": synchronized,
        "count": len([item for item in synchronized if item["synced"]]),
        "bounded": True,
    }
