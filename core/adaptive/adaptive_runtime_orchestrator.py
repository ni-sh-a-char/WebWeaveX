from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.adaptive.adaptive_runtime_graph_engine import build_adaptive_runtime_graph
from core.adaptive.adaptive_snapshot_engine import build_adaptive_snapshot
from core.adaptive.extraction_memory_engine import remember_extraction_runtime
from core.adaptive.runtime_adaptation_engine import run_runtime_adaptation
from core.adaptive.runtime_reconciliation_engine import reconcile_runtime_state
from core.adaptive.schema_stability_engine import stabilize_extraction_schema


def run_adaptive_extraction(
    url: str,
    dom: Dict[str, Any],
    html: str,
    extraction: Dict[str, Any],
    interactions: Optional[List[Dict[str, Any]]] = None,
    memory: Optional[Dict[str, Any]] = None,
    primary_selector: str = "body",
    page: Any = None,
    stream_state: Optional[Dict[str, Any]] = None,
    identity_state: Optional[Dict[str, Any]] = None,
    pagination_state: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    dom_nodes = list(dom.get("nodes", []))
    interactions = list(interactions or [])
    memory = dict(memory or {})

    adaptation = run_runtime_adaptation(
        url=url,
        dom_nodes=dom_nodes,
        html=html,
        interactions=interactions,
        primary_selector=primary_selector,
        page=page,
    )

    schema = stabilize_extraction_schema(extraction)
    reconciliation = reconcile_runtime_state(
        browser_runtime={"available": True, "url": url},
        stream_runtime=stream_state or {},
        interaction_runtime=adaptation.get("interaction_recovery", {}),
        extraction_runtime=schema,
    )

    snapshot = build_adaptive_snapshot(
        dom=dom,
        selectors=memory.get("selectors", {}),
        interaction_state={"interactions": interactions},
        streaming_state=stream_state or {},
        identity_state=identity_state or {},
        pagination_state=pagination_state or adaptation.get("pagination_recovery", {}),
    )

    updated_memory = remember_extraction_runtime(
        memory,
        {
            "selectors": {
                primary_selector: adaptation["fallback"]["active"]["selector"],
            },
            "healed_selectors": {
                primary_selector: adaptation["fallback"]["chain"][1]["selector"],
            },
            "pagination_patterns": [
                adaptation["pagination_recovery"].get("recovered_selector", ""),
            ],
            "modal_solutions": adaptation["modal_recovery"].get("recovered", []),
            "interaction_chains": adaptation["interaction_recovery"].get("interactions", []),
        },
    )

    graph = build_adaptive_runtime_graph(adaptation)

    return {
        "adaptation": adaptation,
        "schema": schema,
        "reconciliation": reconciliation,
        "snapshot": snapshot,
        "memory": updated_memory,
        "graph": graph,
        "bounded": True,
    }
