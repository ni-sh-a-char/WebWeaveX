from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.evidence_boundary_engine import model_evidence_boundaries
from core.evidence.ontology_boundary_engine import model_ontology_boundaries
from core.evidence.topology_boundary_engine import model_topology_boundaries


def apply_reality_constraints(
    evidence: List[str],
    parser_grounded: bool,
    drift_pressure: float,
) -> Dict[str, Any]:
    ev_bound = model_evidence_boundaries(evidence)
    return {
        "evidence_bounded": ev_bound["bounded"],
        "semantic_growth_allowed": ev_bound["bounded"] and drift_pressure < 0.3,
        "ontology_expansion_allowed": model_ontology_boundaries(evidence)["expansion_allowed"],
        "topology_propagation_allowed": model_topology_boundaries(evidence, parser_grounded)["propagation_allowed"],
        "speculative_coherence_allowed": False,
        "continuity_allowed": ev_bound["bounded"],
    }
