from __future__ import annotations

from typing import Any, Dict, List


MAX_MUTATIONS = 10000


def build_runtime_mutations(
    selector: Dict[str, Any],
    workflow: Dict[str, Any],
    semantic: Dict[str, Any],
    sync: Dict[str, Any],
) -> List[Dict[str, Any]]:
    mutations: List[Dict[str, Any]] = []

    for item in selector.get("selectors", [])[:MAX_MUTATIONS]:
        mutations.append({
            "kind": "selector",
            "target": str(item.get("original", "")),
            "evolved": str(item.get("evolved", "")),
        })

    if workflow.get("execution_ordering"):
        mutations.append({
            "kind": "workflow",
            "target": "execution_ordering",
            "evolved": workflow["execution_ordering"],
        })

    if semantic.get("domain"):
        mutations.append({
            "kind": "semantic",
            "target": "domain",
            "evolved": semantic["domain"],
        })

    if sync.get("convergence"):
        mutations.append({
            "kind": "sync",
            "target": "convergence",
            "evolved": True,
        })

    return sorted(mutations, key=lambda item: (item["kind"], str(item["target"])))
