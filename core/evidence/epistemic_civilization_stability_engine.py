from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.authority_diffusion_engine import diffuse_authority
from core.evidence.epistemic_openness_engine import model_epistemic_openness
from core.evidence.explanatory_diversity_engine import model_explanatory_diversity
from core.evidence.interpretive_decay_engine import resist_interpretive_decay
from core.evidence.interpretive_closure_engine import detect_interpretive_closure
from core.evidence.interpretive_diversity_engine import model_interpretive_diversity
from core.evidence.interpretive_distribution_engine import distribute_interpretations
from core.evidence.ontology_alternative_engine import model_ontology_alternatives
from core.evidence.ontology_hardening_engine import detect_ontology_hardening
from core.evidence.ontology_instability_engine import model_ontology_instability
from core.evidence.plurality_decay_engine import resist_plurality_decay
from core.evidence.recursive_consensus_engine import detect_recursive_consensus
from core.evidence.semantic_alternative_engine import model_semantic_alternatives
from core.evidence.semantic_decentralization_engine import model_semantic_decentralization
from core.evidence.semantic_diversity_engine import model_semantic_diversity
from core.evidence.semantic_homogenization_engine import detect_semantic_homogenization
from core.evidence.semantic_monoculture_engine import detect_semantic_monoculture
from core.evidence.semantic_orthodoxy_engine import detect_semantic_orthodoxy
from core.evidence.semantic_plurality_engine import model_semantic_plurality
from core.evidence.semantic_uniformity_engine import detect_semantic_uniformity
from core.evidence.worldview_convergence_engine import suppress_worldview_convergence
from core.evidence.worldview_diversity_engine import model_worldview_diversity
from core.evidence.causal_plurality_engine import model_causal_plurality


def _depth(bundle: Dict[str, Any]) -> int:
    lineage = bundle.get("lineage", {}) or {}
    stages = lineage.get("stages", [])
    return len(stages) if isinstance(stages, list) else int(lineage.get("depth", 0) or 0)


def apply_epistemic_civilization_stability(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", bundle.get("contradictions", {})) or {}
    unstable = list(bundle.get("unstable_regions", []) or [])
    depth = _depth(bundle)

    plurality = model_semantic_plurality(observed, inferred, ambiguities, contradicted)
    interpretive = model_interpretive_diversity(evidence, inferred)
    interpretations = interpretive.get("interpretations", [])
    decentralization = model_semantic_decentralization(interpretations, len(evidence))
    ontology_inst = model_ontology_instability(unstable, depth)
    worldview = model_worldview_diversity(interpretations, contradicted)
    explanatory = model_explanatory_diversity(inferred, evidence)
    openness = model_epistemic_openness(plurality, decentralization)

    monoculture = detect_semantic_monoculture(interpretations, evidence, depth)
    hardening = detect_ontology_hardening(depth, len(evidence))
    consensus = detect_recursive_consensus(reconciled == inferred, depth, len(evidence))
    orthodoxy = detect_semantic_orthodoxy(interpretations, depth)
    closure = detect_interpretive_closure(plurality.get("alternative_count", 0), depth)
    uniformity = detect_semantic_uniformity(list(inferred.keys()), depth)
    homogenization = detect_semantic_homogenization(uniformity.get("uniformity_detected", False), depth)
    plurality_decay = resist_plurality_decay(plurality.get("alternative_count", 0), depth)
    interpretive_decay = resist_interpretive_decay(len(interpretations), depth)
    worldview_conv = suppress_worldview_convergence(consensus.get("consensus_inflated", False), depth)
    diversity = model_semantic_diversity(observed, inferred, ambiguities)
    alternatives = model_semantic_alternatives(observed, inferred)
    causal = model_causal_plurality(inferred)
    authority = diffuse_authority(interpretations)
    distribution = distribute_interpretations(interpretations)

    suppressed = monoculture.get("suppressed", [])

    bundle["epistemic_openness"] = openness
    bundle["semantic_plurality"] = plurality
    bundle["interpretive_diversity"] = interpretive
    bundle["semantic_decentralization"] = decentralization
    bundle["ontology_instability"] = ontology_inst
    bundle["worldview_diversity"] = worldview
    bundle["explanatory_diversity"] = explanatory
    bundle["semantic_monoculture_suppressed"] = suppressed
    bundle["ontology_hardening_suppressed"] = hardening.get("suppress", False)
    bundle["recursive_consensus_suppressed"] = consensus.get("suppress", False)
    bundle["semantic_orthodoxy_suppressed"] = orthodoxy.get("suppress", False)
    bundle["interpretive_closure_suppressed"] = closure.get("suppress", False)
    bundle["semantic_diversity"] = diversity
    bundle["semantic_alternatives"] = alternatives
    bundle["causal_plurality"] = causal
    bundle["authority_diffusion"] = authority
    bundle["interpretive_distribution"] = distribution
    bundle["plurality_decay_resistance"] = plurality_decay
    bundle["interpretive_decay_resistance"] = interpretive_decay
    bundle["worldview_convergence_suppressed"] = worldview_conv.get("suppress", False)
    bundle["semantic_homogenization_suppressed"] = homogenization.get("suppress", False)
    bundle["civilization_stability"] = {
        "stable": openness.get("open", True),
        "plurality_preserved": plurality.get("preserved", True),
        "anti_monoculture": bool(suppressed) or not monoculture.get("detected"),
    }
    return bundle
