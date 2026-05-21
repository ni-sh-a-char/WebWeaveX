from core.workflows.workflow_recovery_engine import recover_workflow_runtime
from core.workflows.workflow_state_engine import build_workflow_state


def test_recovery_determinism():
    state = build_workflow_state({"steps": [{"id": "s1"}]}, {"executed": []}, current_step=1)

    first = recover_workflow_runtime(state, ["selector_drift"])
    second = recover_workflow_runtime(state, ["selector_drift"])

    assert first == second
    assert first["recovered"] is True
