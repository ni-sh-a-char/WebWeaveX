"""
WebWeaveX System Graph Derivation (Phase V6)

Purpose:
    Convert semantic graph to system graph structure
    - Derives components from nodes
    - Derives relationships from edges
    - NO maps, pure derivation
"""

from typing import Dict, Any, List


def derive_system_graph(semantic_graph: Dict[str, Any]) -> Dict[str, Any]:
    """Derive system graph from semantic graph."""
    if not isinstance(semantic_graph, dict):
        return {"components": [], "relationships": []}
    
    nodes = semantic_graph.get("nodes", [])
    edges = semantic_graph.get("edges", [])
    
    components = []
    seen_components = set()
    
    for node in nodes:
        name = node.get("id", "")
        if name and name not in seen_components:
            components.append({
                "name": name,
                "role": node.get("type", "unknown")
            })
            seen_components.add(name)
    
    relationships = []
    for edge in edges:
        from_node = edge.get("from", "")
        to_node = edge.get("to", "")
        
        if from_node and to_node:
            relationships.append({
                "from": from_node,
                "to": to_node,
                "type": edge.get("relation", "relates_to")
            })
    
    return {
        "components": sorted(components, key=lambda x: x["name"]),
        "relationships": sorted(relationships, key=lambda x: (x.get("from", ""), x.get("to", "")))
    }


def validate_system_graph() -> bool:
    """Validate system graph derivation."""
    test_semantic = {
        "nodes": [
            {"id": "build", "type": "verb"},
            {"id": "api", "type": "system"},
            {"id": "database", "type": "storage"}
        ],
        "edges": [
            {"from": "build", "to": "api", "relation": "builds"}
        ]
    }
    
    graph = derive_system_graph(test_semantic)
    
    if not isinstance(graph, dict):
        return False
    
    if len(graph.get("components", [])) < 1:
        return False
    
    return True


if __name__ == "__main__":
    ok = validate_system_graph()
    print("SYSTEM GRAPH:", "PASS" if ok else "FAIL")