from core.causal_intelligence import (
    analyze_dependency_cascade,
    analyze_drift_causality,
    analyze_execution_timing,
    analyze_recovery_causality,
    build_distributed_causal_graph,
    build_mutation_lineage,
    build_runtime_failure_lineage,
    compute_runtime_equilibrium,
    compute_scheduling_pressure,
    forecast_recovery_outcome,
    forecast_runtime_instability,
    forecast_stability_horizon,
    measure_runtime_resonance,
    propagate_distributed_state,
    propagate_runtime_waves,
    replay_causal_sequence,
    trace_execution_mutations,
)
from core.causal_intelligence.runtime_semantic_equilibrium_engine import (
    assess_semantic_equilibrium,
)


def test_failure_lineage():
    result = build_runtime_failure_lineage(
        {
            "runtime_conflicts": {
                "conflicts": [("a", "b")]
            }
        }
    )
    assert len(result["failure_lineage"]) == 1


def test_propagation():
    result = propagate_distributed_state(
        {
            "distributed_topology": {
                "edges": [{"from": "a", "to": "b"}]
            }
        }
    )
    assert len(result["propagation_paths"]) == 1


def test_recovery_causality():
    result = analyze_recovery_causality(
        {"journal": {"entries": [{"e": 1}]}}
    )
    assert result["recovery_possible"] is True


def test_instability_forecast():
    result = forecast_runtime_instability(
        {"execution_pressure": {"pressure_score": 6000}}
    )
    assert result["instability_forecast"] == "high"


def test_execution_timing():
    result = analyze_execution_timing(
        {
            "event_stream": {
                "events": [
                    {"id": "b", "timestamp": 2},
                    {"id": "a", "timestamp": 1},
                ]
            }
        }
    )
    assert result["timing_sequence"][0] == "a"


def test_dependency_cascade():
    runtime = {
        "runtime_causality_graph": {
            "edges": [{"from": "a", "to": "b"}]
        }
    }
    result = analyze_dependency_cascade(runtime)
    assert result["cascade_length"] == 1


def test_mutation_lineage():
    result = build_mutation_lineage({"z": 1, "a": 2})
    assert result["mutation_lineage"][0]["key"] == "a"


def test_scheduling_pressure():
    result = compute_scheduling_pressure(
        {
            "tasks": [{}, {}],
            "distributed_workers": [{}],
        }
    )
    assert result["scheduling_pressure"] == 2


def test_drift_causality():
    result = analyze_drift_causality(
        {"a": 1, "b": 2},
        {"a": 1},
    )
    assert result["drift_count"] == 1


def test_causal_replay():
    result = replay_causal_sequence(
        {"journal": {"entries": [{"id": "e1"}]}}
    )
    assert result["replay_count"] == 1


def test_recovery_forecast():
    result = forecast_recovery_outcome(
        {
            "recovery_causality": {
                "recovery_possible": True
            }
        }
    )
    assert result["recovery_forecast"] == "successful"


def test_semantic_equilibrium():
    result = assess_semantic_equilibrium(
        {
            "runtime_equilibrium": {"equilibrium": "stable"},
            "execution_pressure": {"pressure_score": 1},
        }
    )
    assert result["balanced"] is True


def test_execution_mutations():
    result = trace_execution_mutations(
        [{"from": "b", "to": "c"}, {"from": "a", "to": "b"}]
    )
    assert result["mutation_count"] == 2


def test_wave_propagation():
    result = propagate_runtime_waves(
        [{"source": "a", "target": "b"}]
    )
    assert result["wave_count"] == 1


def test_distributed_causal_graph():
    runtime = {
        "runtime_causality_graph": {
            "edges": [{"from": "a", "to": "b"}]
        },
        "distributed_propagation": {
            "propagation_paths": [
                {"source": "x", "target": "y"}
            ]
        },
    }
    result = build_distributed_causal_graph(runtime)
    assert result["edge_count"] == 2


def test_runtime_resonance():
    result = measure_runtime_resonance(
        {
            "execution_pressure": {"pressure_score": 10},
            "runtime_entropy": {"entropy_score": 5},
        }
    )
    assert result["resonance_score"] == 15


def test_stability_horizon():
    result = forecast_stability_horizon(
        {
            "instability_forecast": {
                "instability_forecast": "high"
            }
        }
    )
    assert result["stability_horizon"] == "short"
