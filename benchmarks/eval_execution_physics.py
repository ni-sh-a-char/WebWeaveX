from __future__ import annotations

from typing import Any, Dict

from core.execution_physics import (
    analyze_execution_waves,
    analyze_runtime_turbulence,
    build_pressure_field,
    compute_execution_physics,
    compute_semantic_momentum,
    orchestrate_execution_physics,
    propagate_runtime_energy,
    stabilize_runtime_recovery,
)
from core.execution_physics.semantic_equilibrium_field_engine import (
    build_equilibrium_field,
)


def eval_execution_physics(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_execution_physics(case.get("runtime_ir", {}))
    pred = result.get("physics_state") == case.get("expected_state")
    return {
        "predicted": pred,
        "actual": {"physics_state": result.get("physics_state")},
        "expected": case.get("expected_state"),
    }


def eval_pressure_field(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_pressure_field(case.get("runtime_ir", {}))
    pred = len(result.get("pressure_field", [])) == case.get(
        "expected_field_size"
    )
    return {
        "predicted": pred,
        "actual": {"size": len(result.get("pressure_field", []))},
        "expected": case.get("expected_field_size"),
    }


def eval_runtime_turbulence(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_runtime_turbulence(case.get("runtime_ir", {}))
    pred = result.get("runtime_turbulence") == case.get(
        "expected_turbulence"
    )
    return {
        "predicted": pred,
        "actual": {"turbulence": result.get("runtime_turbulence")},
        "expected": case.get("expected_turbulence"),
    }


def eval_energy_propagation(case: Dict[str, Any]) -> Dict[str, Any]:
    result = propagate_runtime_energy(case.get("runtime_ir", {}))
    pred = len(result.get("energy_propagation", [])) == case.get(
        "expected_propagation_count"
    )
    return {
        "predicted": pred,
        "actual": {"count": len(result.get("energy_propagation", []))},
        "expected": case.get("expected_propagation_count"),
    }


def eval_momentum(case: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_semantic_momentum(case.get("runtime_ir", {}))
    pred = result.get("runtime_momentum") == case.get("expected_momentum")
    return {
        "predicted": pred,
        "actual": {"momentum": result.get("runtime_momentum")},
        "expected": case.get("expected_momentum"),
    }


def eval_recovery_stabilization(case: Dict[str, Any]) -> Dict[str, Any]:
    result = stabilize_runtime_recovery(case.get("runtime_ir", {}))
    pred = result.get("stabilized") == case.get("expected_stabilized")
    return {
        "predicted": pred,
        "actual": {"stabilized": result.get("stabilized")},
        "expected": case.get("expected_stabilized"),
    }


def eval_execution_waves(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_execution_waves(case.get("runtime_ir", {}))
    pred = len(result.get("execution_waves", [])) == case.get(
        "expected_wave_count"
    )
    return {
        "predicted": pred,
        "actual": {"count": len(result.get("execution_waves", []))},
        "expected": case.get("expected_wave_count"),
    }


def eval_equilibrium_mechanics(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_equilibrium_field(case.get("runtime_ir", {}))
    pred = result.get("field_state") == case.get("expected_field_state")
    return {
        "predicted": pred,
        "actual": {"field_state": result.get("field_state")},
        "expected": case.get("expected_field_state"),
    }
