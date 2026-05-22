from __future__ import annotations

import json
from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash


def stable_memory_hash(memory: Dict[str, Any]) -> str:
    """Deterministic fingerprint for runtime memory snapshots."""
    history = memory.get("runtime_history", [])
    lineage = memory.get("lineage", [])
    relations = memory.get("semantic_relations", [])

    canonical = {
        "memory_id": memory.get("memory_id", ""),
        "runtime_history": sorted(
            history,
            key=lambda h: (
                int(h.get("tick", 0)),
                str(h.get("kind", "")),
                str(h.get("source", "")),
            ),
        ),
        "lineage": sorted(lineage, key=lambda x: str(x.get("id", ""))),
        "semantic_relations": sorted(
            relations,
            key=lambda r: (str(r.get("from", "")), str(r.get("to", ""))),
        ),
    }
    return compute_kaalka_hash(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    )
