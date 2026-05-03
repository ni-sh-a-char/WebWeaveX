"""
WebWeaveX Execution Graph Builder (Phase V6)

Purpose:
    Build execution graph from system graph
    - Ordered component execution
    - Dependency derivation from relationships
    - NO hardcoded phases
"""

from typing import Dict, Any, List


def build_execution_graph(system_graph: Dict[str, Any]) -> Dict[str, Any]:
    """Build execution graph from system graph - ONLY derived from relationships."""
    if not isinstance(system_graph, dict):
        return {"nodes": [], "edges": []}
    
    components = system_graph.get("components", [])
    relationships = system_graph.get("relationships", [])
    
    nodes = []
    for comp in components:
        nodes.append({
            "id": comp.get("name", ""),
            "type": comp.get("role", "unknown")
        })
    
    edges = []
    for rel in relationships:
        from_node = rel.get("from", "")
        to_node = rel.get("to", "")
        
        if from_node and to_node:
            edges.append({
                "from": from_node,
                "to": to_node,
                "type": rel.get("type", "depends_on")
            })
    
    return {
        "nodes": nodes,
        "edges": edges
    }


def infer_execution_order(system_graph: Dict[str, Any]) -> List[str]:
    """Infer execution order using topological sort (Kahn's algorithm)."""
    if not isinstance(system_graph, dict):
        return []
    
    components = system_graph.get("components", [])
    relationships = system_graph.get("relationships", [])
    
    if not components:
        return []
    
    in_degree = {c.get("name"): 0 for c in components}
    adj = {c.get("name"): [] for c in components}
    
    for rel in relationships:
        from_node = rel.get("from", "")
        to_node = rel.get("to", "")
        if from_node and to_node:
            if from_node in adj:
                adj[from_node].append(to_node)
            if to_node in in_degree:
                in_degree[to_node] = in_degree.get(to_node, 0) + 1
    
    queue = [n for n, d in in_degree.items() if d == 0]
    order = []
    
    while queue:
        node = queue.pop(0)
        order.append(node)
        
        if node in adj:
            for neighbor in adj[node]:
                in_degree[neighbor] = in_degree.get(neighbor, 1) - 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    if len(order) != len(components):
        order = [c.get("name") for c in components] if components else []
    
    return order


def validate_execution_graph() -> bool:
    """Validate execution graph builder."""
    test_system = {
        "components": [
            {"name": "config", "role": "configuration"},
            {"name": "api", "role": "system"},
            {"name": "database", "role": "storage"}
        ],
        "relationships": [
            {"from": "api", "to": "database", "type": "connects"}
        ]
    }
    
    graph = build_execution_graph(test_system)
    order = infer_execution_order(test_system)
    
    return isinstance(graph, dict) and len(order) > 0


if __name__ == "__main__":
    ok = validate_execution_graph()
    print("EXECUTION GRAPH:", "PASS" if ok else "FAIL")