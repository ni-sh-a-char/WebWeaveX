from core.evolution import (
    adapt_semantic_runtime,
    analyze_semantic_dependencies,
    analyze_semantic_stability,
    compress_semantic_repository,
    detect_runtime_drift,
    diff_semantic_repository,
    distill_semantic_knowledge,
    evolve_semantic_topology,
    forecast_semantic_change,
    optimize_semantic_architecture,
    plan_runtime_mutation,
    prove_architecture_consistency,
    reconcile_semantic_graphs,
    simulate_repository_runtime,
    suggest_semantic_refactors,
)
from core.evolution.semantic_adaptation_policy_engine import (
    enforce_adaptation_policies,
)
from core.evolution.semantic_structural_heuristics_engine import (
    compute_structural_heuristics,
)


def test_refactor_engine():
    result = suggest_semantic_refactors(
        {"nodes": [{"id": "a.py"}]}
    )
    assert len(result["suggestions"]) == 1


def test_architecture_optimizer():
    result = optimize_semantic_architecture(
        {"nodes": [{"id": "b.py"}, {"id": "a.py"}]}
    )
    assert result["optimized_nodes"][0]["id"] == "a.py"


def test_dependency_intelligence():
    result = analyze_semantic_dependencies(
        {
            "edges": [
                {"from": "a.py", "to": "b.py"},
            ]
        }
    )
    assert result["dependency_map"]["a.py"] == ["b.py"]


def test_change_forecast():
    result = forecast_semantic_change(
        [{"id": "b"}, {"id": "a"}]
    )
    assert result["forecast"][0]["id"] == "a"


def test_repository_diff():
    result = diff_semantic_repository(
        {"a": 1},
        {"a": 1, "b": 2},
    )
    assert result["added"] == ["b"]


def test_mutation_planner():
    result = plan_runtime_mutation({"x": 1, "y": 2})
    assert result["mutation_candidates"] == ["x", "y"]


def test_knowledge_distillation():
    result = distill_semantic_knowledge([{"goal": "x"}])
    assert result["distilled"][0] == ["goal"]


def test_drift_detection():
    result = detect_runtime_drift(
        {"a": 1, "b": 2},
        {"a": 1},
    )
    assert result["drift_detected"] is True


def test_consistency_proof():
    result = prove_architecture_consistency(
        {"nodes": [{"id": "a"}]}
    )
    assert result["consistent"] is True


def test_repository_simulation():
    result = simulate_repository_runtime(
        {"edges": [{"from": "a", "to": "b"}]}
    )
    assert result["simulation_steps"] == 1


def test_runtime_adaptation():
    result = adapt_semantic_runtime({"a": 1})
    assert result["adaptation_count"] == 1


def test_repository_compression():
    state = {f"k{i}": i for i in range(300)}
    result = compress_semantic_repository(state)
    assert len(result["compressed"]) == 256


def test_adaptation_policies():
    result = enforce_adaptation_policies(
        {"goal": "x"},
        [{"key": "goal"}],
    )
    assert len(result["allowed"]) == 1


def test_structural_heuristics():
    result = compute_structural_heuristics(
        {
            "nodes": [{}, {}],
            "edges": [{}],
        }
    )
    assert result["node_count"] == 2


def test_topology_evolution():
    result = evolve_semantic_topology(
        {"nodes": [{"id": "a"}, {"id": "b"}]}
    )
    assert result["step_count"] == 2


def test_graph_reconciliation():
    result = reconcile_semantic_graphs(
        {"nodes": [{"id": "a"}]},
        {"nodes": [{"id": "a"}, {"id": "b"}]},
    )
    assert result["right_only"] == ["b"]
