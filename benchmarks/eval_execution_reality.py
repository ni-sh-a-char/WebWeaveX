from __future__ import annotations

from typing import Any, Dict

from core.execution_reality import (
    analyze_runtime_contention,
    analyze_scheduler_intelligence,
    balance_runtime_load,
    compute_execution_pressure,
    compute_runtime_entropy,
    compute_state_convergence,
    detect_execution_bottlenecks,
    detect_runtime_conflicts,
    forecast_execution_collapse,
    orchestrate_execution_reality,
)


def eval_execution_pressure(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_execution_pressure(case.get("runtime_ir", {}))
    pred = result.get("pressure_score") == case.get("expected_pressure")
    return {
        "predicted": pred,
        "actual": {"pressure_score": result.get("pressure_score")},
        "expected": case.get("expected_pressure"),
    }


def eval_runtime_contention(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_runtime_contention(case.get("runtime_ir", {}))
    target = case.get("target", "")
    pred = result.get("contention", {}).get(target) == case.get(
        "expected_contention"
    )
    return {
        "predicted": pred,
        "actual": {
            "contention": result.get("contention", {}).get(target)
        },
        "expected": case.get("expected_contention"),
    }


def eval_state_convergence(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_state_convergence(case.get("runtime_ir", {}))
    pred = result.get("converged") == case.get("expected_converged")
    return {
        "predicted": pred,
        "actual": {"converged": result.get("converged")},
        "expected": case.get("expected_converged"),
    }


def eval_runtime_entropy(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_runtime_entropy(case.get("runtime_ir", {}))
    pred = result.get("entropy_score") == case.get("expected_entropy")
    return {
        "predicted": pred,
        "actual": {"entropy_score": result.get("entropy_score")},
        "expected": case.get("expected_entropy"),
    }


def eval_execution_bottlenecks(case: Dict[str, Any]) -> Dict[str, Any]:
    result = detect_execution_bottlenecks(case.get("runtime_ir", {}))
    pred = len(result.get("bottlenecks", [])) == case.get(
        "expected_bottleneck_count"
    )
    return {
        "predicted": pred,
        "actual": {"count": len(result.get("bottlenecks", []))},
        "expected": case.get("expected_bottleneck_count"),
    }


def eval_runtime_conflicts(case: Dict[str, Any]) -> Dict[str, Any]:
    result = detect_runtime_conflicts(case.get("runtime_ir", {}))
    pred = len(result.get("conflicts", [])) == case.get(
        "expected_conflict_count"
    )
    return {
        "predicted": pred,
        "actual": {"count": len(result.get("conflicts", []))},
        "expected": case.get("expected_conflict_count"),
    }


def eval_collapse_forecast(case: Dict[str, Any]) -> Dict[str, Any]:
    result = forecast_execution_collapse(case.get("runtime_ir", {}))
    pred = result.get("collapse_risk") == case.get("expected_risk")
    return {
        "predicted": pred,
        "actual": {"collapse_risk": result.get("collapse_risk")},
        "expected": case.get("expected_risk"),
    }


def eval_scheduler_intelligence(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_scheduler_intelligence(case.get("runtime_ir", {}))
    first = (
        result.get("scheduled_tasks", [{}])[0].get("id")
        if result.get("scheduled_tasks")
        else None
    )
    pred = first == case.get("expected_first_task")
    return {
        "predicted": pred,
        "actual": {"first_task": first},
        "expected": case.get("expected_first_task"),
    }


def eval_load_balancing(case: Dict[str, Any]) -> Dict[str, Any]:
    result = balance_runtime_load(case.get("runtime_ir", {}))
    pred = len(result.get("assignments", {})) == case.get(
        "expected_workers"
    )
    return {
        "predicted": pred,
        "actual": {"workers": len(result.get("assignments", {}))},
        "expected": case.get("expected_workers"),
    }
