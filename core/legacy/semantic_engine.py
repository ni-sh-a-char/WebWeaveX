"""
WebWeaveX Semantic Engine (Pure Version)

Purpose:
    Pure tokenization and graph derivation
    - No semantic maps
    - No keyword logic
    - Deterministic relationships
"""

from typing import Dict, Any, List


def _tokenize(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return [
        t for t in text.lower()
        .replace(",", " ")
        .replace(".", " ")
        .replace("-", " ")
        .replace("_", " ")
        .split()
        if t
    ]


def process_all_semantics(user_input: str) -> Dict[str, Any]:
    """Process semantics from raw user input string (PURE FUNCTION)."""
    if not user_input:
        return _empty_semantics()
    
    return _extract_entities_from_input(user_input)


def _empty_semantics() -> Dict[str, Any]:
    return {"nodes": [], "relationships": [], "version": "v3_1"}


def _extract_entities_from_input(user_input: str) -> Dict[str, Any]:
    """Extract semantics from user input only."""
    if not user_input:
        return _empty_semantics()

    tokens = user_input.replace(",", " ").replace("-", " ").replace("_", " ").split()
    
    node_ids = set()
    for t in tokens:
        if t:
            node_ids.add(t)
    
    relationships = []
    for i in range(len(tokens) - 1):
        if tokens[i] and tokens[i + 1]:
            relationships.append({
                "from": tokens[i],
                "to": tokens[i + 1],
                "relation": "follows"
            })
    
    nodes = [{"id": n} for n in sorted(node_ids)]

    return {
        "nodes": nodes,
        "relationships": relationships,
        "version": "v3_1"
    }


def calculate_semantic_confidence(semantics: Dict[str, Any]) -> float:
    """Calculate confidence score for semantics."""
    if not isinstance(semantics, dict):
        return 0.0
    
    entities = semantics.get("entities", [])
    actions = semantics.get("actions", [])
    relationships = semantics.get("relationships", [])
    
    # Simple confidence based on content
    total_items = len(entities) + len(actions) + len(relationships)
    return min(1.0, total_items / 10.0)