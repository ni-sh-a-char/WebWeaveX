from core.execution_reality import (
    analyze_execution_replay,
    analyze_runtime_contention,
    analyze_scheduler_intelligence,
    assess_distributed_stability,
    balance_runtime_load,
    compute_execution_heat,
    compute_runtime_entropy,
    compute_state_convergence,
    detect_execution_bottlenecks,
    detect_execution_drift,
    detect_runtime_conflicts,
    forecast_execution_collapse,
    forecast_runtime_load,
    measure_queue_pressure,
    mutate_runtime_topology,
    optimize_runtime_execution,
    simulate_runtime_recovery,
    trace_execution_cascade,
)


def test_contention():
    result = analyze_runtime_contention(
        {
            "distributed_topology": {
                "edges": [
                    {"to": "api"},
                    {"to": "api"},
                ]
            }
        }
    )
    assert result["contention"]["api"] == 2


def test_convergence_with_conflicts():
    result = compute_state_convergence(
        {"semantic_crdt": {"conflicts": [1]}}
    )
    assert result["converged"] is False


def test_entropy():
    result = compute_runtime_entropy(
        {
            "transitions": [
                {"from": "a", "to": "b"},
                {"from": "b", "to": "c"},
            ]
        }
    )
    assert result["entropy_score"] == 3


def test_bottlenecks():
    edges = [{"to": "hub"} for _ in range(3)]
    result = detect_execution_bottlenecks(
        {"distributed_topology": {"edges": edges}}
    )
    assert len(result["bottlenecks"]) == 1


def test_conflicts():
    t = {"from": "a", "to": "b"}
    result = detect_runtime_conflicts(
        {"transitions": [t, t]}
    )
    assert len(result["conflicts"]) == 1


def test_collapse_forecast():
    result = forecast_execution_collapse(
        {"execution_pressure": {"pressure_score": 20000}}
    )
    assert result["collapse_risk"] == "high"


def test_execution_heat():
    result = compute_execution_heat(
        {
            "distributed_topology": {
                "nodes": [{"id": "b"}, {"id": "a"}]
            }
        }
    )
    assert result["heatmap"][0]["node"] == "a"


def test_topology_mutation():
    result = mutate_runtime_topology(
        {
            "distributed_topology": {
                "nodes": [{"id": "a"}]
            }
        }
    )
    assert (
        result["topology_mutation"]["predicted_growth"]
        == 2
    )


def test_scheduler():
    result = analyze_scheduler_intelligence(
        {
            "tasks": [
                {"id": "b", "priority": 1},
                {"id": "a", "priority": 2},
            ]
        }
    )
    assert result["scheduled_tasks"][0]["id"] == "b"


def test_balancer():
    result = balance_runtime_load(
        {
            "distributed_workers": [
                {"worker": "w1"},
                {"worker": "w2"},
            ]
        }
    )
    assert len(result["assignments"]) == 2


def test_queue_pressure():
    result = measure_queue_pressure(
        {
            "tasks": [{}, {}],
            "distributed_workers": [{}],
        }
    )
    assert result["queue_pressure"] == 2


def test_execution_drift():
    result = detect_execution_drift(
        {"a": 1, "b": 2},
        {"a": 1},
    )
    assert result["drift_detected"] is True


def test_cascade():
    result = trace_execution_cascade(
        [
            {"from": "b", "to": "c"},
            {"from": "a", "to": "b"},
        ]
    )
    assert result["cascade_length"] == 2


def test_recovery_simulation():
    result = simulate_runtime_recovery(
        {"journal": {"e1": 1}}
    )
    assert result["simulated"] is True


def test_replay_intelligence():
    result = analyze_execution_replay(
        [
            {"id": "b", "timestamp": 2},
            {"id": "a", "timestamp": 1},
        ]
    )
    assert result["replay_sequence"][0]["id"] == "a"


def test_distributed_stability():
    result = assess_distributed_stability(
        {"execution_pressure": {"pressure_score": 10}}
    )
    assert result["stable"] is True


def test_load_forecast():
    result = forecast_runtime_load(
        {"execution_pressure": {"pressure_score": 0}}
    )
    assert result["load_tier"] == "idle"


def test_runtime_optimization():
    result = optimize_runtime_execution(
        {
            "execution_bottlenecks": {
                "bottlenecks": [{"node": "hub"}]
            }
        }
    )
    assert result["optimization_count"] == 1
