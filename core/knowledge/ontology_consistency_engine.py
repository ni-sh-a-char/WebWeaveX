from __future__ import annotations

from typing import Any, Dict, List


def check_ontology_consistency(edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    violations = []
    for e in edges or []:
        if not isinstance(e, dict):
            continue
        ev = e.get("evidence", []) or []
        if not ev:
            violations.append({"from": e.get("from"), "to": e.get("to"), "reason": "missing_evidence"})
        if "type" in e:
            violations.append({"from": e.get("from"), "to": e.get("to"), "reason": "forbidden_type_field"})
    return {
        "consistent": len(violations) == 0,
        "violations": violations,
        "edge_count": len(edges or []),
        "deterministic_inputs": [f"violations={len(violations)}", f"edges={len(edges or [])}"],
    }
