from __future__ import annotations

from typing import Any, Dict, List, Optional


def evolve_semantic_runtime(
    semantic: Optional[Dict[str, Any]] = None,
    history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    semantic = semantic or {}
    history = history or []
    inner = semantic.get("semantic", semantic)
    entities = inner.get("entities", {}).get("entities", [])

    recurring = {}
    for entity in entities:
        label = str(entity.get("label", entity.get("type", "")))
        recurring[label] = recurring.get(label, 0) + 1

    stable = sorted(
        [label for label, count in recurring.items() if count >= 1],
        key=str,
    )

    return {
        "recurring_entities": stable,
        "stable_ontology": inner.get("ontology", {}),
        "domain": inner.get("domain", {}).get("domain", ""),
        "semantic_convergence": len(stable),
        "domain_stabilized": bool(inner.get("domain")),
        "history_length": len(history),
        "bounded": True,
    }
