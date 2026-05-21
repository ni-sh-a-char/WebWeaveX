from core.execution.runtime_execution_engine import execute_runtime_action
from core.execution.runtime_sandbox_engine import build_runtime_sandbox


def test_sandbox_enforcement():
    sandbox = build_runtime_sandbox(
        runtime="browser",
        allowed_actions=["browser_click"],
    )
    result = execute_runtime_action(
        {"type": "terminal_command", "command": "pwd"},
        sandbox=sandbox,
        tick=0,
    )

    assert result["executed"] is False
    assert result["reason"] == "sandbox_forbidden"
