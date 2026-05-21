from core.evolution_runtime.runtime_policy_engine import build_runtime_policy, enforce_runtime_policy
from core.evolution_runtime import run_evolution_runtime


def test_policy_enforcement():
    policy = build_runtime_policy()
    enforcement = enforce_runtime_policy(policy, mutations=[], repairs=[], depth=1)

    assert enforcement["within_bounds"] is True
    assert policy["mutation_constraints"]["allow_code_synthesis"] is False


def test_evolution_graph_nodes():
    result = run_evolution_runtime(tick=0)
    assert result["graph"]["nodes"]
    assert result["graph"]["edges"]
