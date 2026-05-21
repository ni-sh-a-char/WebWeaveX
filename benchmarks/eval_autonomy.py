from __future__ import annotations

from typing import Any, Dict

from core.autonomy import (
    assess_runtime_health,
    decompose_semantic_task,
    forecast_semantic_resources,
    orchestrate_semantic_runtime,
    resolve_semantic_goal,
)


def eval_autonomy_goal(case: Dict[str, Any]) -> Dict[str, Any]:
    result = resolve_semantic_goal(case.get("payload", {}))
    pred = result.get("resolved") == case.get("expected_resolved")
    return {
        "predicted": pred,
        "actual": {"resolved": result.get("resolved")},
        "expected": case.get("expected_resolved"),
    }


def eval_autonomy_orchestration(case: Dict[str, Any]) -> Dict[str, Any]:
    result = orchestrate_semantic_runtime(case.get("payload", {}))
    count = result.get("decomposition", {}).get("count", 0)
    pred = count >= case.get("min_subtasks", 0)
    return {
        "predicted": pred,
        "actual": {"count": count},
        "expected": case.get("min_subtasks"),
    }


def eval_autonomy_decomposition(case: Dict[str, Any]) -> Dict[str, Any]:
    result = decompose_semantic_task(case.get("task", {}))
    pred = result.get("count") == case.get("expected_count")
    return {
        "predicted": pred,
        "actual": {"count": result.get("count")},
        "expected": case.get("expected_count"),
    }


def eval_autonomy_resource_forecast(case: Dict[str, Any]) -> Dict[str, Any]:
    result = forecast_semantic_resources(case.get("tasks", []))
    pred = result.get("cpu_units") == case.get("expected_cpu_units")
    return {
        "predicted": pred,
        "actual": {"cpu_units": result.get("cpu_units")},
        "expected": case.get("expected_cpu_units"),
    }


def eval_autonomy_runtime_health(case: Dict[str, Any]) -> Dict[str, Any]:
    result = assess_runtime_health(case.get("runtime", {}))
    pred = result.get("healthy") == case.get("expected_healthy")
    return {
        "predicted": pred,
        "actual": {"healthy": result.get("healthy")},
        "expected": case.get("expected_healthy"),
    }
