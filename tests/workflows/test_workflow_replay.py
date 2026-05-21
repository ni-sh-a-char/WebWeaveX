from core.workflows import run_autonomous_workflow
from core.workflows.workflow_replay_engine import replay_workflow_runtime


def test_workflow_replay_identical():
    result = run_autonomous_workflow(objective="monitor_metrics")
    memory = result["memory"]

    first = replay_workflow_runtime(memory)
    second = replay_workflow_runtime(memory)

    assert first == second
    assert result["replay"] == first
