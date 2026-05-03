"""
WebWeaveX V7 - Pure Deterministic System Compiler

Pipeline: INPUT → TOKENIZATION → NODE SET → RELATIONSHIPS → GRAPH → SYSTEM → EXECUTION GRAPH → OUTPUT

NO other paths. NO legacy structures.
"""

from typing import Dict, Any
from core.version import ENGINE_VERSION

PIPELINE_VERSION = ENGINE_VERSION


def run_pipeline(user_input: str, mode: str = "compiler") -> dict:
    """V7 Single Pipeline - Pure Compiler Only."""
    
    # Tokenization
    tokens = _tokenize(user_input)
    
    # Node generation
    nodes = _generate_nodes(tokens)
    
    # Relationship generation  
    relationships = _generate_relationships(tokens)
    
    # System derivation
    system = _derive_system(nodes, relationships)
    
    # Execution graph
    execution_graph = _build_execution_graph(nodes, relationships)
    
    # Execution order
    execution_order = _derive_execution_order(nodes)
    
    # Spec
    spec = _build_spec(nodes, relationships)
    
    # Final output
    return {
        "structured_data": {
            "system": system,
            "execution_graph": execution_graph,
            "execution_order": execution_order,
            "spec": spec
        },
        "confidence": 1.0,
        "source": "compiler",
        "version": PIPELINE_VERSION
    }


def _tokenize(user_input: str) -> list:
    """Tokenize input string."""
    if not user_input:
        return []
    
    tokens = user_input.lower()
    tokens = tokens.replace(",", " ").replace("-", " ").replace("_", " ")
    tokens = tokens.replace(".", " ").replace("(", " ").replace(")", " ")
    tokens = tokens.replace("/", " ").split()
    tokens = [t for t in tokens if t]
    
    return tokens


def _generate_nodes(tokens: list) -> list:
    """Generate nodes from tokens."""
    if not tokens:
        return []
    
    # Deduplicate and SORT for determinism
    unique_tokens = sorted(set(tokens))
    nodes = [{"id": t} for t in unique_tokens]
    
    return sorted(nodes, key=lambda x: x["id"])


def _generate_relationships(tokens: list) -> list:
    """Generate relationships using SEQUENCE + FULL CONNECTIVITY."""
    if not tokens:
        return []
    
    relationships = []
    
    # RULE 1: SEQUENCE (preserve order meaning)
    for i in range(len(tokens) - 1):
        relationships.append({
            "from": tokens[i],
            "to": tokens[i + 1]
        })
    
    # RULE 2: FULL CONNECTIVITY (critical for real graph)
    for i in range(len(tokens)):
        for j in range(len(tokens)):
            if i != j:
                relationships.append({
                    "from": tokens[i],
                    "to": tokens[j]
                })
    
    # DEDUPLICATE
    seen = set()
    unique = []
    
    for r in relationships:
        key = (r["from"], r["to"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    # SORT for determinism
    return sorted(unique, key=lambda x: (x["from"], x["to"]))


def _derive_system(nodes: list, relationships: list) -> dict:
    """Derive system from graph."""
    components = sorted([{"name": n.get("id", "")} for n in nodes], key=lambda x: x["name"])
    
    return {
        "system_type": "",
        "architecture": "",
        "components": components,
        "relationships": relationships
    }


def _build_execution_graph(nodes: list, relationships: list) -> dict:
    """Build execution graph."""
    # Use relationships directly as edges (already sorted from _generate_relationships)
    edges = [
        {"from": r.get("from", ""), "to": r.get("to", "")}
        for r in relationships
    ]
    
    return {
        "nodes": nodes,
        "edges": sorted(edges, key=lambda x: (x["from"], x["to"]))
    }


def _derive_execution_order(nodes: list) -> list:
    """Derive execution order (sorted node IDs)."""
    return sorted([n.get("id", "") for n in nodes])


def _build_spec(nodes: list, relationships: list) -> dict:
    """Build spec."""
    return {
        "node_count": len(nodes),
        "edge_count": len(relationships)
    }


# Backward compatibility
def _run_compiler_mode(user_input: str) -> dict:
    """Legacy alias."""
    return run_pipeline(user_input, "compiler")


def _run_full_pipeline(user_input: str) -> dict:
    """Legacy alias - same as compiler."""
    return run_pipeline(user_input, "compiler")