from __future__ import annotations

from typing import Any, Dict

from core.documents.instructional_flow_engine import extract_instructional_flow
from core.documents.concept_transition_engine import model_concept_transitions


def build_document_dependency_graph(text: str) -> Dict[str, Any]:
    flow = extract_instructional_flow(text)
    trans = model_concept_transitions(text)
    nodes = [{"id": s.get("title", f"step{i}"), "kind": "step"} for i, s in enumerate(flow["steps"])]
    edges = trans.get("transitions", [])
    return {"nodes": nodes, "edges": edges, "prerequisites": flow.get("prerequisites", [])}
