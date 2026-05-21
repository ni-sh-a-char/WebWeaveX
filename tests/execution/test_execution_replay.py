from core.execution.runtime_action_engine import build_runtime_action
from core.execution.runtime_replay_engine import replay_runtime_execution


def test_execution_replay_identical():
    actions = [
        build_runtime_action("browser_click", "browser", {"selector": "#a"}, tick=1),
        build_runtime_action("browser_click", "browser", {"selector": "#b"}, tick=2),
    ]

    first = replay_runtime_execution(actions, tick=1)
    second = replay_runtime_execution(actions, tick=1)

    assert first == second
    assert first["identical"] is True
