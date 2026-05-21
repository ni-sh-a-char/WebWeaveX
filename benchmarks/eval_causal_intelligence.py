from __future__ import annotations

from typing import Any, Dict

from core.causal_intelligence import (
    analyze_recovery_causality,
    build_semantic_causality_graph,
    build_runtime_failure_lineage,
    compute_runtime_equilibrium,
    forecast_runtime_instability,
    orchestrate_semantic_causal_intelligence,
    propagate_distributed_state,
    analyze_execution_timing,
    replay_causal_sequence,
)


def eval_causality_graph(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_semantic_causality_graph(case.get("runtime_ir", {}))
    pred = len(result.get("edges", [])) == case.get("expected_edges", 0)
    return {
        "predicted": pred,
        "actual": {"edges": len(result.get("edges", []))},
        "expected": case.get("expected_edges"),
    }


def eval_failure_lineage(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_runtime_failure_lineage(case.get("runtime_ir", {}))
    pred = len(result.get("failure_lineage", [])) == case.get(
        "expected_lineage_count"
    )
    return {
        "predicted": pred,
        "actual": {"count": len(result.get("failure_lineage", []))},
        "expected": case.get("expected_lineage_count"),
    }


def eval_propagation(case: Dict[str, Any]) -> Dict[str, Any]:
    result = propagate_distributed_state(case.get("runtime_ir", {}))
    pred = len(result.get("propagation_paths", [])) == case.get(
        "expected_paths"
    )
    return {
        "predicted": pred,
        "actual": {"paths": len(result.get("propagation_paths", []))},
        "expected": case.get("expected_paths"),
    }


def eval_recovery_causality(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_recovery_causality(case.get("runtime_ir", {}))
    pred = result.get("recovery_possible") == case.get(
        "expected_recovery_possible"
    )
    return {
        "predicted": pred,
        "actual": {"recovery_possible": result.get("recovery_possible")},
        "expected": case.get("expected_recovery_possible"),
    }


def eval_equilibrium(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_runtime_equilibrium(case.get("runtime_ir", {}))
    pred = result.get("equilibrium") == case.get("expected_equilibrium")
    return {
        "predicted": pred,
        "actual": {"equilibrium": result.get("equilibrium")},
        "expected": case.get("expected_equilibrium"),
    }


def eval_instability(case: Dict[str, Any]) -> Dict[str, Any]:
    result = forecast_runtime_instability(case.get("runtime_ir", {}))
    pred = result.get("instability_forecast") == case.get(
        "expected_instability"
    )
    return {
        "predicted": pred,
        "actual": {"instability": result.get("instability_forecast")},
        "expected": case.get("expected_instability"),
    }


def eval_timing_semantics(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_execution_timing(case.get("runtime_ir", {}))
    first = (
        result.get("timing_sequence", [None])[0]
        if result.get("timing_sequence")
        else None
    )
    pred = first == case.get("expected_first_event")
    return {
        "predicted": pred,
        "actual": {"first": first},
        "expected": case.get("expected_first_event"),
    }


def eval_causal_replay(case: Dict[str, Any]) -> Dict[str, Any]:
    result = replay_causal_sequence(case.get("runtime_ir", {}))
    pred = result.get("replay_count") == case.get("expected_replay_count")
    return {
        "predicted": pred,
        "actual": {"replay_count": result.get("replay_count")},
        "expected": case.get("expected_replay_count"),
    }
