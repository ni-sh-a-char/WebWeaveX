from core.memory.runtime_memory_policy_engine import (
    build_runtime_memory_policy,
    enforce_memory_policy,
)


def test_policy_enforcement():
    policy = build_runtime_memory_policy()
    enforcement = enforce_memory_policy(policy, [], [], 0)

    assert enforcement["within_bounds"] is True
    assert policy["federation_constraints"] == 1000
