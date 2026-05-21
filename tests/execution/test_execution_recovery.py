from core.execution.runtime_recovery_engine import recover_runtime_execution


def test_execution_recovery():
    result = recover_runtime_execution(
        failed_actions=[{"id": "failed:1"}],
        checkpoint={"state": {"browser": {}}},
        interrupted_workflows=[{"id": "wf:1"}],
    )

    assert result["replay_safe"] is True
    assert result["checkpoint_restored"] is True
    assert len(result["recovered_actions"]) == 1
