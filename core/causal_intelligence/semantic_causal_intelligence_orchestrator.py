from __future__ import annotations

from typing import Any, Dict

from .semantic_causality_graph_engine import (
    build_semantic_causality_graph,
)
from .runtime_failure_lineage_engine import (
    build_runtime_failure_lineage,
)
from .distributed_propagation_engine import (
    propagate_distributed_state,
)
from .semantic_recovery_causality_engine import (
    analyze_recovery_causality,
)
from .runtime_equilibrium_engine import (
    compute_runtime_equilibrium,
)
from .semantic_instability_forecast_engine import (
    forecast_runtime_instability,
)
from .execution_timing_semantics_engine import (
    analyze_execution_timing,
)
from .dependency_cascade_intelligence_engine import (
    analyze_dependency_cascade,
)
from .semantic_runtime_mutation_lineage_engine import (
    build_mutation_lineage,
)
from .distributed_scheduling_pressure_engine import (
    compute_scheduling_pressure,
)
from .runtime_drift_causality_engine import (
    analyze_drift_causality,
)
from .semantic_causal_replay_engine import (
    replay_causal_sequence,
)
from .semantic_recovery_forecast_engine import (
    forecast_recovery_outcome,
)
from .runtime_semantic_equilibrium_engine import (
    assess_semantic_equilibrium,
)
from .semantic_execution_mutation_engine import (
    trace_execution_mutations,
)
from .semantic_runtime_wave_propagation_engine import (
    propagate_runtime_waves,
)
from .distributed_runtime_causal_graph_engine import (
    build_distributed_causal_graph,
)
from .semantic_runtime_resonance_engine import (
    measure_runtime_resonance,
)
from .semantic_execution_stability_horizon_engine import (
    forecast_stability_horizon,
)


def orchestrate_semantic_causal_intelligence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    causality_graph = build_semantic_causality_graph(
        runtime_ir
    )
    runtime_ir["runtime_causality_graph"] = causality_graph

    failure_lineage = build_runtime_failure_lineage(
        runtime_ir
    )
    propagation = propagate_distributed_state(
        runtime_ir
    )
    runtime_ir["distributed_propagation"] = propagation

    recovery = analyze_recovery_causality(runtime_ir)
    runtime_ir["recovery_causality"] = recovery

    equilibrium = compute_runtime_equilibrium(
        runtime_ir
    )
    runtime_ir["runtime_equilibrium"] = equilibrium

    instability = forecast_runtime_instability(
        runtime_ir
    )
    runtime_ir["instability_forecast"] = instability

    timing = analyze_execution_timing(runtime_ir)
    cascade = analyze_dependency_cascade(runtime_ir)
    mutation_lineage = build_mutation_lineage(runtime_ir)
    scheduling_pressure = compute_scheduling_pressure(
        runtime_ir
    )
    baseline = dict(runtime_ir.get("baseline", {}) or {})
    drift_causality = analyze_drift_causality(
        runtime_ir, baseline
    )
    causal_replay = replay_causal_sequence(runtime_ir)
    recovery_forecast = forecast_recovery_outcome(
        runtime_ir
    )
    semantic_equilibrium = assess_semantic_equilibrium(
        runtime_ir
    )
    execution_mutations = trace_execution_mutations(
        list(runtime_ir.get("transitions", []) or [])
    )
    waves = propagate_runtime_waves(
        propagation.get("propagation_paths", [])
    )
    distributed_causal_graph = build_distributed_causal_graph(
        runtime_ir
    )
    resonance = measure_runtime_resonance(runtime_ir)
    stability_horizon = forecast_stability_horizon(
        runtime_ir
    )

    return {
        "causality_graph": causality_graph,
        "failure_lineage": failure_lineage,
        "distributed_propagation": propagation,
        "recovery_causality": recovery,
        "runtime_equilibrium": equilibrium,
        "instability_forecast": instability,
        "execution_timing": timing,
        "dependency_cascade": cascade,
        "mutation_lineage": mutation_lineage,
        "scheduling_pressure": scheduling_pressure,
        "drift_causality": drift_causality,
        "causal_replay": causal_replay,
        "recovery_forecast": recovery_forecast,
        "semantic_equilibrium": semantic_equilibrium,
        "execution_mutations": execution_mutations,
        "wave_propagation": waves,
        "distributed_causal_graph": distributed_causal_graph,
        "runtime_resonance": resonance,
        "stability_horizon": stability_horizon,
        "deterministic": True,
        "bounded": True,
    }
