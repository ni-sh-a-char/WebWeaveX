from __future__ import annotations

from typing import Any, Dict, List

from core.documents.instructional_semantics_engine import analyze_instructional_semantics
from core.documents.tutorial_dependency_engine import reconstruct_tutorial_dependencies


def infer_tutorial_prerequisites(text: str) -> Dict[str, Any]:
    inst = analyze_instructional_semantics(text)
    legacy = reconstruct_tutorial_dependencies(text)
    chain: List[Dict[str, str]] = []
    steps = inst.get("ordering", [])
    for i in range(1, len(steps)):
        chain.append({
            "prerequisite": steps[i - 1].get("title", ""),
            "requires": steps[i].get("title", ""),
            "evidence": "discourse:instructional_order",
        })
    return {
        "chain": chain,
        "prerequisites": inst.get("prerequisites", []),
        "legacy_flow": legacy.get("reconciled", {}),
        "deterministic_inputs": [f"chain={len(chain)}"],
    }
