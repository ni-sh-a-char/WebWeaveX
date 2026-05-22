from __future__ import annotations

from typing import Any, Dict, List


class MemorySnapshotContract:
    """Canonical memory snapshot for deterministic merge/replay."""

    @staticmethod
    def canonicalize(snapshot: Dict[str, Any]) -> Dict[str, Any]:
        history = list(snapshot.get("runtime_history", []))
        history_sorted = sorted(
            history,
            key=lambda h: (
                int(h.get("tick", 0)),
                str(h.get("kind", "")),
                str(h.get("source", "")),
            ),
        )
        return {
            **{k: v for k, v in sorted(snapshot.items()) if k != "runtime_history"},
            "runtime_history": history_sorted,
            "bounded": True,
        }
