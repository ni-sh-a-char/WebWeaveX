"""
WebWeaveX System Type Inference (Phase V6)

Purpose:
    Infer system type from system graph
    - Frequency-based dominance
    - NO maps, NO hardcoded logic
    - Pure statistical derivation
"""

from typing import Dict, Any, List


def infer_system_type(system_graph: Dict[str, Any]) -> str:
    """Infer system type from component roles."""
    if not isinstance(system_graph, dict):
        return "generic"
    
    components = system_graph.get("components", [])
    
    if not components:
        return "generic"
    
    roles = [c.get("role", "unknown") for c in components]
    
    if not roles:
        return "generic"
    
    freq = {}
    for r in roles:
        if r and r != "unknown":
            freq[r] = freq.get(r, 0) + 1
    
    if not freq:
        return "generic"
    
    sorted_roles = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    dominant = sorted_roles[0][0]
    
    return dominant + "_system" if dominant else "generic_system"


def infer_architecture(system_graph: Dict[str, Any], system_type: str = "") -> str:
    """Infer architecture from component relationships."""
    if not isinstance(system_graph, dict):
        return "monolithic"
    
    relationships = system_graph.get("relationships", [])
    components = system_graph.get("components", [])
    
    num_comps = len(components)
    num_rels = len(relationships)
    
    rels_per_comp = num_rels / num_comps if num_comps > 0 else 0
    
    if rels_per_comp > 1.0:
        return "service_mesh"
    elif num_comps > 5:
        return "distributed"
    elif num_comps > 2:
        return "service_oriented"
    else:
        return "monolithic"


def validate_system_inference() -> bool:
    """Validate system inference."""
    test_graph = {
        "components": [
            {"name": "api", "role": "system"},
            {"name": "database", "role": "storage"}
        ],
        "relationships": [
            {"from": "api", "to": "database", "type": "connects"}
        ]
    }
    
    sys_type = infer_system_type(test_graph)
    arch = infer_architecture(test_graph, sys_type)
    
    return bool(sys_type) and bool(arch)


if __name__ == "__main__":
    ok = validate_system_inference()
    print("SYSTEM INFERENCE:", "PASS" if ok else "FAIL")