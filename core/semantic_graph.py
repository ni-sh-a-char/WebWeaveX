"""
WebWeaveX Semantic Graph Builder (Phase V6)

Purpose:
    Convert semantics into graph structure
    - Entities as nodes
    - Actions as edges
    - Pure derivation, no maps
"""

from typing import Dict, Any, List


def build_semantic_graph(semantics: Dict[str, Any]) -> Dict[str, Any]:
    """Build semantic graph from semantics."""
    if not isinstance(semantics, dict):
        return {"nodes": [], "edges": []}
    
    nodes = []
    node_ids = set()
    
    for ent in semantics.get("entities", []):
        ent_id = ent.get("text", "")
        if ent_id and ent_id not in node_ids:
            nodes.append({
                "id": ent_id,
                "type": ent.get("category", "unknown")
            })
            node_ids.add(ent_id)
    
    edges = []
    for pair in semantics.get("action_pairs", []):
        action = pair.get("action", "")
        entity = pair.get("entity", "")
        
        if action and entity:
            edges.append({
                "from": action,
                "to": entity,
                "relation": pair.get("normalized_action", "acts_on")
            })
    
    for act in semantics.get("actions", []):
        act_id = act.get("text", "")
        if act_id and act_id not in node_ids:
            nodes.append({
                "id": act_id,
                "type": "verb"
            })
            node_ids.add(act_id)
    
    return {
        "nodes": sorted(nodes, key=lambda x: x["id"]),
        "edges": sorted(edges, key=lambda x: (x.get("from", ""), x.get("to", "")))
    }


def validate_semantic_graph() -> bool:
    """Validate semantic graph builder."""
    test_semantics = {
        "entities": [
            {"text": "api", "category": "system"},
            {"text": "database", "category": "storage"}
        ],
        "actions": [{"text": "build", "type": "verb"}],
        "action_pairs": [
            {"action": "build", "entity": "api", "normalized_action": "build"}
        ]
    }
    
    graph = build_semantic_graph(test_semantics)
    
    if not isinstance(graph, dict):
        return False
    
    if len(graph.get("nodes", [])) < 1:
        return False
    
    return True


if __name__ == "__main__":
    ok = validate_semantic_graph()
    print("SEMANTIC GRAPH:", "PASS" if ok else "FAIL")