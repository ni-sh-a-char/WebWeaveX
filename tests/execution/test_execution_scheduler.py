from core.execution.runtime_action_engine import build_runtime_action
from core.execution.runtime_scheduler_engine import schedule_runtime_execution


def test_execution_scheduler_deterministic():
    actions = [
        build_runtime_action("browser_click", "browser", {"selector": "#a"}, tick=0),
        build_runtime_action("browser_click", "browser", {"selector": "#b"}, tick=0),
    ]

    priorities = {actions[0]["id"]: 1, actions[1]["id"]: 0}
    first = schedule_runtime_execution(actions, priorities=priorities, tick=1)
    second = schedule_runtime_execution(actions, priorities=priorities, tick=1)

    assert first == second
    assert first["deterministic"] is True
