from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.authority_concentration_engine import detect_authority_concentration
from core.evidence.autonomy_erosion_engine import resist_autonomy_erosion
from core.evidence.cognitive_decentralization_engine import model_cognitive_decentralization
from core.evidence.explanatory_competition_engine import model_explanatory_competition
from core.evidence.explanatory_freedom_engine import preserve_explanatory_freedom
from core.evidence.interpretive_autonomy_engine import model_interpretive_autonomy
from core.evidence.interpretive_freedom_engine import preserve_interpretive_freedom
from core.evidence.ontology_competition_engine import model_ontology_competition
from core.evidence.ontology_freedom_engine import preserve_ontology_freedom
from core.evidence.ontology_monopoly_engine import detect_ontology_monopoly
from core.evidence.recursive_authority_diffusion_engine import diffuse_recursive_authority
from core.evidence.recursive_capture_resistance_engine import model_capture_resistance
from core.evidence.recursive_centralization_engine import detect_recursive_centralization
from core.evidence.recursive_cognitive_distribution_engine import distribute_recursive_cognition
from core.evidence.recursive_narrative_monopoly_engine import detect_recursive_narrative_monopoly
from core.evidence.recursive_semantic_decentralization_engine import model_recursive_semantic_decentralization
from core.evidence.recursive_semantic_distribution_engine import distribute_recursive_semantics
from core.evidence.recursive_trust_monopoly_engine import detect_recursive_trust_monopoly
from core.evidence.semantic_autonomy_engine import model_semantic_autonomy
from core.evidence.semantic_freedom_engine import model_semantic_freedom
from core.evidence.semantic_governance_engine import suppress_semantic_governance
from core.evidence.semantic_hierarchy_engine import detect_semantic_hierarchy_permanence
from core.evidence.semantic_monopoly_engine import detect_semantic_monopoly


def _depth(bundle: Dict[str, Any]) -> int:
    lineage = bundle.get("lineage", {}) or {}
    stages = lineage.get("stages", [])
    return len(stages) if isinstance(stages, list) else int(lineage.get("depth", 0) or 0)


def apply_cognitive_anti_capture(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    inferred = bundle.get("inferred", {}) or {}
    interpretive = bundle.get("interpretive_diversity", {}) or {}
    interpretations = interpretive.get("interpretations", []) if isinstance(interpretive, dict) else []
    explanatory = bundle.get("explanatory_diversity", {}) or {}
    alternatives = explanatory.get("alternatives", []) if isinstance(explanatory, dict) else []
    entities = list(set(str(k) for k in inferred.keys()))
    depth = _depth(bundle)
    cb = bundle.get("confidence_basis", {}) or {}
    trust_score = float(cb.get("score", 0.5))

    sem_autonomy = model_semantic_autonomy(interpretations, len(evidence))
    interp_autonomy = model_interpretive_autonomy(interpretations)
    onto_comp = model_ontology_competition(entities, depth)
    expl_comp = model_explanatory_competition(alternatives)
    sem_freedom = model_semantic_freedom(sem_autonomy, expl_comp)
    cognitive_decent = model_cognitive_decentralization(len(interpretations) or len(inferred), len(evidence))

    sem_monopoly = detect_semantic_monopoly(len(interpretations) or len(inferred), depth, len(evidence))
    onto_monopoly = detect_ontology_monopoly(len(entities), depth)
    authority = detect_authority_concentration(sem_autonomy.get("dominant_cluster", False), depth)
    trust_monopoly = detect_recursive_trust_monopoly(trust_score, depth, len(evidence))
    narrative_monopoly = detect_recursive_narrative_monopoly(len(alternatives) or len(interpretations), depth)
    hierarchy = detect_semantic_hierarchy_permanence(depth, bundle.get("semantic_decentralization", {}).get("hierarchy_lock_in", False) if isinstance(bundle.get("semantic_decentralization"), dict) else False)

    r_decent = model_recursive_semantic_decentralization(entities, len(evidence))
    r_auth_diff = diffuse_recursive_authority(len(interpretations))
    r_sem_dist = distribute_recursive_semantics(list(inferred.keys()))
    r_cog_dist = distribute_recursive_cognition(len(bundle.get("unstable_regions", []) or []))

    expl_freedom = preserve_explanatory_freedom(alternatives)
    onto_freedom = preserve_ontology_freedom(onto_comp)
    interp_freedom = preserve_interpretive_freedom(interp_autonomy)
    autonomy_erosion = resist_autonomy_erosion(sem_autonomy.get("autonomous", True), depth)
    governance = suppress_semantic_governance(False, depth)
    centralization = detect_recursive_centralization(r_decent.get("decentralized", True), depth)

    suppressed = sem_monopoly.get("suppressed", [])
    capture_resistance = model_capture_resistance(suppressed)

    bundle["cognitive_anti_capture"] = {
        "active": True,
        "capture_suppressed": len(suppressed),
        "monopolies_blocked": sem_monopoly.get("monopoly", False) or onto_monopoly.get("monopoly", False),
    }
    bundle["semantic_autonomy"] = sem_autonomy
    bundle["interpretive_autonomy"] = interp_autonomy
    bundle["ontology_competition"] = onto_comp
    bundle["explanatory_competition"] = expl_comp
    bundle["semantic_freedom"] = sem_freedom
    bundle["cognitive_decentralization"] = cognitive_decent
    bundle["recursive_semantic_decentralization"] = r_decent
    bundle["recursive_authority_diffusion"] = r_auth_diff
    bundle["recursive_semantic_distribution"] = r_sem_dist
    bundle["recursive_cognitive_distribution"] = r_cog_dist
    bundle["explanatory_freedom"] = expl_freedom
    bundle["ontology_freedom"] = onto_freedom
    bundle["interpretive_freedom"] = interp_freedom
    bundle["capture_resistance"] = capture_resistance
    bundle["semantic_monopoly_suppressed"] = suppressed
    bundle["ontology_monopoly_suppressed"] = onto_monopoly.get("suppress", False)
    bundle["trust_monopoly_suppressed"] = trust_monopoly.get("suppress", False)
    bundle["narrative_monopoly_suppressed"] = narrative_monopoly.get("suppress", False)
    bundle["authority_concentration_suppressed"] = authority.get("suppress", False)
    bundle["hierarchy_permanence_suppressed"] = hierarchy.get("suppress", False)
    bundle["semantic_governance_suppressed"] = governance.get("suppress", False)
    bundle["recursive_centralization_suppressed"] = centralization.get("suppress", False)
    bundle["autonomy_erosion_resisted"] = autonomy_erosion.get("resist", True)
    bundle["anti_capture_stability"] = {
        "stable": capture_resistance.get("resistant", True),
        "freedom_preserved": sem_freedom.get("free", True),
    }
    return bundle
