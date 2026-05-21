from core.runtime.runtime_simulation_engine import (
    simulate_runtime_execution,
)


def test_runtime_simulation():

    transitions = [
        {"from": "a", "to": "b"},
        {"from": "b", "to": "c"},
    ]

    r = simulate_runtime_execution(
        transitions
    )

    assert r["final_state"] == "c"
