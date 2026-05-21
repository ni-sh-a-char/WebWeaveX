from core.synchronization.runtime_convergence_engine import converge_runtime_state


def test_convergence_stability():
    realities = [
        {"reality_id": "primary", "state": {"a": 1}},
        {"reality_id": "distributed", "state": {"b": 2}},
    ]

    first = converge_runtime_state(realities)
    second = converge_runtime_state(realities)

    assert first == second
    assert first["converged"] is True
