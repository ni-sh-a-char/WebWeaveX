from __future__ import annotations

import hashlib
from typing import Any, Dict, List


def build_runtime_evolution(
    mutations: List[Dict[str, Any]],
    lineage: List[Dict[str, Any]],
) -> Dict[str, Any]:
    payload = "|".join(
        sorted(
            f"{m.get('kind', '')}:{m.get('target', '')}"
            for m in mutations
        )
    )
    evolution_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]

    return {
        "evolution_id": evolution_id,
        "mutations": sorted(mutations, key=lambda item: str(item.get("target", ""))),
        "lineage": sorted(lineage, key=lambda item: str(item.get("id", ""))),
        "improvements": {
            "selector_repairs": sum(1 for m in mutations if m.get("kind") == "selector"),
            "workflow_optimizations": sum(1 for m in mutations if m.get("kind") == "workflow"),
            "semantic_convergence": sum(1 for m in mutations if m.get("kind") == "semantic"),
            "sync_improvements": sum(1 for m in mutations if m.get("kind") == "sync"),
        },
        "bounded": True,
    }
