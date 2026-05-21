from __future__ import annotations

from typing import Any, Callable, Dict


def eval_ontology_consistency(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.knowledge.ontology_consistency_engine import check_ontology_consistency

    edges = case["input"].get("edges", [])
    r = check_ontology_consistency(edges)
    exp = case["expected"]
    pred = r["consistent"] == exp["consistent"]
    return {"predicted": pred, "actual": r, "expected": exp}


def eval_contradiction_count(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.evidence.contradiction_lattice_engine import build_contradiction_lattice

    r = build_contradiction_lattice(case["input"].get("pairs", []))
    pred = r["count"] == case["expected"]["count"]
    return {"predicted": pred, "actual": {"count": r["count"]}, "expected": case["expected"]}


def eval_import_graph(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.parsers.parser_registry import parse_source

    inp = case["input"]
    parsed = parse_source(inp["source"], path=inp.get("path", "t.py"))
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    n = len(sym.get("imports", []) or [])
    pred = n >= case["expected"]["min_imports"]
    return {"predicted": pred, "actual": {"imports": n}, "expected": case["expected"]}


def eval_rhetorical_units(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.documents.rhetorical_structure_engine import extract_rhetorical_structure

    r = extract_rhetorical_structure(case["input"]["text"])
    n = len(r.get("units", []))
    pred = n >= case["expected"]["min_units"]
    return {"predicted": pred, "actual": {"units": n}, "expected": case["expected"]}


def eval_trust_calibrated(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.internet.probabilistic_trust_engine import compute_probabilistic_trust

    inp = case["input"]
    r = compute_probabilistic_trust(inp["url"], corroboration_count=inp.get("corroboration", 0))
    exp = case["expected"]
    score = r.get("trust_score", 0)
    ok = r.get("calibrated") == exp["calibrated"]
    if "min_score" in exp:
        ok = ok and score >= exp["min_score"]
    if "max_score" in exp:
        ok = ok and score <= exp["max_score"]
    return {"predicted": ok, "actual": {"score": score, "calibrated": r.get("calibrated")}, "expected": exp}


def eval_topology_proof(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.graph.topology_proof_engine import prove_topology

    r = prove_topology(case["input"])
    exp = case["expected"]
    pred = r["proved"] == exp["proved"]
    if "max_degree" in exp:
        pred = pred and r["max_degree"] == exp["max_degree"]
    return {"predicted": pred, "actual": r, "expected": exp}


def eval_semantic_consistency(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.evidence.semantic_consistency_engine import assess_semantic_consistency

    inp = case["input"]
    r = assess_semantic_consistency(inp["observed"], inp["inferred"], inp["reconciled"])
    pred = r["consistent"] == case["expected"]["consistent"]
    return {"predicted": pred, "actual": r, "expected": case["expected"]}


def eval_merge_rigor(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.knowledge.semantic_merge_rigor_engine import merge_with_evidence

    r = merge_with_evidence(case["input"]["sources"])
    pred = r["merged"] == case["expected"]["merged"]
    return {"predicted": pred, "actual": r, "expected": case["expected"]}


def eval_instructional_flow(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.documents.instructional_flow_engine import extract_instructional_flow

    r = extract_instructional_flow(case["input"]["text"])
    n = len(r.get("steps", []))
    pred = n >= case["expected"]["min_steps"]
    return {"predicted": pred, "actual": {"steps": n}, "expected": case["expected"]}


def eval_api_paths(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.repository.api_surface_reasoning_engine import reason_api_surface

    r = reason_api_surface(case["input"]["spec"])
    n = len(r.get("paths", []))
    pred = n >= case["expected"]["min_paths"]
    return {"predicted": pred, "actual": {"paths": n}, "expected": case["expected"]}


def eval_service_boundaries(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.repository.infra_semantic_engine import detect_infra_signals

    r = detect_infra_signals(case["input"]["files"])
    n = len(r.get("signals", []))
    pred = n >= case["expected"]["min_signals"]
    return {"predicted": pred, "actual": {"signals": n}, "expected": case["expected"]}


def eval_citation_verify(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.internet.citation_verification_engine import verify_citations

    r = verify_citations(case["input"]["text"])
    pred = r["verified"] == case["expected"]["verified"]
    return {"predicted": pred, "actual": r, "expected": case["expected"]}


def eval_semantic_dependency(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.evidence.semantic_dependency_calculus import derive_dependency

    inp = case["input"]
    r = derive_dependency(inp["from_keys"], inp["to_keys"], inp.get("evidence", []))
    pred = r["derivable"] == case["expected"]["derivable"]
    return {"predicted": pred, "actual": r, "expected": case["expected"]}


def eval_cycle_detection(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.graph.semantic_cycle_analysis_engine import detect_cycles

    r = detect_cycles(case["input"])
    has = r["cycle_count"] > 0
    pred = has == case["expected"]["has_cycle"]
    return {"predicted": pred, "actual": {"has_cycle": has, "count": r["cycle_count"]}, "expected": case["expected"]}


def eval_merge_validation(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.knowledge.semantic_merge_validator import validate_semantic_merge

    inp = case["input"]
    r = validate_semantic_merge(inp.get("sources", []), inp.get("edges", []))
    pred = r["allowed"] == case["expected"]["allowed"]
    return {"predicted": pred, "actual": {"allowed": r["allowed"]}, "expected": case["expected"]}


def eval_document_ir(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.documents.document_semantic_ir_engine import build_document_semantic_ir

    r = build_document_semantic_ir(case["input"]["text"])
    n = len(r.get("prerequisites", {}).get("chain", []))
    pred = n >= case["expected"].get("min_chain", 0)
    return {"predicted": pred, "actual": {"chain": n}, "expected": case["expected"]}


def eval_discourse_causality(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.documents.tutorial_causality_engine import reconstruct_tutorial_causality

    r = reconstruct_tutorial_causality(case.get("sections", []))
    pred = r["count"] == case["expected_edge_count"]
    return {"predicted": pred, "actual": {"count": r["count"]}, "expected": case["expected_edge_count"]}


def eval_runtime_state_machine(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.runtime.runtime_transition_engine import apply_runtime_transitions

    r = apply_runtime_transitions(case.get("states", []))
    pred = r["final_state"] == case["expected_final"]
    return {"predicted": pred, "actual": {"final_state": r["final_state"]}, "expected": case["expected_final"]}


def eval_runtime_events(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.repository.runtime_event_engine import infer_runtime_events

    r = infer_runtime_events(case.get("dependencies", []), case.get("parser_evidence", []))
    pred = set(r["events"]) == set(case.get("expected_events", []))
    return {"predicted": pred, "actual": {"events": r["events"]}, "expected": case.get("expected_events")}


def eval_topology_traversal(case: Dict[str, Any]) -> Dict[str, Any]:
    from core.query.semantic_traversal_engine import traverse_graph

    order = traverse_graph(case.get("adjacency", {}), case.get("start", ""))
    pred = order == case.get("expected_order", [])
    return {"predicted": pred, "actual": {"order": order}, "expected": case.get("expected_order")}


def eval_semantic_agents_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_agents import eval_semantic_agents

    return eval_semantic_agents(case)


def eval_service_mesh_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_service_mesh import eval_service_mesh

    return eval_service_mesh(case)


def eval_runtime_scheduler_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_runtime_scheduler import eval_runtime_scheduler

    return eval_runtime_scheduler(case)


def eval_repository_world_model_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_repository_world_model import eval_repository_world_model

    return eval_repository_world_model(case)


def eval_semantic_architecture_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_architecture import eval_semantic_architecture

    return eval_semantic_architecture(case)


def eval_semantic_impact_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_impact import eval_semantic_impact

    return eval_semantic_impact(case)


def eval_autonomy_goal_resolution_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_autonomy import eval_autonomy_goal

    return eval_autonomy_goal(case)


def eval_autonomy_orchestration_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_autonomy import eval_autonomy_orchestration

    return eval_autonomy_orchestration(case)


def eval_autonomy_decomposition_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_autonomy import eval_autonomy_decomposition

    return eval_autonomy_decomposition(case)


def eval_autonomy_resource_forecast_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_autonomy import eval_autonomy_resource_forecast

    return eval_autonomy_resource_forecast(case)


def eval_autonomy_runtime_health_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_autonomy import eval_autonomy_runtime_health

    return eval_autonomy_runtime_health(case)


def eval_evolution_runtime_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_runtime

    return eval_evolution_runtime(case)


def eval_evolution_refactor_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_refactor

    return eval_evolution_refactor(case)


def eval_evolution_dependencies_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_dependencies

    return eval_evolution_dependencies(case)


def eval_evolution_consistency_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_consistency

    return eval_evolution_consistency(case)


def eval_evolution_drift_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_drift

    return eval_evolution_drift(case)


def eval_evolution_simulation_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_evolution import eval_evolution_simulation

    return eval_evolution_simulation(case)


def eval_engineering_graph_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_graph

    return eval_engineering_graph(case)


def eval_engineering_failure_forecast_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_failure_forecast

    return eval_engineering_failure_forecast(case)


def eval_engineering_operational_consistency_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_operational_consistency

    return eval_engineering_operational_consistency(case)


def eval_engineering_dependency_pressure_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_dependency_pressure

    return eval_engineering_dependency_pressure(case)


def eval_engineering_diagnostics_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_diagnostics

    return eval_engineering_diagnostics(case)


def eval_engineering_incident_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_engineering import eval_engineering_incident

    return eval_engineering_incident(case)


def eval_execution_pressure_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_execution_pressure

    return eval_execution_pressure(case)


def eval_runtime_contention_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_runtime_contention

    return eval_runtime_contention(case)


def eval_state_convergence_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_state_convergence

    return eval_state_convergence(case)


def eval_runtime_entropy_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_runtime_entropy

    return eval_runtime_entropy(case)


def eval_execution_bottlenecks_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_execution_bottlenecks

    return eval_execution_bottlenecks(case)


def eval_runtime_conflicts_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_runtime_conflicts

    return eval_runtime_conflicts(case)


def eval_collapse_forecast_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_collapse_forecast

    return eval_collapse_forecast(case)


def eval_scheduler_intelligence_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_scheduler_intelligence

    return eval_scheduler_intelligence(case)


def eval_load_balancing_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_reality import eval_load_balancing

    return eval_load_balancing(case)


def eval_causality_graph_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_causality_graph

    return eval_causality_graph(case)


def eval_failure_lineage_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_failure_lineage

    return eval_failure_lineage(case)


def eval_causal_propagation_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_propagation

    return eval_propagation(case)


def eval_recovery_causality_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_recovery_causality

    return eval_recovery_causality(case)


def eval_causal_equilibrium_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_equilibrium

    return eval_equilibrium(case)


def eval_causal_instability_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_instability

    return eval_instability(case)


def eval_timing_semantics_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_timing_semantics

    return eval_timing_semantics(case)


def eval_causal_replay_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_causal_intelligence import eval_causal_replay

    return eval_causal_replay(case)


def eval_execution_physics_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_execution_physics

    return eval_execution_physics(case)


def eval_pressure_field_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_pressure_field

    return eval_pressure_field(case)


def eval_runtime_turbulence_physics_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_runtime_turbulence

    return eval_runtime_turbulence(case)


def eval_energy_propagation_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_energy_propagation

    return eval_energy_propagation(case)


def eval_momentum_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_momentum

    return eval_momentum(case)


def eval_recovery_stabilization_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_recovery_stabilization

    return eval_recovery_stabilization(case)


def eval_execution_waves_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_execution_waves

    return eval_execution_waves(case)


def eval_equilibrium_mechanics_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_execution_physics import eval_equilibrium_mechanics

    return eval_equilibrium_mechanics(case)


def eval_query_language_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_query_language import eval_query_language

    return eval_query_language(case)


def eval_distributed_dag_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_distributed_dag import eval_distributed_dag

    return eval_distributed_dag(case)


def eval_database_kernel_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_database_kernel import eval_database_kernel

    return eval_database_kernel(case)


def eval_compiler_pipeline_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_compiler_pipeline import eval_compiler_pipeline

    return eval_compiler_pipeline(case)


def eval_distributed_execution_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_distributed_execution import eval_distributed_execution

    return eval_distributed_execution(case)


def eval_query_execution_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_query_execution import eval_query_execution

    return eval_query_execution(case)


def eval_semantic_distributed_os_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_distributed_os import eval_semantic_distributed_os

    return eval_semantic_distributed_os(case)


def eval_distributed_semantic_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_distributed_semantic import eval_distributed_semantic

    return eval_distributed_semantic(case)


def eval_semantic_vm_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_vm import eval_semantic_vm

    return eval_semantic_vm(case)


def eval_semantic_scale_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_semantic_scale import eval_semantic_scale

    return eval_semantic_scale(case)


def eval_runtime_simulation_criterion(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_runtime_simulation import eval_runtime_simulation

    return eval_runtime_simulation(case)


def eval_distributed_topology(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_runtime_topology import eval_runtime_topology

    return eval_runtime_topology(case)


def eval_symbol_resolution(case: Dict[str, Any]) -> Dict[str, Any]:
    from benchmarks.eval_ast_execution import eval_ast_execution

    return eval_ast_execution(case)


def eval_ontology_resolution(case: Dict[str, Any]) -> Dict[str, Any]:
    entities = case.get("entities", [])
    pred = bool(entities) and entities[0].get("kind") == case.get("expected_kind")
    return {"predicted": pred, "actual": {"kind": entities[0].get("kind") if entities else None}, "expected": case.get("expected_kind")}


CRITERIA_MAP: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "ontology_consistency": eval_ontology_consistency,
    "contradiction_count": eval_contradiction_count,
    "import_graph": eval_import_graph,
    "rhetorical_units": eval_rhetorical_units,
    "trust_calibrated": eval_trust_calibrated,
    "topology_proof": eval_topology_proof,
    "semantic_consistency": eval_semantic_consistency,
    "merge_rigor": eval_merge_rigor,
    "instructional_flow": eval_instructional_flow,
    "api_paths": eval_api_paths,
    "service_boundaries": eval_service_boundaries,
    "citation_verify": eval_citation_verify,
    "semantic_dependency": eval_semantic_dependency,
    "cycle_detection": eval_cycle_detection,
    "merge_validation": eval_merge_validation,
    "document_ir": eval_document_ir,
    "discourse_causality": eval_discourse_causality,
    "runtime_state_machine": eval_runtime_state_machine,
    "runtime_events": eval_runtime_events,
    "topology_traversal": eval_topology_traversal,
    "topology_reconstruction": eval_topology_traversal,
    "ontology_resolution": eval_ontology_resolution,
    "symbol_resolution": eval_symbol_resolution,
    "distributed_topology": eval_distributed_topology,
    "runtime_simulation": eval_runtime_simulation_criterion,
    "semantic_scale": eval_semantic_scale_criterion,
    "semantic_vm": eval_semantic_vm_criterion,
    "distributed_semantic": eval_distributed_semantic_criterion,
    "semantic_distributed_os": eval_semantic_distributed_os_criterion,
    "compiler_pipeline": eval_compiler_pipeline_criterion,
    "distributed_execution": eval_distributed_execution_criterion,
    "query_execution": eval_query_execution_criterion,
    "query_language": eval_query_language_criterion,
    "distributed_dag": eval_distributed_dag_criterion,
    "database_kernel": eval_database_kernel_criterion,
    "semantic_agents": eval_semantic_agents_criterion,
    "service_mesh": eval_service_mesh_criterion,
    "runtime_scheduler": eval_runtime_scheduler_criterion,
    "repository_world_model": eval_repository_world_model_criterion,
    "semantic_architecture": eval_semantic_architecture_criterion,
    "semantic_impact": eval_semantic_impact_criterion,
    "autonomy_goal_resolution": eval_autonomy_goal_resolution_criterion,
    "autonomy_orchestration": eval_autonomy_orchestration_criterion,
    "autonomy_decomposition": eval_autonomy_decomposition_criterion,
    "autonomy_resource_forecast": eval_autonomy_resource_forecast_criterion,
    "autonomy_runtime_health": eval_autonomy_runtime_health_criterion,
    "evolution_runtime": eval_evolution_runtime_criterion,
    "evolution_refactor": eval_evolution_refactor_criterion,
    "evolution_dependencies": eval_evolution_dependencies_criterion,
    "evolution_consistency": eval_evolution_consistency_criterion,
    "evolution_drift": eval_evolution_drift_criterion,
    "evolution_simulation": eval_evolution_simulation_criterion,
    "engineering_graph": eval_engineering_graph_criterion,
    "engineering_failure_forecast": eval_engineering_failure_forecast_criterion,
    "engineering_operational_consistency": eval_engineering_operational_consistency_criterion,
    "engineering_dependency_pressure": eval_engineering_dependency_pressure_criterion,
    "engineering_diagnostics": eval_engineering_diagnostics_criterion,
    "engineering_incident": eval_engineering_incident_criterion,
    "execution_pressure": eval_execution_pressure_criterion,
    "runtime_contention": eval_runtime_contention_criterion,
    "state_convergence": eval_state_convergence_criterion,
    "runtime_entropy": eval_runtime_entropy_criterion,
    "execution_bottlenecks": eval_execution_bottlenecks_criterion,
    "runtime_conflicts": eval_runtime_conflicts_criterion,
    "collapse_forecast": eval_collapse_forecast_criterion,
    "scheduler_intelligence": eval_scheduler_intelligence_criterion,
    "load_balancing": eval_load_balancing_criterion,
    "causality_graph": eval_causality_graph_criterion,
    "failure_lineage": eval_failure_lineage_criterion,
    "causal_propagation": eval_causal_propagation_criterion,
    "recovery_causality": eval_recovery_causality_criterion,
    "causal_equilibrium": eval_causal_equilibrium_criterion,
    "causal_instability": eval_causal_instability_criterion,
    "timing_semantics": eval_timing_semantics_criterion,
    "causal_replay": eval_causal_replay_criterion,
    "execution_physics": eval_execution_physics_criterion,
    "pressure_field": eval_pressure_field_criterion,
    "runtime_turbulence": eval_runtime_turbulence_physics_criterion,
    "energy_propagation": eval_energy_propagation_criterion,
    "momentum": eval_momentum_criterion,
    "recovery_stabilization": eval_recovery_stabilization_criterion,
    "execution_waves": eval_execution_waves_criterion,
    "equilibrium_mechanics": eval_equilibrium_mechanics_criterion,
}
