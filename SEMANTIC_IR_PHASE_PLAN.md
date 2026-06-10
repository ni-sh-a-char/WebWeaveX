# SEMANTIC_IR_PHASE_PLAN.md

> **Recomputed from `origin/python` 2.0.1 source** by `tools/gen_semantic_ir_phaseplan.py`. Accurate call edges (resolved via each function's own module namespace — no name-collision guessing). Topologically layered so each phase depends only on earlier phases and is independently executable/provable.

**Closure: 292 functions · 3677 lines · 15 phases.**

## Phase summary (topological order; Phase A = leaves)

| Phase | Functions | Lines | Determinism ops | Parity risk |
|-------|----------:|------:|----------------:|:-----------:|
| A | 212 | 1808 | 186 | HIGH |
| B | 36 | 578 | 34 | HIGH |
| C | 17 | 554 | 24 | HIGH |
| D | 6 | 170 | 8 | MEDIUM |
| E | 6 | 234 | 5 | MEDIUM |
| F | 4 | 96 | 2 | MEDIUM |
| G | 1 | 51 | 2 | MEDIUM |
| H | 1 | 47 | 2 | MEDIUM |
| I | 1 | 40 | 5 | MEDIUM |
| J | 1 | 24 | 2 | MEDIUM |
| K | 1 | 8 | 0 | LOW |
| L | 1 | 17 | 0 | LOW |
| M | 1 | 15 | 0 | LOW |
| N | 2 | 28 | 0 | LOW |
| O | 2 | 7 | 0 | LOW |

## Phase A — leaf functions (no in-closure dependencies)

These have **zero unported dependencies** and are ported & proven first.

| Module | Function | Lines | Determinism ops |
|--------|----------|------:|-----------------|
| `core.ast.control_flow_engine` | `build_control_flow_graph` | 26 | — |
| `core.ast.execution_path_engine` | `reconstruct_execution_paths` | 16 | — |
| `core.ast.python_ast_engine` | `_node` | 6 | — |
| `core.ast.symbol_resolution_engine` | `resolve_symbols` | 23 | sorted(×1 |
| `core.documents.argument_dependency_engine` | `reconstruct_argument_dependencies` | 22 | sorted(×1 |
| `core.documents.coreference_resolution_engine` | `resolve_coreferences` | 7 | — |
| `core.documents.heading_engine` | `extract_headings` | 6 | sorted(×1 |
| `core.documents.rhetorical_structure_engine` | `extract_rhetorical_structure` | 16 | — |
| `core.documents.semantic_role_engine` | `assign_semantic_roles` | 8 | — |
| `core.evidence.ambiguity_visibility_engine` | `expose_ambiguity_visibility` | 11 | round(×2, sorted(×1, set(×1 |
| `core.evidence.authority_concentration_engine` | `detect_authority_concentration` | 3 | — |
| `core.evidence.authority_diffusion_engine` | `diffuse_authority` | 2 | — |
| `core.evidence.autonomy_erosion_engine` | `resist_autonomy_erosion` | 3 | — |
| `core.evidence.causal_plurality_engine` | `model_causal_plurality` | 2 | — |
| `core.evidence.civilizational_epistemic_openness_engine` | `_depth` | 4 | — |
| `core.evidence.cognitive_anti_capture_engine` | `_depth` | 4 | — |
| `core.evidence.cognitive_decentralization_engine` | `model_cognitive_decentralization` | 8 | — |
| `core.evidence.cognitive_gravity_engine` | `detect_cognitive_gravity_well` | 3 | — |
| `core.evidence.cognitive_sovereignty_engine` | `model_cognitive_sovereignty` | 7 | — |
| `core.evidence.confidence_cap_engine` | `apply_confidence_caps` | 27 | round(×4 |
| `core.evidence.confidence_echo_engine` | `detect_confidence_echo` | 6 | round(×1 |
| `core.evidence.continuity_refusal_engine` | `refuse_unsupported_continuity` | 7 | sorted(×1, set(×1 |
| `core.evidence.contradiction_lattice_engine` | `build_contradiction_lattice` | 15 | round(×1, sorted(×1 |
| `core.evidence.epistemic_boundary_engine` | `preserve_epistemic_boundaries` | 13 | — |
| `core.evidence.epistemic_civilization_stability_engine` | `_depth` | 4 | — |
| `core.evidence.epistemic_limit_engine` | `model_epistemic_limits` | 19 | sorted(×1, set(×1 |
| `core.evidence.epistemic_openness_engine` | `model_epistemic_openness` | 8 | — |
| `core.evidence.evidence_algebra_engine` | `combine_evidence` | 12 | round(×1, sorted(×1, set(×1 |
| `core.evidence.evidence_boundary_engine` | `model_evidence_boundaries` | 9 | — |
| `core.evidence.evidence_decay_engine` | `model_evidence_decay` | 8 | — |
| `core.evidence.evidence_sufficiency_engine` | `assess_evidence_sufficiency` | 10 | — |
| `core.evidence.evidence_weighting_calculus` | `weight_evidence_calculus` | 18 | round(×1, sorted(×1, set(×1 |
| `core.evidence.explainability_engine` | `build_explainability` | 32 | sorted(×1 |
| `core.evidence.explanatory_antigravity_engine` | `apply_explanatory_antigravity` | 2 | — |
| `core.evidence.explanatory_competition_engine` | `model_explanatory_competition` | 6 | — |
| `core.evidence.explanatory_divergence_engine` | `model_explanatory_divergence` | 2 | — |
| `core.evidence.explanatory_diversity_engine` | `model_explanatory_diversity` | 8 | — |
| `core.evidence.explanatory_fixation_engine` | `detect_explanatory_fixation` | 3 | — |
| `core.evidence.explanatory_freedom_engine` | `preserve_explanatory_freedom` | 2 | — |
| `core.evidence.explanatory_nondomestication_engine` | `resist_explanatory_domestication` | 2 | — |
| `core.evidence.explanatory_self_determination_engine` | `model_explanatory_self_determination` | 6 | — |
| `core.evidence.inference_integrity_engine` | `model_inference_integrity` | 18 | sorted(×3, set(×3 |
| `core.evidence.inference_refusal_engine` | `refuse_inference` | 7 | sorted(×1, set(×1 |
| `core.evidence.inference_termination_engine` | `terminate_inference_chain` | 12 | sorted(×1, set(×1 |
| `core.evidence.instability_preservation_engine` | `preserve_instability` | 16 | sorted(×1, set(×1 |
| `core.evidence.insufficiency_engine` | `mark_insufficiency` | 15 | sorted(×1, set(×1 |
| `core.evidence.interpretive_autonomy_engine` | `model_interpretive_autonomy` | 7 | — |
| `core.evidence.interpretive_closure_engine` | `detect_interpretive_closure` | 3 | — |
| `core.evidence.interpretive_decay_engine` | `resist_interpretive_decay` | 3 | — |
| `core.evidence.interpretive_distribution_engine` | `distribute_interpretations` | 2 | — |
| `core.evidence.interpretive_divergence_engine` | `model_interpretive_divergence` | 2 | — |
| `core.evidence.interpretive_diversity_engine` | `model_interpretive_diversity` | 16 | — |
| `core.evidence.interpretive_freedom_engine` | `preserve_interpretive_freedom` | 2 | — |
| `core.evidence.interpretive_nondomestication_engine` | `resist_interpretive_domestication` | 2 | — |
| `core.evidence.interpretive_self_determination_engine` | `model_interpretive_self_determination` | 7 | — |
| `core.evidence.lineage_engine` | `build_lineage` | 14 | sorted(×2 |
| `core.evidence.narrative_hallucination_engine` | `detect_narrative_hallucination` | 11 | — |
| `core.evidence.noninferable_scope_engine` | `model_noninferable_regions` | 20 | sorted(×1, set(×1 |
| `core.evidence.noninference_engine` | `model_noninference` | 23 | sorted(×3, set(×2 |
| `core.evidence.ontology_antigravity_engine` | `apply_ontology_antigravity` | 2 | — |
| `core.evidence.ontology_boundary_engine` | `model_ontology_boundaries` | 8 | — |
| `core.evidence.ontology_competition_engine` | `model_ontology_competition` | 7 | — |
| `core.evidence.ontology_divergence_engine` | `model_ontology_divergence` | 2 | set(×1 |
| `core.evidence.ontology_fixation_engine` | `detect_ontology_fixation` | 3 | — |
| `core.evidence.ontology_freedom_engine` | `preserve_ontology_freedom` | 2 | — |
| `core.evidence.ontology_hardening_engine` | `detect_ontology_hardening` | 7 | — |
| `core.evidence.ontology_instability_engine` | `model_ontology_instability` | 8 | — |
| `core.evidence.ontology_limit_engine` | `ontology_limits` | 2 | — |
| `core.evidence.ontology_monopoly_engine` | `detect_ontology_monopoly` | 3 | — |
| `core.evidence.ontology_nondomestication_engine` | `resist_ontology_domestication` | 2 | — |
| `core.evidence.ontology_self_determination_engine` | `model_ontology_self_determination` | 6 | — |
| `core.evidence.plurality_decay_engine` | `resist_plurality_decay` | 3 | — |
| `core.evidence.provenance_engine` | `build_provenance` | 16 | sorted(×2, set(×2 |
| `core.evidence.recursive_agency_decay_engine` | `resist_agency_decay` | 2 | — |
| `core.evidence.recursive_agency_engine` | `model_recursive_agency` | 7 | — |
| `core.evidence.recursive_agency_preservation_engine` | `preserve_recursive_agency` | 2 | — |
| `core.evidence.recursive_authority_diffusion_engine` | `diffuse_recursive_authority` | 2 | — |
| `core.evidence.recursive_autonomy_preservation_engine` | `preserve_recursive_autonomy` | 2 | — |
| `core.evidence.recursive_capture_resistance_engine` | `model_capture_resistance` | 6 | — |
| `core.evidence.recursive_centralization_engine` | `detect_recursive_centralization` | 3 | — |
| `core.evidence.recursive_cognitive_distribution_engine` | `distribute_recursive_cognition` | 2 | — |
| `core.evidence.recursive_coherence_inflation_engine` | `detect_recursive_coherence_inflation` | 3 | — |
| `core.evidence.recursive_confidence_echo_engine` | `detect_recursive_confidence_echo` | 6 | round(×1 |
| `core.evidence.recursive_consensus_engine` | `detect_recursive_consensus` | 3 | — |
| `core.evidence.recursive_dependency_engine` | `_record` | 10 | — |
| `core.evidence.recursive_divergence_preservation_engine` | `preserve_recursive_divergence` | 2 | — |
| `core.evidence.recursive_domestication_engine` | `detect_recursive_domestication` | 3 | — |
| `core.evidence.recursive_drift_engine` | `detect_recursive_drift` | 7 | round(×1 |
| `core.evidence.recursive_entropy_engine` | `model_recursive_entropy` | 16 | round(×1 |
| `core.evidence.recursive_entropy_preservation_engine` | `preserve_recursive_entropy` | 3 | round(×1 |
| `core.evidence.recursive_epistemic_sovereignty_engine` | `_depth` | 4 | — |
| `core.evidence.recursive_evidence_ancestry_engine` | `track_recursive_evidence_ancestry` | 3 | — |
| `core.evidence.recursive_exploration_decay_engine` | `resist_exploration_decay` | 3 | — |
| `core.evidence.recursive_guardianship_engine` | `detect_recursive_guardianship` | 3 | — |
| `core.evidence.recursive_independence_decay_engine` | `resist_independence_decay` | 3 | — |
| `core.evidence.recursive_instability_engine` | `model_recursive_instability` | 16 | sorted(×1, set(×1 |
| `core.evidence.recursive_interpretive_independence_engine` | `model_recursive_interpretive_independence` | 2 | — |
| `core.evidence.recursive_lineage_engine` | `preserve_recursive_lineage` | 20 | — |
| `core.evidence.recursive_narrative_monopoly_engine` | `detect_recursive_narrative_monopoly` | 3 | — |
| `core.evidence.recursive_novelty_decay_engine` | `resist_novelty_decay` | 3 | — |
| `core.evidence.recursive_novelty_engine` | `model_recursive_novelty` | 3 | round(×1 |
| `core.evidence.recursive_novelty_preservation_engine` | `preserve_recursive_novelty` | 3 | — |
| `core.evidence.recursive_obedience_engine` | `detect_recursive_obedience` | 3 | — |
| `core.evidence.recursive_ontology_limit_engine` | `recursive_ontology_limits` | 2 | — |
| `core.evidence.recursive_openness_stability_engine` | `model_recursive_openness_stability` | 7 | — |
| `core.evidence.recursive_phase_space_engine` | `model_recursive_phase_space` | 4 | round(×1 |
| `core.evidence.recursive_provenance_engine` | `preserve_recursive_provenance` | 2 | — |
| `core.evidence.recursive_reality_integrity_engine` | `_lineage_depth` | 6 | — |
| `core.evidence.recursive_reality_limit_engine` | `recursive_reality_limits` | 7 | — |
| `core.evidence.recursive_self_confirmation_engine` | `detect_recursive_self_confirmation` | 3 | round(×1 |
| `core.evidence.recursive_semantic_closure_engine` | `_closure_record` | 10 | — |
| `core.evidence.recursive_semantic_decentralization_engine` | `model_recursive_semantic_decentralization` | 3 | — |
| `core.evidence.recursive_semantic_distribution_engine` | `distribute_recursive_semantics` | 2 | set(×2 |
| `core.evidence.recursive_semantic_independence_engine` | `model_recursive_semantic_independence` | 2 | set(×1 |
| `core.evidence.recursive_sovereignty_stability_engine` | `model_sovereignty_stability` | 7 | — |
| `core.evidence.recursive_stabilization_engine` | `detect_recursive_stabilization` | 3 | — |
| `core.evidence.recursive_stabilization_termination_engine` | `terminate_recursive_stabilization` | 3 | sorted(×1, set(×1 |
| `core.evidence.recursive_submission_engine` | `detect_recursive_submission` | 3 | — |
| `core.evidence.recursive_topology_limit_engine` | `recursive_topology_limits` | 2 | — |
| `core.evidence.recursive_trust_monopoly_engine` | `detect_recursive_trust_monopoly` | 3 | — |
| `core.evidence.recursive_truth_boundary_engine` | `model_recursive_truth_boundaries` | 10 | round(×1 |
| `core.evidence.recursive_truth_refusal_engine` | `refuse_recursive_stabilization` | 8 | sorted(×1, set(×1 |
| `core.evidence.recursive_uncertainty_preservation_engine` | `preserve_recursive_uncertainty` | 7 | sorted(×1, set(×1 |
| `core.evidence.semantic_alternative_engine` | `model_semantic_alternatives` | 3 | sorted(×1, set(×2 |
| `core.evidence.semantic_antigravity_engine` | `apply_semantic_antigravity` | 2 | — |
| `core.evidence.semantic_attractor_engine` | `_record` | 10 | — |
| `core.evidence.semantic_autonomy_engine` | `model_semantic_autonomy` | 6 | — |
| `core.evidence.semantic_boundary_engine` | `model_semantic_boundaries` | 8 | sorted(×3 |
| `core.evidence.semantic_confidence_engine` | `score_semantic_confidence` | 37 | round(×1, sorted(×3, set(×1 |
| `core.evidence.semantic_conservatism_engine` | `apply_semantic_conservatism` | 29 | round(×2, sorted(×2, set(×2 |
| `core.evidence.semantic_consistency_engine` | `assess_semantic_consistency` | 19 | round(×1, set(×3 |
| `core.evidence.semantic_decay_engine` | `model_semantic_decay` | 12 | round(×1 |
| `core.evidence.semantic_decentralization_engine` | `model_semantic_decentralization` | 8 | — |
| `core.evidence.semantic_dependency_suppression_engine` | `suppress_semantic_dependency` | 2 | — |
| `core.evidence.semantic_divergence_engine` | `model_semantic_divergence` | 4 | round(×1, set(×2 |
| `core.evidence.semantic_diversity_engine` | `model_semantic_diversity` | 3 | round(×1 |
| `core.evidence.semantic_drift_engine` | `detect_semantic_drift` | 21 | round(×1, sorted(×1, set(×1 |
| `core.evidence.semantic_entropy_engine` | `model_semantic_entropy` | 14 | round(×1 |
| `core.evidence.semantic_fixation_engine` | `detect_semantic_fixation` | 3 | — |
| `core.evidence.semantic_fragility_engine` | `model_fragility` | 35 | round(×1, sorted(×1, set(×1 |
| `core.evidence.semantic_freedom_engine` | `model_semantic_freedom` | 6 | — |
| `core.evidence.semantic_governance_engine` | `suppress_semantic_governance` | 2 | — |
| `core.evidence.semantic_hierarchy_engine` | `detect_semantic_hierarchy_permanence` | 3 | — |
| `core.evidence.semantic_homogenization_engine` | `detect_semantic_homogenization` | 3 | — |
| `core.evidence.semantic_honesty_engine` | `assess_semantic_honesty` | 15 | — |
| `core.evidence.semantic_incompleteness_engine` | `model_incompleteness` | 12 | sorted(×2, set(×2 |
| `core.evidence.semantic_inference_calculus` | `infer_from_evidence` | 16 | sorted(×1, set(×1 |
| `core.evidence.semantic_instability_engine` | `model_semantic_instability` | 14 | round(×1, sorted(×1, set(×1 |
| `core.evidence.semantic_justification_engine` | `build_justification` | 24 | sorted(×2, set(×2 |
| `core.evidence.semantic_limit_engine` | `semantic_limits` | 12 | — |
| `core.evidence.semantic_momentum_engine` | `measure_semantic_momentum` | 9 | round(×1 |
| `core.evidence.semantic_monoculture_engine` | `_suppression_record` | 10 | — |
| `core.evidence.semantic_monopoly_engine` | `_record` | 10 | — |
| `core.evidence.semantic_nondomestication_engine` | `resist_semantic_domestication` | 2 | — |
| `core.evidence.semantic_orthodoxy_engine` | `detect_semantic_orthodoxy` | 3 | — |
| `core.evidence.semantic_overreach_engine` | `detect_semantic_overreach` | 17 | sorted(×1, set(×1 |
| `core.evidence.semantic_plurality_engine` | `model_semantic_plurality` | 14 | set(×2 |
| `core.evidence.semantic_proof_engine` | `prove_semantic_claim` | 14 | sorted(×1, set(×1 |
| `core.evidence.semantic_refusal_engine` | `refuse_unsupported_conclusions` | 15 | sorted(×1, set(×1 |
| `core.evidence.semantic_self_determination_engine` | `model_semantic_self_determination` | 7 | — |
| `core.evidence.semantic_self_limitation_engine` | `apply_semantic_self_limitation` | 20 | sorted(×1, set(×1 |
| `core.evidence.semantic_self_reinforcement_engine` | `detect_semantic_self_reinforcement` | 7 | — |
| `core.evidence.semantic_stability_engine` | `model_semantic_stability` | 23 | round(×1, sorted(×1, set(×1 |
| `core.evidence.semantic_stability_limit_engine` | `semantic_stability_limits` | 5 | — |
| `core.evidence.semantic_support_engine` | `build_support` | 7 | round(×1, sorted(×1, set(×1 |
| `core.evidence.semantic_termination_engine` | `terminate_semantic_chain` | 3 | sorted(×1, set(×1 |
| `core.evidence.semantic_truth_limit_engine` | `semantic_truth_limits` | 6 | — |
| `core.evidence.semantic_uniformity_engine` | `detect_semantic_uniformity` | 3 | set(×1 |
| `core.evidence.semantic_weakness_engine` | `build_weaknesses` | 11 | sorted(×1, set(×1 |
| `core.evidence.speculative_coherence_engine` | `detect_speculative_coherence` | 11 | round(×1 |
| `core.evidence.speculative_inference_engine` | `_suppression_record` | 17 | — |
| `core.evidence.stability_boundary_engine` | `model_stability_boundary` | 6 | — |
| `core.evidence.stabilization_termination_engine` | `terminate_stabilization` | 3 | sorted(×1, set(×1 |
| `core.evidence.topology_boundary_engine` | `model_topology_boundaries` | 7 | — |
| `core.evidence.topology_limit_engine` | `topology_limits` | 2 | — |
| `core.evidence.traceability_engine` | `build_traceability` | 14 | sorted(×2, set(×2 |
| `core.evidence.truth_boundary_engine` | `model_truth_boundaries` | 8 | — |
| `core.evidence.truth_refusal_engine` | `refuse_unsupported_stabilization` | 8 | sorted(×1, set(×1 |
| `core.evidence.uncertainty_engine` | `model_uncertainty` | 21 | round(×3 |
| `core.evidence.uncertainty_visibility_engine` | `expose_uncertainty_visibility` | 15 | round(×2, sorted(×1, set(×1 |
| `core.evidence.unsupported_confidence_engine` | `block_unsupported_confidence_escalation` | 16 | round(×1 |
| `core.evidence.unsupported_continuity_engine` | `_continuation_record` | 9 | — |
| `core.evidence.unsupported_expansion_engine` | `detect_unsupported_expansion` | 13 | — |
| `core.evidence.unsupported_inference_engine` | `suppress_unsupported_inference` | 19 | sorted(×2, set(×1 |
| `core.evidence.unsupported_scope_engine` | `model_unsupported_scope` | 7 | sorted(×1, set(×1 |
| `core.evidence.unsupported_stabilization_engine` | `_stabilization_record` | 9 | — |
| `core.evidence.worldview_antigravity_engine` | `apply_worldview_antigravity` | 2 | — |
| `core.evidence.worldview_convergence_engine` | `suppress_worldview_convergence` | 2 | — |
| `core.evidence.worldview_diversity_engine` | `model_worldview_diversity` | 8 | — |
| `core.evidence.worldview_variance_engine` | `model_worldview_variance` | 3 | round(×1 |
| `core.graph.graph_entropy_engine` | `model_graph_entropy` | 6 | round(×1 |
| `core.graph.semantic_cycle_analysis_engine` | `detect_cycles` | 37 | set(×2 |
| `core.graph.topology_proof_engine` | `prove_topology` | 21 | sorted(×1 |
| `core.ir._base` | `empty_confidence` | 2 | — |
| `core.ir._base` | `empty_lineage` | 2 | — |
| `core.ir._base` | `merge_evidence` | 3 | sorted(×1 |
| `core.parsers.parser_registry` | `parse_source` | 7 | — |
| `core.repository.api_surface_reasoning_engine` | `reason_api_surface` | 15 | — |
| `core.repository.execution_flow_engine` | `reconstruct_execution_flow` | 11 | — |
| `core.repository.infra_semantic_engine` | `detect_infra_signals` | 13 | — |
| `core.repository.runtime_dependency_engine` | `resolve_runtime_dependencies` | 26 | sorted(×2, set(×2 |
| `core.repository.service_interaction_engine` | `infer_service_interactions` | 14 | sorted(×1 |
| `core.semantic.ambiguity_pressure_engine` | `compute_ambiguity_pressure` | 8 | round(×2 |
| `core.semantic.contradiction_pressure_engine` | `compute_contradiction_pressure` | 15 | round(×2 |
| `core.semantic.evidence_boundary_pressure_engine` | `compute_evidence_boundary_pressure` | 4 | round(×1 |
| `core.semantic.evidence_decay_pressure_engine` | `compute_evidence_decay_pressure` | 3 | round(×1 |
| `core.semantic.recursive_boundary_pressure_engine` | `compute_recursive_boundary_pressure` | 2 | round(×1 |
| `core.semantic.recursive_convergence_pressure_engine` | `compute_recursive_convergence_pressure` | 3 | round(×1 |
| `core.semantic.recursive_dependency_pressure_engine` | `compute_recursive_dependency_pressure` | 3 | round(×1 |
| `core.semantic.semantic_boundary_pressure_engine` | `compute_semantic_boundary_pressure` | 3 | round(×1 |
| `core.semantic.truth_boundary_pressure_engine` | `compute_truth_boundary_pressure` | 3 | round(×1 |
| `core.semantic.uncertainty_pressure_engine` | `compute_uncertainty_pressure` | 9 | round(×2 |

## Determinism-sensitive operations (whole closure)

Every site below must match Python bit-for-bit:

| Operation | Total occurrences |
|-----------|------------------:|
| `sorted(` | 101 |
| `set(` | 90 |
| `round(` | 79 |

## Full DAG (function → in-closure dependencies)

<details><summary>expand</summary>

```
build_control_flow_graph  <-  []
reconstruct_execution_paths  <-  []
_node  <-  []
parse_python_ast  <-  [_node]
compile_semantic_ast_ir  <-  [build_control_flow_graph, reconstruct_execution_paths, parse_python_ast, resolve_symbols]
resolve_symbols  <-  []
build_argument_dependencies  <-  [reconstruct_argument_dependencies]
reconstruct_argument_dependencies  <-  []
build_argument_graph  <-  [extract_rhetorical_structure]
model_concept_progression  <-  [model_semantic_transitions]
model_concept_transitions  <-  [parse_semantic_discourse]
build_coreference_graph  <-  [resolve_coreferences, parse_rhetorical_structure]
resolve_coreferences  <-  []
build_document_dependency_graph  <-  [model_concept_transitions, extract_instructional_flow]
build_document_semantic_ir  <-  [build_argument_dependencies, model_concept_progression, build_coreference_graph, build_document_dependency_graph, parse_rhetorical_structure, infer_tutorial_prerequisites]
extract_headings  <-  []
extract_instructional_flow  <-  [extract_rhetorical_structure]
analyze_instructional_semantics  <-  [extract_instructional_flow, assign_semantic_roles]
analyze_long_range_discourse  <-  [build_document_semantic_ir]
parse_rhetorical_structure  <-  [extract_rhetorical_structure, assign_semantic_roles]
extract_rhetorical_structure  <-  []
extract_sections  <-  [extract_headings]
parse_semantic_discourse  <-  [build_argument_graph, extract_rhetorical_structure]
assign_semantic_roles  <-  []
model_semantic_transitions  <-  [model_concept_transitions, parse_rhetorical_structure]
reconstruct_tutorial_dependencies  <-  [extract_tutorial_flow, structure_cognition]
infer_tutorial_prerequisites  <-  [analyze_instructional_semantics, reconstruct_tutorial_dependencies]
extract_tutorial_flow  <-  [extract_sections, structure_cognition]
expose_ambiguity_visibility  <-  []
detect_authority_concentration  <-  []
diffuse_authority  <-  []
resist_autonomy_erosion  <-  []
model_causal_plurality  <-  []
_depth  <-  []
apply_civilizational_epistemic_openness  <-  [_depth, detect_cognitive_gravity_well, apply_explanatory_antigravity, model_explanatory_divergence, detect_explanatory_fixation, model_interpretive_divergence, apply_ontology_antigravity, model_ontology_divergence, detect_ontology_fixation, preserve_recursive_divergence, preserve_recursive_entropy, resist_exploration_decay, resist_novelty_decay, model_recursive_novelty, preserve_recursive_novelty, model_recursive_openness_stability, model_recursive_phase_space, detect_recursive_stabilization, apply_semantic_antigravity, detect_semantic_attractor, model_semantic_divergence, detect_semantic_fixation, apply_worldview_antigravity, model_worldview_variance, compute_recursive_convergence_pressure]
_depth  <-  []
apply_cognitive_anti_capture  <-  [detect_authority_concentration, resist_autonomy_erosion, _depth, model_cognitive_decentralization, model_explanatory_competition, preserve_explanatory_freedom, model_interpretive_autonomy, preserve_interpretive_freedom, model_ontology_competition, preserve_ontology_freedom, detect_ontology_monopoly, diffuse_recursive_authority, model_capture_resistance, detect_recursive_centralization, distribute_recursive_cognition, detect_recursive_narrative_monopoly, model_recursive_semantic_decentralization, distribute_recursive_semantics, detect_recursive_trust_monopoly, model_semantic_autonomy, model_semantic_freedom, suppress_semantic_governance, detect_semantic_hierarchy_permanence, detect_semantic_monopoly]
model_cognitive_decentralization  <-  []
detect_cognitive_gravity_well  <-  []
apply_cognitive_humility  <-  [expose_ambiguity_visibility, apply_confidence_degradation, terminate_inference_chain, model_noninferable_regions, model_fragility, semantic_limits, refuse_unsupported_conclusions, apply_semantic_self_limitation, detect_semantic_speculation, expose_uncertainty_visibility, block_unsupported_confidence_escalation, compute_ambiguity_pressure, compute_uncertainty_pressure]
apply_cognitive_integrity  <-  [model_epistemic_limits, model_inference_integrity, model_inference_limits, model_fragility, assess_semantic_honesty, detect_semantic_overreach, suppress_unsupported_inference, model_unsupported_scope]
model_cognitive_sovereignty  <-  []
apply_confidence_caps  <-  []
apply_confidence_collapse  <-  [apply_reality_bounded_confidence]
apply_confidence_degradation  <-  [apply_confidence_caps]
detect_confidence_echo  <-  []
refuse_unsupported_continuity  <-  []
build_contradiction_lattice  <-  []
reason_deterministically  <-  [combine_evidence, infer_from_evidence]
preserve_epistemic_boundaries  <-  []
_depth  <-  []
apply_epistemic_civilization_stability  <-  [diffuse_authority, model_causal_plurality, _depth, model_epistemic_openness, model_explanatory_diversity, detect_interpretive_closure, resist_interpretive_decay, distribute_interpretations, model_interpretive_diversity, detect_ontology_hardening, model_ontology_instability, resist_plurality_decay, detect_recursive_consensus, model_semantic_alternatives, model_semantic_decentralization, model_semantic_diversity, detect_semantic_homogenization, detect_semantic_monoculture, detect_semantic_orthodoxy, model_semantic_plurality, detect_semantic_uniformity, suppress_worldview_convergence, model_worldview_diversity]
score_epistemic_confidence  <-  [assess_evidence_sufficiency, build_support, build_weaknesses]
attach_epistemic_state  <-  [apply_civilizational_epistemic_openness, apply_cognitive_anti_capture, apply_cognitive_humility, apply_cognitive_integrity, apply_epistemic_civilization_stability, score_epistemic_confidence, assess_evidence_sufficiency, preserve_incompleteness, mark_insufficiency, apply_reality_alignment, apply_recursive_epistemic_sovereignty, apply_recursive_reality_integrity, score_reliability, apply_epistemic_restraint, build_support, propagate_uncertainty, build_weaknesses, apply_truth_preservation, apply_contradiction_restraint]
model_epistemic_limits  <-  []
model_epistemic_openness  <-  []
combine_evidence  <-  []
model_evidence_boundaries  <-  []
model_evidence_decay  <-  []
assess_evidence_sufficiency  <-  []
weight_evidence_calculus  <-  []
build_explainability  <-  []
apply_explanatory_antigravity  <-  []
model_explanatory_competition  <-  []
model_explanatory_divergence  <-  []
model_explanatory_diversity  <-  []
detect_explanatory_fixation  <-  []
preserve_explanatory_freedom  <-  []
resist_explanatory_domestication  <-  []
model_explanatory_self_determination  <-  []
apply_formal_semantic_foundation  <-  [build_contradiction_lattice, reason_deterministically, weight_evidence_calculus, validate_inference, assess_semantic_consistency, model_semantic_entropy, build_justification, prove_semantic_claim, propagate_uncertainty_math]
structure_cognition  <-  [apply_semantic_conservatism, build_semantic_integrity_object]
preserve_incompleteness  <-  [model_incompleteness]
model_inference_integrity  <-  []
model_inference_limits  <-  [model_semantic_boundaries]
refuse_inference  <-  []
terminate_inference_chain  <-  []
validate_inference  <-  [infer_from_evidence]
preserve_instability  <-  []
mark_insufficiency  <-  []
model_interpretive_autonomy  <-  []
detect_interpretive_closure  <-  []
resist_interpretive_decay  <-  []
distribute_interpretations  <-  []
model_interpretive_divergence  <-  []
model_interpretive_diversity  <-  []
preserve_interpretive_freedom  <-  []
resist_interpretive_domestication  <-  []
model_interpretive_self_determination  <-  []
build_lineage  <-  []
detect_narrative_hallucination  <-  []
model_noninferable_regions  <-  []
model_noninference  <-  []
apply_ontology_antigravity  <-  []
model_ontology_boundaries  <-  []
model_ontology_competition  <-  []
model_ontology_divergence  <-  []
detect_ontology_fixation  <-  []
preserve_ontology_freedom  <-  []
detect_ontology_hardening  <-  []
model_ontology_instability  <-  []
ontology_limits  <-  []
detect_ontology_monopoly  <-  []
resist_ontology_domestication  <-  []
model_ontology_self_determination  <-  []
resist_plurality_decay  <-  []
build_provenance  <-  []
apply_reality_alignment  <-  [refuse_unsupported_continuity, preserve_epistemic_boundaries, model_evidence_boundaries, detect_narrative_hallucination, model_ontology_boundaries, ontology_limits, apply_reality_bounded_confidence, apply_reality_constraints, model_semantic_boundaries, detect_semantic_drift, measure_semantic_momentum, model_semantic_stability, semantic_stability_limits, terminate_semantic_chain, detect_speculative_coherence, model_stability_boundary, model_topology_boundaries, topology_limits, collect_unsupported_continuity, compute_evidence_boundary_pressure, compute_semantic_boundary_pressure]
apply_reality_bounded_confidence  <-  [apply_confidence_degradation]
apply_reality_constraints  <-  [model_evidence_boundaries, model_ontology_boundaries, model_topology_boundaries]
resist_agency_decay  <-  []
model_recursive_agency  <-  []
preserve_recursive_agency  <-  []
diffuse_recursive_authority  <-  []
preserve_recursive_autonomy  <-  []
model_capture_resistance  <-  []
detect_recursive_centralization  <-  []
distribute_recursive_cognition  <-  []
detect_recursive_coherence_inflation  <-  []
apply_recursive_confidence_decay  <-  [apply_confidence_collapse]
detect_recursive_confidence_echo  <-  []
detect_recursive_consensus  <-  []
_record  <-  []
detect_recursive_dependency  <-  [_record]
preserve_recursive_divergence  <-  []
detect_recursive_domestication  <-  []
detect_recursive_drift  <-  []
model_recursive_entropy  <-  []
preserve_recursive_entropy  <-  []
_depth  <-  []
apply_recursive_epistemic_sovereignty  <-  [model_cognitive_sovereignty, resist_explanatory_domestication, model_explanatory_self_determination, resist_interpretive_domestication, model_interpretive_self_determination, resist_ontology_domestication, model_ontology_self_determination, resist_agency_decay, model_recursive_agency, preserve_recursive_agency, preserve_recursive_autonomy, detect_recursive_dependency, detect_recursive_domestication, _depth, detect_recursive_guardianship, resist_independence_decay, model_recursive_interpretive_independence, detect_recursive_obedience, model_recursive_semantic_independence, model_sovereignty_stability, detect_recursive_submission, suppress_semantic_dependency, resist_semantic_domestication, model_semantic_self_determination, compute_recursive_dependency_pressure]
track_recursive_evidence_ancestry  <-  []
resist_exploration_decay  <-  []
detect_recursive_guardianship  <-  []
resist_independence_decay  <-  []
model_recursive_instability  <-  []
model_recursive_interpretive_independence  <-  []
preserve_recursive_lineage  <-  []
detect_recursive_narrative_monopoly  <-  []
resist_novelty_decay  <-  []
model_recursive_novelty  <-  []
preserve_recursive_novelty  <-  []
detect_recursive_obedience  <-  []
recursive_ontology_limits  <-  []
model_recursive_openness_stability  <-  []
model_recursive_phase_space  <-  []
preserve_recursive_provenance  <-  []
_lineage_depth  <-  []
apply_recursive_reality_integrity  <-  [detect_recursive_coherence_inflation, apply_recursive_confidence_decay, detect_recursive_confidence_echo, detect_recursive_drift, model_recursive_entropy, track_recursive_evidence_ancestry, model_recursive_instability, preserve_recursive_lineage, recursive_ontology_limits, preserve_recursive_provenance, _lineage_depth, recursive_reality_limits, detect_recursive_self_confirmation, detect_recursive_semantic_closure, terminate_recursive_stabilization, recursive_topology_limits, model_recursive_truth_boundaries, refuse_recursive_stabilization, preserve_recursive_uncertainty, compute_recursive_boundary_pressure]
recursive_reality_limits  <-  []
detect_recursive_self_confirmation  <-  []
_closure_record  <-  []
detect_recursive_semantic_closure  <-  [_closure_record]
model_recursive_semantic_decentralization  <-  []
distribute_recursive_semantics  <-  []
model_recursive_semantic_independence  <-  []
model_sovereignty_stability  <-  []
detect_recursive_stabilization  <-  []
terminate_recursive_stabilization  <-  []
detect_recursive_submission  <-  []
recursive_topology_limits  <-  []
detect_recursive_trust_monopoly  <-  []
model_recursive_truth_boundaries  <-  []
refuse_recursive_stabilization  <-  []
preserve_recursive_uncertainty  <-  []
model_semantic_alternatives  <-  []
apply_semantic_antigravity  <-  []
_record  <-  []
detect_semantic_attractor  <-  [_record]
model_semantic_autonomy  <-  []
model_semantic_boundaries  <-  []
score_semantic_confidence  <-  []
apply_semantic_conservatism  <-  []
assess_semantic_consistency  <-  []
model_semantic_decay  <-  []
model_semantic_decentralization  <-  []
suppress_semantic_dependency  <-  []
model_semantic_divergence  <-  []
model_semantic_diversity  <-  []
detect_semantic_drift  <-  []
model_semantic_entropy  <-  []
detect_semantic_fixation  <-  []
model_fragility  <-  []
model_semantic_freedom  <-  []
suppress_semantic_governance  <-  []
detect_semantic_hierarchy_permanence  <-  []
detect_semantic_homogenization  <-  []
assess_semantic_honesty  <-  []
model_incompleteness  <-  []
infer_from_evidence  <-  []
model_semantic_instability  <-  []
_ground_parser  <-  [build_provenance]
build_semantic_integrity_object  <-  [attach_epistemic_state, build_explainability, apply_formal_semantic_foundation, build_lineage, build_provenance, score_semantic_confidence, _ground_parser, build_traceability]
build_justification  <-  []
semantic_limits  <-  []
measure_semantic_momentum  <-  []
_suppression_record  <-  []
detect_semantic_monoculture  <-  [_suppression_record]
_record  <-  []
detect_semantic_monopoly  <-  [_record]
resist_semantic_domestication  <-  []
detect_semantic_orthodoxy  <-  []
detect_semantic_overreach  <-  []
model_semantic_plurality  <-  []
prove_semantic_claim  <-  []
refuse_unsupported_conclusions  <-  []
score_reliability  <-  [assess_evidence_sufficiency, build_support]
apply_epistemic_restraint  <-  [apply_confidence_caps, refuse_inference, model_noninference, model_semantic_boundaries, detect_unsupported_expansion, model_unsupported_scope, compute_contradiction_pressure]
model_semantic_self_determination  <-  []
apply_semantic_self_limitation  <-  []
detect_semantic_self_reinforcement  <-  []
detect_semantic_speculation  <-  [collect_suppressed_speculation]
model_semantic_stability  <-  []
semantic_stability_limits  <-  []
build_support  <-  []
terminate_semantic_chain  <-  []
semantic_truth_limits  <-  []
propagate_uncertainty  <-  [model_uncertainty]
detect_semantic_uniformity  <-  []
build_weaknesses  <-  []
detect_speculative_coherence  <-  []
_suppression_record  <-  []
collect_suppressed_speculation  <-  [suppress_speculative_inference]
suppress_speculative_inference  <-  [_suppression_record]
model_stability_boundary  <-  []
terminate_stabilization  <-  []
model_topology_boundaries  <-  []
topology_limits  <-  []
build_traceability  <-  []
model_truth_boundaries  <-  []
apply_truth_preservation  <-  [apply_confidence_collapse, detect_confidence_echo, model_evidence_decay, preserve_instability, model_semantic_decay, model_semantic_entropy, model_semantic_instability, detect_semantic_self_reinforcement, semantic_truth_limits, terminate_stabilization, model_truth_boundaries, refuse_unsupported_stabilization, detect_unsupported_stabilization, compute_evidence_decay_pressure, compute_truth_boundary_pressure]
refuse_unsupported_stabilization  <-  []
model_uncertainty  <-  []
propagate_uncertainty_math  <-  [model_uncertainty]
expose_uncertainty_visibility  <-  []
block_unsupported_confidence_escalation  <-  []
_continuation_record  <-  []
collect_unsupported_continuity  <-  [suppress_unsupported_continuity]
suppress_unsupported_continuity  <-  [_continuation_record]
detect_unsupported_expansion  <-  []
suppress_unsupported_inference  <-  []
model_unsupported_scope  <-  []
_stabilization_record  <-  []
detect_unsupported_stabilization  <-  [_stabilization_record]
apply_worldview_antigravity  <-  []
suppress_worldview_convergence  <-  []
model_worldview_diversity  <-  []
model_worldview_variance  <-  []
model_graph_entropy  <-  []
detect_cycles  <-  []
prove_topology  <-  []
reason_topology  <-  [model_graph_entropy, prove_topology]
empty_confidence  <-  []
empty_lineage  <-  []
merge_evidence  <-  []
compile_document_ir  <-  [build_document_semantic_ir, empty_lineage, merge_evidence, empty_document_ir]
empty_document_ir  <-  [empty_confidence, empty_lineage]
compile_repository_ir  <-  [compile_semantic_ast_ir, empty_lineage, merge_evidence, empty_repository_ir, build_repository_execution_ir]
empty_repository_ir  <-  [empty_confidence, empty_lineage]
parse_source  <-  []
query_documents  <-  [compile_document_ir]
query_repository  <-  [compile_repository_ir]
reason_discourse_semantic  <-  [analyze_long_range_discourse, compile_document_ir]
reason_runtime_semantic  <-  [compile_repository_ir, model_runtime_state]
reason_topology_semantic  <-  [detect_cycles, reason_topology]
reason_api_contract  <-  [reason_api_surface]
reason_api_surface  <-  []
analyze_deployment_semantics  <-  [model_infra_relationships]
model_execution_dependencies  <-  [parse_source, reconstruct_execution_flow]
reconstruct_execution_flow  <-  []
model_infra_relationships  <-  [detect_infra_signals]
detect_infra_signals  <-  []
build_repository_execution_ir  <-  [reason_api_contract, analyze_deployment_semantics, build_repository_semantic_ir, reason_runtime_flow, build_service_runtime_graph]
build_repository_semantic_ir  <-  [reconstruct_execution_flow, resolve_runtime_dependencies, infer_service_interactions]
resolve_runtime_dependencies  <-  []
analyze_runtime_execution  <-  [parse_source, reconstruct_execution_flow, analyze_runtime_semantics]
reason_runtime_flow  <-  [model_execution_dependencies, analyze_runtime_semantics]
analyze_runtime_semantics  <-  [parse_source, resolve_runtime_dependencies]
model_runtime_state  <-  [analyze_runtime_execution]
infer_service_interactions  <-  []
build_service_runtime_graph  <-  [parse_source, infer_service_interactions]
compute_ambiguity_pressure  <-  []
compute_contradiction_pressure  <-  []
apply_contradiction_restraint  <-  [compute_contradiction_pressure]
compute_evidence_boundary_pressure  <-  []
compute_evidence_decay_pressure  <-  []
compute_recursive_boundary_pressure  <-  []
compute_recursive_convergence_pressure  <-  []
compute_recursive_dependency_pressure  <-  []
compute_semantic_boundary_pressure  <-  []
compute_truth_boundary_pressure  <-  []
compute_uncertainty_pressure  <-  []
```
</details>

## Execution protocol per phase

1. Port the phase's functions to `lib/src/semantic_ir/` (canonical, no approximation).
2. Add executable fixtures calling exactly those functions.
3. Execute Python (canonical), JavaScript (engine), Dart.
4. Verify `hash(Python) == hash(JS) == hash(Dart)` and deep equality.
5. Commit vectors + parity tests. Only then advance to the next phase.
6. The 6 public APIs (`compile_document`, `query_documents`, `compile_repository`, `query_repository`, `query_semantics`, `reason_semantically`) promote to Complete only when the final phase closes the whole closure with executable proof.
