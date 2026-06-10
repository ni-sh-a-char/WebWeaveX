"""Execute Python (canonical) semantic-IR closure functions; emit output + hash.
Usage: PYTHONPATH=<py2.0.1> python run_python.py fixtures.json > python_results.json
"""
import importlib
import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

# fn name -> module path (canonical source location)
REGISTRY = {
    # A.1 — core.documents leaves
    "extract_rhetorical_structure": "core.documents.rhetorical_structure_engine",
    "assign_semantic_roles": "core.documents.semantic_role_engine",
    "extract_headings": "core.documents.heading_engine",
    "reconstruct_argument_dependencies": "core.documents.argument_dependency_engine",
    "resolve_coreferences": "core.documents.coreference_resolution_engine",
    # A.2 — core.semantic pressure leaves
    "compute_ambiguity_pressure": "core.semantic.ambiguity_pressure_engine",
    "compute_contradiction_pressure": "core.semantic.contradiction_pressure_engine",
    "compute_evidence_boundary_pressure": "core.semantic.evidence_boundary_pressure_engine",
    "compute_evidence_decay_pressure": "core.semantic.evidence_decay_pressure_engine",
    "compute_recursive_boundary_pressure": "core.semantic.recursive_boundary_pressure_engine",
    "compute_recursive_convergence_pressure": "core.semantic.recursive_convergence_pressure_engine",
    "compute_recursive_dependency_pressure": "core.semantic.recursive_dependency_pressure_engine",
    "compute_semantic_boundary_pressure": "core.semantic.semantic_boundary_pressure_engine",
    "compute_truth_boundary_pressure": "core.semantic.truth_boundary_pressure_engine",
    "compute_uncertainty_pressure": "core.semantic.uncertainty_pressure_engine",
    # A.2 — core.ir._base leaves
    "empty_confidence": "core.ir._base",
    "empty_lineage": "core.ir._base",
    "merge_evidence": "core.ir._base",
    # A.2 — core.graph leaves
    "model_graph_entropy": "core.graph.graph_entropy_engine",
    "detect_cycles": "core.graph.semantic_cycle_analysis_engine",
    "prove_topology": "core.graph.topology_proof_engine",
    # A.2 — core.repository leaves
    "reason_api_surface": "core.repository.api_surface_reasoning_engine",
    "reconstruct_execution_flow": "core.repository.execution_flow_engine",
    "detect_infra_signals": "core.repository.infra_semantic_engine",
    "resolve_runtime_dependencies": "core.repository.runtime_dependency_engine",
    "infer_service_interactions": "core.repository.service_interaction_engine",
    # A.2 — core.ast leaves
    "build_control_flow_graph": "core.ast.control_flow_engine",
    "reconstruct_execution_paths": "core.ast.execution_path_engine",
    "resolve_symbols": "core.ast.symbol_resolution_engine",
    # A.3 batch 1 — core.evidence trivial leaves
    "detect_authority_concentration": "core.evidence.authority_concentration_engine",
    "diffuse_authority": "core.evidence.authority_diffusion_engine",
    "resist_autonomy_erosion": "core.evidence.autonomy_erosion_engine",
    "model_causal_plurality": "core.evidence.causal_plurality_engine",
    "model_cognitive_decentralization": "core.evidence.cognitive_decentralization_engine",
    "detect_cognitive_gravity_well": "core.evidence.cognitive_gravity_engine",
    "model_cognitive_sovereignty": "core.evidence.cognitive_sovereignty_engine",
    "detect_confidence_echo": "core.evidence.confidence_echo_engine",
    "refuse_unsupported_continuity": "core.evidence.continuity_refusal_engine",
    "model_epistemic_openness": "core.evidence.epistemic_openness_engine",
    "model_evidence_decay": "core.evidence.evidence_decay_engine",
    "apply_explanatory_antigravity": "core.evidence.explanatory_antigravity_engine",
    "model_explanatory_competition": "core.evidence.explanatory_competition_engine",
    "model_explanatory_divergence": "core.evidence.explanatory_divergence_engine",
    "model_explanatory_diversity": "core.evidence.explanatory_diversity_engine",
    "detect_explanatory_fixation": "core.evidence.explanatory_fixation_engine",
    "preserve_explanatory_freedom": "core.evidence.explanatory_freedom_engine",
    "resist_explanatory_domestication": "core.evidence.explanatory_nondomestication_engine",
    "model_explanatory_self_determination": "core.evidence.explanatory_self_determination_engine",
    "refuse_inference": "core.evidence.inference_refusal_engine",
    "model_interpretive_autonomy": "core.evidence.interpretive_autonomy_engine",
    "detect_interpretive_closure": "core.evidence.interpretive_closure_engine",
    "resist_interpretive_decay": "core.evidence.interpretive_decay_engine",
    "distribute_interpretations": "core.evidence.interpretive_distribution_engine",
    "model_interpretive_divergence": "core.evidence.interpretive_divergence_engine",
    "preserve_interpretive_freedom": "core.evidence.interpretive_freedom_engine",
    "resist_interpretive_domestication": "core.evidence.interpretive_nondomestication_engine",
    "model_interpretive_self_determination": "core.evidence.interpretive_self_determination_engine",
    "apply_ontology_antigravity": "core.evidence.ontology_antigravity_engine",
    "model_ontology_boundaries": "core.evidence.ontology_boundary_engine",
    "model_ontology_competition": "core.evidence.ontology_competition_engine",
    "model_ontology_divergence": "core.evidence.ontology_divergence_engine",
    "detect_ontology_fixation": "core.evidence.ontology_fixation_engine",
    "preserve_ontology_freedom": "core.evidence.ontology_freedom_engine",
    "detect_ontology_hardening": "core.evidence.ontology_hardening_engine",
    "model_ontology_instability": "core.evidence.ontology_instability_engine",
    "ontology_limits": "core.evidence.ontology_limit_engine",
    "detect_ontology_monopoly": "core.evidence.ontology_monopoly_engine",
    "resist_ontology_domestication": "core.evidence.ontology_nondomestication_engine",
    "model_ontology_self_determination": "core.evidence.ontology_self_determination_engine",
    "resist_plurality_decay": "core.evidence.plurality_decay_engine",
    "resist_agency_decay": "core.evidence.recursive_agency_decay_engine",
    "model_recursive_agency": "core.evidence.recursive_agency_engine",
    "preserve_recursive_agency": "core.evidence.recursive_agency_preservation_engine",
    "diffuse_recursive_authority": "core.evidence.recursive_authority_diffusion_engine",
    "preserve_recursive_autonomy": "core.evidence.recursive_autonomy_preservation_engine",
    "model_capture_resistance": "core.evidence.recursive_capture_resistance_engine",
    "detect_recursive_centralization": "core.evidence.recursive_centralization_engine",
    "distribute_recursive_cognition": "core.evidence.recursive_cognitive_distribution_engine",
    "detect_recursive_coherence_inflation": "core.evidence.recursive_coherence_inflation_engine",
    "detect_recursive_confidence_echo": "core.evidence.recursive_confidence_echo_engine",
    "detect_recursive_consensus": "core.evidence.recursive_consensus_engine",
    "model_stability_boundary": "core.evidence.stability_boundary_engine",
    "model_topology_boundaries": "core.evidence.topology_boundary_engine",
    "topology_limits": "core.evidence.topology_limit_engine",
    "model_truth_boundaries": "core.evidence.truth_boundary_engine",
    "apply_worldview_antigravity": "core.evidence.worldview_antigravity_engine",
    "suppress_worldview_convergence": "core.evidence.worldview_convergence_engine",
    "model_worldview_diversity": "core.evidence.worldview_diversity_engine",
    "model_worldview_variance": "core.evidence.worldview_variance_engine",
}


def main():
    fixtures = json.load(open(sys.argv[1], encoding="utf-8"))
    out = []
    for fx in fixtures:
        fn = fx["fn"]
        try:
            mod = importlib.import_module(REGISTRY[fn])
            result = getattr(mod, fn)(*fx["args"])
            out.append({"id": fx["id"], "fn": fn, "output": result, "hash": H(result)})
        except Exception as e:  # noqa: BLE001
            out.append({"id": fx["id"], "fn": fn,
                        "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
