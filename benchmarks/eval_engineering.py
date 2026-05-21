from __future__ import annotations

from typing import Any, Dict

from core.engineering import (
    build_semantic_engineering_graph,
    compute_dependency_pressure,
    diagnose_semantic_runtime,
    forecast_runtime_failures,
    orchestrate_semantic_engineering,
    prove_operational_consistency,
    reconstruct_semantic_incident,
)


def eval_engineering_graph(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_semantic_engineering_graph(case.get("runtime_ir", {}))
    pred = result.get("graph_size") == case.get("expected_graph_size")
    return {
        "predicted": pred,
        "actual": {"graph_size": result.get("graph_size")},
        "expected": case.get("expected_graph_size"),
    }


def eval_engineering_failure_forecast(case: Dict[str, Any]) -> Dict[str, Any]:
    result = forecast_runtime_failures(case.get("runtime_ir", {}))
    pred = result.get("forecast_count") == case.get("expected_forecast_count")
    return {
        "predicted": pred,
        "actual": {"forecast_count": result.get("forecast_count")},
        "expected": case.get("expected_forecast_count"),
    }


def eval_engineering_operational_consistency(case: Dict[str, Any]) -> Dict[str, Any]:
    result = prove_operational_consistency(case.get("runtime_ir", {}))
    pred = result.get("consistent") == case.get("expected_consistent")
    return {
        "predicted": pred,
        "actual": {"consistent": result.get("consistent")},
        "expected": case.get("expected_consistent"),
    }


def eval_engineering_dependency_pressure(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_dependency_pressure(case.get("graph", {}))
    target = case.get("target", "")
    pred = result.get("dependency_pressure", {}).get(target) == case.get(
        "expected_pressure"
    )
    return {
        "predicted": pred,
        "actual": {
            "pressure": result.get("dependency_pressure", {}).get(target)
        },
        "expected": case.get("expected_pressure"),
    }


def eval_engineering_diagnostics(case: Dict[str, Any]) -> Dict[str, Any]:
    result = diagnose_semantic_runtime(case.get("runtime_ir", {}))
    pred = result.get("healthy") == case.get("expected_healthy")
    return {
        "predicted": pred,
        "actual": {"healthy": result.get("healthy")},
        "expected": case.get("expected_healthy"),
    }


def eval_engineering_incident(case: Dict[str, Any]) -> Dict[str, Any]:
    result = reconstruct_semantic_incident(case.get("events", []))
    pred = len(result.get("incident_path", [])) == case.get("expected_events")
    return {
        "predicted": pred,
        "actual": {"events": len(result.get("incident_path", []))},
        "expected": case.get("expected_events"),
    }
