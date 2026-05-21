from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_dependency_engine import reconstruct_discourse_dependencies
from core.documents.semantic_narrative_engine import reconstruct_narrative
from core.evidence import structure_cognition


def reconstruct_semantic_flow(text: str) -> Dict[str, Any]:
    discourse = reconstruct_discourse_dependencies(text)
    narrative = reconstruct_narrative(text)
    flow_edges = discourse.get("reconciled", {}).get("discourse_flow", [])
    observed = {"discourse_edges": len(flow_edges)}
    inferred = {
        "semantic_flow": flow_edges,
        "narrative_flow": narrative.get("narrative_flow", []),
        "transitions": flow_edges,
    }
    reconciled = {"flow": flow_edges, "continuity": narrative.get("narrative_flow", [])}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
