from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_edge_engine import build_semantic_edge
from core.documents.semantic_section_reconstruction_engine import reconstruct_semantic_sections
from core.evidence import structure_cognition


def reconstruct_semantic_causality(text: str) -> Dict[str, Any]:
    sections = reconstruct_semantic_sections(text)
    explains = sections.get("inferred", {}).get("semantic", {}).get("explains", [])
    causal: List[Dict[str, Any]] = []
    for link in explains:
        if not isinstance(link, dict):
            continue
        f, t = link.get("from", ""), link.get("to", "")
        if f and t:
            causal.append(build_semantic_edge(f, t, "causes", ["discourse:section_order"]))
            causal.append(build_semantic_edge(f, t, "explains", ["discourse:explanation"]))
    enables = [build_semantic_edge(c["from"], c["to"], "enables", ["causal:enables"]) for c in causal[:20]]
    requires = [
        build_semantic_edge(causal[i + 1]["from"], causal[i]["to"], "requires", ["causal:prerequisite"])
        for i in range(max(0, len(causal) - 1))
    ]
    observed = {"section_links": len(explains)}
    inferred = {"causal_edges": causal, "enables": enables, "requires": requires}
    reconciled = {
        "what_enables_what": enables,
        "what_requires_what": requires,
        "what_explains_what": [e for e in causal if e.get("relation") == "explains"],
        "what_contradicts_what": [],
    }
    return structure_cognition(observed, inferred, reconciled, parsed=None)
