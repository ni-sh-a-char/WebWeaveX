from core.runtime.runtime_state_propagation_engine import propagate_runtime_state


def test_propagate_reachable_states():
    transitions = [
        {"from": "init", "to": "running"},
        {"from": "running", "to": "done"},
    ]
    r = propagate_runtime_state(transitions)
    assert r["state_count"] == 3
    assert r["reachable_states"] == ["done", "init", "running"]
