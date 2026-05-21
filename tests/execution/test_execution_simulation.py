from core.execution.runtime_simulation_engine import simulate_runtime_execution


def test_simulation_stability():
    actions = [{"type": "browser_click", "selector": "#submit"}]

    first = simulate_runtime_execution(actions, tick=0)
    second = simulate_runtime_execution(actions, tick=0)

    assert first == second
    assert first["simulated"] is True
    assert first["runtime_mutated"] is False
