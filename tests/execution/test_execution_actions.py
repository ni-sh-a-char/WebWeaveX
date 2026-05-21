from core.execution.runtime_execution_engine import execute_runtime_action
from core.execution.runtime_permissions_engine import build_runtime_permissions
from core.execution.runtime_sandbox_engine import build_runtime_sandbox


def test_action_determinism():
    action = {"type": "browser_click", "selector": "#submit"}
    sandbox = build_runtime_sandbox(runtime="browser")
    permissions = build_runtime_permissions(scopes=["browser"])

    first = execute_runtime_action(action, sandbox=sandbox, permissions=permissions, tick=1)
    second = execute_runtime_action(action, sandbox=sandbox, permissions=permissions, tick=1)

    assert first == second
    assert first["executed"] is True
    assert first["action_id"] == second["action_id"]
