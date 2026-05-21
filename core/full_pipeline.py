"""
WebWeaveX V7/V8 - FINAL PURE + INTELLIGENCE PIPELINE

Pipeline:
INPUT → TOKENIZATION → NODES → RELATIONSHIPS → GRAPH → SYSTEM → EXECUTION → INTELLIGENCE → OUTPUT

STRICT RULES:
- Deterministic
- No heuristics
- No type fields
- No keyword logic
"""

from typing import Dict, Any
from core.version import ENGINE_VERSION

try:
    from core.intelligence.intelligence_engine import run_intelligence
    from core.crypto.kaalka_wrapper import graph_fingerprint
    KAALKA_AVAILABLE = True
except ImportError:
    KAALKA_AVAILABLE = False

PIPELINE_VERSION = ENGINE_VERSION


def run_pipeline(user_input: str, mode: str = "compiler") -> dict:
    """Main pipeline."""

    tokens = _tokenize(user_input)
    nodes = _generate_nodes(tokens)
    relationships = _generate_relationships(tokens)

    system = _derive_system(nodes, relationships)
    execution_graph = _build_execution_graph(nodes, relationships)
    execution_order = _derive_execution_order(nodes)
    spec = _build_spec(nodes, relationships)

    # SINGLE SOURCE GRAPH (CRITICAL FIX)
    # Intelligence ALWAYS independent of Kaalka
    intelligence = {}
    
    try:
        from core.intelligence.intelligence_engine import run_intelligence
        intelligence = run_intelligence(execution_graph)
    except ImportError:
        pass
    
    # Kaalka ONLY for fingerprint
    fingerprint = ""
    
    if KAALKA_AVAILABLE:
        fp_bytes = graph_fingerprint(execution_graph)
        fingerprint = fp_bytes.hex()

    output = {
        "structured_data": {
            "system": system,
            "execution_graph": execution_graph,
            "execution_order": execution_order,
            "spec": spec,
            "intelligence": intelligence,
            "fingerprint": fingerprint
        },
        "confidence": 1.0,
        "source": "compiler",
        "version": PIPELINE_VERSION
    }
    
    return output


def _tokenize(user_input: str) -> list:
    if not user_input:
        return []

    tokens = user_input.lower()
    tokens = tokens.replace(",", " ").replace("-", " ").replace("_", " ")
    tokens = tokens.replace(".", " ").replace("(", " ").replace(")", " ")
    tokens = tokens.replace("/", " ").split()

    return [t for t in tokens if t]


def _generate_nodes(tokens: list) -> list:
    unique_tokens = sorted(set(tokens))
    nodes = [{"id": t} for t in unique_tokens]
    return sorted(nodes, key=lambda x: x["id"])


def _generate_relationships(tokens: list) -> list:
    if not tokens:
        return []

    WINDOW = 3
    relationships = []

    # SYMMETRIC WINDOW (no positional bias)
    for i in range(len(tokens)):
        for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
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

    return sorted(unique, key=lambda x: (x["from"], x["to"]))


def _derive_system(nodes: list, relationships: list) -> dict:
    components = sorted(
        [{"name": n.get("id", "")} for n in nodes],
        key=lambda x: x["name"]
    )

    return {
        "system_type": "",
        "architecture": "",
        "components": components,
        "relationships": relationships
    }


def _build_execution_graph(nodes: list, relationships: list) -> dict:
    edges = [{"from": r.get("from", ""), "to": r.get("to", "")} for r in relationships]

    return {
        "nodes": nodes,
        "edges": sorted(edges, key=lambda x: (x["from"], x["to"]))
    }


def _derive_execution_order(nodes: list) -> list:
    return sorted([n.get("id", "") for n in nodes])


def _build_spec(nodes: list, relationships: list) -> dict:
    return {
        "node_count": len(nodes),
        "edge_count": len(relationships)
    }