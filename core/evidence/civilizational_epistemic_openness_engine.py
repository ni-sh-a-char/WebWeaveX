from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.cognitive_gravity_engine import detect_cognitive_gravity_well
from core.evidence.explanatory_antigravity_engine import apply_explanatory_antigravity
from core.evidence.explanatory_divergence_engine import model_explanatory_divergence
from core.evidence.explanatory_fixation_engine import detect_explanatory_fixation
from core.evidence.interpretive_divergence_engine import model_interpretive_divergence
from core.evidence.ontology_antigravity_engine import apply_ontology_antigravity
from core.evidence.ontology_divergence_engine import model_ontology_divergence
from core.evidence.ontology_fixation_engine import detect_ontology_fixation
from core.evidence.recursive_divergence_preservation_engine import preserve_recursive_divergence
from core.evidence.recursive_entropy_preservation_engine import preserve_recursive_entropy
from core.evidence.recursive_exploration_decay_engine import resist_exploration_decay
from core.evidence.recursive_novelty_decay_engine import resist_novelty_decay
from core.evidence.recursive_novelty_engine import model_recursive_novelty
from core.evidence.recursive_novelty_preservation_engine import preserve_recursive_novelty
from core.evidence.recursive_openness_stability_engine import model_recursive_openness_stability
from core.evidence.recursive_phase_space_engine import model_recursive_phase_space
from core.evidence.recursive_stabilization_engine import detect_recursive_stabilization
from core.evidence.semantic_antigravity_engine import apply_semantic_antigravity
from core.evidence.semantic_attractor_engine import detect_semantic_attractor
from core.evidence.semantic_divergence_engine import model_semantic_divergence
from core.evidence.semantic_fixation_engine import detect_semantic_fixation
from core.evidence.worldview_antigravity_engine import apply_worldview_antigravity
from core.evidence.worldview_variance_engine import model_worldview_variance
from core.semantic.recursive_convergence_pressure_engine import compute_recursive_convergence_pressure


def _depth(bundle: Dict[str, Any]) -> int:
    lineage = bundle.get("lineage", {}) or {}
    stages = lineage.get("stages", [])
    return len(stages) if isinstance(stages, list) else int(lineage.get("depth", 0) or 0)


def apply_civilizational_epistemic_openness(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    uncertainties: List[str] = list(bundle.get("uncertainties", bundle.get("uncertain", [])) or [])
    if isinstance(uncertainties, dict):
        uncertainties = list(uncertainties.keys())
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", bundle.get("contradictions", {})) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    interpretive = bundle.get("interpretive_diversity", {}) or {}
    interpretations = interpretive.get("interpretations", []) if isinstance(interpretive, dict) else []
    explanatory = bundle.get("explanatory_diversity", {}) or {}
    alternatives = explanatory.get("alternatives", []) if isinstance(explanatory, dict) else []
    entities = list(inferred.keys())
    depth = _depth(bundle)
    interp_count = len(interpretations) or len(inferred)
    cb = bundle.get("confidence_basis", {}) or {}
    score = float(cb.get("score", 0.5))

    sem_div = model_semantic_divergence(observed, inferred, ambiguities)
    novelty = model_recursive_novelty(depth, len(set(observed) | set(inferred)), len(ambiguities))
    wv = model_worldview_variance(interp_count, len(pairs))
    interp_div = model_interpretive_divergence(interpretations)
    onto_div = model_ontology_divergence(entities, depth)
    expl_div = model_explanatory_divergence(alternatives)

    attractor = detect_semantic_attractor(depth, interp_count, len(evidence))
    gravity = detect_cognitive_gravity_well(score > 0.75, interp_count <= 1, depth)
    stabilization = detect_recursive_stabilization(reconciled == inferred, depth)
    sem_fix = detect_semantic_fixation(len(set(inferred.keys())) <= 1, depth)
    expl_fix = detect_explanatory_fixation(len(alternatives), depth)
    onto_fix = detect_ontology_fixation(len(entities), depth)

    phase_space = model_recursive_phase_space(len(set(observed) | set(inferred)), len(ambiguities), depth)
    r_entropy = preserve_recursive_entropy(ambiguities, uncertainties, depth)
    div_pres = preserve_recursive_divergence(sem_div["divergence_score"])
    nov_pres = preserve_recursive_novelty(novelty, depth)
    conv_pressure = compute_recursive_convergence_pressure(depth, sem_div["divergence_score"])
    expl_decay = resist_exploration_decay(interp_count > 1 or len(ambiguities) > 0, depth)
    nov_decay = resist_novelty_decay(novelty["novelty"], depth)

    antigrav_sem = apply_semantic_antigravity(gravity.get("suppress", False))
    antigrav_onto = apply_ontology_antigravity(onto_fix.get("suppress", False))
    antigrav_expl = apply_explanatory_antigravity(expl_fix.get("suppress", False))
    antigrav_wv = apply_worldview_antigravity(bundle.get("worldview_convergence_suppressed", False))

    openness_stable = model_recursive_openness_stability(sem_div["preserved"], depth)
    exploratory = interp_count > 1 or len(ambiguities) > 0 or len(alternatives) > 1

    bundle["civilizational_openness"] = {
        "open": True,
        "anti_convergence": True,
        "attractors_suppressed": len(attractor.get("suppressed", [])),
        "phase_space_preserved": phase_space["preserved"],
    }
    bundle["semantic_divergence"] = sem_div
    bundle["recursive_novelty"] = {**novelty, **nov_pres}
    bundle["worldview_variance"] = wv
    bundle["interpretive_divergence"] = interp_div
    bundle["ontology_divergence"] = onto_div
    bundle["explanatory_divergence"] = expl_div
    bundle["semantic_attractors_suppressed"] = attractor.get("suppressed", [])
    bundle["cognitive_gravity_suppressed"] = gravity.get("suppress", False)
    bundle["recursive_stabilization_suppressed"] = stabilization.get("suppress", False)
    bundle["semantic_fixation_suppressed"] = sem_fix.get("suppress", False)
    bundle["explanatory_fixation_suppressed"] = expl_fix.get("suppress", False)
    bundle["ontology_fixation_suppressed"] = onto_fix.get("suppress", False)
    bundle["recursive_phase_space"] = phase_space
    bundle["recursive_entropy_preservation"] = r_entropy
    bundle["exploratory_capacity"] = {"capacity": exploratory, "preserved": exploratory, "collapse_blocked": True}
    bundle["semantic_exploration"] = {"active": exploratory, "novelty": novelty["novelty"]}
    bundle["ontology_exploration"] = {"active": onto_div["preserved"], "entities": len(entities)}
    bundle["interpretive_exploration"] = {"active": interp_div["exploration_maintained"]}
    bundle["worldview_exploration"] = {"active": wv["preserved"]}
    bundle["novelty_preservation"] = nov_pres
    bundle["antigravity"] = {"semantic": antigrav_sem, "ontology": antigrav_onto, "explanatory": antigrav_expl, "worldview": antigrav_wv}
    bundle["openness_stability"] = openness_stable
    bundle["exploration_decay_resisted"] = expl_decay.get("resist", True)
    bundle["novelty_decay_resisted"] = nov_decay.get("resist", True)
    bundle["recursive_convergence_pressure"] = conv_pressure
    bundle["divergence_preservation"] = div_pres
    return bundle
