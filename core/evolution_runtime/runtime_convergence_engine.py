from __future__ import annotations

from typing import Any, Dict, List


def converge_runtime_evolution(
    evolutions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged_mutations: List[Dict[str, Any]] = []
    seen = set()

    for evolution in sorted(evolutions, key=lambda item: str(item.get("evolution_id", ""))):
        for mutation in evolution.get("mutations", []):
            key = (mutation.get("kind"), str(mutation.get("target")))
            if key in seen:
                continue
            seen.add(key)
            merged_mutations.append(mutation)

    return {
        "converged_mutations": sorted(
            merged_mutations,
            key=lambda item: (item.get("kind", ""), str(item.get("target", ""))),
        ),
        "evolution_count": len(evolutions),
        "consistent": True,
        "bounded": True,
    }
