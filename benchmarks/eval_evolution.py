from __future__ import annotations

from typing import Any, Dict

from core.evolution import (
    analyze_semantic_dependencies,
    detect_runtime_drift,
    evolve_semantic_runtime,
    orchestrate_semantic_evolution,
    prove_architecture_consistency,
    simulate_repository_runtime,
    suggest_semantic_refactors,
)


def eval_evolution_runtime(case: Dict[str, Any]) -> Dict[str, Any]:
    result = evolve_semantic_runtime(case.get("runtime", {}))
    pred = result.get("evolution_size") == case.get("expected_size")
    return {
        "predicted": pred,
        "actual": {"evolution_size": result.get("evolution_size")},
        "expected": case.get("expected_size"),
    }


def eval_evolution_refactor(case: Dict[str, Any]) -> Dict[str, Any]:
    result = suggest_semantic_refactors(case.get("repository_ir", {}))
    count = len(result.get("suggestions", []))
    pred = count == case.get("expected_suggestions", 0)
    return {
        "predicted": pred,
        "actual": {"count": count},
        "expected": case.get("expected_suggestions"),
    }


def eval_evolution_dependencies(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_semantic_dependencies(case.get("repository_ir", {}))
    pred = len(result.get("dependency_map", {})) == case.get(
        "expected_sources", 0
    )
    return {
        "predicted": pred,
        "actual": {"sources": len(result.get("dependency_map", {}))},
        "expected": case.get("expected_sources"),
    }


def eval_evolution_consistency(case: Dict[str, Any]) -> Dict[str, Any]:
    result = prove_architecture_consistency(case.get("graph", {}))
    pred = result.get("consistent") == case.get("expected_consistent")
    return {
        "predicted": pred,
        "actual": {"consistent": result.get("consistent")},
        "expected": case.get("expected_consistent"),
    }


def eval_evolution_drift(case: Dict[str, Any]) -> Dict[str, Any]:
    result = detect_runtime_drift(
        case.get("current", {}),
        case.get("baseline", {}),
    )
    pred = result.get("drift_detected") == case.get("expected_drift")
    return {
        "predicted": pred,
        "actual": {"drift_detected": result.get("drift_detected")},
        "expected": case.get("expected_drift"),
    }


def eval_evolution_simulation(case: Dict[str, Any]) -> Dict[str, Any]:
    result = simulate_repository_runtime(case.get("repository_ir", {}))
    pred = result.get("simulation_steps") == case.get("expected_steps")
    return {
        "predicted": pred,
        "actual": {"steps": result.get("simulation_steps")},
        "expected": case.get("expected_steps"),
    }


def eval_evolution_orchestration(case: Dict[str, Any]) -> Dict[str, Any]:
    result = orchestrate_semantic_evolution(case.get("runtime", {}))
    pred = result.get("stability", {}).get("stable") == case.get(
        "expected_stable"
    )
    return {
        "predicted": pred,
        "actual": {"stable": result.get("stability", {}).get("stable")},
        "expected": case.get("expected_stable"),
    }
