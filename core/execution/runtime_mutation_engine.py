from __future__ import annotations

from typing import Any, Dict, List, Optional


def track_runtime_mutations(
    prior: Optional[List[Dict[str, Any]]] = None,
    mutation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    mutations = list(prior or [])
    if mutation:
        entry = {
            "kind": str(mutation.get("kind", "unknown")),
            "target": str(mutation.get("target", "")),
            "tick": int(mutation.get("tick", 0)),
            "ordered_index": len(mutations),
        }
        mutations.append(entry)

    sorted_mutations = sorted(
        mutations,
        key=lambda item: (int(item.get("tick", 0)), int(item.get("ordered_index", 0)), str(item.get("kind", ""))),
    )

    by_kind = {
        "dom": [m for m in sorted_mutations if m.get("kind") == "dom"],
        "native": [m for m in sorted_mutations if m.get("kind") == "native"],
        "workflow": [m for m in sorted_mutations if m.get("kind") == "workflow"],
        "synchronization": [m for m in sorted_mutations if m.get("kind") == "sync"],
        "memory": [m for m in sorted_mutations if m.get("kind") == "memory"],
    }

    return {
        "mutations": sorted_mutations,
        "by_kind": by_kind,
        "count": len(sorted_mutations),
        "deterministic_order": True,
        "bounded": True,
    }
