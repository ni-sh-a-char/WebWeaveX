"""
WebWeaveX Compiler Engine (Pure Version)

Purpose:
    True system compiler kernel
    - No maps
    - No templates
    - Pure graph derivation
"""

from typing import Dict, Any, List


def run_compiler(semantics: Dict[str, Any]) -> Dict[str, Any]:
    """Pure system compilation from semantics."""
    if not isinstance(semantics, dict):
        return _empty_compiler_output()

    # PURE: nodes and relationships directly from semantics
    nodes = semantics.get("nodes", [])
    relationships = semantics.get("relationships", [])

    # Components = nodes (NO transformation, NO type fields)
    components = [{"name": n.get("id", "")} for n in nodes]

    # Execution graph = relationships as edges
    edges = [
        {"from": rel.get("from", ""), "to": rel.get("to", "")}
        for rel in relationships
    ]

    # Deterministic execution order (sorted node IDs)
    node_ids = sorted([n.get("id", "") for n in nodes])
    execution_order = node_ids

    # Artifacts empty for pure compiler
    artifacts = []

    # Spec = counts only (NO hardcoded type)
    spec = {
        "node_count": len(nodes),
        "edge_count": len(relationships)
    }

    return {
        "system": {
            "system_type": "",
            "architecture": "",
            "components": components,
            "relationships": relationships
        },
        "execution_graph": {"nodes": nodes, "edges": edges},
        "execution_order": execution_order,
        "artifacts": artifacts,
        "spec": spec
    }


def run_compiler_from_input(semantics: Dict[str, Any], user_input: str = "") -> Dict[str, Any]:
    """Run compiler with user input context."""
    result = run_compiler(semantics)
    
    if user_input:
        result["user_input"] = user_input
    
    return result


def _empty_compiler_output() -> Dict[str, Any]:
    return {
        "system": {
            "system_type": "generic_system",
            "architecture": "monolithic",
            "components": [],
            "relationships": []
        },
        "execution_graph": {"nodes": [], "edges": []},
        "execution_order": [],
        "artifacts": [],
        "spec": {
            "system_type": "generic_system",
            "components": 0,
            "relationships": 0
        }
    }


def validate_compiler() -> bool:
    """Validate compiler engine."""
    test_semantics = {
        "nodes": [
            {"id": "api"},
            {"id": "build"}
        ],
        "relationships": [
            {"from": "build", "to": "api"}
        ]
    }
    
    result = run_compiler(test_semantics)
    
    if not isinstance(result, dict):
        return False
    
    if "system" not in result:
        return False
    
    if "execution_graph" not in result:
        return False
    
    if "artifacts" not in result:
        return False
    
    return True


if __name__ == "__main__":
    ok = validate_compiler()
    print("COMPILER ENGINE:", "PASS" if ok else "FAIL")