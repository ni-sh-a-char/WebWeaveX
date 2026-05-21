from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.cognitive_sovereignty_engine import model_cognitive_sovereignty
from core.evidence.explanatory_nondomestication_engine import resist_explanatory_domestication
from core.evidence.explanatory_self_determination_engine import model_explanatory_self_determination
from core.evidence.interpretive_nondomestication_engine import resist_interpretive_domestication
from core.evidence.interpretive_self_determination_engine import model_interpretive_self_determination
from core.evidence.ontology_nondomestication_engine import resist_ontology_domestication
from core.evidence.ontology_self_determination_engine import model_ontology_self_determination
from core.evidence.recursive_agency_decay_engine import resist_agency_decay
from core.evidence.recursive_agency_engine import model_recursive_agency
from core.evidence.recursive_agency_preservation_engine import preserve_recursive_agency
from core.evidence.recursive_autonomy_preservation_engine import preserve_recursive_autonomy
from core.evidence.recursive_dependency_engine import detect_recursive_dependency
from core.evidence.recursive_domestication_engine import detect_recursive_domestication
from core.evidence.recursive_guardianship_engine import detect_recursive_guardianship
from core.evidence.recursive_independence_decay_engine import resist_independence_decay
from core.evidence.recursive_interpretive_independence_engine import model_recursive_interpretive_independence
from core.evidence.recursive_obedience_engine import detect_recursive_obedience
from core.evidence.recursive_semantic_independence_engine import model_recursive_semantic_independence
from core.evidence.recursive_sovereignty_stability_engine import model_sovereignty_stability
from core.evidence.recursive_submission_engine import detect_recursive_submission
from core.evidence.semantic_dependency_suppression_engine import suppress_semantic_dependency
from core.evidence.semantic_nondomestication_engine import resist_semantic_domestication
from core.evidence.semantic_self_determination_engine import model_semantic_self_determination
from core.semantic.recursive_dependency_pressure_engine import compute_recursive_dependency_pressure


def _depth(bundle: Dict[str, Any]) -> int:
    lineage = bundle.get("lineage", {}) or {}
    stages = lineage.get("stages", [])
    return len(stages) if isinstance(stages, list) else int(lineage.get("depth", 0) or 0)


def apply_recursive_epistemic_sovereignty(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    interpretive = bundle.get("interpretive_diversity", {}) or {}
    interpretations = interpretive.get("interpretations", []) if isinstance(interpretive, dict) else []
    explanatory = bundle.get("explanatory_diversity", {}) or {}
    alternatives = explanatory.get("alternatives", []) if isinstance(explanatory, dict) else []
    entities = list(inferred.keys())
    depth = _depth(bundle)
    interp_count = len(interpretations) or len(inferred)
    cb = bundle.get("confidence_basis", {}) or {}
    score = float(cb.get("score", 0.5))

    independent = interp_count > 1 or len(evidence) >= 2
    sem_self = model_semantic_self_determination(independent, depth)
    interp_self = model_interpretive_self_determination(interp_count)
    onto_self = model_ontology_self_determination(len(entities))
    expl_self = model_explanatory_self_determination(len(alternatives))
    agency = model_recursive_agency(independent, depth)
    sovereignty = model_cognitive_sovereignty(independent)

    dependency = detect_recursive_dependency(depth, interp_count, len(evidence))
    obedience = detect_recursive_obedience(score > 0.7, len(evidence) < 2, depth)
    submission = detect_recursive_submission(reconciled == inferred, depth, len(evidence))
    domestication = detect_recursive_domestication(interp_count <= 1, depth)
    guardianship = detect_recursive_guardianship(
        bundle.get("cognitive_decentralization", {}).get("dominance_without_evidence", False)
        if isinstance(bundle.get("cognitive_decentralization"), dict)
        else False,
        depth,
    )
    dep_pressure = compute_recursive_dependency_pressure(depth, interp_count)

    sem_indep = model_recursive_semantic_independence(list(inferred.keys()), depth)
    interp_indep = model_recursive_interpretive_independence(interp_count)
    agency_pres = preserve_recursive_agency(independent)
    autonomy_pres = preserve_recursive_autonomy(independent)
    dep_suppress = suppress_semantic_dependency(dependency.get("suppressed", []))

    nondom_sem = resist_semantic_domestication(domestication.get("suppress", False))
    nondom_interp = resist_interpretive_domestication(domestication.get("suppress", False))
    nondom_onto = resist_ontology_domestication(submission.get("suppress", False))
    nondom_expl = resist_explanatory_domestication(bundle.get("narrative_monopoly_suppressed", False))

    stab = model_sovereignty_stability(independent, depth)
    indep_decay = resist_independence_decay(independent, depth)
    agency_decay = resist_agency_decay(independent, depth)

    bundle["epistemic_sovereignty"] = {
        "preserved": True,
        "anti_dependent": True,
        "dependency_suppressed": len(dependency.get("suppressed", [])),
    }
    bundle["semantic_self_determination"] = sem_self
    bundle["interpretive_self_determination"] = interp_self
    bundle["ontology_self_determination"] = onto_self
    bundle["explanatory_self_determination"] = expl_self
    bundle["recursive_agency"] = agency
    bundle["cognitive_sovereignty"] = sovereignty
    bundle["recursive_dependency_suppressed"] = dependency.get("suppressed", [])
    bundle["recursive_obedience_suppressed"] = obedience.get("suppress", False)
    bundle["recursive_submission_suppressed"] = submission.get("suppress", False)
    bundle["recursive_domestication_suppressed"] = domestication.get("suppress", False)
    bundle["recursive_guardianship_suppressed"] = guardianship.get("suppress", False)
    bundle["recursive_semantic_independence"] = sem_indep
    bundle["recursive_interpretive_independence"] = interp_indep
    bundle["recursive_agency_preservation"] = agency_pres
    bundle["recursive_autonomy_preservation"] = autonomy_pres
    bundle["dependency_resistance"] = dep_suppress
    bundle["sovereignty_stability"] = stab
    bundle["independence_decay_resisted"] = indep_decay.get("resist", True)
    bundle["agency_decay_resisted"] = agency_decay.get("resist", True)
    bundle["recursive_dependency_pressure"] = dep_pressure
    bundle["nondomestication"] = {
        "semantic": nondom_sem,
        "interpretive": nondom_interp,
        "ontology": nondom_onto,
        "explanatory": nondom_expl,
    }
    return bundle
