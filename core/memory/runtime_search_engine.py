from __future__ import annotations

from typing import Any, Dict, List


def search_runtime_memory(
    index: Dict[str, Any],
    term: str,
    search_type: str = "structural",
) -> Dict[str, Any]:
    matches: List[Dict[str, Any]] = []
    normalized = term.lower().strip()

    if search_type == "semantic":
        for key, value in index.get("entity_index", {}).items():
            if normalized in key.lower():
                matches.append({"match": key, "value": value, "kind": "entity"})
    elif search_type == "lineage":
        for key, value in index.get("workflow_index", {}).items():
            if normalized in key.lower():
                matches.append({"match": key, "value": value, "kind": "workflow"})
    elif search_type == "graph":
        for key, value in index.get("graph_index", {}).items():
            matches.append({"match": key, "value": value, "kind": "graph"})
    else:
        for bucket in ("entity_index", "workflow_index", "connector_index"):
            for key, value in index.get(bucket, {}).items():
                if normalized in key.lower() or normalized in str(value).lower():
                    matches.append({"match": key, "value": value, "kind": bucket})

    return {
        "search_type": search_type,
        "term": term,
        "matches": sorted(matches, key=lambda item: str(item.get("match", ""))),
        "count": len(matches),
        "bounded": True,
    }
