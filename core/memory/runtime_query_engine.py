from __future__ import annotations

from typing import Any, Dict, List


def query_runtime_memory(
    memory: Dict[str, Any],
    query_type: str = "semantic",
    term: str = "",
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    if query_type == "semantic":
        for relation in memory.get("semantic_relations", []):
            if term in str(relation.get("from", "")) or term in str(relation.get("to", "")):
                results.append(relation)
    elif query_type == "lineage":
        for item in memory.get("lineage", []):
            if term in str(item.get("id", "")):
                results.append(item)
    elif query_type == "topology":
        for item in memory.get("runtime_history", []):
            if term in str(item.get("runtime", "")):
                results.append(item)
    elif query_type == "sync":
        for item in memory.get("synchronization_history", []):
            results.append(item)
    else:
        for item in memory.get("runtime_history", []):
            if term in str(item):
                results.append(item)

    return {
        "query_type": query_type,
        "term": term,
        "results": sorted(results, key=lambda item: str(item)),
        "count": len(results),
        "bounded": True,
    }
