from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_lineage_memory(
    selector: Optional[List[Dict[str, Any]]] = None,
    workflow: Optional[List[Dict[str, Any]]] = None,
    sync: Optional[List[Dict[str, Any]]] = None,
    evolution: Optional[List[Dict[str, Any]]] = None,
    extraction: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    lineage: List[Dict[str, Any]] = []

    for bucket, items in (
        ("selector", selector or []),
        ("workflow", workflow or []),
        ("sync", sync or []),
        ("evolution", evolution or []),
        ("extraction", extraction or []),
    ):
        for index, item in enumerate(items[:1000]):
            lineage.append({
                "id": str(item.get("id", f"{bucket}:{index}")),
                "kind": bucket,
                "ancestor": str(item.get("ancestor", "")),
            })

    return {
        "lineage": sorted(lineage, key=lambda item: (item["kind"], item["id"])),
        "selector_ancestry": [item for item in lineage if item["kind"] == "selector"],
        "workflow_ancestry": [item for item in lineage if item["kind"] == "workflow"],
        "sync_ancestry": [item for item in lineage if item["kind"] == "sync"],
        "evolution_ancestry": [item for item in lineage if item["kind"] == "evolution"],
        "extraction_ancestry": [item for item in lineage if item["kind"] == "extraction"],
        "bounded": True,
    }
